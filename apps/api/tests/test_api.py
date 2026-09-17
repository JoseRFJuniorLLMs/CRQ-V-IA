import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "ok"

def test_login_success():
    response = client.post("/api/auth/login", json={
        "email": "fiscal1@crqv.org.br",
        "password": "crqv@fiscal2026"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["email"] == "fiscal1@crqv.org.br"
    assert data["role"] == "fiscal"

def test_login_invalid_password():
    response = client.post("/api/auth/login", json={
        "email": "fiscal1@crqv.org.br",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_concurrent_sessions():
    """Garante requisito TR-007: suporte a múltiplos acessos simultâneos."""
    r1 = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    r2 = client.post("/api/auth/login", json={"email": "fiscal2@crqv.org.br", "password": "crqv@fiscal2026"})
    assert r1.status_code == 200
    assert r2.status_code == 200
    
    token2 = r2.json()["access_token"]
    headers = {"Authorization": f"Bearer {token2}"}
    sessions_resp = client.get("/api/auth/sessions", headers=headers)
    assert sessions_resp.status_code == 200
    s_data = sessions_resp.json()
    assert s_data["concurrency_guarantee_met"] is True
    assert s_data["minimum_required_by_tr"] == 2

def test_prospects_search():
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Busca geral
    resp = client.get("/api/prospects", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] > 0
    assert len(data["items"]) > 0

    # Filtro por cidade (Porto Alegre)
    resp_poa = client.get("/api/prospects?city=Porto Alegre", headers=headers)
    assert resp_poa.status_code == 200
    poa_data = resp_poa.json()
    assert all(i["city"] == "Porto Alegre" for i in poa_data["items"])

    # Filtro por prioridade HIGH (CFQ 339)
    resp_high = client.get("/api/prospects?tier=HIGH", headers=headers)
    assert resp_high.status_code == 200
    high_data = resp_high.json()
    assert all(i["cfq_tier"] == "HIGH" for i in high_data["items"])

def test_prospect_detail_and_live_check():
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Busca CNPJ da Petroquímica
    cnpj = "92754738000180"
    resp = client.get(f"/api/prospects/{cnpj}", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["cnpj"] == cnpj
    assert data["chemical_score"] >= 90.0
    assert "Resolução CFQ nº 339/2025" in data["cfq_norm_reference"]

    # Teste de consulta cadastral ao vivo
    live_resp = client.get(f"/api/prospects/{cnpj}/live-check", headers=headers)
    assert live_resp.status_code == 200
    live_data = live_resp.json()
    assert live_data["success"] is True

def test_saved_lists_and_items():
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Cria nova lista
    create_resp = client.post("/api/lists", json={
        "name": "Roteiro Teste Serra Gaúcha",
        "description": "Fiscalização de vinícolas e químicas em Caxias e Bento"
    }, headers=headers)
    assert create_resp.status_code == 200
    list_id = create_resp.json()["id"]

    # Busca listas
    lists_resp = client.get("/api/lists", headers=headers)
    assert lists_resp.status_code == 200
    assert any(l["id"] == list_id for l in lists_resp.json())

def test_exports():
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Export CSV
    csv_resp = client.get("/api/exports/prospects.csv", headers=headers)
    assert csv_resp.status_code == 200
    assert "text/csv" in csv_resp.headers["content-type"]
    assert "CNPJ;Razao_Social" in csv_resp.text

    # Export XLSX
    xlsx_resp = client.get("/api/exports/prospects.xlsx", headers=headers)
    assert xlsx_resp.status_code == 200
    assert "spreadsheetml.sheet" in xlsx_resp.headers["content-type"]

def test_dashboard_stats():
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/api/stats/dashboard", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_establishments_rs"] > 0
    assert len(data["by_city"]) > 0
    assert len(data["by_cnae"]) > 0

def test_user_profile_and_password():
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Consulta perfil /me
    me_resp = client.get("/api/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "fiscal1@crqv.org.br"

    # Atualiza perfil /me
    upd_resp = client.put("/api/auth/me", json={"full_name": "Agente Fiscal CRQ-V (Posto 01 Atualizado)"}, headers=headers)
    assert upd_resp.status_code == 200
    assert upd_resp.json()["full_name"] == "Agente Fiscal CRQ-V (Posto 01 Atualizado)"

    # Restaura nome
    client.put("/api/auth/me", json={"full_name": "Agente Fiscal CRQ-V (Posto 01)"}, headers=headers)

def test_paginated_users_and_audit():
    login_resp = client.post("/api/auth/login", json={"email": "admin@crqv.org.br", "password": "admin@crqv2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Tabela paginada de usuários
    users_resp = client.get("/api/auth/users?page=1&page_size=2", headers=headers)
    assert users_resp.status_code == 200
    u_data = users_resp.json()
    assert "items" in u_data
    assert u_data["total"] >= 4
    assert len(u_data["items"]) == 2
    assert u_data["page"] == 1
    assert u_data["total_pages"] >= 2

    # Tabela paginada de auditoria
    audit_resp = client.get("/api/audit?page=1&page_size=5", headers=headers)
    assert audit_resp.status_code == 200
    a_data = audit_resp.json()
    assert "items" in a_data
    assert a_data["total"] > 0
    assert len(a_data["items"]) <= 5
    assert a_data["page"] == 1
