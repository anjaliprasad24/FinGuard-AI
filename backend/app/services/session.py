"""SessionService for managing Session domain operations and lifecycle logic."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.enums import SessionStatus
from app.exceptions import EntityNotFoundError, ValidationError
from app.models.base import utc_now
from app.repositories.session import SessionRepository
from app.repositories.user import UserRepository
from app.schemas.session import SessionCreate, SessionRead, SessionUpdate


class SessionService:
    """Service layer for Session domain entity business rules."""

    def __init__(self, db: Session) -> None:
        """Initialize SessionService with a caller-owned database session.

        Args:
            db: An active SQLAlchemy Session owned by the caller.
        """
        self.db = db
        self.session_repo = SessionRepository(db)
        self.user_repo = UserRepository(db)

    def create_session(self, data: SessionCreate) -> SessionRead:
        """Create a new interaction session for a user.

        Args:
            data: Session creation schema.

        Returns:
            SessionRead schema representation.

        Raises:
            EntityNotFoundError: If the referenced user does not exist.
        """
        user_orm = self.user_repo.get_by_id(data.user_id)
        if user_orm is None:
            raise EntityNotFoundError(f"User with id '{data.user_id}' not found.")

        session_orm = self.session_repo.create(**data.model_dump(exclude_unset=True))
        return SessionRead.model_validate(session_orm)

    def get_session(self, session_id: str) -> SessionRead:
        """Retrieve a session by unique ID.

        Args:
            session_id: Session primary key.

        Returns:
            SessionRead schema representation.

        Raises:
            EntityNotFoundError: If the session is not found.
        """
        session_orm = self.session_repo.get_by_id(session_id)
        if session_orm is None:
            raise EntityNotFoundError(f"Session with id '{session_id}' not found.")
        return SessionRead.model_validate(session_orm)

    def list_user_sessions(self, user_id: str) -> List[SessionRead]:
        """List all sessions belonging to a specific user.

        Args:
            user_id: User primary key.

        Returns:
            List of SessionRead schemas.

        Raises:
            EntityNotFoundError: If the referenced user does not exist.
        """
        user_orm = self.user_repo.get_by_id(user_id)
        if user_orm is None:
            raise EntityNotFoundError(f"User with id '{user_id}' not found.")

        sessions_orm = self.session_repo.list_by_user(user_id)
        return [SessionRead.model_validate(s) for s in sessions_orm]

    def update_session(self, session_id: str, data: SessionUpdate) -> SessionRead:
        """Update fields and enforce status transition rules for a session.

        Args:
            session_id: Session primary key.
            data: Session update schema.

        Returns:
            Updated SessionRead schema representation.

        Raises:
            EntityNotFoundError: If session is not found.
            ValidationError: If status transition or timestamp combination is invalid.
        """
        session_orm = self.session_repo.get_by_id(session_id)
        if session_orm is None:
            raise EntityNotFoundError(f"Session with id '{session_id}' not found.")

        current_status = session_orm.status
        target_status = data.status if data.status is not None else current_status

        # 1. Reject invalid status transitions back to ACTIVE
        terminal_statuses = (
            SessionStatus.COMPLETED,
            SessionStatus.FAILED,
            SessionStatus.ABANDONED,
        )
        if current_status in terminal_statuses and target_status == SessionStatus.ACTIVE:
            raise ValidationError(
                f"Cannot transition session from '{current_status.value}' to 'ACTIVE'."
            )

        update_payload = data.model_dump(exclude_unset=True)

        # Determine resulting ended_at
        if "ended_at" in update_payload:
            resulting_ended_at = update_payload["ended_at"]
        else:
            resulting_ended_at = session_orm.ended_at

        # 2. ACTIVE session cannot have ended_at set
        if target_status == SessionStatus.ACTIVE and resulting_ended_at is not None:
            raise ValidationError("An ACTIVE session cannot have an ended_at timestamp.")

        # 3. Automatically populate ended_at when transitioning from ACTIVE -> terminal state if not supplied
        if current_status == SessionStatus.ACTIVE and target_status in terminal_statuses:
            if resulting_ended_at is None:
                update_payload["ended_at"] = utc_now()

        updated_orm = self.session_repo.update(session_id, **update_payload)
        return SessionRead.model_validate(updated_orm)

    def delete_session(self, session_id: str) -> bool:
        """Delete a session by unique ID.

        Args:
            session_id: Session primary key.

        Returns:
            True if session was deleted.

        Raises:
            EntityNotFoundError: If session is not found.
        """
        session_orm = self.session_repo.get_by_id(session_id)
        if session_orm is None:
            raise EntityNotFoundError(f"Session with id '{session_id}' not found.")
        return self.session_repo.delete(session_id)
