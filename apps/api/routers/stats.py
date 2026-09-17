from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from apps.api.core.database import get_db
from apps.api.core.deps import get_current_user
from apps.api.core.security import get_active_sessions_count
from apps.api.models.user import User
from apps.api.models.company import Establishment, Company
from apps.api.schemas.stats import DashboardStatsResponse, MetricItem

router = APIRouter(prefix="/stats", tags=["Métricas e Painel"])

@router.get("/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Establishment).count()
    high = db.query(Establishment).filter(Establishment.cfq_tier == "HIGH").count()
    med = db.query(Establishment).filter(Establishment.cfq_tier == "MEDIUM").count()
    low = db.query(Establishment).filter(Establishment.cfq_tier == "LOW").count()
    active_comp = db.query(Establishment).filter(Establishment.registration_status == "ATIVA").count()

    # Top cidades no RS
    city_counts = (
        db.query(Establishment.city, func.count(Establishment.id).label("cnt"))
        .group_by(Establishment.city)
        .order_by(func.count(Establishment.id).desc())
        .limit(8)
        .all()
    )
    by_city = [MetricItem(label=c[0], count=c[1]) for c in city_counts]

    # Top CNAEs
    cnae_counts = (
        db.query(Establishment.primary_cnae, func.count(Establishment.id).label("cnt"))
        .group_by(Establishment.primary_cnae)
        .order_by(func.count(Establishment.id).desc())
        .limit(6)
        .all()
    )
    by_cnae = [MetricItem(label=c[0], count=c[1]) for c in cnae_counts]

    # Por Porte
    size_counts = (
        db.query(Company.company_size, func.count(Establishment.id).label("cnt"))
        .join(Establishment, Establishment.company_id == Company.id)
        .group_by(Company.company_size)
        .all()
    )
    by_size = [MetricItem(label=c[0] or "DEMAIS", count=c[1]) for c in size_counts]

    # Por Status CRQ-V
    crq_counts = (
        db.query(Establishment.crq_status, func.count(Establishment.id).label("cnt"))
        .group_by(Establishment.crq_status)
        .all()
    )
    by_crq = [MetricItem(label=c[0] or "NAO_CADASTRADA", count=c[1]) for c in crq_counts]

    return DashboardStatsResponse(
        total_establishments_rs=total,
        total_high_priority=high,
        total_medium_priority=med,
        total_low_priority=low,
        active_companies=active_comp,
        by_city=by_city,
        by_cnae=by_cnae,
        by_size=by_size,
        by_crq_status=by_crq,
        active_concurrent_sessions=get_active_sessions_count()
    )
