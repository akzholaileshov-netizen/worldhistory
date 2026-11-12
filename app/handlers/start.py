import html

from aiogram import F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message

from app.core.constants import GRADES, REFERRAL_PREFIX
from app.db.client import Database
from app.db.models import UserRecord
from app.db.repositories.users import UserRepository
from app.keyboards.main_menu import grade_keyboard, main_menu
from app.texts import kk


async def _apply_referral(db: Database, user: UserRecord, payload: str | None) -> bool:
    if not payload or not payload.startswith(REFERRAL_PREFIX):
        return False
    repo = UserRepository(db)
    referrer = await repo.get_by_ref_code(payload.removeprefix(REFERRAL_PREFIX).upper())
    if referrer is None:
        return False
    return await repo.attach_referrer(user.tg_id, referrer["tg_id"])


async def cmd_start(message: Message, command: CommandObject, user: UserRecord, db: Database) -> None:
    name = html.escape(user.full_name or "дос")

    if user.is_new and await _apply_referral(db, user, command.args):
        await message.answer(kk.REFERRAL_WELCOME)

    if user.grade is None:
        await message.answer(kk.WELCOME_NEW.format(name=name), reply_markup=grade_keyboard())
        return

    await message.answer(kk.WELCOME_BACK.format(name=name, line=kk.LINE), reply_markup=main_menu())


async def on_grade(callback: CallbackQuery, user: UserRecord, db: Database) -> None:
    key = callback.data.split(":", 1)[1]
    if key in GRADES:
        await UserRepository(db).set_grade(user.tg_id, key)
        text = kk.GRADE_SAVED.format(grade=GRADES[key])
    else:
        text = kk.GRADE_SKIPPED

    await callback.answer()
    if callback.message:
        await callback.message.edit_text(text)
        await callback.message.answer(kk.MENU_TITLE.format(line=kk.LINE), reply_markup=main_menu())


async def cmd_menu(message: Message) -> None:
    await message.answer(kk.MENU_TITLE.format(line=kk.LINE), reply_markup=main_menu())


async def cmd_help(message: Message) -> None:
    await message.answer(kk.HELP)


def create_router() -> Router:
    router = Router(name="start")
    router.message.register(cmd_start, CommandStart())
    router.callback_query.register(on_grade, F.data.startswith("grade:"))
    router.message.register(cmd_menu, Command("menu"))
    router.message.register(cmd_help, Command("help"))
    return router
