from dataclasses import replace
from threading import RLock
from typing import Protocol

from app.modules.users.models import User, utc_now


class UserRepository(Protocol):
    def list(self) -> list[User]: ...
    def get(self, user_id: str) -> User | None: ...
    def get_by_email(self, email: str) -> User | None: ...
    def create(self, user: User) -> User: ...
    def update(self, user_id: str, changes: dict[str, object]) -> User | None: ...
    def delete(self, user_id: str) -> bool: ...


class InMemoryUserRepository:
    """Simple in-memory repository for local development and tests.

    Replace this with SQLAlchemy, SQLModel, Tortoise ORM, Beanie, or your preferred
    database implementation when you connect real persistence.
    """

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._lock = RLock()

    def list(self) -> list[User]:
        with self._lock:
            return list(self._users.values())

    def get(self, user_id: str) -> User | None:
        with self._lock:
            return self._users.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        normalized_email = email.lower()
        with self._lock:
            return next(
                (user for user in self._users.values() if user.email.lower() == normalized_email),
                None,
            )

    def create(self, user: User) -> User:
        with self._lock:
            self._users[user.id] = user
            return user

    def update(self, user_id: str, changes: dict[str, object]) -> User | None:
        with self._lock:
            current = self._users.get(user_id)
            if current is None:
                return None

            next_user = replace(current, updated_at=utc_now(), **changes)
            self._users[user_id] = next_user
            return next_user

    def delete(self, user_id: str) -> bool:
        with self._lock:
            if user_id not in self._users:
                return False
            del self._users[user_id]
            return True
