"""User ORM Model."""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, generate_uuid, utc_now


class User(Base):
    """User account model."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    risk_tolerance = Column(String(32), default="MODERATE")  # LOW, MODERATE, HIGH
    min_reserve_threshold = Column(Float, default=10000.00)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    policies = relationship("BudgetPolicy", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("FinancialGoal", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("SystemAuditLog", back_populates="user", cascade="all, delete-orphan")
