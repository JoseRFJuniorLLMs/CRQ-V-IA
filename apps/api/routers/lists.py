from typing import List, Optional
import math
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from apps.api.core.database import get_db
from apps.api.core.deps import get_current_user, record_audit
from apps.api.models.user import User
from apps.api.models.company import Establishment
from apps.api.models.saved_list import SavedList, SavedListItem
from apps.api.schemas.list import SavedListCreate, SavedListResponse, SavedListItemCreate, SavedListItemUpdate, SavedListItemResponse
from apps.api.schemas.prospect import ProspectListItem

router = APIRouter(prefix="/lists", tags=["Listas e Roteiros de Fiscalização"])

@router.get("", response_model=List[SavedListResponse])
def get_lists(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lists = db.query(SavedList).all()
    results = []
    for l in lists:
        results.append(
            SavedListResponse(
                id=l.id,
                name=l.name,
                description=l.description,
                created_by_id=l.created_by_id,
                created_at=l.created_at,
                items_count=len(l.items)
            )
        )
    return results

@router.post("", response_model=SavedListResponse)
def create_list(
    payload: SavedListCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_list = SavedList(
        name=payload.name,
        description=payload.description,
        created_by_id=current_user.id
    )
    db.add(new_list)
    db.commit()
    db.refresh(new_list)

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(
        db=db,
        action="CREATE_SAVED_LIST",
        user=current_user,
        target_type="SAVED_LIST",
        target_id=str(new_list.id),
        details={"name": new_list.name},
        ip_address=client_ip
    )

    return SavedListResponse(
        id=new_list.id,
        name=new_list.name,
        description=new_list.description,
        created_by_id=new_list.created_by_id,
        created_at=new_list.created_at,
        items_count=0
    )

@router.get("/{list_id}/items")
def get_list_items(
    list_id: int,
    page: Optional[int] = None,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    saved_list = db.query(SavedList).filter(SavedList.id == list_id).first()
    if not saved_list:
        raise HTTPException(status_code=404, detail="Lista de fiscalização não encontrada")

    items_query = db.query(SavedListItem).filter(SavedListItem.list_id == list_id).order_by(SavedListItem.id.asc())
    total = items_query.count()

    if page is not None:
        total_pages = max(1, math.ceil(total / page_size))
        db_items = items_query.offset((page - 1) * page_size).limit(page_size).all()
    else:
        total_pages = 1
        db_items = items_query.all()

    results = []
    for item in db_items:
        est = item.establishment
        prospect_dto = None
        if est:
            prospect_dto = {
                "id": est.id,
                "cnpj": est.cnpj,
                "legal_name": est.company.legal_name,
                "trade_name": est.trade_name,
                "branch_type": est.branch_type,
                "registration_status": est.registration_status,
                "primary_cnae": est.primary_cnae,
                "city": est.city,
                "state": est.state,
                "company_size": est.company.company_size,
                "capital_social": est.company.capital_social,
                "chemical_score": est.chemical_score,
                "cfq_tier": est.cfq_tier,
                "cfq_rationale": est.cfq_rationale,
                "crq_status": est.crq_status,
                "opening_date": str(est.opening_date) if est.opening_date else None
            }
        results.append({
            "id": item.id,
            "list_id": item.list_id,
            "establishment_id": item.establishment_id,
            "fiscal_status": item.fiscal_status,
            "priority": item.priority,
            "notes": item.notes,
            "added_at": item.added_at.isoformat() if item.added_at else None,
            "updated_at": item.updated_at.isoformat() if item.updated_at else None,
            "establishment": prospect_dto
        })

    if page is not None:
        return {
            "items": results,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
    return results

@router.post("/{list_id}/items", response_model=SavedListItemResponse)
def add_item_to_list(
    list_id: int,
    payload: SavedListItemCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    saved_list = db.query(SavedList).filter(SavedList.id == list_id).first()
    if not saved_list:
        raise HTTPException(status_code=404, detail="Lista não encontrada")

    est = db.query(Establishment).filter(Establishment.id == payload.establishment_id).first()
    if not est:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    # Verifica se já está na lista
    existing = db.query(SavedListItem).filter(
        SavedListItem.list_id == list_id,
        SavedListItem.establishment_id == payload.establishment_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Esta empresa já consta nesta lista de fiscalização")

    item = SavedListItem(
        list_id=list_id,
        establishment_id=payload.establishment_id,
        priority=payload.priority or "MEDIA",
        notes=payload.notes,
        fiscal_status="PENDENTE"
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(
        db=db,
        action="ADD_COMPANY_TO_LIST",
        user=current_user,
        target_type="SAVED_LIST_ITEM",
        target_id=str(item.id),
        details={"list_id": list_id, "establishment_id": est.id, "cnpj": est.cnpj},
        ip_address=client_ip
    )

    return SavedListItemResponse(
        id=item.id,
        list_id=item.list_id,
        establishment_id=item.establishment_id,
        fiscal_status=item.fiscal_status,
        priority=item.priority,
        notes=item.notes,
        added_at=item.added_at,
        updated_at=item.updated_at,
        establishment=None
    )

@router.patch("/{list_id}/items/{item_id}")
def update_item_status(
    list_id: int,
    item_id: int,
    payload: SavedListItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(SavedListItem).filter(SavedListItem.id == item_id, SavedListItem.list_id == list_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item da lista não encontrado")

    if payload.fiscal_status:
        item.fiscal_status = payload.fiscal_status.upper()
    if payload.priority:
        item.priority = payload.priority.upper()
    if payload.notes is not None:
        item.notes = payload.notes

    db.commit()
    return {"success": True, "item_id": item.id, "fiscal_status": item.fiscal_status}

@router.delete("/{list_id}/items/{item_id}")
def remove_item(
    list_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(SavedListItem).filter(SavedListItem.id == item_id, SavedListItem.list_id == list_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(item)
    db.commit()
    return {"success": True, "removed_item_id": item_id}
