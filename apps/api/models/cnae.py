from sqlalchemy import Column, String, Boolean, Integer, Text
from apps.api.core.database import Base

class CNAE(Base):
    __tablename__ = "cnaes"

    code = Column(String(20), primary_key=True, index=True) # ex: "2029-1/00"
    description = Column(String(500), nullable=False)
    division = Column(String(10), index=True) # ex: "20"
    group_code = Column(String(10)) # ex: "20.2"
    class_code = Column(String(10)) # ex: "20.29-1"
    subclass_code = Column(String(20))
    is_chemistry_related = Column(Boolean, default=False, index=True)
    cfq_tier = Column(String(20), nullable=True, index=True) # "HIGH", "MEDIUM", "LOW"
    cfq_scope = Column(String(50), nullable=True) # "basic", "service", "support"
    rationale = Column(Text, nullable=True)
