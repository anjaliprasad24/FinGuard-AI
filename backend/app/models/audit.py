"""System Audit Log ORM Model."""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, generate_uuid, utc_now


class SystemAuditLog(Base):
    """System audit log model."""

    __tablename__ = "system_audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)  # ANOMALY_FLAGGED, POLICY_BREACH, SIMULATION, COPILOT_QUERY
    reference_id = Column(String(36), nullable=True)
    evidence_payload = Column(JSON, nullable=False)
    ai_generated_explanation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="audit_logs")
