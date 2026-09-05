"""Budget Policy ORM Model."""

from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base, generate_uuid, utc_now


class BudgetPolicy(Base):
    """Budget policy model."""

    __tablename__ = "budget_policies"
    __table_args__ = (UniqueConstraint("user_id", "category", name="uq_user_category"),)

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(64), nullable=False)
    monthly_limit = Column(Float, nullable=False)
    hard_cap = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="policies")
