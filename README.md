# CRQ-V-IA

Plataforma de prospecção e priorização de empresas potencialmente sujeitas à fiscalização do Conselho Regional de Química da 5ª Região (CRQ-V), com foco no Estado do Rio Grande do Sul.

## Objetivo

O projeto traduz os requisitos do Pregão Eletrônico nº 0005/2026, Processo CRQ-V nº 1729/2026, em uma solução web/cloud de baixo custo operacional, rastreável e aderente à LGPD. A aplicação deverá localizar e segmentar empresas, consultar situação cadastral de CNPJ, suportar pelo menos dois acessos simultâneos, operar sem infraestrutura local do CRQ-V e manter suporte durante toda a vigência contratual.

## Diferencial técnico

O núcleo de prospecção não depende de uma “caixa-preta” de IA. A primeira camada é determinística e auditável, usando CNAE, localização, porte, situação cadastral e regras regulatórias vigentes. A camada de IA serve para priorização, explicação e descoberta de indícios, nunca para produzir automaticamente uma conclusão fiscal ou jurídica.

O principal referencial regulatório de classificação é a Resolução CFQ nº 339/2025, que consolidou atividades econômicas sujeitas a registro em CRQ e passou a usar a CNAE como referência. O próprio texto da resolução deixa claro que o CNAE serve para identificar atividades a fiscalizar e que o enquadramento definitivo depende da confirmação da atividade efetivamente desenvolvida pela fiscalização.

## Arquitetura proposta

- Frontend: Next.js + TypeScript.
- API: FastAPI/Python.
- Banco: PostgreSQL + PostGIS + `pg_trgm`.
- ETL: Python + Polars/DuckDB para processamento mensal dos dados abertos do CNPJ.
- Armazenamento de artefatos: S3 compatível.
- Jobs: worker Python com fila persistida em PostgreSQL, sem obrigatoriedade de Redis.
- Deploy: containers OCI, Docker Compose para homologação e opção Kubernetes/PaaS para produção.
- Observabilidade: OpenTelemetry + logs estruturados + métricas.

## Fontes de dados previstas

1. Dados Abertos do CNPJ/RFB para descoberta e carga em lote.
2. API Consulta CNPJ do Conecta gov.br, quando o CRQ-V disponibilizar credenciais institucionais.
3. API Consulta CNPJ do Serpro como adaptador comercial opcional.
4. CNAE/CONCLA-IBGE.
5. Resolução CFQ nº 339/2025 e normas correlatas.
6. Base interna do CRQ-V, quando fornecida, para identificar empresas já registradas, fiscalizadas ou dispensadas.

## Estrutura

- `docs/specs/`: especificações funcionais e técnicas.
- `docs/procurement/`: matriz de aderência, aceite e habilitação.
- `docs/research/`: pesquisa e fontes oficiais.
- `docs/architecture/`: arquitetura, ADRs e modelo de dados.
- `apps/web/`: frontend.
- `apps/api/`: backend.
- `services/ingest/`: ingestão e atualização de bases.
- `infra/`: infraestrutura como código e execução local.

## Regra de ouro

Nenhum score gerado pela plataforma equivale a autuação, registro obrigatório ou conclusão jurídica. Ele é uma ferramenta de triagem para o Departamento de Fiscalização e Autuação. Toda indicação deverá exibir os fatores que a originaram e a fonte dos dados.

## Status

Fase inicial de especificação e arquitetura. O backlog completo está em `docs/specs/SPEC-0017-ROADMAP.md`.
