from pydantic import BaseModel
from typing import List, Dict

class MetricItem(BaseModel):
    label: str
    count: int

class DashboardStatsResponse(BaseModel):
    total_establishments_rs: int
    total_high_priority: int
    total_medium_priority: int
    total_low_priority: int
    active_companies: int
    by_city: List[MetricItem]
    by_cnae: List[MetricItem]
    by_size: List[MetricItem]
    by_crq_status: List[MetricItem]
    active_concurrent_sessions: int
