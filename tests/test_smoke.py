import os

os.environ.setdefault("BOT_TOKEN", "123456:TEST")
os.environ.setdefault("DATABASE_URL", "postgresql://u:p@localhost:5432/db")

from app.bot import build_dispatcher
from app.config import Settings
from app.core.constants import GRADES
from app.db.client import Database
from app.keyboards.main_menu import grade_keyboard, main_menu
from app.texts import kk


def test_settings_admin_ids():
    s = Settings(bot_token="x", database_url="y", admin_ids="1, 2,abc,3")
    assert s.admin_id_set == {1, 2, 3}


def test_main_menu_has_all_buttons():
    kb = main_menu()
    labels = [b.text for row in kb.keyboard for b in row]
    assert labels == list(kk.MENU_BUTTONS)
    assert len(labels) == 9


def test_grade_keyboard():
    kb = grade_keyboard()
    data = [b.callback_data for row in kb.inline_keyboard for b in row]
    assert data == [f"grade:{k}" for k in GRADES] + ["grade:skip"]


def test_dispatcher_builds():
    dp = build_dispatcher(Database(), Settings(bot_token="x", database_url="y"))
    assert dp is not None


def test_texts_format():
    kk.WELCOME_NEW.format(name="Айдос")
    kk.WELCOME_BACK.format(name="Айдос", line=kk.LINE)
    kk.MENU_TITLE.format(line=kk.LINE)
    kk.COMING_SOON.format(section="x", line=kk.LINE)
