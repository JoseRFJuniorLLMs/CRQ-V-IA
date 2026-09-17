# SPEC-0007 — Autenticação, RBAC e acessos simultâneos

## Requisito editalício

No mínimo dois acessos simultâneos.

## Política do produto

Não impor limite técnico de 2 usuários. O tenant CRQ-V deve permitir pelo menos 2 sessões simultâneas e preferencialmente um número configurável de contas, evitando interpretação restritiva de “acesso”.

## Perfis

- `ADMIN`
- `COORDINATOR`
- `INSPECTOR`
- `READ_ONLY`

## Segurança

- Senhas Argon2id.
- MFA obrigatório para admins, recomendável para todos.
- Sessões revogáveis.
- Lockout progressivo/rate limit.
- Auditoria de login, logout e falhas.

## SSO

OIDC/SAML fica preparado como extensão, sem ser dependência do MVP.

## Teste de aceite

Abrir duas sessões em navegadores/usuários distintos e executar consultas simultaneamente sem expulsão, serialização artificial ou degradação relevante.
