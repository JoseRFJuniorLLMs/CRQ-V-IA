# SPEC-0006 — Geografia, cobertura e roteiros

## Escopo mínimo

Filtros por município e agrupamentos territoriais do RS.

## Recursos adicionais

- Mapa por município.
- Heatmap de quantidade de prospects.
- Contagem por CNAE e faixa de score.
- Agrupamento de empresas por proximidade quando latitude/longitude estiver disponível.

## Geocodificação

Não é requisito obrigatório do certame. Se usada:

- Preferir endereço empresarial público.
- Guardar `geocode_source`, `confidence` e data.
- Não depender de geocoding para funcionamento da busca principal.

## Roteiros

Roteirização é feature opcional. Não deve ser entregue como “otimização automática de fiscalização” sem confirmação humana. A saída é sugestão de sequência de visitas.
