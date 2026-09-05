"""ProcessingJobService for managing ProcessingJob domain operations and lifecycle logic."""

from typing import List

from sqlalchemy.orm import Session

from app.core.enums import ProcessingJobStatus
from app.exceptions import EntityNotFoundError, ValidationError
from app.models.base import utc_now
from app.repositories.processing_job import ProcessingJobRepository
from app.repositories.session import SessionRepository
from app.schemas.processing_job import (
    ProcessingJobCreate,
    ProcessingJobRead,
    ProcessingJobUpdate,
)


class ProcessingJobService:
    """Service layer for ProcessingJob domain entity business rules."""

    def __init__(self, db: Session) -> None:
        """Initialize ProcessingJobService with a caller-owned database session.

        Args:
            db: An active SQLAlchemy Session owned by the caller.
        """
        self.db = db
        self.job_repo = ProcessingJobRepository(db)
        self.session_repo = SessionRepository(db)

    def create_job(self, data: ProcessingJobCreate) -> ProcessingJobRead:
        """Create a new asynchronous processing job for a session.

        Args:
            data: ProcessingJob creation schema.

        Returns:
            ProcessingJobRead schema representation.

        Raises:
            EntityNotFoundError: If the referenced session does not exist.
        """
        session_orm = self.session_repo.get_by_id(data.session_id)
        if session_orm is None:
            raise EntityNotFoundError(f"Session with id '{data.session_id}' not found.")

        job_orm = self.job_repo.create(**data.model_dump(exclude_unset=True))
        return ProcessingJobRead.model_validate(job_orm)

    def get_job(self, job_id: str) -> ProcessingJobRead:
        """Retrieve a processing job by unique ID.

        Args:
            job_id: ProcessingJob primary key.

        Returns:
            ProcessingJobRead schema representation.

        Raises:
            EntityNotFoundError: If processing job is not found.
        """
        job_orm = self.job_repo.get_by_id(job_id)
        if job_orm is None:
            raise EntityNotFoundError(f"ProcessingJob with id '{job_id}' not found.")
        return ProcessingJobRead.model_validate(job_orm)

    def list_session_jobs(self, session_id: str) -> List[ProcessingJobRead]:
        """List all processing jobs belonging to a session.

        Args:
            session_id: Session primary key.

        Returns:
            List of ProcessingJobRead schemas.

        Raises:
            EntityNotFoundError: If the referenced session does not exist.
        """
        session_orm = self.session_repo.get_by_id(session_id)
        if session_orm is None:
            raise EntityNotFoundError(f"Session with id '{session_id}' not found.")

        jobs_orm = self.job_repo.list_by_session(session_id)
        return [ProcessingJobRead.model_validate(j) for j in jobs_orm]

    def update_job(self, job_id: str, data: ProcessingJobUpdate) -> ProcessingJobRead:
        """Update job fields and enforce job lifecycle business rules.

        Args:
            job_id: ProcessingJob primary key.
            data: ProcessingJob update schema.

        Returns:
            Updated ProcessingJobRead schema representation.

        Raises:
            EntityNotFoundError: If job is not found.
            ValidationError: If attempt count is negative, transition is illegal, or error state is inconsistent.
        """
        job_orm = self.job_repo.get_by_id(job_id)
        if job_orm is None:
            raise EntityNotFoundError(f"ProcessingJob with id '{job_id}' not found.")

        # 1. Reject negative attempt_count
        if data.attempt_count is not None and data.attempt_count < 0:
            raise ValidationError("attempt_count cannot be negative.")

        current_status = job_orm.status
        target_status = data.status if data.status is not None else current_status

        # 2. Reject illegal transitions from COMPLETED
        if current_status == ProcessingJobStatus.COMPLETED and target_status != ProcessingJobStatus.COMPLETED:
            raise ValidationError(
                f"Cannot transition completed job status to '{target_status.value}'."
            )

        update_payload = data.model_dump(exclude_unset=True)

        # 3. Entering PROCESSING automatically populates started_at if absent
        if target_status == ProcessingJobStatus.PROCESSING:
            if "started_at" not in update_payload and job_orm.started_at is None:
                update_payload["started_at"] = utc_now()

        # 4. Entering COMPLETED automatically populates completed_at if absent & enforces clean error state
        if target_status == ProcessingJobStatus.COMPLETED:
            if data.error is not None and data.error.strip() != "":
                raise ValidationError("COMPLETED jobs must have clean error state.")
            if "completed_at" not in update_payload and job_orm.completed_at is None:
                update_payload["completed_at"] = utc_now()
            # Ensure error is cleared on completion
            update_payload["error"] = None

        updated_orm = self.job_repo.update(job_id, **update_payload)
        return ProcessingJobRead.model_validate(updated_orm)

    def delete_job(self, job_id: str) -> bool:
        """Delete a processing job by unique ID.

        Args:
            job_id: ProcessingJob primary key.

        Returns:
            True if job was deleted.

        Raises:
            EntityNotFoundError: If job is not found.
        """
        job_orm = self.job_repo.get_by_id(job_id)
        if job_orm is None:
            raise EntityNotFoundError(f"ProcessingJob with id '{job_id}' not found.")
        return self.job_repo.delete(job_id)
