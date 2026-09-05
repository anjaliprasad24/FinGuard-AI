"""Unit tests for Goal Optimizer."""

from datetime import date, timedelta
from app.services.goal_optimizer import GoalOptimizer


def test_goal_optimizer_on_track():
    target_date = date.today() + timedelta(days=300)
    traj = GoalOptimizer.calculate_goal_trajectory(
        target_amount=100000.0,
        current_savings=45000.0,
        target_date=target_date
    )
    assert traj["status"] == "ON_TRACK"
    assert traj["required_monthly_savings"] > 0


def test_goal_optimizer_delayed_on_deficit():
    target_date = date.today() + timedelta(days=300)
    traj = GoalOptimizer.calculate_goal_trajectory(
        target_amount=100000.0,
        current_savings=45000.0,
        target_date=target_date,
        monthly_deficit=15000.0
    )
    assert traj["status"] in ["DELAYED", "AT_RISK"]
    assert traj["months_delayed"] > 0
