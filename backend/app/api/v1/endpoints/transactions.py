"""Transactions Ingest & Management Endpoints."""

from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_id, hash_password
from app.models.user import User
from app.models.transaction import Transaction
from app.models.policy import BudgetPolicy
from app.schemas.transaction import TransactionIngestRequest, TransactionRead, TransactionIngestResponse
from app.services.pii_scrubber import PIIScrubber
from app.services.classifier import MerchantClassifier
from app.services.anomaly_detector import AnomalyDetector
from app.services.policy_controller import PolicyController
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


@router.post("/ingest", response_model=TransactionIngestResponse)
def ingest_transaction(
    req: TransactionIngestRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = _ensure_user(db, user_id)

    # Step 1: PII Scrubber
    scrubbed_merchant = PIIScrubber.scrub(req.raw_merchant)

    # Step 2: Category & Entity Classification
    if req.category:
        clean_merchant = scrubbed_merchant
        category = req.category
        confidence = 1.0
    else:
        clean_merchant, category, confidence = MerchantClassifier.classify(scrubbed_merchant)

    min_reserve = user.min_reserve_threshold or 10000.00

    past_txns = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.category == category
    ).all()
    history_amounts = [t.amount for t in past_txns]

    # Step 3: Anomaly Engine
    is_anomaly, risk_level, anomaly_score, evidence_payload = AnomalyDetector.evaluate(
        req.amount, history_amounts
    )

    # Step 4: Policy & Runway Check
    current_category_spend = sum(t.amount for t in past_txns if t.transaction_type == "EXPENSE")
    policy = db.query(BudgetPolicy).filter(
        BudgetPolicy.user_id == user_id,
        BudgetPolicy.category == category
    ).first()

    monthly_limit = policy.monthly_limit if policy else None
    hard_cap = policy.hard_cap if policy else False

    all_expenses = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == "EXPENSE"
    ).all()
    total_spent = sum(t.amount for t in all_expenses)
    current_balance = 50000.0 - total_spent

    policy_breached, policy_warning, policy_evidence = PolicyController.evaluate_transaction(
        category=category,
        amount=req.amount,
        current_category_spend=current_category_spend,
        monthly_limit=monthly_limit,
        hard_cap=hard_cap,
        current_user_balance=current_balance,
        min_reserve_threshold=min_reserve,
        projected_monthly_spend=total_spent * 1.1
    )

    full_evidence = {
        **evidence_payload,
        "policy": policy_evidence,
        "clean_merchant": clean_merchant,
        "category": category,
        "confidence_score": confidence
    }

    # Step 5: Save Transaction to DB
    txn = Transaction(
        user_id=user_id,
        raw_merchant=req.raw_merchant,
        clean_merchant=clean_merchant,
        amount=req.amount,
        currency=req.currency or "INR",
        category=category,
        transaction_type=req.transaction_type or "EXPENSE",
        confidence_score=confidence,
        is_recurring=False,
        anomaly_score=anomaly_score,
        risk_level=risk_level,
        source=req.source or "API",
        transaction_date=req.transaction_date or date.today()
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)

    # Step 6: Log Audit Trail
    if is_anomaly or policy_breached or policy_warning:
        event_type = "ANOMALY_FLAGGED" if is_anomaly else "POLICY_BREACH"
        AuditLogger.log_event(
            db=db,
            user_id=user_id,
            event_type=event_type,
            evidence_payload=full_evidence,
            reference_id=txn.id,
            ai_explanation=policy_warning or f"Transaction of ₹{req.amount} flagged with risk level {risk_level}."
        )

    txn_read = TransactionRead.model_validate(txn)
    txn_read.evidence_payload = full_evidence

    return TransactionIngestResponse(
        transaction=txn_read,
        is_anomaly=is_anomaly,
        policy_breach=policy_breached,
        policy_warning=policy_warning,
        evidence_payload=full_evidence
    )


@router.get("/", response_model=List[TransactionRead])
def list_transactions(
    limit: int = 50,
    category: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if category:
        query = query.filter(Transaction.category == category)
    return query.order_by(Transaction.transaction_date.desc()).limit(limit).all()


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    txn = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == user_id
    ).first()

    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    db.delete(txn)
    db.commit()
    return {"message": "Transaction deleted successfully", "id": transaction_id}
