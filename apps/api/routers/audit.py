from typing import Optional
import math
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
    page: int = 1,
    page_size: int = 15,
    action: Optional[str] = None,
    user_email: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Consulta os eventos de auditoria com paginação completa para compliance LGPD."""
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action == action)
    if user_email:
        query = query.filter(AuditLog.user_email.ilike(f"%{user_email}%"))
    if q:
        query = query.filter(
            (AuditLog.target_id.ilike(f"%{q}%")) |
            (AuditLog.user_email.ilike(f"%{q}%")) |
            (AuditLog.ip_address.ilike(f"%{q}%"))
        )

    total = query.count()
    total_pages = max(1, math.ceil(total / page_size))
    logs = query.order_by(desc(AuditLog.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    items = [
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

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

from apps.api.engine.audit_sink import audit_sink

@router.get("/heraclitus/integrity")
def check_heraclitus_integrity(
    current_user: User = Depends(get_current_user)
):
    """Consulta o status e a integridade da árvore de Merkle do HeraclitusDB (SPEC-0022)."""
    return audit_sink.verify_integrity()

