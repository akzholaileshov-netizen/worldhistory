"""/start ағынын жалған Database және жалған Telegram сессиясымен тексереді."""

import os
from datetime import datetime

os.environ.setdefault("BOT_TOKEN", "123456:TEST")
os.environ.setdefault("DATABASE_URL", "postgresql://u:p@localhost:5432/db")

import pytest
from aiogram import Bot
from aiogram.client.session.base import BaseSession
from aiogram.methods import AnswerCallbackQuery, EditMessageText, SendMessage
from aiogram.types import CallbackQuery, Chat, Message, Update, User

from app.bot import build_dispatcher
from app.config import Settings
from app.core.constants import GRADES
from app.db.client import Database
from app.texts import kk


class FakeDb(Database):
    def __init__(self) -> None:
        super().__init__()
        self.users: dict[int, dict] = {}
        self.executed: list[tuple] = []

    async def fetchrow(self, query, *args):
        if "INSERT INTO users" in query:
            tg_id, username, full_name, ref_code, _subject = args
            is_new = tg_id not in self.users
            if is_new:
                self.users[tg_id] = dict(
                    tg_id=tg_id, username=username, full_name=full_name, grade=None,
                    current_subject_id=1, ref_code=ref_code, referred_by=None,
                    xp=0, streak=0, is_banned=False,
                )
            return {**self.users[tg_id], "is_new": is_new}
        return None

    async def fetchval(self, query, *args):
        return None

    async def execute(self, query, *args):
        self.executed.append((query, args))
        if query.startswith("UPDATE users SET grade"):
            grade, tg_id = args
            self.users[tg_id]["grade"] = grade


class FakeSession(BaseSession):
    def __init__(self) -> None:
        super().__init__()
        self.calls: list = []

    async def close(self) -> None:  # pragma: no cover
        pass

    async def stream_content(self, *a, **k):  # pragma: no cover
        yield b""

    async def make_request(self, bot, method, timeout=None):
        self.calls.append(method)
        if isinstance(method, AnswerCallbackQuery):
            return True
        return Message(message_id=len(self.calls), date=datetime.now(), chat=Chat(id=1, type="private"))


def _setup():
    session = FakeSession()
    bot = Bot("123456:TEST", session=session)
    db = FakeDb()
    dp = build_dispatcher(db, Settings(bot_token="x", database_url="y"), throttle_seconds=0)
    return bot, dp, db, session


def _msg(text: str, uid: int = 1) -> Message:
    return Message(
        message_id=1, date=datetime.now(), chat=Chat(id=uid, type="private"),
        from_user=User(id=uid, is_bot=False, first_name="Айдос"), text=text,
        entities=[{"type": "bot_command", "offset": 0, "length": 6}] if text.startswith("/start") else None,
    )


@pytest.mark.asyncio
async def test_new_user_gets_grade_picker_then_menu():
    bot, dp, db, session = _setup()

    await dp.feed_update(bot, Update(update_id=1, message=_msg("/start")))
    assert 1 in db.users and db.users[1]["grade"] is None
    sent = [c for c in session.calls if isinstance(c, SendMessage)]
    assert "Алдымен, қай сыныптасың" in sent[0].text
    assert sent[0].reply_markup is not None

    cb = CallbackQuery(
        id="1", chat_instance="x", data="grade:11",
        from_user=User(id=1, is_bot=False, first_name="Айдос"),
        message=Message(message_id=5, date=datetime.now(), chat=Chat(id=1, type="private")),
    )
    await dp.feed_update(bot, Update(update_id=2, callback_query=cb))
    assert db.users[1]["grade"] == "11"
    assert any(isinstance(c, EditMessageText) and GRADES["11"] in c.text for c in session.calls)
    assert any(isinstance(c, SendMessage) and "Бас мәзір" in c.text for c in session.calls)


@pytest.mark.asyncio
async def test_menu_button_shows_placeholder():
    bot, dp, db, session = _setup()
    await dp.feed_update(bot, Update(update_id=1, message=_msg(kk.BTN_TEST)))
    sent = [c for c in session.calls if isinstance(c, SendMessage)]
    assert sent and "жақында" in sent[0].text
