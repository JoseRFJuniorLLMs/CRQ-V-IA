"""
Script de Verificação Global de Integridade do CRQ-V-IA.
Executa diagnóstico completo do sistema e valida conformidade.
"""

import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.core.database import SessionLocal
from apps.api.models.cnae import CNAE
from apps.api.models.company import Establishment, Company
from apps.api.models.user import User
from apps.api.models.saved_list import SavedList

def verify():
    print("==========================================================")
    print("   VERIFICAÇÃO GLOBAL DE INTEGRIDADE: CRQ-V-IA            ")
    print("   Conselho Regional de Química da 5ª Região (RS)         ")
    print("==========================================================\n")

    # 1. Banco de Dados
    print("[1/5] Verificando Base de Dados...")
    db = SessionLocal()
    try:
        cnae_count = db.query(CNAE).count()
        user_count = db.query(User).count()
        est_count = db.query(Establishment).count()
        list_count = db.query(SavedList).count()

        print(f"  ✓ CNAEs e regras CFQ 339/2025: {cnae_count} registros")
        print(f"  ✓ Usuários cadastrados (TR 02 acessos): {user_count} registros")
        print(f"  ✓ Estabelecimentos classificados no RS: {est_count} registros")
        print(f"  ✓ Roteiros de fiscalização ativos: {list_count} listas")
        assert cnae_count >= 40, "Base de CNAEs incompleta"
        assert user_count >= 3, "Usuários insuficientes"
        assert est_count >= 15, "Poucas empresas no RS"
    finally:
        db.close()

    # 2. Testes de API
    print("\n[2/5] Testando Endpoints da API REST...")
    client = TestClient(app)

    # Health
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json()["status"] == "healthy", "Healthcheck falhou"
    print("  ✓ GET /api/health: OK (Healthy)")

    # Login
    r = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    assert r.status_code == 200, "Login fiscal1 falhou"
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("  ✓ POST /api/auth/login: OK (JWT emitido)")

    # Sessões simultâneas
    r_sess = client.get("/api/auth/sessions", headers=headers)
    assert r_sess.status_code == 200 and r_sess.json()["concurrency_guarantee_met"] is True
    print(f"  ✓ Concorrência TR-007: OK (Mínimo {r_sess.json()['minimum_required_by_tr']} acessos)")

    # Prospecção
    r_pros = client.get("/api/prospects?tier=HIGH", headers=headers)
    assert r_pros.status_code == 200 and r_pros.json()["total"] > 0
    print(f"  ✓ Prospecção CFQ 339/2025: OK ({r_pros.json()['total']} empresas High Priority encontradas)")

    # 3. Exportações
    print("\n[3/5] Verificando Exportações Eletrônicas...")
    r_csv = client.get("/api/exports/prospects.csv", headers=headers)
    assert r_csv.status_code == 200 and len(r_csv.content) > 500
    print(f"  ✓ Exportação CSV: OK ({len(r_csv.content)} bytes gerados)")

    r_xlsx = client.get("/api/exports/prospects.xlsx", headers=headers)
    assert r_xlsx.status_code == 200 and len(r_xlsx.content) > 1000
    print(f"  ✓ Exportação Excel (XLSX): OK ({len(r_xlsx.content)} bytes gerados)")

    # 4. Frontend
    print("\n[4/5] Verificando Frontend Unificado...")
    r_web = client.get("/")
    assert r_web.status_code == 200 and "CRQ-V-IA" in r_web.text
    print("  ✓ Entrega da SPA em /: OK (HTML responsivo servido)")

    # 5. Documentação
    print("\n[5/5] Verificando Pacote de Documentos do Edital...")
    docs_to_check = [
        "README.md",
        "relatorio.md",
        "run.ps1",
        "docs/specs/SPEC-0018-CONFORMIDADE.md",
        "docs/delivery/MANUAL_DO_USUARIO.md",
        "docs/delivery/TERMO_ONBOARDING_CREDENCIAIS.md",
        "docs/delivery/PLANO_SUPORTE_SLA.md",
        "docs/delivery/POLITICA_PRIVACIDADE_LGPD.md",
        "docs/procurement/PROPOSTA_COMERCIAL_PREENCHIDA.md",
        "docs/procurement/DECLARACOES_OBRIGATORIAS.md"
    ]
    for d in docs_to_check:
        p = Path(d)
        assert p.exists() and p.stat().st_size > 0, f"Arquivo {d} não encontrado"
        print(f"  ✓ {d}: OK ({p.stat().st_size} bytes)")

    print("\n==========================================================")
    print("   TODAS AS VERIFICAÇÕES PASSARAM COM 100% DE SUCESSO!   ")
    print("   A PLATAFORMA CRQ-V-IA ESTÁ PRONTA PARA HOMOLOGAÇÃO!    ")
    print("==========================================================")

if __name__ == "__main__":
    verify()
