"""Financial Goal Trajectory Optimizer."""

from datetime import date, timedelta
import math
from typing import Dict, Any, List, Tuple


class GoalOptimizer:
    """Recalculates financial goal completion timelines and status trajectory."""

    @classmethod
    def calculate_goal_trajectory(
        cls,
        target_amount: float,
        current_savings: float,
        target_date: date,
        monthly_savings_capacity: float = 0.0,
        monthly_deficit: float = 0.0
    ) -> Dict[str, Any]:
        today = date.today()
        remaining_days = max(1, (target_date - today).days)
        remaining_months = max(0.1, remaining_days / 30.4375)

        remaining_amount = max(0.0, target_amount - current_savings)
        required_monthly_savings = round(remaining_amount / remaining_months, 2)

        status = "ON_TRACK"
        months_delayed = 0.0
        projected_completion_date = target_date

        if remaining_amount <= 0:
            status = "COMPLETED"
            required_monthly_savings = 0.0
        elif monthly_deficit > 0 and required_monthly_savings > 0:
            # Deficit delays goal completion
            months_delayed = round(monthly_deficit / required_monthly_savings, 1)
            additional_days = int(math.ceil(months_delayed * 30.4375))
            projected_completion_date = target_date + timedelta(days=additional_days)
            status = "DELAYED" if months_delayed >= 1.0 else "AT_RISK"
        elif monthly_savings_capacity > 0 and monthly_savings_capacity < required_monthly_savings:
            status = "AT_RISK"
            months_needed = remaining_amount / monthly_savings_capacity
            additional_months = max(0.0, months_needed - remaining_months)
            additional_days = int(math.ceil(additional_months * 30.4375))
            projected_completion_date = target_date + timedelta(days=additional_days)

        return {
            "required_monthly_savings": required_monthly_savings,
            "remaining_amount": round(remaining_amount, 2),
            "remaining_months": round(remaining_months, 1),
            "status": status,
            "months_delayed": months_delayed,
            "projected_completion_date": projected_completion_date
        }
