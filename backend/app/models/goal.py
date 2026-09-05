"""Financial Goal ORM Model."""

from sqlalchemy import Column, String, Float, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, generate_uuid, utc_now


class FinancialGoal(Base):
    """Financial goal model."""

    __tablename__ = "financial_goals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(128), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_savings = Column(Float, default=0.00)
    target_date = Column(Date, nullable=False)
    priority = Column(Integer, default=1)
    status = Column(String(32), default="ON_TRACK")  # ON_TRACK, AT_RISK, DELAYED
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="goals")
