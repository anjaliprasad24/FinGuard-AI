"""Budget Policy & Runway Controller."""

from typing import Dict, Any, Optional, Tuple, List


class PolicyController:
    """Evaluates budget limits, category caps, and min reserve floor threshold."""

    @classmethod
    def evaluate_transaction(
        cls,
        category: str,
        amount: float,
        current_category_spend: float,
        monthly_limit: Optional[float],
        hard_cap: bool,
        current_user_balance: float,
        min_reserve_threshold: float,
        projected_monthly_spend: float
    ) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        """
        Returns:
            breached (bool)
            warning_message (Optional[str])
            evidence (Dict[str, Any])
        """
        breached = False
        warning = None

        new_category_spend = current_category_spend + amount
        limit_exceeded = False
        pct_used = 0.0

        if monthly_limit and monthly_limit > 0:
            pct_used = round((new_category_spend / monthly_limit) * 100.0, 1)
            if new_category_spend > monthly_limit:
                limit_exceeded = True
                if hard_cap:
                    breached = True
                    warning = f"Hard cap breach! Spending ₹{new_category_spend:,.2f} exceeds strict monthly limit of ₹{monthly_limit:,.2f} for '{category}'."
                else:
                    warning = f"Budget limit exceeded! Spend ₹{new_category_spend:,.2f} is {pct_used}% of ₹{monthly_limit:,.2f} limit."
            elif pct_used >= 85.0:
                warning = f"Category '{category}' is at {pct_used}% of its monthly budget (₹{new_category_spend:,.2f} / ₹{monthly_limit:,.2f})."

        # Projected end-of-month balance
        projected_eom_balance = current_user_balance - projected_monthly_spend - amount
        reserve_breach = projected_eom_balance < min_reserve_threshold

        if reserve_breach:
            warning = (warning or "") + f" Reserve Floor Alert: Projected balance (₹{projected_eom_balance:,.2f}) falls below safety threshold (₹{min_reserve_threshold:,.2f})."

        evidence = {
            "category": category,
            "incoming_amount": amount,
            "previous_spend": current_category_spend,
            "new_spend": new_category_spend,
            "monthly_limit": monthly_limit,
            "hard_cap": hard_cap,
            "limit_exceeded": limit_exceeded,
            "pct_limit_used": pct_used,
            "current_user_balance": current_user_balance,
            "projected_eom_balance": projected_eom_balance,
            "min_reserve_threshold": min_reserve_threshold,
            "reserve_breach": reserve_breach,
            "policy_breached": breached
        }

        return breached, warning, evidence
