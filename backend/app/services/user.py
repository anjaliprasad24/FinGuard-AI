"""UserService for managing User application operations."""

from typing import List

from sqlalchemy.orm import Session

from app.exceptions import EntityNotFoundError
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserRead


class UserService:
    """Service layer for User entity business logic and orchestration."""

    def __init__(self, db: Session) -> None:
        """Initialize UserService with a caller-owned database session.

        Args:
            db: An active SQLAlchemy Session owned by the caller.
        """
        self.db = db
        self.user_repo = UserRepository(db)

    def create_user(self, data: UserCreate) -> UserRead:
        """Create a new user.

        Args:
            data: User creation schema.

        Returns:
            UserRead schema representation of created user.
        """
        user_orm = self.user_repo.create(**data.model_dump(exclude_unset=True))
        return UserRead.model_validate(user_orm)

    def get_user(self, user_id: str) -> UserRead:
        """Retrieve a user by unique ID.

        Args:
            user_id: User primary key.

        Returns:
            UserRead schema representation.

        Raises:
            EntityNotFoundError: If user is not found.
        """
        user_orm = self.user_repo.get_by_id(user_id)
        if user_orm is None:
            raise EntityNotFoundError(f"User with id '{user_id}' not found.")
        return UserRead.model_validate(user_orm)

    def list_users(self) -> List[UserRead]:
        """List all users.

        Returns:
            List of UserRead schemas.
        """
        users_orm = self.user_repo.list()
        return [UserRead.model_validate(u) for u in users_orm]

    def delete_user(self, user_id: str) -> bool:
        """Delete a user by unique ID.

        Args:
            user_id: User primary key.

        Returns:
            True if user was deleted.

        Raises:
            EntityNotFoundError: If user is not found.
        """
        user_orm = self.user_repo.get_by_id(user_id)
        if user_orm is None:
            raise EntityNotFoundError(f"User with id '{user_id}' not found.")
        return self.user_repo.delete(user_id)
