"""
Popula a tabela de CNAEs e regras regulatórias da Resolução CFQ nº 339/2025.
"""

from sqlalchemy.orm import Session
from apps.api.models.cnae import CNAE
from apps.api.engine.cfq_rules import CFQ_CNAE_RULES

def seed_cnaes(db: Session):
    count = 0
    for code, info in CFQ_CNAE_RULES.items():
        existing = db.query(CNAE).filter(CNAE.code == code).first()
        if not existing:
            cnae_record = CNAE(
                code=code,
                description=info["desc"],
                division=code.split("-")[0][:2] if "-" in code else code[:2],
                group_code=code.split("-")[0] if "-" in code else code[:3],
                class_code=code,
                is_chemistry_related=True,
                cfq_tier=info["tier"],
                cfq_scope="basic" if info["tier"] == "HIGH" else "service",
                rationale=info["rationale"]
            )
            db.add(cnae_record)
            count += 1
    
    # Adiciona alguns CNAEs de controle (não-químicos) para testes de filtros
    non_chemical = [
        ("6201-5/01", "Desenvolvimento de programas de computador sob encomenda", "62", False),
        ("4711-3/01", "Comércio varejista de mercadorias em geral (Hipermercados)", "47", False),
        ("6911-7/01", "Serviços advocatícios", "69", False),
        ("5611-2/01", "Restaurantes e similares", "56", False)
    ]
    for code, desc, div, chem in non_chemical:
        if not db.query(CNAE).filter(CNAE.code == code).first():
            db.add(CNAE(
                code=code,
                description=desc,
                division=div,
                class_code=code.split("/")[0] if "/" in code else code,
                is_chemistry_related=chem,
                cfq_tier="NONE",
                rationale="Atividade econômica não sujeita a registro no CRQ-V."
            ))
            count += 1

    db.commit()
    print(f"[Seed] {count} CNAEs e regras CFQ 339/2025 carregados com sucesso.")
