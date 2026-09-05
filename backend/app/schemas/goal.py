"""Financial Goal Pydantic Schemas."""

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class FinancialGoalCreate(BaseModel):
    title: str
    target_amount: float
    current_savings: Optional[float] = 0.00
    target_date: date
    priority: Optional[int] = 1


class FinancialGoalRead(BaseModel):
    id: str
    user_id: str
    title: str
    target_amount: float
    current_savings: float
    target_date: date
    priority: int
    status: str  # ON_TRACK, AT_RISK, DELAYED
    required_monthly_savings: Optional[float] = 0.0
    projected_completion_date: Optional[date] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
