from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from apps.api.core.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    cnpj_base = Column(String(8), unique=True, index=True, nullable=False)
    legal_name = Column(String(255), index=True, nullable=False)
    company_size = Column(String(50), default="DEMAIS") # "ME", "EPP", "DEMAIS"
    capital_social = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    establishments = relationship("Establishment", back_populates="company")

class Establishment(Base):
    __tablename__ = "establishments"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    cnpj = Column(String(14), unique=True, index=True, nullable=False) # 14 dígitos sem pontuação
    branch_type = Column(String(20), default="MATRIZ") # "MATRIZ", "FILIAL"
    trade_name = Column(String(255), index=True, nullable=True) # Nome Fantasia
    registration_status = Column(String(50), default="ATIVA", index=True) # ATIVA, BAIXADA, INAPTA, SUSPENSA
    status_date = Column(String(10), nullable=True) # YYYY-MM-DD
    opening_date = Column(String(10), nullable=True) # YYYY-MM-DD
    
    primary_cnae = Column(String(20), index=True, nullable=False)
    secondary_cnaes = Column(JSON, default=list) # Lista de strings com códigos CNAE
    
    # Endereço (RS)
    street = Column(String(255), nullable=True)
    number = Column(String(50), nullable=True)
    complement = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    postal_code = Column(String(10), nullable=True) # CEP
    city = Column(String(100), index=True, nullable=False) # Município RS
    state = Column(String(2), default="RS", index=True, nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    
    # Classificação Química e Score Regulatório
    chemical_score = Column(Float, default=0.0, index=True) # 0.0 a 100.0
    cfq_tier = Column(String(20), default="LOW", index=True) # HIGH, MEDIUM, LOW, NONE
    cfq_rationale = Column(Text, nullable=True) # Justificativa explicável
    cfq_norm_reference = Column(String(100), default="Resolução CFQ nº 339/2025")
    
    # Estado Operacional Interno do CRQ-V
    crq_status = Column(String(50), default="NAO_CADASTRADA", index=True) # REGISTRADA, NAO_CADASTRADA, DISPENSADA, EM_FISCALIZACAO, AUTUADA
    crq_notes = Column(Text, nullable=True)
    last_inspected_at = Column(DateTime, nullable=True)
    
    # Responsabilidade Técnica e AFT (Art. 3º e 4º RN CFQ 339/2025)
    technical_manager = Column(String(255), nullable=True) # Nome do Químico Responsável Técnico
    technical_manager_crq = Column(String(50), nullable=True) # Nº Registro CRQ-V do RT
    aft_number = Column(String(50), nullable=True) # Anotação de Função Técnica (AFT)
    aft_valid_until = Column(String(10), nullable=True) # Validade da AFT (máx 1 ano)
    state_registration = Column(String(50), nullable=True) # Inscrição Estadual (SEFAZ/RS)
    regulatory_status = Column(String(50), default="MANDATORY_REGISTRATION") # MANDATORY_REGISTRATION, CHEMICAL_SUPPORT_ACTIVITY, SERVICE_TO_THIRD_PARTIES
    
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    company = relationship("Company", back_populates="establishments")

