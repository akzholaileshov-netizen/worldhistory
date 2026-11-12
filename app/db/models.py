from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class UserRecord:
    tg_id: int
    username: str | None
    full_name: str
    grade: str | None
    current_subject_id: int | None
    ref_code: str
    referred_by: int | None
    xp: int
    streak: int
    is_banned: bool
    is_new: bool = False

    @classmethod
    def from_record(cls, row: Any) -> "UserRecord":
        return cls(
            tg_id=row["tg_id"],
            username=row["username"],
            full_name=row["full_name"],
            grade=row["grade"],
            current_subject_id=row["current_subject_id"],
            ref_code=row["ref_code"],
            referred_by=row["referred_by"],
            xp=row["xp"],
            streak=row["streak"],
            is_banned=row["is_banned"],
            is_new=bool(row["is_new"]) if "is_new" in row.keys() else False,
        )
