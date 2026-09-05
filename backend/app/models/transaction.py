"""Transaction ORM Model."""

from datetime import date
from sqlalchemy import Column, String, Float, Boolean, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, generate_uuid, utc_now


class Transaction(Base):
    """Financial transaction model."""

    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    raw_merchant = Column(String(255), nullable=False)
    clean_merchant = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="INR")
    category = Column(String(64), nullable=False)
    transaction_type = Column(String(16), default="EXPENSE")  # EXPENSE, INCOME
    confidence_score = Column(Float, default=1.0000)
    is_recurring = Column(Boolean, default=False)
    anomaly_score = Column(Float, default=0.0000)
    risk_level = Column(String(16), default="LOW")  # LOW, MEDIUM, HIGH, CRITICAL
    source = Column(String(32), default="CSV")  # CSV, OCR, SIMULATOR
    transaction_date = Column(Date, nullable=False)
    embedding = Column(JSON, nullable=True)  # Vector embedding float list
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="transactions")
