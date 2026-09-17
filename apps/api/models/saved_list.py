from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from apps.api.core.database import Base

class SavedList(Base):
    __tablename__ = "saved_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    items = relationship("SavedListItem", back_populates="saved_list", cascade="all, delete-orphan")

class SavedListItem(Base):
    __tablename__ = "saved_list_items"

    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("saved_lists.id"), nullable=False)
    establishment_id = Column(Integer, ForeignKey("establishments.id"), nullable=False)
    
    # Status na fila de fiscalização
    fiscal_status = Column(String(50), default="PENDENTE", index=True) # PENDENTE, NOTIFICADA, EM_INSPECAO, REGULARIZADA, DISPENSADA
    priority = Column(String(20), default="MEDIA") # ALTA, MEDIA, BAIXA
    notes = Column(Text, nullable=True)
    
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    saved_list = relationship("SavedList", back_populates="items")
    establishment = relationship("Establishment")
