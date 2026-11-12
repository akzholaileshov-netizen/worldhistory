from app.db.client import Database


class SubjectRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def list_active(self):
        return await self.db.fetch(
            "SELECT id, code, name_kk FROM subjects WHERE is_active ORDER BY sort_order, id"
        )

    async def get_by_code(self, code: str):
        return await self.db.fetchrow("SELECT id, code, name_kk FROM subjects WHERE code = %s", code)
