# Arquitetura do CRQ-V-IA

## 1. Princípios

1. **Explicabilidade antes de inteligência opaca.** O motor regulatório deve justificar por que uma empresa entrou na fila.
2. **Fonte oficial primeiro.** Receita Federal, CONCLA/IBGE, CFQ/CRQ e dados internos autorizados.
3. **Baixo custo.** O valor estimado do contrato exige arquitetura enxuta, sem clusters desnecessários.
4. **Cloud-native, mas portátil.** Containers OCI, PostgreSQL padrão e sem lock-in obrigatório.
5. **Privacidade por padrão.** Não coletar QSA ou dados pessoais que não sejam necessários à fiscalização.
6. **Auditoria completa.** Toda lista, score e exportação deve ser reproduzível pela versão da regra e da base.

## 2. Componentes

### `apps/web`

Interface web para fiscais e administradores.

Principais telas:

- Dashboard.
- Busca/prospecção.
- Perfil de empresa.
- Mapa/lista por município.
- Filas de fiscalização.
- Listas salvas.
- Exportações.
- Administração.
- Auditoria.

### `apps/api`

API HTTP REST responsável por autenticação, busca, filtros, score, exportações, auditoria e integrações.

### `services/ingest`

Pipeline que baixa/processa dados abertos, valida schema, filtra RS, normaliza e publica versão nova sem indisponibilidade.

### PostgreSQL

Extensões:

- `postgis` para recursos geográficos.
- `pg_trgm` para busca textual aproximada.
- `unaccent` para nomes empresariais.

### S3 compatível

Armazena arquivos de importação, relatórios e exports temporários. Dados com prazo de retenção configurável.

## 3. Fluxo principal

1. Job mensal detecta nova competência de dados da RFB.
2. Arquivos são baixados e validados por checksum/tamanho/schema.
3. DuckDB/Polars processa empresas e estabelecimentos.
4. Filtro `UF=RS` reduz volume cedo.
5. Dados são normalizados em staging.
6. Regras regulatórias versionadas classificam CNAEs.
7. Score de prospecção é calculado.
8. Nova versão é publicada atomicamente.
9. Usuários pesquisam e criam listas.
10. Para empresas selecionadas, a API pode realizar verificação on-demand via Conecta gov.br/Serpro.
11. Cada ação relevante é registrada no audit log.

## 4. Alta disponibilidade compatível com o orçamento

MVP:

- 1 instância app com restart automático.
- PostgreSQL gerenciado com backup diário.
- Object storage gerenciado.
- Health checks externos.

Produção reforçada, se o preço permitir:

- 2 réplicas do app.
- Load balancer.
- PostgreSQL com failover gerenciado.

O software não deve exigir que o CRQ-V compre servidores, licenças de banco ou appliance local.

## 5. Segurança

- TLS 1.2+.
- Cookies `HttpOnly`, `Secure`, `SameSite=Lax/Strict`.
- Senhas com Argon2id.
- MFA para administradores.
- RBAC por tenant.
- Rate limit de autenticação.
- Proteção CSRF quando aplicável.
- Logs sem secrets.
- Segredos em secret manager/environment protegida.
- SBOM e varredura de dependências na CI.
- Backup criptografado.

## 6. Multi-tenant

O produto deve suportar multi-tenant desde o modelo de dados, mesmo que o primeiro cliente seja o CRQ-V. Isso permite reaproveitar a solução em outros CRQs sem misturar dados.

Todas as tabelas de negócio específicas do cliente carregam `tenant_id` e políticas de autorização na aplicação. Para uma implantação exclusiva, um único tenant é criado.
