# SPEC-0003 — Motor regulatório CNAE/CFQ

## Objetivo

Transformar a legislação de referência em regras versionadas, legíveis, auditáveis e atualizáveis.

## Norma base

Resolução CFQ nº 339/2025 e seu Anexo I.

## Modelo

Uma regra não declara que a empresa “está irregular”. Ela indica que a atividade registrada no CNPJ corresponde a uma atividade potencialmente sujeita à fiscalização segundo a norma.

## Classificação

- `DIRECT_PRIMARY`: CNAE principal enquadrado em regra de atividade básica/serviço.
- `DIRECT_SECONDARY`: CNAE secundário enquadrado.
- `SUPPORT_ACTIVITY`: indício de atividade de apoio que exige revisão humana.
- `TEXT_REVIEW`: objeto/descrição complementar requer análise humana, se base interna fornecer texto.
- `NOT_MATCHED`: sem correspondência conhecida.

## Score base recomendado

- CNAE principal direto: +60.
- CNAE secundário direto: +35.
- Mais de um CNAE relevante: +10.
- Empresa ativa: +10.
- Empresa aberta nos últimos 24 meses: +8.
- Nunca vista na base interna CRQ-V: +10.
- Já registrada/regular: reduzir ou excluir conforme configuração.

O score é configurável por tenant. Nenhum valor deve ser apresentado como probabilidade jurídica.

## Explicação

Toda classificação deve retornar:

```json
{
  "rule_set": "CFQ-339-2025:v1",
  "matched_cnaes": ["20.61-4"],
  "factors": [
    "CNAE principal relacionado no Anexo I",
    "Estabelecimento ativo no RS"
  ],
  "review_required": true
}
```

## Atualização normativa

Nova resolução => novo `rule_set_version`, nunca sobrescrever a versão histórica. Listas exportadas devem manter a versão usada na geração.
