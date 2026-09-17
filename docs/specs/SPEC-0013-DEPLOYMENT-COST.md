# SPEC-0013 — Deploy, cloud e custo

## Restrição de negócio

O Termo de Referência fixou valor estimativo global baixo. A plataforma deve evitar arquitetura superdimensionada.

## Perfil MVP

- 1 app web/API ou dois containers leves.
- 1 worker.
- PostgreSQL gerenciado pequeno.
- Object storage.
- monitoramento básico.

## Ambientes

- `dev`
- `staging`
- `prod`

## Containers

Todos os serviços executáveis devem possuir `Dockerfile` e health check.

## CI/CD

Pipeline:

1. lint;
2. unit tests;
3. type check;
4. SAST/dependency scan;
5. build image;
6. SBOM;
7. deploy staging;
8. smoke test;
9. aprovação;
10. produção.

## Banco

Migrações com Alembic. Toda migração deve ser reversível quando tecnicamente possível.

## Backup

- diário automático;
- retenção mínima definida por contrato/política;
- teste periódico de restore.

## Portabilidade

A solução deve poder migrar entre provedores sem reescrever a aplicação.
