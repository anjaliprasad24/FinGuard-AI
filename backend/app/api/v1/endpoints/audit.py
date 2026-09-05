"""System Audit Log Endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.audit import SystemAuditLog
from app.schemas.audit import AuditLogRead

router = APIRouter()


@router.get("/logs", response_model=List[AuditLogRead])
def get_audit_logs(
    limit: int = 50,
    event_type: Optional[str] = Query(None),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    query = db.query(SystemAuditLog).filter(SystemAuditLog.user_id == user_id)
    if event_type:
        query = query.filter(SystemAuditLog.event_type == event_type)
    return query.order_by(SystemAuditLog.created_at.desc()).limit(limit).all()
