"""MemoryService for managing Memory domain operations."""

from typing import List

from sqlalchemy.orm import Session

from app.exceptions import EntityNotFoundError, ValidationError
from app.repositories.memory import MemoryRepository
from app.repositories.session import SessionRepository
from app.schemas.memory import MemoryCreate, MemoryRead, MemoryUpdate


class MemoryService:
    """Service layer for Memory entity business rules."""

    def __init__(self, db: Session) -> None:
        """Initialize MemoryService with a caller-owned database session.

        Args:
            db: An active SQLAlchemy Session owned by the caller.
        """
        self.db = db
        self.memory_repo = MemoryRepository(db)
        self.session_repo = SessionRepository(db)

    def create_memory(self, data: MemoryCreate) -> MemoryRead:
        """Create a new memory attached to a session.

        Args:
            data: Memory creation schema.

        Returns:
            MemoryRead schema representation.

        Raises:
            EntityNotFoundError: If referenced session does not exist.
            ValidationError: If title or content is empty or whitespace.
        """
        session_orm = self.session_repo.get_by_id(data.session_id)
        if session_orm is None:
            raise EntityNotFoundError(f"Session with id '{data.session_id}' not found.")

        if not data.title or not data.title.strip():
            raise ValidationError("Memory title must not be empty.")
        if not data.content or not data.content.strip():
            raise ValidationError("Memory content must not be empty.")

        memory_orm = self.memory_repo.create(**data.model_dump(exclude_unset=True))
        return MemoryRead.model_validate(memory_orm)

    def get_memory(self, memory_id: str) -> MemoryRead:
        """Retrieve a memory by unique ID.

        Args:
            memory_id: Memory primary key.

        Returns:
            MemoryRead schema representation.

        Raises:
            EntityNotFoundError: If memory is not found.
        """
        memory_orm = self.memory_repo.get_by_id(memory_id)
        if memory_orm is None:
            raise EntityNotFoundError(f"Memory with id '{memory_id}' not found.")
        return MemoryRead.model_validate(memory_orm)

    def list_session_memories(self, session_id: str) -> List[MemoryRead]:
        """List all memories belonging to a session.

        Args:
            session_id: Session primary key.

        Returns:
            List of MemoryRead schemas.

        Raises:
            EntityNotFoundError: If referenced session does not exist.
        """
        session_orm = self.session_repo.get_by_id(session_id)
        if session_orm is None:
            raise EntityNotFoundError(f"Session with id '{session_id}' not found.")

        memories_orm = self.memory_repo.list_by_session(session_id)
        return [MemoryRead.model_validate(m) for m in memories_orm]

    def update_memory(self, memory_id: str, data: MemoryUpdate) -> MemoryRead:
        """Update fields of an existing memory.

        Args:
            memory_id: Memory primary key.
            data: Memory update schema.

        Returns:
            Updated MemoryRead schema representation.

        Raises:
            EntityNotFoundError: If memory is not found.
            ValidationError: If title or content is provided as empty/whitespace.
        """
        memory_orm = self.memory_repo.get_by_id(memory_id)
        if memory_orm is None:
            raise EntityNotFoundError(f"Memory with id '{memory_id}' not found.")

        if data.title is not None and not data.title.strip():
            raise ValidationError("Memory title must not be empty.")
        if data.content is not None and not data.content.strip():
            raise ValidationError("Memory content must not be empty.")

        updated_orm = self.memory_repo.update(memory_id, **data.model_dump(exclude_unset=True))
        return MemoryRead.model_validate(updated_orm)

    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory by unique ID.

        Args:
            memory_id: Memory primary key.

        Returns:
            True if memory was deleted.

        Raises:
            EntityNotFoundError: If memory is not found.
        """
        memory_orm = self.memory_repo.get_by_id(memory_id)
        if memory_orm is None:
            raise EntityNotFoundError(f"Memory with id '{memory_id}' not found.")
        return self.memory_repo.delete(memory_id)
