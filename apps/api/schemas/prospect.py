from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProspectListItem(BaseModel):
    id: int
    cnpj: str
    legal_name: str
    trade_name: Optional[str] = None
    branch_type: str
    registration_status: str
    primary_cnae: str
    primary_cnae_desc: Optional[str] = None
    city: str
    state: str = "RS"
    company_size: str
    capital_social: float
    chemical_score: float
    cfq_tier: str
    cfq_rationale: Optional[str] = None
    crq_status: str
    opening_date: Optional[str] = None

    class Config:
        from_attributes = True

class PaginatedProspects(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[ProspectListItem]

class ProspectDetail(BaseModel):
    id: int
    cnpj: str
    legal_name: str
    trade_name: Optional[str] = None
    branch_type: str
    registration_status: str
    status_date: Optional[str] = None
    opening_date: Optional[str] = None
    
    company_size: str
    capital_social: float
    
    primary_cnae: str
    primary_cnae_desc: Optional[str] = None
    secondary_cnaes: List[str] = []
    
    # Endereço completo
    street: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    district: Optional[str] = None
    postal_code: Optional[str] = None
    city: str
    state: str
    phone: Optional[str] = None
    email: Optional[str] = None
    
    # Motor Regulatório
    chemical_score: float
    cfq_tier: str
    cfq_rationale: Optional[str] = None
    cfq_norm_reference: str
    
    # CRQ-V Interno
    crq_status: str
    crq_notes: Optional[str] = None
    last_inspected_at: Optional[datetime] = None
    updated_at: datetime

    class Config:
        from_attributes = True
