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
    assert "regulatory_status" in data

    # Teste de consulta cadastral ao vivo (SPEC-0021)
    live_resp = client.get(f"/api/prospects/{cnpj}/live-check", headers=headers)
    assert live_resp.status_code == 200
    live_data = live_resp.json()
    assert "verification_status" in live_data
    if live_data["success"]:
        assert live_data["verification_status"] == "CONFIRMED"
    else:
        assert live_data["verification_status"] == "UNAVAILABLE"
        assert live_data["registration_status"] == "NAO_VERIFICADO"

def test_search_by_secondary_cnae_and_division():
    """Garante busca em CNAEs secundários e por divisão da hierarquia (SPEC-0021)."""
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Busca por CNAE 2031 (presente como secundário na Petroquímica)
    resp_sec = client.get("/api/prospects?cnae=2031", headers=headers)
    assert resp_sec.status_code == 200
    data_sec = resp_sec.json()
    assert data_sec["total"] > 0
    assert any("92754738000180" in item["cnpj"] for item in data_sec["items"])

    # Busca por Divisão 20 (Fabricação de produtos químicos)
    resp_div = client.get("/api/prospects?division=20", headers=headers)
    assert resp_div.status_code == 200
    assert resp_div.json()["total"] > 0


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

def test_login_web2ajax_admin():
    """Valida autenticação do usuário master admin web2ajax@gmail.com."""
    response = client.post("/api/auth/login", json={
        "email": "web2ajax@gmail.com",
        "password": "debian23"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "web2ajax@gmail.com"
    assert data["role"] == "admin"
    assert "access_token" in data

def test_all_individual_prospect_filters():
    """Testa individualmente cada parâmetro de busca e filtro da API de prospects."""
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Busca textual por Razão Social
    r_q_name = client.get("/api/prospects?q=Tintas", headers=headers)
    assert r_q_name.status_code == 200
    assert r_q_name.json()["total"] > 0

    # 2. Busca textual por CNPJ (sem formatação)
    r_q_cnpj = client.get("/api/prospects?q=92754738000180", headers=headers)
    assert r_q_cnpj.status_code == 200
    assert r_q_cnpj.json()["total"] == 1
    assert r_q_cnpj.json()["items"][0]["cnpj"] == "92754738000180"

    # 3. Busca por CNAE Primário
    r_cnae = client.get("/api/prospects?cnae=2021", headers=headers)
    assert r_cnae.status_code == 200
    assert r_cnae.json()["total"] > 0

    # 4. Busca por Divisão Econômica (2 dígitos)
    r_div = client.get("/api/prospects?division=20", headers=headers)
    assert r_div.status_code == 200
    assert r_div.json()["total"] > 0
    assert len(r_div.json()["items"]) > 0

    # 5. Filtro por Município (RS)
    r_city = client.get("/api/prospects?city=Triunfo", headers=headers)
    assert r_city.status_code == 200
    assert r_city.json()["total"] > 0
    assert all(i["city"] == "Triunfo" for i in r_city.json()["items"])

    # 6. Filtro por Bairro/Distrito
    r_dist = client.get("/api/prospects?district=Navegantes", headers=headers)
    assert r_dist.status_code == 200
    assert r_dist.json()["total"] > 0
    assert any("Navegantes" in (i["district"] or "") for i in r_dist.json()["items"])

    # 7. Filtro por Tipo de Estabelecimento (MATRIZ e FILIAL)
    r_matriz = client.get("/api/prospects?branch_type=MATRIZ", headers=headers)
    assert r_matriz.status_code == 200
    assert all(i["branch_type"] == "MATRIZ" for i in r_matriz.json()["items"])

    r_filial = client.get("/api/prospects?branch_type=FILIAL", headers=headers)
    assert r_filial.status_code == 200
    assert all(i["branch_type"] == "FILIAL" for i in r_filial.json()["items"])

    # 8. Filtro por Porte Empresarial
    r_me = client.get("/api/prospects?size=ME", headers=headers)
    assert r_me.status_code == 200
    assert all(i["company_size"] == "ME" for i in r_me.json()["items"])

    r_demais = client.get("/api/prospects?size=DEMAIS", headers=headers)
    assert r_demais.status_code == 200
    assert all(i["company_size"] == "DEMAIS" for i in r_demais.json()["items"])

    # 9. Filtro por Situação Cadastral RFB
    r_ativa = client.get("/api/prospects?status=ATIVA", headers=headers)
    assert r_ativa.status_code == 200
    assert all(i["registration_status"] == "ATIVA" for i in r_ativa.json()["items"])

    r_baixada = client.get("/api/prospects?status=BAIXADA", headers=headers)
    assert r_baixada.status_code == 200
    assert all(i["registration_status"] == "BAIXADA" for i in r_baixada.json()["items"])

    # 10. Filtro por Situação Interna no CRQ-V
    r_crq_alvo = client.get("/api/prospects?crq_status=NAO_CADASTRADA", headers=headers)
    assert r_crq_alvo.status_code == 200
    assert all(i["crq_status"] == "NAO_CADASTRADA" for i in r_crq_alvo.json()["items"])

    r_crq_fisc = client.get("/api/prospects?crq_status=EM_FISCALIZACAO", headers=headers)
    assert r_crq_fisc.status_code == 200
    assert all(i["crq_status"] == "EM_FISCALIZACAO" for i in r_crq_fisc.json()["items"])

    # 11. Filtro por Score Químico Mínimo
    r_score = client.get("/api/prospects?min_score=85", headers=headers)
    assert r_score.status_code == 200
    assert all(i["chemical_score"] >= 85.0 for i in r_score.json()["items"])

    # 12. Filtro por Capital Social Mínimo
    r_cap = client.get("/api/prospects?min_capital=1000000", headers=headers)
    assert r_cap.status_code == 200
    assert all(i["capital_social"] >= 1000000.0 for i in r_cap.json()["items"])

def test_combined_multi_criteria_query():
    """Testa consulta combinando múltiplos filtros simultâneos."""
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    url = "/api/prospects?city=Triunfo&division=20&tier=HIGH&status=ATIVA&branch_type=MATRIZ&min_score=80"
    resp = client.get(url, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] > 0
    for item in data["items"]:
        assert item["city"] == "Triunfo"
        assert item["primary_cnae"].startswith("20")
        assert item["cfq_tier"] == "HIGH"
        assert item["registration_status"] == "ATIVA"
        assert item["branch_type"] == "MATRIZ"
        assert item["chemical_score"] >= 80.0

def test_prospects_pagination_and_limits():
    """Testa paginação rigorosa com limites e navegação entre páginas."""
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Página 1 com 3 itens
    r1 = client.get("/api/prospects?page=1&page_size=3", headers=headers)
    assert r1.status_code == 200
    d1 = r1.json()
    assert len(d1["items"]) == 3
    assert d1["page"] == 1
    assert d1["page_size"] == 3

    # Página 2 com 3 itens
    r2 = client.get("/api/prospects?page=2&page_size=3", headers=headers)
    assert r2.status_code == 200
    d2 = r2.json()
    assert len(d2["items"]) == 3
    assert d2["page"] == 2

    # Itens da página 1 devem ser distintos da página 2
    p1_cnpjs = {i["cnpj"] for i in d1["items"]}
    p2_cnpjs = {i["cnpj"] for i in d2["items"]}
    assert p1_cnpjs.isdisjoint(p2_cnpjs)

def test_crq_status_mutation_flow():
    """Testa atualização de situação de fiscalização (PATCH) e persistência no banco."""
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    cnpj = "92754738000180"
    # Altera para EM_FISCALIZACAO com observações
    patch_resp = client.patch(f"/api/prospects/{cnpj}/crq-status", json={
        "crq_status": "EM_FISCALIZACAO",
        "crq_notes": "Notificação expedida para vistoria in loco"
    }, headers=headers)
    assert patch_resp.status_code == 200
    assert patch_resp.json()["crq_status"] == "EM_FISCALIZACAO"

    # Confirma persistência no GET da ficha detalhada
    detail_resp = client.get(f"/api/prospects/{cnpj}", headers=headers)
    assert detail_resp.status_code == 200
    assert detail_resp.json()["crq_status"] == "EM_FISCALIZACAO"
    assert detail_resp.json()["crq_notes"] == "Notificação expedida para vistoria in loco"

def test_saved_lists_complete_lifecycle():
    """Testa ciclo completo de listas: criação, adição de empresa, consulta paginada e remoção."""
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Cria lista
    create_list = client.post("/api/lists", json={
        "name": "Roteiro Operacional Canoas/Esteio",
        "description": "Diligências programadas"
    }, headers=headers)
    assert create_list.status_code == 200
    list_id = create_list.json()["id"]

    # 2. Busca um prospect para obter id
    prospect_resp = client.get("/api/prospects?page=1&page_size=1", headers=headers)
    est_id = prospect_resp.json()["items"][0]["id"]

    # 3. Adiciona item à lista
    add_item = client.post(f"/api/lists/{list_id}/items", json={
        "establishment_id": est_id,
        "priority": "ALTA",
        "notes": "Verificar responsável técnico in loco"
    }, headers=headers)
    assert add_item.status_code == 200
    item_id = add_item.json()["id"]

    # 4. Consulta itens paginados da lista
    items_resp = client.get(f"/api/lists/{list_id}/items?page=1&page_size=5", headers=headers)
    assert items_resp.status_code == 200
    items_data = items_resp.json()
    assert items_data["total"] >= 1
    assert any(i["id"] == item_id for i in items_data["items"])

    # 5. Remove item da lista
    del_item = client.delete(f"/api/lists/{list_id}/items/{item_id}", headers=headers)
    assert del_item.status_code == 200

    # 6. Exclui lista
    del_list = client.delete(f"/api/lists/{list_id}", headers=headers)
    assert del_list.status_code == 200

def test_exports_with_specific_filters():
    """Testa exportação CSV e XLSX aplicando filtros de consulta."""
    login_resp = client.post("/api/auth/login", json={"email": "fiscal1@crqv.org.br", "password": "crqv@fiscal2026"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # CSV com filtro de cidade
    csv_resp = client.get("/api/exports/prospects.csv?city=Porto Alegre", headers=headers)
    assert csv_resp.status_code == 200
    assert "Porto Alegre" in csv_resp.text

    # XLSX com filtro de prioridade HIGH
    xlsx_resp = client.get("/api/exports/prospects.xlsx?tier=HIGH", headers=headers)
    assert xlsx_resp.status_code == 200
    assert len(xlsx_resp.content) > 1000


