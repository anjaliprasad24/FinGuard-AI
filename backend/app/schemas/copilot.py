"""Copilot & Simulation Pydantic Schemas."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class SimulationRequest(BaseModel):
    amount: float
    category: str
    merchant: Optional[str] = "Simulated Vendor"


class SimulationResponse(BaseModel):
    feasible: bool
    policy_breach: bool
    reserve_breach: bool
    current_category_spend: float
    monthly_limit: Optional[float]
    projected_end_of_month_balance: float
    impacted_goals: List[Dict[str, Any]]
    explanation: str


class CopilotChatRequest(BaseModel):
    query: str


class CopilotChatResponse(BaseModel):
    answer: str
    evidence_citation: Dict[str, Any]
