"""ProcessingJob Pydantic contracts."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import ProcessingJobStatus


class ProcessingJobBase(BaseModel):
    """Base fields for ProcessingJob entity."""

    status: ProcessingJobStatus = ProcessingJobStatus.QUEUED


class ProcessingJobCreate(ProcessingJobBase):
    """Payload contract for creating a ProcessingJob."""

    session_id: str


class ProcessingJobUpdate(BaseModel):
    """Payload contract for updating a ProcessingJob."""

    status: Optional[ProcessingJobStatus] = None
    attempt_count: Optional[int] = Field(default=None, ge=0)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class ProcessingJobRead(ProcessingJobBase):
    """Response contract for reading a ProcessingJob."""

    id: str
    session_id: str
    attempt_count: int
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
