"""Session Pydantic contracts."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.enums import SessionStatus


class SessionBase(BaseModel):
    """Base fields for Session entity."""

    status: SessionStatus = SessionStatus.ACTIVE


class SessionCreate(SessionBase):
    """Payload contract for creating a Session."""

    user_id: str
    started_at: Optional[datetime] = None


class SessionUpdate(BaseModel):
    """Payload contract for updating a Session."""

    status: Optional[SessionStatus] = None
    ended_at: Optional[datetime] = None


class SessionRead(SessionBase):
    """Response contract for reading a Session."""

    id: str
    user_id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
