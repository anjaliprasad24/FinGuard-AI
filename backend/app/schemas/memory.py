"""Memory Pydantic contracts."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import MemoryType


class MemoryBase(BaseModel):
    """Base fields for Memory entity."""

    title: str = Field(..., max_length=255)
    content: str
    memory_type: MemoryType = MemoryType.EPISODIC


class MemoryCreate(MemoryBase):
    """Payload contract for creating a Memory."""

    session_id: str


class MemoryUpdate(BaseModel):
    """Payload contract for updating a Memory."""

    title: Optional[str] = Field(default=None, max_length=255)
    content: Optional[str] = None
    memory_type: Optional[MemoryType] = None


class MemoryRead(MemoryBase):
    """Response contract for reading a Memory."""

    id: str
    session_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
