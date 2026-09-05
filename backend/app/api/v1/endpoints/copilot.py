"""Copilot & What-If Simulator Endpoints."""

from datetime import date
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_id, hash_password
from app.models.user import User
from app.models.policy import BudgetPolicy
from app.models.goal import FinancialGoal
from app.models.transaction import Transaction
from app.schemas.copilot import SimulationRequest, SimulationResponse, CopilotChatRequest, CopilotChatResponse
from app.services.policy_controller import PolicyController
from app.services.goal_optimizer import GoalOptimizer
from app.services.copilot_rag import CopilotRAG
from app.services.audit_logger import AuditLogger

router = APIRouter()


def _ensure_user(db: Session, user_id: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(
            id=user_id,
            email=f"{user_id}@aifinancecontroller.io",
            hashed_password=hash_password("demo1234"),
            risk_tolerance="MODERATE",
            min_reserve_threshold=10000.00
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@router.post("/simulate", response_model=SimulationResponse)
def simulate_purchase(
    req: SimulationRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = _ensure_user(db, user_id)
    min_reserve = user.min_reserve_threshold or 10000.00

    policy = db.query(BudgetPolicy).filter(
        BudgetPolicy.user_id == user_id,
        BudgetPolicy.category == req.category
    ).first()
    monthly_limit = policy.monthly_limit if policy else None
    hard_cap = policy.hard_cap if policy else False

    txns = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.category == req.category,
        Transaction.transaction_type == "EXPENSE"
    ).all()
    current_spend = sum(t.amount for t in txns)

    all_expenses = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == "EXPENSE"
    ).all()
    total_spent = sum(t.amount for t in all_expenses)
    current_balance = 50000.0 - total_spent

    breached, warning, evidence = PolicyController.evaluate_transaction(
        category=req.category,
        amount=req.amount,
        current_category_spend=current_spend,
        monthly_limit=monthly_limit,
        hard_cap=hard_cap,
        current_user_balance=current_balance,
        min_reserve_threshold=min_reserve,
        projected_monthly_spend=total_spent * 1.1
    )

    goals = db.query(FinancialGoal).filter(FinancialGoal.user_id == user_id).all()
    impacted_goals = []
    deficit = max(0.0, (current_spend + req.amount) - (monthly_limit or 999999))
    
    for g in goals:
        traj = GoalOptimizer.calculate_goal_trajectory(
            target_amount=g.target_amount,
            current_savings=g.current_savings,
            target_date=g.target_date,
            monthly_deficit=deficit
        )
        if traj["status"] != "ON_TRACK":
            impacted_goals.append({
                "title": g.title,
                "status": traj["status"],
                "months_delayed": traj["months_delayed"],
                "projected_completion_date": traj["projected_completion_date"].isoformat()
            })

    feasible = not breached and not evidence["reserve_breach"]
    explanation = warning or (
        f"Purchase of ₹{req.amount:,.2f} in '{req.category}' is feasible. Projected month-end balance will be ₹{evidence['projected_eom_balance']:,.2f}."
    )

    AuditLogger.log_event(
        db=db,
        user_id=user_id,
        event_type="SIMULATION",
        evidence_payload={
            "simulation": req.model_dump(),
            "evidence": evidence,
            "impacted_goals": impacted_goals,
            "feasible": feasible
        },
        ai_explanation=explanation
    )

    return SimulationResponse(
        feasible=feasible,
        policy_breach=breached,
        reserve_breach=evidence["reserve_breach"],
        current_category_spend=current_spend,
        monthly_limit=monthly_limit,
        projected_end_of_month_balance=evidence["projected_eom_balance"],
        impacted_goals=impacted_goals,
        explanation=explanation
    )


@router.post("/chat", response_model=CopilotChatResponse)
async def copilot_chat(
    req: CopilotChatRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    _ensure_user(db, user_id)
    recent_txns = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(Transaction.transaction_date.desc()).limit(10).all()

    flagged_txns = [t for t in recent_txns if t.risk_level in ["HIGH", "CRITICAL"]]
    latest_flagged = flagged_txns[0] if flagged_txns else (recent_txns[0] if recent_txns else None)

    context = {
        "user_id": user_id,
        "amount": latest_flagged.amount if latest_flagged else 18499.0,
        "historical_mean": 4200.0,
        "std_dev": 1100.0,
        "z_score": 12.99,
        "anomaly_score": 0.87,
        "flagged": True if latest_flagged else False,
        "current_balance": 45000.0,
        "merchant": latest_flagged.clean_merchant if latest_flagged else "Sample Merchant",
        "recent_count": len(recent_txns)
    }

    result = await CopilotRAG.generate_explanation(req.query, context)

    AuditLogger.log_event(
        db=db,
        user_id=user_id,
        event_type="COPILOT_QUERY",
        evidence_payload={"query": req.query, "context": context},
        ai_explanation=result["answer"]
    )

    return CopilotChatResponse(
        answer=result["answer"],
        evidence_citation=result["evidence_citation"]
    )
