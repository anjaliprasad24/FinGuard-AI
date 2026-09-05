"""Budget Policies Endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.policy import BudgetPolicy
from app.models.transaction import Transaction
from app.schemas.policy import BudgetPolicyCreate, BudgetPolicyRead

router = APIRouter()


@router.get("/", response_model=List[BudgetPolicyRead])
def list_policies(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    policies = db.query(BudgetPolicy).filter(BudgetPolicy.user_id == user_id).all()
    results = []
    for p in policies:
        # Calculate current monthly spend
        txns = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.category == p.category,
            Transaction.transaction_type == "EXPENSE"
        ).all()
        spend = sum(t.amount for t in txns)
        
        status = "NORMAL"
        if spend > p.monthly_limit:
            status = "BREACHED"
        elif spend >= 0.85 * p.monthly_limit:
            status = "WARNING"

        item = BudgetPolicyRead.model_validate(p)
        item.current_spend = round(spend, 2)
        item.status = status
        results.append(item)

    return results


@router.post("/", response_model=BudgetPolicyRead)
def create_or_update_policy(
    policy_in: BudgetPolicyCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    existing = db.query(BudgetPolicy).filter(
        BudgetPolicy.user_id == user_id,
        BudgetPolicy.category == policy_in.category
    ).first()

    if existing:
        existing.monthly_limit = policy_in.monthly_limit
        existing.hard_cap = policy_in.hard_cap or False
        db.commit()
        db.refresh(existing)
        pol = existing
    else:
        pol = BudgetPolicy(
            user_id=user_id,
            category=policy_in.category,
            monthly_limit=policy_in.monthly_limit,
            hard_cap=policy_in.hard_cap or False
        )
        db.add(pol)
        db.commit()
        db.refresh(pol)

    item = BudgetPolicyRead.model_validate(pol)
    item.current_spend = 0.0
    item.status = "NORMAL"
    return item
