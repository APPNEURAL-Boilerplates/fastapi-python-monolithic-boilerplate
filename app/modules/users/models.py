from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class User:
    id: str
    name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, *, name: str, email: str) -> "User":
        now = utc_now()
        return cls(
            id=str(uuid4()),
            name=name,
            email=email,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
