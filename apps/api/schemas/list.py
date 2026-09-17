from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from apps.api.schemas.prospect import ProspectListItem

class SavedListItemCreate(BaseModel):
    establishment_id: int
    priority: Optional[str] = "MEDIA" # ALTA, MEDIA, BAIXA
    assigned_inspector: Optional[str] = None
    notes: Optional[str] = None

class SavedListItemUpdate(BaseModel):
    fiscal_status: Optional[str] = None # PENDENTE, EM_ANALISE, NOTIFICADA, AUTUADA, CONCLUIDA, DISPENSADA, NEW, REVIEWING, SELECTED, DISMISSED, EXPORTED, INSPECTED
    priority: Optional[str] = None # ALTA, MEDIA, BAIXA
    assigned_inspector: Optional[str] = None
    notes: Optional[str] = None

class SavedListItemResponse(BaseModel):
    id: int
    list_id: int
    establishment_id: int
    fiscal_status: str
    priority: str
    assigned_inspector: Optional[str] = None
    notes: Optional[str] = None
    added_at: datetime
    updated_at: datetime
    establishment: Optional[ProspectListItem] = None

    class Config:
        from_attributes = True

class SavedListCreate(BaseModel):
    name: str
    description: Optional[str] = None

class SavedListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_by_id: int
    created_at: datetime
    items_count: int = 0

    class Config:
        from_attributes = True

class PaginatedSavedListItemsResponse(BaseModel):
    items: List[SavedListItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
