"""MemoryEvidence Pydantic contracts."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import MemorySourceType


class MemoryEvidenceBase(BaseModel):
    """Base fields for MemoryEvidence entity."""

    source_type: MemorySourceType
    source_reference: str


class MemoryEvidenceCreate(MemoryEvidenceBase):
    """Payload contract for creating MemoryEvidence."""

    memory_id: str


class MemoryEvidenceRead(MemoryEvidenceBase):
    """Response contract for reading MemoryEvidence."""

    id: str
    memory_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
