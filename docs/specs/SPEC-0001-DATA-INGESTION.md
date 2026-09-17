# SPEC-0001 — Ingestão e atualização de dados

## Objetivo

Criar pipeline reprodutível para importar dados empresariais de fontes oficiais, com foco no RS.

## Requisitos

### ING-001 — Versionamento por competência

Cada importação deve gerar `source_version` imutável. A versão em produção aponta para uma competência aprovada.

### ING-002 — Staging isolado

Nenhum dado parcial pode ficar visível na busca. Importação em schema/tabelas de staging e publicação atômica.

### ING-003 — Filtro antecipado

Filtrar estabelecimentos por `UF=RS` antes de joins custosos.

### ING-004 — Validação

Validar:

- presença de arquivos esperados;
- encoding;
- quantidade mínima de linhas;
- schema;
- duplicidade de CNPJ;
- domínios de situação cadastral;
- integridade entre empresas e estabelecimentos.

### ING-005 — Observabilidade

Registrar duração, linhas lidas, linhas válidas, rejeitadas, tamanho, hash e versão.

### ING-006 — Rollback

A publicação deve ser reversível para a versão anterior sem reprocessamento.

## Implementação

Usar Polars/DuckDB para leitura em streaming/batch. Persistir somente os campos necessários à prospecção.

## Testes

- Dataset sintético mínimo.
- Arquivo corrompido.
- Coluna ausente.
- Competência duplicada.
- Falha no meio do processamento.
- Rollback após publicação.
