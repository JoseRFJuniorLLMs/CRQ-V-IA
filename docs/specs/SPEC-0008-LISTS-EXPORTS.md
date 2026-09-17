# SPEC-0008 — Listas, workflow e exportação

## Listas salvas

Usuário deve poder:

- criar lista a partir de consulta;
- adicionar/remover empresa;
- definir prioridade;
- atribuir responsável;
- registrar nota operacional;
- marcar estado de triagem.

## Estados sugeridos

`NEW`, `REVIEWING`, `SELECTED`, `DISMISSED`, `EXPORTED`, `INSPECTED`.

## Exportações

Formatos:

- CSV UTF-8.
- XLSX.
- PDF resumido opcional.

Campos mínimos:

- CNPJ.
- Razão social.
- Nome fantasia.
- Município.
- CNAE principal/secundários relevantes.
- Porte.
- Situação cadastral.
- Score.
- Fatores.
- Fonte e data.
- Regra normativa/versionamento.

Toda exportação deve registrar um evento de auditoria.
