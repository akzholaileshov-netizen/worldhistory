"""Барлық қазақша мәтіндер осы жерде. Жаңа тіл қосу керек болса, сәйкес файл жасалады."""

LINE = "━━━━━━━━━━━━━━"

# --- Бас мәзір батырмалары ---
BTN_TEST = "📚 Тест тапсыру"
BTN_AI = "🧠 AI мұғалім"
BTN_READY = "📝 Дайын тесттер"
BTN_LIBRARY = "📖 Кітапхана"
BTN_MISTAKES = "❌ Қателерім"
BTN_STATS = "📊 Статистика"
BTN_RATING = "🏆 Рейтинг"
BTN_REFERRAL = "👥 Достарды шақыру"
BTN_PRO = "💎 Pro"

MENU_BUTTONS = (
    BTN_TEST,
    BTN_AI,
    BTN_READY,
    BTN_LIBRARY,
    BTN_MISTAKES,
    BTN_STATS,
    BTN_RATING,
    BTN_REFERRAL,
    BTN_PRO,
)

# --- Бастау ---
WELCOME_NEW = (
    "🔷 <b>World History AI</b>\n"
    f"{LINE}\n"
    "Сәлем, <b>{name}</b>! 👋\n\n"
    "Мен сені ҰБТ-ға <b>Дүниежүзі тарихынан</b> дайындаймын:\n"
    "🔹 тесттер мен қателермен жұмыс\n"
    "🔹 AI мұғалім және кітаптан іздеу\n"
    "🔹 статистика мен рейтинг\n\n"
    "Алдымен, қай сыныптасың?"
)
WELCOME_BACK = "🔷 <b>World History AI</b>\n{line}\nҚайта оралғаныңа қуаныштымын, <b>{name}</b>! 👋\nБөлімді таңда 👇"
GRADE_SAVED = "✅ Керемет! <b>{grade}</b> сақталды."
GRADE_SKIPPED = "Жарайды, кейін өзгертуге болады."
BTN_SKIP = "Өткізіп жіберу"
MENU_TITLE = "🔷 <b>Бас мәзір</b>\n{line}\nБөлімді таңда 👇"
REFERRAL_WELCOME = "🎁 Сені досың шақырды! Екеуің де бонус аласыңдар (жақында)."

# --- Қызмет ---
HELP = (
    "🔷 <b>Көмек</b>\n"
    f"{LINE}\n"
    "/start: ботты бастау\n"
    "/menu: бас мәзір\n"
    "/help: көмек\n"
)
COMING_SOON = "🔹 <b>{section}</b>\n{line}\nБұл бөлім жақында қосылады. ⏳"
BANNED = "⛔ Сіздің аккаунтыңыз бұғатталған."
TOO_FAST = "⏳ Сәл баяуырақ."
ERROR_GENERIC = "⚠️ Қате орын алды. Кейінірек қайталап көріңіз."
