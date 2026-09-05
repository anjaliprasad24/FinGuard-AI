"""MemoryFeedback Pydantic contracts."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import MemoryFeedbackType


class MemoryFeedbackBase(BaseModel):
    """Base fields for MemoryFeedback entity."""

    feedback_type: MemoryFeedbackType


class MemoryFeedbackCreate(MemoryFeedbackBase):
    """Payload contract for creating MemoryFeedback."""

    memory_id: str


class MemoryFeedbackRead(MemoryFeedbackBase):
    """Response contract for reading MemoryFeedback."""

    id: str
    memory_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
