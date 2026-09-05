"""Budget Policy Pydantic Schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BudgetPolicyCreate(BaseModel):
    category: str
    monthly_limit: float
    hard_cap: Optional[bool] = False


class BudgetPolicyRead(BaseModel):
    id: str
    user_id: str
    category: str
    monthly_limit: float
    hard_cap: bool
    current_spend: Optional[float] = 0.0
    status: Optional[str] = "NORMAL"  # NORMAL, WARNING, BREACHED
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
