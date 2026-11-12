# World History AI

ҰБТ-ға дайындалатын оқушыларға арналған Telegram бот (Дүниежүзі тарихы).
Стек: Python 3.12, Aiogram 3, Supabase PostgreSQL, Gemini Flash.

## Іске қосу (Windows / PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy-Item .env.example .env      # .env ішіне BOT_TOKEN және DATABASE_URL жазыңыз
python -m scripts.migrate        # Supabase-те кестелерді жасайды
python main.py                   # ботты іске қосады (polling)
```

## Тест

```powershell
pytest
```

## Құрылым

- `app/handlers` — Telegram хендлерлері (жұқа қабат)
- `app/services` — бизнес-логика
- `app/db/repositories` — SQL қабаты
- `app/texts/kk.py` — барлық қазақша мәтіндер
- `migrations/` — нөмірленген SQL миграциялар
- `scripts/` — бір реттік құралдар (миграция, PDF импорт)
- `data/` — PDF-тер (git-ке қосылмайды), пән бойынша бөлінген

Жаңа пән қосу: `subjects` кестесіне жол қосып, `data/<пән>/` папкасына контент салу жеткілікті.
