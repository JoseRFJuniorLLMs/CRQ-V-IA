from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, cast, String
from apps.api.core.database import get_db
from apps.api.core.deps import get_current_user, record_audit
from apps.api.models.user import User
from apps.api.models.company import Establishment, Company
from apps.api.models.cnae import CNAE
from apps.api.schemas.prospect import PaginatedProspects, ProspectListItem, ProspectDetail
from apps.api.engine.cnpj_adapter import fetch_live_cnpj_data

router = APIRouter(prefix="/prospects", tags=["Prospecção e Empresas"])

@router.get("", response_model=PaginatedProspects)
def search_prospects(
    request: Request,
    q: Optional[str] = Query(None, description="Busca textual por Razão Social, Nome Fantasia ou CNPJ"),
    cnae: Optional[str] = Query(None, description="Código ou prefixo do CNAE (busca em primário e secundários)"),
    division: Optional[str] = Query(None, description="Divisão CNAE (2 dígitos, ex: 20 para Químicos)"),
    city: Optional[str] = Query(None, description="Município do Rio Grande do Sul"),
    district: Optional[str] = Query(None, description="Bairro"),
    postal_code: Optional[str] = Query(None, description="CEP"),
    branch_type: Optional[str] = Query(None, description="Tipo de Estabelecimento (MATRIZ / FILIAL)"),
    status: Optional[str] = Query(None, description="Situação Cadastral (ATIVA, BAIXADA, etc.)"),
    size: Optional[str] = Query(None, description="Porte Empresarial (ME, EPP, DEMAIS)"),
    tier: Optional[str] = Query(None, description="Prioridade CFQ (HIGH, MEDIUM, LOW)"),
    crq_status: Optional[str] = Query(None, description="Status interno CRQ-V"),
    min_score: Optional[float] = Query(None, description="Score mínimo (0 a 100)"),
    min_capital: Optional[float] = Query(None, description="Capital social mínimo"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Establishment).join(Company)

    # Filtros
    if q:
        clean_q = q.strip()
        digits_only = "".join(c for c in clean_q if c.isdigit())
        if len(digits_only) >= 4:
            query = query.filter(Establishment.cnpj.ilike(f"%{digits_only}%"))
        else:
            query = query.filter(
                or_(
                    Company.legal_name.ilike(f"%{clean_q}%"),
                    Establishment.trade_name.ilike(f"%{clean_q}%")
                )
            )

    # Busca em CNAE primário E secundários (SPEC-0021)
    if cnae:
        clean_cnae = cnae.replace(".", "").replace("/", "").replace("-", "").strip()
        query = query.filter(
            or_(
                Establishment.primary_cnae.ilike(f"%{clean_cnae}%"),
                cast(Establishment.secondary_cnaes, String).ilike(f"%{clean_cnae}%")
            )
        )

    # Divisão CNAE (hierarquia 2 dígitos)
    if division:
        clean_div = "".join(c for c in division if c.isdigit())
        if clean_div:
            query = query.filter(
                or_(
                    Establishment.primary_cnae.startswith(clean_div),
                    cast(Establishment.secondary_cnaes, String).ilike(f'%"{clean_div}%')
                )
            )

    if city:
        query = query.filter(Establishment.city.ilike(f"%{city.strip()}%"))

    if district:
        query = query.filter(Establishment.district.ilike(f"%{district.strip()}%"))

    if postal_code:
        clean_cep = "".join(c for c in postal_code if c.isdigit())
        query = query.filter(Establishment.postal_code.ilike(f"%{clean_cep}%"))

    if branch_type:
        query = query.filter(Establishment.branch_type == branch_type.upper().strip())

    if status:
        query = query.filter(Establishment.registration_status == status.upper())

    if size:
        query = query.filter(Company.company_size == size.upper())

    if tier:
        query = query.filter(Establishment.cfq_tier == tier.upper())

    if crq_status:
        query = query.filter(Establishment.crq_status == crq_status.upper())

    if min_score is not None:
        query = query.filter(Establishment.chemical_score >= min_score)

    if min_capital is not None:
        query = query.filter(Company.capital_social >= min_capital)

    # Ordenação: prioriza maior score de química, depois data de abertura mais recente
    query = query.order_by(desc(Establishment.chemical_score), desc(Establishment.id))

    total = query.count()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    offset = (page - 1) * page_size
    items_db = query.offset(offset).limit(page_size).all()

    # CNAE descriptions cache
    cnaes_db = {c.code: c.description for c in db.query(CNAE).all()}

    prospects = []
    for est in items_db:
        prospects.append(
            ProspectListItem(
                id=est.id,
                cnpj=est.cnpj,
                legal_name=est.company.legal_name,
                trade_name=est.trade_name,
                branch_type=est.branch_type,
                registration_status=est.registration_status,
                primary_cnae=est.primary_cnae,
                primary_cnae_desc=cnaes_db.get(est.primary_cnae),
                city=est.city,
                state=est.state,
                company_size=est.company.company_size,
                capital_social=est.company.capital_social,
                chemical_score=est.chemical_score,
                cfq_tier=est.cfq_tier,
                cfq_rationale=est.cfq_rationale,
                crq_status=est.crq_status,
                opening_date=est.opening_date,
                district=est.district,
                postal_code=est.postal_code
            )
        )

    # Registro de auditoria
    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(
        db=db,
        action="SEARCH_PROSPECTS",
        user=current_user,
        target_type="ESTABLISHMENT",
        details={
            "q": q, "cnae": cnae, "division": division, "city": city,
            "tier": tier, "page": page, "results": len(prospects)
        },
        ip_address=client_ip
    )

    return PaginatedProspects(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=prospects
    )

@router.get("/{cnpj}", response_model=ProspectDetail)
def get_prospect_detail(
    cnpj: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    clean_cnpj = "".join(c for c in cnpj if c.isdigit())
    est = db.query(Establishment).join(Company).filter(Establishment.cnpj == clean_cnpj).first()
    if not est:
        raise HTTPException(status_code=404, detail="Empresa não encontrada na base do RS")

    cnae_obj = db.query(CNAE).filter(CNAE.code == est.primary_cnae).first()
    primary_cnae_desc = cnae_obj.description if cnae_obj else None

    # Auditoria de visualização da ficha
    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(
        db=db,
        action="VIEW_PROSPECT_CARD",
        user=current_user,
        target_type="ESTABLISHMENT",
        target_id=clean_cnpj,
        details={"legal_name": est.company.legal_name, "cnpj": clean_cnpj},
        ip_address=client_ip
    )

    return ProspectDetail(
        id=est.id,
        cnpj=est.cnpj,
        legal_name=est.company.legal_name,
        trade_name=est.trade_name,
        branch_type=est.branch_type,
        registration_status=est.registration_status,
        status_date=est.status_date,
        opening_date=est.opening_date,
        company_size=est.company.company_size,
        capital_social=est.company.capital_social,
        primary_cnae=est.primary_cnae,
        primary_cnae_desc=primary_cnae_desc,
        secondary_cnaes=est.secondary_cnaes or [],
        street=est.street,
        number=est.number,
        complement=est.complement,
        district=est.district,
        postal_code=est.postal_code,
        city=est.city,
        state=est.state,
        phone=est.phone,
        email=est.email,
        chemical_score=est.chemical_score,
        cfq_tier=est.cfq_tier,
        cfq_rationale=est.cfq_rationale,
        cfq_norm_reference=est.cfq_norm_reference,
        regulatory_status=est.regulatory_status or "MANDATORY_REGISTRATION",
        crq_status=est.crq_status,
        crq_notes=est.crq_notes,
        last_inspected_at=est.last_inspected_at,
        technical_manager=est.technical_manager,
        technical_manager_crq=est.technical_manager_crq,
        aft_number=est.aft_number,
        aft_valid_until=est.aft_valid_until,
        state_registration=est.state_registration,
        updated_at=est.updated_at
    )

@router.get("/{cnpj}/live-check")
async def check_cnpj_live(
    cnpj: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Consulta em tempo real a situação cadastral oficial na RFB."""
    clean_cnpj = "".join(c for c in cnpj if c.isdigit())
    live_result = await fetch_live_cnpj_data(clean_cnpj)

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(
        db=db,
        action="LIVE_RFB_CNPJ_CHECK",
        user=current_user,
        target_type="ESTABLISHMENT",
        target_id=clean_cnpj,
        details={"source": live_result.get("source"), "status": live_result.get("registration_status")},
        ip_address=client_ip
    )

    return live_result

@router.patch("/{cnpj}/crq-status")
def update_crq_internal_status(
    cnpj: str,
    status_update: dict,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza o estado de fiscalização interno da empresa no CRQ-V."""
    clean_cnpj = "".join(c for c in cnpj if c.isdigit())
    est = db.query(Establishment).filter(Establishment.cnpj == clean_cnpj).first()
    if not est:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    if "crq_status" in status_update:
        est.crq_status = status_update["crq_status"].upper()
    if "crq_notes" in status_update:
        est.crq_notes = status_update["crq_notes"]
    
    db.commit()

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(
        db=db,
        action="UPDATE_CRQ_STATUS",
        user=current_user,
        target_type="ESTABLISHMENT",
        target_id=clean_cnpj,
        details=status_update,
        ip_address=client_ip
    )

    return {"success": True, "cnpj": clean_cnpj, "crq_status": est.crq_status}
