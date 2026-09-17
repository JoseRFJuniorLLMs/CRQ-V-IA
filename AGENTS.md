# AGENTS.md — instruções para agentes de desenvolvimento

## Objetivo

Implementar o CRQ-V-IA de acordo com as SPECs em `docs/specs/`.

## Regras

1. Não inventar requisitos jurídicos.
2. Não transformar score em conclusão de irregularidade.
3. Não raspar páginas protegidas por captcha.
4. Não ingerir QSA por padrão.
5. Toda regra regulatória precisa de `source_norm` e `rule_set_version`.
6. Toda informação cadastral precisa de fonte e timestamp.
7. Toda exportação precisa gerar auditoria.
8. Cada feature deve referenciar o ID do requisito correspondente.
9. Não introduzir Redis/Kafka/Elasticsearch sem benchmark que justifique.
10. Priorizar PostgreSQL e componentes simples para reduzir custo.

## Definition of Done

- testes unitários;
- testes de integração;
- lint/typecheck;
- documentação de endpoint;
- segurança básica;
- migração de banco;
- evidência de aceite atualizada.
