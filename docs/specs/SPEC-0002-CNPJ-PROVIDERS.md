# SPEC-0002 — Situação cadastral e provedores CNPJ

## Objetivo

Permitir consulta confiável da situação cadastral de empresas e deixar claro o grau de atualidade da informação.

## Estratégia em camadas

### Camada 1 — Dados Abertos da RFB

Usada na prospecção massiva. Cada registro exibe a competência e a data da fonte.

### Camada 2 — Conecta gov.br

Adaptador preferencial para consulta on-demand quando o CRQ-V fornecer credenciais e autorizações institucionais.

### Camada 3 — Serpro comercial

Adaptador opcional se a empresa contratada decidir assumir a contratação e o custo da API.

## Interface de provider

```text
CnpjProvider.verify(cnpj, actor_context) -> VerificationResult
```

`VerificationResult` deve conter:

- `cnpj`
- `status_code`
- `status_text`
- `status_date`
- `reason`
- `source`
- `verified_at`
- `raw_hash`

## Regras

- Nunca “raspar” página protegida por captcha como backend oficial.
- Cachear consultas on-demand por período configurável.
- Mostrar fonte e timestamp no frontend.
- Em falha do provider online, manter informação da base aberta e marcar como “não confirmada em tempo real”.
- Não bloquear a busca massiva por indisponibilidade do provider online.
