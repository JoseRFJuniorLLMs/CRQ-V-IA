# SPEC-0000 — Produto e escopo

## Objetivo

Entregar uma plataforma web de prospecção empresarial para o Departamento de Fiscalização e Autuação do CRQ-V, capaz de localizar, filtrar, priorizar e organizar empresas do Rio Grande do Sul com potencial de atuação na área da Química.

## Personas

### Fiscal

Pesquisa empresas, aplica filtros, examina fatores de risco, verifica CNPJ, salva listas e exporta resultados.

### Coordenador de fiscalização

Define critérios, distribui listas, acompanha produtividade, revisa score e configura regras de priorização.

### Administrador

Gerencia usuários, integrações, fontes, parâmetros, logs e retenção.

## Escopo MVP obrigatório

1. Login seguro.
2. Pelo menos 2 acessos simultâneos.
3. Busca por empresa/CNPJ.
4. Filtros por CNAE/setor, município/região e porte.
5. Situação cadastral do CNPJ.
6. Regras de potencial químico.
7. Lista de resultados paginada.
8. Perfil da empresa com explicação da seleção.
9. Listas salvas.
10. Exportação CSV/XLSX.
11. Auditoria.
12. Suporte e observabilidade.
13. LGPD.

## Escopo competitivo recomendado

- Mapa e agrupamento por município.
- Score explicável de prospecção.
- Prioridade por combinação de CNAE principal/secundário, situação, tempo de abertura e porte.
- Importação da base interna do CRQ-V para evitar retrabalho com empresas já regularizadas.
- Consulta on-demand à API oficial CNPJ.
- Relatório de cobertura por município e setor.
- Alertas de novas empresas na competência mensal da Receita Federal.
- Comparação “nova competência x competência anterior”.

## Fora de escopo inicial

- Autuação automática.
- Decisão jurídica automatizada.
- Robôs que contornem captcha da Receita.
- Coleta indiscriminada de dados de sócios.
- Scraping agressivo de redes sociais.
