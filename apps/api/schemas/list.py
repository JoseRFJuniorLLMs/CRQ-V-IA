from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from apps.api.schemas.prospect import ProspectListItem

class SavedListItemCreate(BaseModel):
    establishment_id: int
    priority: Optional[str] = "MEDIA" # ALTA, MEDIA, BAIXA
    notes: Optional[str] = None

class SavedListItemUpdate(BaseModel):
    fiscal_status: Optional[str] = None # PENDENTE, NOTIFICADA, EM_INSPECAO, REGULARIZADA, DISPENSADA
    priority: Optional[str] = None
    notes: Optional[str] = None

class SavedListItemResponse(BaseModel):
    id: int
    list_id: int
    establishment_id: int
    fiscal_status: str
    priority: str
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
