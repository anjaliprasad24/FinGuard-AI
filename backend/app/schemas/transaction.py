"""Transaction Pydantic Schemas."""

from datetime import date, datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict


class TransactionIngestRequest(BaseModel):
    raw_merchant: str
    amount: float
    category: Optional[str] = None
    currency: Optional[str] = "INR"
    transaction_date: Optional[date] = None
    transaction_type: Optional[str] = "EXPENSE"
    source: Optional[str] = "API"


class TransactionRead(BaseModel):
    id: str
    user_id: str
    raw_merchant: str
    clean_merchant: str
    amount: float
    currency: str
    category: str
    transaction_type: str
    confidence_score: float
    is_recurring: bool
    anomaly_score: float
    risk_level: str
    source: str
    transaction_date: date
    created_at: datetime
    evidence_payload: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class TransactionIngestResponse(BaseModel):
    transaction: TransactionRead
    is_anomaly: bool
    policy_breach: bool
    policy_warning: Optional[str] = None
    evidence_payload: Dict[str, Any]
