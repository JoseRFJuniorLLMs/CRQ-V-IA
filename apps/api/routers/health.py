from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timezone
from apps.api.core.database import get_db

router = APIRouter(tags=["Health & SLA"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint para monitoramento de SLA e disponibilidade (TR item 4.12 / SPEC-0009)."""
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy" if db_status == "ok" else "degraded",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
        "service": "CRQ-V-IA Engine"
    }
