# SPEC-0011 — API

## Convenções

- REST/JSON.
- Versionamento `/api/v1`.
- IDs opacos para objetos internos.
- CNPJ normalizado apenas dígitos.
- OpenAPI gerado automaticamente.

## Endpoints mínimos

```text
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
GET    /api/v1/me
GET    /api/v1/companies
GET    /api/v1/companies/{id}
POST   /api/v1/companies/{id}/verify-cnpj
GET    /api/v1/facets
GET    /api/v1/rulesets
GET    /api/v1/saved-searches
POST   /api/v1/saved-searches
GET    /api/v1/lists
POST   /api/v1/lists
POST   /api/v1/lists/{id}/items
POST   /api/v1/exports
GET    /api/v1/exports/{id}
GET    /api/v1/audit
GET    /health/live
GET    /health/ready
```

## Busca

Query deve aceitar estrutura tipada, evitando SQL dinâmico inseguro.

## Erros

Formato:

```json
{
  "error": {
    "code": "CNPJ_PROVIDER_UNAVAILABLE",
    "message": "Consulta em tempo real indisponível",
    "request_id": "..."
  }
}
```

## Idempotência

Jobs de exportação e verificações podem aceitar `Idempotency-Key`.
