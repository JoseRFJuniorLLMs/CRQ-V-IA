# SPEC-0010 — LGPD e segurança

## Objetivo

Atender às obrigações do Termo de Referência e reduzir o tratamento ao estritamente necessário.

## Controles

### Minimização

- QSA desabilitado por padrão.
- Não coletar CPF.
- Não coletar dados de redes sociais.
- Endereços tratados são endereços empresariais do estabelecimento.

### Controle de acesso

- RBAC.
- menor privilégio.
- MFA administrativo.
- logs de alteração/exportação.

### Criptografia

- TLS em trânsito.
- criptografia de volumes/backups.
- secrets fora do código.

### Retenção

- Dados públicos empresariais: enquanto necessários à finalidade contratual e conforme política do controlador.
- Logs: prazo configurável.
- Exports: expiração automática.
- Payload bruto de consulta on-demand: retenção curta ou somente hash, salvo necessidade operacional.

### Incidente

Fluxo:

1. detectar;
2. conter;
3. preservar evidência;
4. classificar dados afetados;
5. comunicar CRQ-V sem demora injustificada;
6. apoiar avaliação de obrigações perante ANPD/titulares;
7. documentar pós-incidente.

## Desenvolvimento seguro

- SAST.
- dependency scanning.
- secret scanning.
- SBOM CycloneDX/SPDX.
- revisão de permissões.
- testes OWASP Top 10.
