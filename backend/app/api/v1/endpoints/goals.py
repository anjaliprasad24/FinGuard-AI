"""Financial Goals Endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.goal import FinancialGoal
from app.schemas.goal import FinancialGoalCreate, FinancialGoalRead
from app.services.goal_optimizer import GoalOptimizer

router = APIRouter()


@router.get("/", response_model=List[FinancialGoalRead])
def list_goals(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    goals = db.query(FinancialGoal).filter(FinancialGoal.user_id == user_id).all()
    results = []
    for g in goals:
        traj = GoalOptimizer.calculate_goal_trajectory(
            target_amount=g.target_amount,
            current_savings=g.current_savings,
            target_date=g.target_date
        )
        item = FinancialGoalRead.model_validate(g)
        item.required_monthly_savings = traj["required_monthly_savings"]
        item.projected_completion_date = traj["projected_completion_date"]
        item.status = traj["status"]
        results.append(item)
    return results


@router.post("/", response_model=FinancialGoalRead)
def create_goal(
    goal_in: FinancialGoalCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    traj = GoalOptimizer.calculate_goal_trajectory(
        target_amount=goal_in.target_amount,
        current_savings=goal_in.current_savings or 0.0,
        target_date=goal_in.target_date
    )
    
    goal = FinancialGoal(
        user_id=user_id,
        title=goal_in.title,
        target_amount=goal_in.target_amount,
        current_savings=goal_in.current_savings or 0.0,
        target_date=goal_in.target_date,
        priority=goal_in.priority or 1,
        status=traj["status"]
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)

    item = FinancialGoalRead.model_validate(goal)
    item.required_monthly_savings = traj["required_monthly_savings"]
    item.projected_completion_date = traj["projected_completion_date"]
    return item
