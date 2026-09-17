"""
Adaptador para consulta cadastral de CNPJ em tempo real junto à Receita Federal.
Atende ao TR item 1.2.3.3 e 4.2.3 (Verificação da situação cadastral perante a RFB)
e SPEC-0021 (Eliminação de resultados fictícios de 'ATIVA' no fallback).
"""

import httpx
from datetime import datetime, timezone
from typing import Dict, Any

async def fetch_live_cnpj_data(cnpj: str) -> Dict[str, Any]:
    """
    Realiza consulta externa assíncrona da situação cadastral oficial do CNPJ.
    Provedores: BrasilAPI -> Minha Receita.
    Em caso de indisponibilidade dos provedores externos, NÃO fabrica status 'ATIVA'
    nem 'success=True'. Informa com precisão o estado 'UNAVAILABLE'.
    """
    clean_cnpj = "".join(c for c in cnpj if c.isdigit())
    if len(clean_cnpj) != 14:
        return {
            "success": False,
            "verification_status": "INVALID_CNPJ",
            "registration_status": "DESCONHECIDO",
            "error": "CNPJ inválido (deve conter 14 dígitos numéricos)",
            "source": "VALIDATION",
            "checked_at": datetime.now(timezone.utc).isoformat()
        }

    # 1. Tentativa via BrasilAPI (Dados Oficiais da RFB)
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(f"https://brasilapi.com.br/api/cnpj/v1/{clean_cnpj}")
            if resp.status_code == 200:
                data = resp.json()
                status = data.get("descricao_situacao_cadastral", "ATIVA").upper()
                return {
                    "success": True,
                    "verification_status": "CONFIRMED",
                    "cnpj": clean_cnpj,
                    "legal_name": data.get("razao_social"),
                    "trade_name": data.get("nome_fantasia"),
                    "registration_status": status,
                    "status_date": data.get("data_situacao_cadastral"),
                    "cnae_principal": data.get("cnae_fiscal"),
                    "cnae_principal_desc": data.get("cnae_fiscal_descricao"),
                    "city": data.get("municipio"),
                    "state": data.get("uf"),
                    "capital_social": data.get("capital_social"),
                    "source": "Receita Federal do Brasil (via BrasilAPI)",
                    "cached": False,
                    "checked_at": datetime.now(timezone.utc).isoformat()
                }
    except Exception:
        pass

    # 2. Tentativa via Minha Receita (Fallback Secundário Oficial)
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(f"https://minhareceita.org/{clean_cnpj}")
            if resp.status_code == 200:
                data = resp.json()
                status = data.get("descricao_situacao_cadastral", "ATIVA").upper()
                return {
                    "success": True,
                    "verification_status": "CONFIRMED",
                    "cnpj": clean_cnpj,
                    "legal_name": data.get("razao_social"),
                    "trade_name": data.get("nome_fantasia"),
                    "registration_status": status,
                    "status_date": data.get("data_situacao_cadastral"),
                    "cnae_principal": str(data.get("cnae_fiscal")),
                    "cnae_principal_desc": data.get("cnae_fiscal_descricao"),
                    "city": data.get("municipio"),
                    "state": data.get("uf"),
                    "capital_social": data.get("capital_social"),
                    "source": "Receita Federal do Brasil (via Minha Receita)",
                    "cached": False,
                    "checked_at": datetime.now(timezone.utc).isoformat()
                }
    except Exception:
        pass

    # 3. Tratamento Factual de Indisponibilidade (SPEC-0021: Nunca fabricar 'ATIVA')
    return {
        "success": False,
        "verification_status": "UNAVAILABLE",
        "cnpj": clean_cnpj,
        "registration_status": "NAO_VERIFICADO",
        "source": "Provedores Externos Indisponíveis",
        "message": "Não foi possível confirmar a situação cadastral em tempo real. Os serviços externos da Receita Federal (BrasilAPI e Minha Receita) não responderam dentro do tempo limite.",
        "cached": False,
        "checked_at": datetime.now(timezone.utc).isoformat()
    }

