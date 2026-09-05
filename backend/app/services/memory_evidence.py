"""MemoryEvidenceService for managing MemoryEvidence domain operations."""

from typing import List

from sqlalchemy.orm import Session

from app.exceptions import EntityNotFoundError, ValidationError
from app.repositories.memory import MemoryRepository
from app.repositories.memory_evidence import MemoryEvidenceRepository
from app.schemas.memory_evidence import MemoryEvidenceCreate, MemoryEvidenceRead


class MemoryEvidenceService:
    """Service layer for MemoryEvidence domain entity business rules."""

    def __init__(self, db: Session) -> None:
        """Initialize MemoryEvidenceService with a caller-owned database session.

        Args:
            db: An active SQLAlchemy Session owned by the caller.
        """
        self.db = db
        self.evidence_repo = MemoryEvidenceRepository(db)
        self.memory_repo = MemoryRepository(db)

    def create_evidence(self, data: MemoryEvidenceCreate) -> MemoryEvidenceRead:
        """Create a context evidence record for a memory.

        Args:
            data: MemoryEvidence creation schema.

        Returns:
            MemoryEvidenceRead schema representation.

        Raises:
            EntityNotFoundError: If referenced memory does not exist.
            ValidationError: If source_reference is empty or whitespace.
        """
        memory_orm = self.memory_repo.get_by_id(data.memory_id)
        if memory_orm is None:
            raise EntityNotFoundError(f"Memory with id '{data.memory_id}' not found.")

        if not data.source_reference or not data.source_reference.strip():
            raise ValidationError("source_reference must not be empty.")

        evidence_orm = self.evidence_repo.create(**data.model_dump(exclude_unset=True))
        return MemoryEvidenceRead.model_validate(evidence_orm)

    def get_evidence(self, evidence_id: str) -> MemoryEvidenceRead:
        """Retrieve a memory evidence record by unique ID.

        Args:
            evidence_id: MemoryEvidence primary key.

        Returns:
            MemoryEvidenceRead schema representation.

        Raises:
            EntityNotFoundError: If evidence is not found.
        """
        evidence_orm = self.evidence_repo.get_by_id(evidence_id)
        if evidence_orm is None:
            raise EntityNotFoundError(f"MemoryEvidence with id '{evidence_id}' not found.")
        return MemoryEvidenceRead.model_validate(evidence_orm)

    def list_memory_evidence(self, memory_id: str) -> List[MemoryEvidenceRead]:
        """List all context evidence records belonging to a memory.

        Args:
            memory_id: Memory primary key.

        Returns:
            List of MemoryEvidenceRead schemas.

        Raises:
            EntityNotFoundError: If referenced memory does not exist.
        """
        memory_orm = self.memory_repo.get_by_id(memory_id)
        if memory_orm is None:
            raise EntityNotFoundError(f"Memory with id '{memory_id}' not found.")

        evidences_orm = self.evidence_repo.list_by_memory(memory_id)
        return [MemoryEvidenceRead.model_validate(e) for e in evidences_orm]

    def delete_evidence(self, evidence_id: str) -> bool:
        """Delete a memory evidence record by unique ID.

        Args:
            evidence_id: MemoryEvidence primary key.

        Returns:
            True if evidence was deleted.

        Raises:
            EntityNotFoundError: If evidence is not found.
        """
        evidence_orm = self.evidence_repo.get_by_id(evidence_id)
        if evidence_orm is None:
            raise EntityNotFoundError(f"MemoryEvidence with id '{evidence_id}' not found.")
        return self.evidence_repo.delete(evidence_id)
