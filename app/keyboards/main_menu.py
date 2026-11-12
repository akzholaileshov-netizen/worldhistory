from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.core.constants import GRADES
from app.texts import kk


def main_menu() -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    for text in kk.MENU_BUTTONS:
        b.button(text=text)
    # 2-2-2-2-1 қатар, ыңғайлы әрі минималистік
    b.adjust(2, 2, 2, 2, 1)
    return b.as_markup(resize_keyboard=True, is_persistent=True, input_field_placeholder="Бөлімді таңда…")


def grade_keyboard() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for key, label in GRADES.items():
        b.button(text=f"🔹 {label}", callback_data=f"grade:{key}")
    b.button(text=kk.BTN_SKIP, callback_data="grade:skip")
    b.adjust(2, 2, 1)
    return b.as_markup()
