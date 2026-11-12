from aiogram import Router

from app.handlers import placeholders, start


def get_root_router() -> Router:
    root = Router(name="root")
    root.include_router(start.create_router())
    # Жаңа бөлімдер (test, ai_teacher, ...) placeholders-тен ЕЖЕЛЕ қосылады
    root.include_router(placeholders.create_router())
    return root
