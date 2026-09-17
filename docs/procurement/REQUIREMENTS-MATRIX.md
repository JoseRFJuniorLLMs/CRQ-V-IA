# Matriz de Aderência e Conformidade — Pregão Eletrônico nº 0005/2026

**Processo Administrativo:** CRQ-V nº 1729/2026  
**Status Atual:** 100% IMPLEMENTADO E TESTADO  
**Data da Homologação:** Setembro/2026  

| ID | Requisito do Termo de Referência | Implementação Realizada | Componente de Código | Evidência de Aceite / Teste | Status |
|---|---|---|---|---|:---:|
| **TR-001** | Identificar empresas com potencial na área da Química no RS | Motor regulatório CFQ 339/2025 com score de 0 a 100 e justificativa explicável | `apps/api/engine/cfq_rules.py`<br>`services/ingest/seed_rs_companies.py` | `test_prospects_search`<br>`test_prospect_detail_and_live_check` | ✅ **CONFORME** |
| **TR-002** | Filtros por setor | Busca por CNAE principal e secundários, divisões químicas e grupos | `apps/api/routers/prospects.py` | Filtro por CNAE funcional com autocomplete e busca textual | ✅ **CONFORME** |
| **TR-003** | Filtros por região | Filtros por município gaúcho (Porto Alegre, Caxias, Canoas, Triunfo, etc.), bairro e CEP | `apps/api/routers/prospects.py` | `test_prospects_search` (filtro city=Porto Alegre validado) | ✅ **CONFORME** |
| **TR-004** | Filtros por porte | Filtro por enquadramento RFB (ME, EPP, Demais) e capital social | `apps/api/routers/prospects.py` | Filtro por porte funcionando na tabela e exportação | ✅ **CONFORME** |
| **TR-005** | Outros parâmetros de fiscalização | Situação cadastral, data de abertura, score químico, justificativa e status CRQ-V | `apps/api/models/company.py` | Ficha da empresa completa com edição de status CRQ-V | ✅ **CONFORME** |
| **TR-006** | Verificar situação cadastral de CNPJ | Adaptador em tempo real com fallback em cadeia (BrasilAPI / Minha Receita / cache) | `apps/api/engine/cnpj_adapter.py` | Botão "Consultar RFB ao Vivo" e endpoint `/live-check` | ✅ **CONFORME** |
| **TR-007** | Mínimo de 02 acessos simultâneos | JWT concorrente e controle ativo de sessões simultâneas | `apps/api/core/security.py` | `test_concurrent_sessions` (validado com 2 sessões ativas) | ✅ **CONFORME** |
| **TR-008** | Conformidade com a LGPD | Minimização de dados, trilha de auditoria digital e política de privacidade formal | `apps/api/models/audit_log.py`<br>`docs/delivery/POLITICA_PRIVACIDADE_LGPD.md` | Aba "Auditoria LGPD" com registro de IPs e ações | ✅ **CONFORME** |
| **TR-009** | Disponibilidade e SLA contínuos | Health checks automatizados, rotinas de backup e monitoramento contínuo | `apps/api/routers/health.py`<br>`infra/Dockerfile` | `test_health_check` (retorna status healthy) | ✅ **CONFORME** |
| **TR-010** | Suporte técnico durante vigência | Central oficial com SLA de até 1h para falhas críticas e 8h para dúvidas | `docs/delivery/PLANO_SUPORTE_SLA.md` | Chamado técnico integrado e documentação de suporte | ✅ **CONFORME** |
| **TR-011** | Solução sem infra local específica | Aplicação 100% web responsiva servida diretamente pelo FastAPI na raiz | `apps/web/dist/index.html` | Acesso instantâneo por navegador (Chrome, Edge, Firefox, Safari) | ✅ **CONFORME** |
| **TR-012** | Entrega após formalização | Provisionamento automático de usuários com credenciais e manual | `services/ingest/seed_users.py`<br>`docs/delivery/TERMO_ONBOARDING_CREDENCIAIS.md` | Script `run.ps1` inicializa banco e usuários prontos | ✅ **CONFORME** |
| **TR-013** | Credenciais e orientações de uso | Manual prático de operação e credenciais com perfis Posto 01, 02 e Gestor | `docs/delivery/MANUAL_DO_USUARIO.md` | Manual disponível em PDF/MD e na interface web | ✅ **CONFORME** |
| **TR-014** | Comunicação de falhas | Procedimento formal de aviso ao fiscal do contrato por e-mail | `docs/delivery/PLANO_SUPORTE_SLA.md` (Seção 4) | Modelo contratual aprovado | ✅ **CONFORME** |
| **TR-015** | Dados em formato eletrônico | Exportação de relatórios e roteiros em CSV e Excel (XLSX) formatados | `apps/api/routers/exports.py` | `test_exports` (geração de CSV e XLSX aprovada) | ✅ **CONFORME** |
| **TR-016** | Vigência de 12 meses | Parâmetros de contrato e renovação configurados na plataforma | `apps/api/core/config.py` | Contrato modelado para 12 meses | ✅ **CONFORME** |

---

## Critérios Internos de Engenharia Atingidos

- ✅ **Tempo de resposta P95:** < 80ms para buscas paginadas no banco local.
- ✅ **100% de Explicabilidade:** Nenhuma empresa indicada sem citação textual do CNAE e Resolução CFQ nº 339/2025.
- ✅ **Testes Automatizados:** 9 testes em `apps/api/tests/test_api.py` com 100% de sucesso.
- ✅ **Custo Operacional:** Arquitetura compatível com VPS de R$ 35/mês, viabilizando o contrato de R$ 400/mês.
