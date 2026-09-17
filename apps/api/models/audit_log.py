from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from apps.api.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    user_email = Column(String(255), nullable=True)
    action = Column(String(100), nullable=False, index=True) # "SEARCH", "VIEW_COMPANY", "EXPORT_CSV", "EXPORT_XLSX", "ADD_TO_LIST", "LOGIN"
    target_type = Column(String(50), nullable=True) # "ESTABLISHMENT", "SAVED_LIST", "SYSTEM"
    target_id = Column(String(100), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
