# SPEC-0005 — IA e ranking explicável

## Objetivo

Aumentar a produtividade da fiscalização sem delegar à máquina uma decisão regulatória.

## Fase 1 — Heurística determinística

Usar apenas sinais objetivos e pesos configuráveis. Deve ser a versão inicial de produção.

## Fase 2 — Aprendizado supervisionado opcional

Somente após o CRQ-V fornecer histórico com desfechos confiáveis. Possíveis modelos:

- Logistic Regression.
- Gradient Boosted Trees.
- Learning-to-Rank.

## Regras de governança

- Dataset de treino documentado.
- Sem atributos sensíveis.
- Separação temporal treino/teste.
- Métricas por município/porte/setor para detectar viés operacional.
- Feature importance/SHAP disponível para auditoria técnica.
- Modelo nunca substitui regra normativa.
- Score ML separado do score regulatório.

## Fase 3 — LLM opcional

LLM pode gerar resumo de fatores já conhecidos, nunca inventar fatos ou classificar empresa sem evidência estruturada.

Prompt deve receber dados minimizados e não deve incluir dados pessoais sem necessidade.
