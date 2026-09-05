"""System Audit Log Pydantic Schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class AuditLogRead(BaseModel):
    id: str
    user_id: str
    event_type: str
    reference_id: Optional[str] = None
    evidence_payload: Dict[str, Any]
    ai_generated_explanation: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
