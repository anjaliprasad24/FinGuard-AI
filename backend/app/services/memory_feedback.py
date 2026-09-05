"""MemoryFeedbackService for managing MemoryFeedback domain operations."""

from typing import List

from sqlalchemy.orm import Session

from app.exceptions import EntityNotFoundError
from app.repositories.memory import MemoryRepository
from app.repositories.memory_feedback import MemoryFeedbackRepository
from app.schemas.memory_feedback import MemoryFeedbackCreate, MemoryFeedbackRead


class MemoryFeedbackService:
    """Service layer for MemoryFeedback domain entity business rules."""

    def __init__(self, db: Session) -> None:
        """Initialize MemoryFeedbackService with a caller-owned database session.

        Args:
            db: An active SQLAlchemy Session owned by the caller.
        """
        self.db = db
        self.feedback_repo = MemoryFeedbackRepository(db)
        self.memory_repo = MemoryRepository(db)

    def create_feedback(self, data: MemoryFeedbackCreate) -> MemoryFeedbackRead:
        """Create a user feedback record for a memory.

        Args:
            data: MemoryFeedback creation schema.

        Returns:
            MemoryFeedbackRead schema representation.

        Raises:
            EntityNotFoundError: If referenced memory does not exist.
        """
        memory_orm = self.memory_repo.get_by_id(data.memory_id)
        if memory_orm is None:
            raise EntityNotFoundError(f"Memory with id '{data.memory_id}' not found.")

        feedback_orm = self.feedback_repo.create(**data.model_dump(exclude_unset=True))
        return MemoryFeedbackRead.model_validate(feedback_orm)

    def get_feedback(self, feedback_id: str) -> MemoryFeedbackRead:
        """Retrieve a memory feedback record by unique ID.

        Args:
            feedback_id: MemoryFeedback primary key.

        Returns:
            MemoryFeedbackRead schema representation.

        Raises:
            EntityNotFoundError: If feedback is not found.
        """
        feedback_orm = self.feedback_repo.get_by_id(feedback_id)
        if feedback_orm is None:
            raise EntityNotFoundError(f"MemoryFeedback with id '{feedback_id}' not found.")
        return MemoryFeedbackRead.model_validate(feedback_orm)

    def list_memory_feedback(self, memory_id: str) -> List[MemoryFeedbackRead]:
        """List all user feedback records belonging to a memory.

        Args:
            memory_id: Memory primary key.

        Returns:
            List of MemoryFeedbackRead schemas.

        Raises:
            EntityNotFoundError: If referenced memory does not exist.
        """
        memory_orm = self.memory_repo.get_by_id(memory_id)
        if memory_orm is None:
            raise EntityNotFoundError(f"Memory with id '{memory_id}' not found.")

        feedbacks_orm = self.feedback_repo.list_by_memory(memory_id)
        return [MemoryFeedbackRead.model_validate(f) for f in feedbacks_orm]

    def delete_feedback(self, feedback_id: str) -> bool:
        """Delete a memory feedback record by unique ID.

        Args:
            feedback_id: MemoryFeedback primary key.

        Returns:
            True if feedback was deleted.

        Raises:
            EntityNotFoundError: If feedback is not found.
        """
        feedback_orm = self.feedback_repo.get_by_id(feedback_id)
        if feedback_orm is None:
            raise EntityNotFoundError(f"MemoryFeedback with id '{feedback_id}' not found.")
        return self.feedback_repo.delete(feedback_id)
