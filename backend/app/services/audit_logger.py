"""System Audit Logger Service."""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.audit import SystemAuditLog


class AuditLogger:
    """Records audit trail entries with JSON evidence payloads into the system_audit_logs table."""

    @classmethod
    def log_event(
        cls,
        db: Session,
        user_id: str,
        event_type: str,
        evidence_payload: Dict[str, Any],
        reference_id: Optional[str] = None,
        ai_explanation: Optional[str] = None
    ) -> SystemAuditLog:
        log_entry = SystemAuditLog(
            user_id=user_id,
            event_type=event_type,
            reference_id=reference_id,
            evidence_payload=evidence_payload,
            ai_generated_explanation=ai_explanation
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry
