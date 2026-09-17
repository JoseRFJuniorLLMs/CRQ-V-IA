# SPEC-0004 — Busca, filtros e segmentação

## Busca livre

Pesquisar por:

- CNPJ completo ou parcial normalizado.
- Razão social.
- Nome fantasia.
- Município.
- CNAE/código/descritivo.

## Facetas mínimas

- Situação cadastral.
- Município.
- Região do estado.
- CNAE principal.
- CNAE secundário.
- Divisão/grupo/classe CNAE.
- Porte.
- Capital social por faixa.
- Data de abertura.
- Score/tier.
- Match regulatório.
- Estado no CRQ-V, quando base interna disponível.

## Operadores

- AND entre grupos de filtros.
- OR dentro de seleção múltipla da mesma faceta.
- Inclusão/exclusão de CNAEs.
- Intervalos de capital/data.

## Performance

- Paginação por cursor para grandes resultados.
- Contagens facetadas calculadas de forma eficiente.
- P95 alvo < 1,5 s para consultas comuns.

## Persistência

Usuário pode salvar uma consulta com nome e filtros. A consulta deve ser serializável em JSON e reexecutável em competência futura.
