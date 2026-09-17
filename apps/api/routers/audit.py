from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from apps.api.core.database import get_db
from apps.api.core.deps import get_current_user
from apps.api.models.user import User
from apps.api.models.audit_log import AuditLog

router = APIRouter(prefix="/audit", tags=["Auditoria e Governança LGPD"])

@router.get("")
def list_audit_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Consulta os últimos eventos de auditoria para fins de compliance LGPD."""
    logs = db.query(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit).all()
    return [
        {
            "id": l.id,
            "user_email": l.user_email,
            "action": l.action,
            "target_type": l.target_type,
            "target_id": l.target_id,
            "details": l.details,
            "ip_address": l.ip_address,
            "created_at": l.created_at.isoformat()
        }
        for l in logs
    ]
