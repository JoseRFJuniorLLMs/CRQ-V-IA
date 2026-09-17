import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from apps.api.core.database import SessionLocal, init_db
from apps.api.models.saved_list import SavedList, SavedListItem
from apps.api.models.company import Establishment
from apps.api.models.user import User
from services.ingest.seed_cfq_cnaes import seed_cnaes
from services.ingest.seed_users import seed_users
from services.ingest.seed_rs_companies import seed_companies

def run():
    print("=== Inicializando Banco de Dados e Schemas ===")
    init_db()

    db = SessionLocal()
    try:
        print("\n=== 1. Carga de CNAEs e Regras CFQ 339/2025 ===")
        seed_cnaes(db)

        print("\n=== 2. Carga de Usuários e Fiscais do CRQ-V ===")
        seed_users(db)

        print("\n=== 3. Carga e Classificação de Empresas do RS ===")
        seed_companies(db)

        print("\n=== 4. Criando Roteiro Inicial de Fiscalização de Demonstração ===")
        fiscal_user = db.query(User).filter(User.email == "fiscal1@crqv.org.br").first()
        existing_list = db.query(SavedList).filter(SavedList.name.ilike("%Polo Petroquímico%")).first()

        if not existing_list and fiscal_user:
            demo_list = SavedList(
                name="Roteiro 01 - Polo Petroquímico e Região Metropolitana",
                description="Roteiro de fiscalização prioritária para indústrias químicas e petroquímicas não cadastradas.",
                created_by_id=fiscal_user.id
            )
            db.add(demo_list)
            db.flush()

            # Pega as primeiras empresas High Tier não cadastradas
            targets = db.query(Establishment).filter(
                Establishment.cfq_tier == "HIGH",
                Establishment.crq_status == "NAO_CADASTRADA"
            ).limit(3).all()

            for t in targets:
                db.add(SavedListItem(
                    list_id=demo_list.id,
                    establishment_id=t.id,
                    priority="ALTA",
                    fiscal_status="PENDENTE",
                    notes="Empresa com alto potencial químico não localizada no cadastro ativo do CRQ-V. Diligência presencial prioritária."
                ))
            db.commit()
            print(f"[Seed] Lista de fiscalização '{demo_list.name}' criada com {len(targets)} alvos.")

        print("\n[OK] Base de dados do CRQ-V-IA 100% pronta e operacional!")
    finally:
        db.close()

if __name__ == "__main__":
    run()
