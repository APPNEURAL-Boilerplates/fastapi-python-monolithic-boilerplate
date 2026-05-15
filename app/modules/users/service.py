from app.common.errors import ConflictException, NotFoundException
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def list_users(self) -> list[User]:
        return self._repository.list()

    def get_user(self, user_id: str) -> User:
        user = self._repository.get(user_id)
        if user is None:
            raise NotFoundException("User not found.")
        return user

    def create_user(self, payload: UserCreate) -> User:
        if self._repository.get_by_email(str(payload.email)) is not None:
            raise ConflictException("A user with this email already exists.")

        user = User.create(name=payload.name, email=str(payload.email))
        return self._repository.create(user)

    def update_user(self, user_id: str, payload: UserUpdate) -> User:
        current = self.get_user(user_id)
        changes = payload.model_dump(exclude_unset=True)

        if "email" in changes and changes["email"] is not None:
            email = str(changes["email"])
            existing = self._repository.get_by_email(email)
            if existing is not None and existing.id != current.id:
                raise ConflictException("A user with this email already exists.")
            changes["email"] = email

        # Treat explicit null values as "no change" for PATCH convenience.
        changes = {key: value for key, value in changes.items() if value is not None}
        updated = self._repository.update(user_id, changes)
        if updated is None:
            raise NotFoundException("User not found.")
        return updated

    def delete_user(self, user_id: str) -> None:
        if not self._repository.delete(user_id):
            raise NotFoundException("User not found.")
