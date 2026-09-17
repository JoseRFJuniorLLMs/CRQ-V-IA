# CRQ-V-IA — Plataforma de Prospecção Fiscal Inteligente

[![CI Status](https://github.com/JoseRFJuniorLLMs/CRQ-V-IA/actions/workflows/ci.yml/badge.svg)](https://github.com/JoseRFJuniorLLMs/CRQ-V-IA/actions)
[![Conformidade TR](https://img.shields.io/badge/Pregão%200005%2F2026-100%25%20Conforme-emerald)](docs/specs/SPEC-0018-CONFORMIDADE.md)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal)](https://fastapi.tiangolo.com)
[![Licença](https://img.shields.io/badge/Licença-MIT-slate)](LICENSE.md)

Solução especializada para prospecção, qualificação, segmentação e priorização de empresas potencialmente sujeitas à fiscalização do **Conselho Regional de Química da 5ª Região (CRQ-V)**, com foco estrito no **Estado do Rio Grande do Sul**.

Desenvolvida sob medida para atender integralmente ao **Pregão Eletrônico nº 0005/2026 (Processo CRQ-V nº 1729/2026)**.

---

## 🚀 Como Executar em 1 Clique

### No Windows (PowerShell):
```powershell
# Executa a inicialização automática e abre o sistema no navegador
.\run.ps1
```

### Manualmente (com uv ou python):
```bash
# 1. Instalar dependências
uv pip install -r apps/api/requirements.txt

# 2. Inicializar banco e carregar dados do RS (CNAEs CFQ 339, usuários e empresas)
python services/ingest/run_seed.py

# 3. Iniciar o servidor unificado (API + Frontend)
uvicorn apps.api.main:app --port 8000
```

* **Aplicação Web:** [http://localhost:8000](http://localhost:8000)
* **Documentação Interativa (Swagger OpenAPI):** [http://localhost:8000/docs](http://localhost:8000/docs)

### Credenciais de Acesso (Mínimo 2 Acessos Simultâneos - TR 1.2.3.4):
* **Posto Fiscal 01:** `fiscal1@crqv.org.br` | Senha: `crqv@fiscal2026`
* **Posto Fiscal 02:** `fiscal2@crqv.org.br` | Senha: `crqv@fiscal2026`
* **Gestor Fiscal:** `gestor@crqv.org.br` | Senha: `crqv@gestor2026`
* **Administrador:** `admin@crqv.org.br` | Senha: `admin@crqv2026`

---

## 🎯 Diferencial Técnico e Regulatório

1. **Motor Regulatório Transparente e Explicável:**  
   Não é uma "caixa-preta". O enquadramento fundamenta-se nas classes e subclasses da **Resolução Normativa CFQ nº 339/2025**. Toda empresa prospectada detalha explicitamente quais CNAEs (primário e secundários) motivaram a indicação, o peso do fator e o texto normativo aplicável.
2. **Consulta em Tempo Real de Situação Cadastral (RFB):**  
   Adaptador com fallback em cadeia (BrasilAPI, Minha Receita e base interna em cache) para validação ao vivo da situação cadastral do CNPJ sem necessidade de credenciais pagas ou que dependam de liberação do órgão.
3. **Controle Ativo de Concorrência:**  
   Garante e monitora ativamente múltiplos acessos simultâneos sem bloqueios (contador em tempo real na interface e no endpoint `/api/auth/sessions`).
4. **Montagem de Roteiros e Exportação em 1 Clique:**  
   Permite salvar empresas em listas de fiscalização de campo e exportá-las em planilhas formatadas (**Excel XLSX** e **CSV**) contendo endereços, contatos e notas.
5. **Conformidade LGPD e Rastreabilidade Total:**  
   Minimização de dados (sem exposição desnecessária de quadros societários) e trilha completa de auditoria imutável (`/api/audit`) registrando usuário, IP, ação e parâmetros.

---

## 🏛️ Matriz de Conformidade com o Pregão 0005/2026

A especificação exaustiva de atendimento encontra-se em **[SPEC-0018-CONFORMIDADE.md](docs/specs/SPEC-0018-CONFORMIDADE.md)**.

| Requisito do Termo de Referência | Como é Atendido | Status |
|---|---|---|
| **TR 1.1 / 4.2.1** — Prospecção na área da Química no RS | Base de empresas gaúchas classificada pelo motor CFQ 339/2025 | ✅ Conforme |
| **TR 4.2.2** — Filtros por setor, região, porte e situação | Painel multifacetado com busca por CNAE, cidades do RS, porte e status RFB | ✅ Conforme |
| **TR 4.2.3** — Verificação da situação cadastral do CNPJ | Consulta em tempo real via endpoint `/live-check` e botão na ficha cadastral | ✅ Conforme |
| **TR 4.2.4** — Mínimo de 02 acessos simultâneos | JWT concorrente e monitor de sessões ativas | ✅ Conforme |
| **TR 4.2.6** — Conformidade estrita com a LGPD | Política de minimização no banco e log de auditoria para todas as operações | ✅ Conforme |
| **TR 4.3.2** — Dados em formato eletrônico (redução de papel) | Exportação de relatórios e roteiros em CSV e XLSX estruturados | ✅ Conforme |
| **TR 4.5 / 4.12** — Suporte e comunicação de falhas | Central oficial de suporte com SLA de 1h para incidentes críticos | ✅ Conforme |
| **TR 4.11** — Entrega, credenciamento e orientações | Manual do Usuário em PDF/MD e Termo de Credenciamento formalizados | ✅ Conforme |
| **TR 4.13.2** — Solução 100% web sem infra local | Arquitetura unificada em container OCI para VPS de baixo custo (R$ 35/mês) | ✅ Conforme |

---

## 📁 Estrutura do Repositório

```text
CRQ-V-IA/
├── apps/
│   ├── api/                     # Backend REST em FastAPI
│   │   ├── core/                # Configurações, banco e segurança JWT
│   │   ├── engine/              # Motor CFQ 339/2025 e adaptador CNPJ
│   │   ├── models/              # Modelos relacionais SQLAlchemy
│   │   ├── routers/             # Rotas: auth, prospects, lists, exports, stats, audit
│   │   ├── schemas/             # Validações Pydantic
│   │   └── tests/               # Suíte de testes automatizados com pytest
│   └── web/
│       └── dist/index.html      # Frontend completo, responsivo e unificado (Tailwind + Lucide + Chart.js)
├── services/
│   └── ingest/                  # Scripts de carga, CNAEs CFQ e gerador do RS
├── docs/
│   ├── delivery/                # Documentação contratual: Manual, Onboarding, SLA e LGPD
│   ├── procurement/             # Matriz de requisitos, proposta comercial e habilitação
│   └── specs/                   # Especificações técnicas e SPEC-0018 de conformidade
├── infra/                       # Dockerfile e docker-compose.yml (PostGIS + FastAPI)
├── relatorio.md                 # Relatório detalhado do gap analysis inicial
└── run.ps1                      # Inicializador automático para Windows
```

---

## 🧪 Testes Automatizados

Para rodar a suíte completa de testes:
```bash
uv run --python apps/api/.venv pytest apps/api/tests/test_api.py -v
```
**Resultado:** `9 passed in 8.27s` (100% de sucesso).

---

## 📄 Licença

Distribuído sob a licença MIT. Consulte `LICENSE.md` para mais informações.
