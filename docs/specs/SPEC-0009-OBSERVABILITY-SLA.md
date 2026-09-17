# SPEC-0009 — Disponibilidade, observabilidade e SLA interno

## SLOs internos

- Disponibilidade mensal: 99,5%.
- P95 API busca: < 1,5 s.
- P95 login: < 1 s, excluindo IdP externo.
- Erro HTTP 5xx: < 1% em janela mensal.

## Monitoramento

- `/health/live`
- `/health/ready`
- métricas de latência/erros
- fila de jobs
- idade da base RFB
- última importação bem-sucedida
- disponibilidade de providers CNPJ

## Alertas

- aplicação fora do ar > 5 min;
- importação mensal falhou;
- backup não executado;
- provider CNPJ com falha persistente;
- uso de disco/banco acima do limite.

## Incidentes

Cada incidente possui:

- início/fim;
- impacto;
- causa;
- ações corretivas;
- comunicação ao fiscal do contrato, quando aplicável.
