import secrets
import string

from psycopg.errors import UniqueViolation

from app.core.constants import REFERRAL_CODE_LENGTH
from app.db.client import Database
from app.db.models import UserRecord

_ALPHABET = string.ascii_uppercase + string.digits

_UPSERT = """
INSERT INTO users (tg_id, username, full_name, ref_code, current_subject_id)
VALUES (%s, %s, %s, %s, (SELECT id FROM subjects WHERE code = %s))
ON CONFLICT (tg_id) DO UPDATE
    SET username = EXCLUDED.username,
        full_name = EXCLUDED.full_name,
        last_active = now()
RETURNING *, (xmax = 0) AS is_new
"""


def _new_ref_code() -> str:
    return "".join(secrets.choice(_ALPHABET) for _ in range(REFERRAL_CODE_LENGTH))


class UserRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def upsert_from_telegram(
        self, tg_id: int, username: str | None, full_name: str, default_subject: str
    ) -> UserRecord:
        for _ in range(5):  # ref_code коллизиясы өте сирек, бірақ қайталап көреміз
            try:
                row = await self.db.fetchrow(
                    _UPSERT, tg_id, username, full_name, _new_ref_code(), default_subject
                )
                return UserRecord.from_record(row)
            except UniqueViolation as e:
                if e.diag.constraint_name is None or "ref_code" not in e.diag.constraint_name:
                    raise
        raise RuntimeError("Бірегей ref_code жасау мүмкін болмады")

    async def set_grade(self, tg_id: int, grade: str) -> None:
        await self.db.execute("UPDATE users SET grade = %s WHERE tg_id = %s", grade, tg_id)

    async def get_by_ref_code(self, code: str):
        return await self.db.fetchrow("SELECT tg_id FROM users WHERE ref_code = %s", code)

    async def attach_referrer(self, user_id: int, referrer_id: int) -> bool:
        """Жаңа қолданушыны шақырушымен байлайды. Тек бір рет жұмыс істейді."""
        if user_id == referrer_id:
            return False
        updated = await self.db.fetchval(
            "UPDATE users SET referred_by = %s WHERE tg_id = %s AND referred_by IS NULL RETURNING tg_id",
            referrer_id,
            user_id,
        )
        if updated is None:
            return False
        await self.db.execute(
            "INSERT INTO referrals (referrer_id, referred_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            referrer_id,
            user_id,
        )
        return True
