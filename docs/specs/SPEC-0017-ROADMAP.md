# SPEC-0017 — Roadmap de Implementação e Status de Execução

**Situação Atual do Projeto:** 100% IMPLEMENTADO, TESTADO E HOMOLOGADO  
**Data de Conclusão:** Setembro/2026  

---

## Status das Fases de Desenvolvimento

### ✅ Fase 0 — Fundação (CONCLUÍDA)
- [x] Estrutura monorepo unificada (`apps/api`, `apps/web`, `services/ingest`, `infra`).
- [x] Configuração de CI com GitHub Actions (`.github/workflows/ci.yml`).
- [x] Banco de dados SQLAlchemy configurado (SQLite local / PostgreSQL produção).
- [x] Autenticação JWT com controle ativo de sessões simultâneas (mínimo 2 acessos).
- [x] Modelo de dados relacional (`User`, `CNAE`, `Company`, `Establishment`, `SavedList`, `AuditLog`).

### ✅ Fase 1 — Dados e Ingestão (CONCLUÍDA)
- [x] Carga da tabela oficial de CNAEs e regras regulatórias (`seed_cfq_cnaes.py`).
- [x] Filtro geográfico exclusivo para o Estado do Rio Grande do Sul (UF = 'RS').
- [x] Base inicial representativa dos polos industriais e químicos do RS (`seed_rs_companies.py`).
- [x] Orquestrador master de execução de seeds (`run_seed.py`).

### ✅ Fase 2 — Regras Regulatórias e Busca (CONCLUÍDA)
- [x] Motor de regras da Resolução Normativa CFQ nº 339/2025 (`cfq_rules.py`).
- [x] Cálculo determinístico de Score (0 a 100) e Tiers (Alta, Média, Baixa Prioridade).
- [x] Explicabilidade e fundamentação legal obrigatória em linguagem natural para cada empresa.
- [x] Endpoints REST de busca com filtros combinados (CNAE, cidades do RS, porte, situação RFB e score).

### ✅ Fase 3 — Interface e Frontend (CONCLUÍDA)
- [x] Aplicação web responsiva completa servida na raiz (`/`) da API (`apps/web/dist/index.html`).
- [x] Tela de Login com atalhos de demonstração para Posto Fiscal 01 e Posto Fiscal 02.
- [x] Painel de prospecção com filtros laterais multifacetados e ordenação por relevância.
- [x] Modal de Ficha da Empresa com endereço, CNAEs, quadro explicativo e alteração de status CRQ-V.
- [x] Módulo de Roteiros e Listas de Fiscalização com criação e remoção de itens.
- [x] Painel executivo com gráficos interativos (Chart.js) por polo/município e CNAE.

### ✅ Fase 4 — CNPJ em Tempo Real, Exportação e Segurança (CONCLUÍDA)
- [x] Adaptador de consulta cadastral do CNPJ ao vivo junto à RFB (`cnpj_adapter.py`).
- [x] Exportação eletrônica estruturada em formatos CSV e Excel XLSX (`exports.py`).
- [x] Módulo de Auditoria LGPD registrando usuário, IP, ação e timestamp (`audit.py`).
- [x] Endpoint de monitoramento de SLA e healthcheck (`health.py`).

### ✅ Fase 5 — Homologação, Entrega e Documentação (CONCLUÍDA)
- [x] Suíte de testes automatizados com pytest (`test_api.py` com 9 testes passando).
- [x] Script de verificação global do sistema (`scripts/verify_all.py`).
- [x] Manual do Usuário para os fiscais de campo (`docs/delivery/MANUAL_DO_USUARIO.md`).
- [x] Termo de Onboarding e Credenciais de Acesso (`docs/delivery/TERMO_ONBOARDING_CREDENCIAIS.md`).
- [x] Plano de Suporte Técnico e SLA Contratual (`docs/delivery/PLANO_SUPORTE_SLA.md`).
- [x] Política de Privacidade e Conformidade LGPD (`docs/delivery/POLITICA_PRIVACIDADE_LGPD.md`).
- [x] Proposta Comercial Preenchida do Anexo II (`docs/procurement/PROPOSTA_COMERCIAL_PREENCHIDA.md`).
- [x] Pacote de Declarações Obrigatórias do Edital (`docs/procurement/DECLARACOES_OBRIGATORIAS.md`).
- [x] Especificação formal de conformidade integral (`docs/specs/SPEC-0018-CONFORMIDADE.md`).
- [x] Script de inicialização em 1 clique para Windows (`run.ps1`) e Linux (`run.sh`).
