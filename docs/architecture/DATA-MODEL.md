# Modelo de dados lógico

## Tabelas principais

### `company`

- `id`
- `cnpj_base`
- `legal_name`
- `legal_nature_code`
- `company_size_code`
- `capital_social`
- `rfb_source_version`

### `establishment`

- `id`
- `company_id`
- `cnpj`
- `branch_type`
- `trade_name`
- `registration_status_code`
- `registration_status_date`
- `registration_status_reason`
- `opening_date`
- `primary_cnae`
- `secondary_cnaes[]`
- `street_type`
- `street_name`
- `number`
- `complement`
- `district`
- `postal_code`
- `state`
- `municipality_code`
- `municipality_name`
- `phone_public`
- `email_public`
- `source_updated_at`

### `cnae`

- `code`
- `description`
- `section`
- `division`
- `group_code`
- `class_code`
- `subclass_code`
- `ibge_version`

### `regulatory_rule`

- `id`
- `rule_set_version`
- `source_norm`
- `cnae_pattern`
- `scope_type` (`basic`, `service`, `support`, `review`)
- `base_weight`
- `rationale`
- `effective_from`
- `effective_to`

### `prospect_score`

- `establishment_id`
- `rule_set_version`
- `score`
- `tier`
- `factors_json`
- `generated_at`

### `tenant_company_state`

Informações próprias do CRQ-V, separadas da base pública:

- `tenant_id`
- `establishment_id`
- `crq_status` (`unknown`, `registered`, `not_registered`, `exempt`, `under_review`)
- `last_inspection_at`
- `notes`
- `source`

### `saved_list`

- `tenant_id`
- `owner_user_id`
- `name`
- `query_json`
- `created_at`

### `saved_list_item`

- `saved_list_id`
- `establishment_id`
- `status`
- `priority`
- `assigned_to`
- `notes`

### `cnpj_verification`

- `establishment_id`
- `provider`
- `verified_at`
- `status_code`
- `status_text`
- `payload_hash`
- `raw_payload_uri` opcional com retenção curta

### `audit_event`

- `tenant_id`
- `actor_user_id`
- `action`
- `entity_type`
- `entity_id`
- `request_id`
- `metadata_json`
- `created_at`

## Dados deliberadamente não obrigatórios

O QSA não é necessário ao escopo mínimo. Ele deve permanecer desabilitado por padrão. Se uma necessidade fiscal específica justificar seu uso, deve existir uma avaliação de finalidade, base legal, minimização e retenção antes de habilitar a ingestão.
