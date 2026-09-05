"""Unit tests for Policy Controller."""

from app.services.policy_controller import PolicyController


def test_policy_controller_within_limit():
    breached, warning, evidence = PolicyController.evaluate_transaction(
        category="Electronics",
        amount=2000.0,
        current_category_spend=5000.0,
        monthly_limit=15000.0,
        hard_cap=True,
        current_user_balance=45000.0,
        min_reserve_threshold=10000.0,
        projected_monthly_spend=15000.0
    )
    assert not breached
    assert not evidence["limit_exceeded"]
    assert not evidence["reserve_breach"]


def test_policy_controller_hard_cap_breach():
    breached, warning, evidence = PolicyController.evaluate_transaction(
        category="Electronics",
        amount=18499.0,
        current_category_spend=5000.0,
        monthly_limit=15000.0,
        hard_cap=True,
        current_user_balance=45000.0,
        min_reserve_threshold=10000.0,
        projected_monthly_spend=15000.0
    )
    assert breached
    assert evidence["limit_exceeded"]
    assert warning is not None
