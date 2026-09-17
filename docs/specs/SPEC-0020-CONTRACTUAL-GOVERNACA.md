Sim. Fiz uma segunda auditoria mais ampla, desta vez cruzando **quatro camadas diferentes**: o edital e anexos do CRQ-V, a árvore atual do `CRQ-V-IA`, softwares reais de prospecção empresarial, e documentos oficiais de contratação de software/SaaS do setor público.

O resultado foi útil: **há lacunas que não apareceram na primeira auditoria**. Não são apenas “mais funcionalidades bonitas”. Algumas afetam rastreabilidade, encerramento contratual, governança de dados, auditoria, atualização normativa e capacidade de provar que o produto entregue continua sendo exatamente o contratado.

E encontrei logo uma pequena joia burocrática: o próprio edital diz que existem **quatro anexos**, incluindo “ANEXO IV – Modelos de Referência”.  Porém, hoje, a página oficial do Pregão 0005/2026 publica somente Edital, Anexo I, Anexo II, Anexo III e publicação no DOU. O Anexo IV não aparece. ([CRQV][1]) Isso merece entrar formalmente no projeto como **inconsistência documental pendente de esclarecimento**, não como conteúdo que vamos inventar.

## O que a pesquisa externa revelou

Os concorrentes confirmam que nossa base funcional está correta, mas mostram alguns recursos operacionais que ainda não modelamos suficientemente. A Econodata permite filtros hierárquicos de localização, CNAE principal/secundário, matriz/filial, situação cadastral, abertura, capital, natureza jurídica, Simples, MEI, busca em massa de CNPJs, filtros negativos e tags. ([Econodata][2]) O EmpresAqui trabalha também com importação de clientes, subusuários, gestão de usuários, atualização mensal e filtros por CNAE, localização, porte, regime e situação. ([EmpresAqui][3])

O ponto interessante não é transformar o CRQ-V-IA numa ferramenta comercial cheia de contatos de vendedores. Isso seria exatamente o tipo de escopo inflado que consegue transformar um contrato de R$ 4.800 em uma plataforma da NASA. O que vale importar desses produtos são os mecanismos de **segmentação, exclusão, atualização, histórico, trabalho em lote e qualidade de dados**.

Também usei a Portaria SGD/MGI nº 5.950/2023 como **benchmark federal de contratação de software e SaaS**, não como obrigação automática do CRQ-V. Ela se aplica formalmente ao SISP do Executivo Federal. Ainda assim, é uma excelente referência de engenharia contratual para SaaS público: aborda propriedade dos dados e logs, portabilidade, estratégia de saída, regiões de armazenamento, isolamento, criptografia, suporte, treinamento e critérios objetivos de aceite. ([Serviços e Informações do Brasil][4])

### Lacunas que eu acrescentaria ao CRQ-V-IA

| Área nova                                      | Situação atual                       | O que acrescentar                                                                         | Prioridade |
| ---------------------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------------- | ---------: |
| **Manifesto do edital**                        | Não existe entidade própria          | Registrar documento, versão, data, SHA-256, URL, cláusula, página e se foi substituído    |     **P0** |
| **Rastreabilidade requisito → código → teste** | Matriz aponta implementação proposta | `requirement_id`, cláusula, arquivo de código, teste, evidência, commit e status          |     **P0** |
| **Release contratual**                         | Não modelada                         | versão, `commit_sha`, build, data, aprovador, mudança, migration e rollback               |     **P0** |
| **Controle de mudanças**                       | Praticamente ausente                 | aprovação formal para mudança funcional relevante e histórico                             |     **P0** |
| **Snapshot de fiscalização**                   | Lista guarda estado atual            | congelar versão RFB, versão de regra, score e filtros usados na criação                   |     **P0** |
| **Histórico cadastral**                        | Guarda estado atual                  | registrar mudanças de CNAE, situação, porte, nome, abertura/baixa etc. entre competências |     **P0** |
| **Eventos de mudança**                         | Ausente                              | `first_seen`, `last_seen`, `changed_fields`, competência anterior/nova                    |     **P0** |
| **Governança da regra CFQ**                    | Versionamento simples                | artigo/item/origem, hash da norma, vigência, revogação, revisão humana, aprovação         |     **P0** |
| **Trilha de auditoria resistente a alteração** | `audit_event` básico                 | append-only, hash, resultado, `before_hash`, `after_hash`, IP/contexto e correlação       |     **P0** |
| **Incidente LGPD completo**                    | Fluxo genérico                       | campos exigidos pela ANPD + retenção mínima pertinente                                    |     **P0** |
| **Portabilidade/exit real**                    | Conceitual                           | exportação completa do CRQ-V, logs, listas, regras e notas em formatos abertos            |     **P0** |
| **Registro de dependências externas**          | Não existe                           | cloud/provider, dados processados, região, custo, finalidade e estratégia de saída        |     **P0** |
| **Data residency**                             | Não definida                         | registrar região primária e backup e impedir migração silenciosa                          |     **P1** |
| **Importação da base CRQ-V**                   | Citada como recurso                  | importador CSV/XLSX, dry-run, mapeamento, validação, rejeições e deduplicação             |     **P0** |
| **Supressão/exclusão**                         | Parcial                              | não prospectar novamente empresas dispensadas, já tratadas ou recentemente fiscalizadas   |     **P0** |
| **Matriz/filial**                              | Campo existe no modelo               | filtro explícito e agrupamento pelo CNPJ raiz                                             |     **P1** |
| **Simples/MEI**                                | Ausentes do modelo atual             | optante Simples, SIMEI/MEI e datas relevantes                                             |     **P1** |
| **Situação especial RFB**                      | Ausente                              | recuperação judicial, liquidação etc. + data da situação especial                         |     **P1** |
| **Busca em massa por CNPJ**                    | Não formalizada                      | colar/importar lista e cruzar milhares de CNPJs com a base                                |     **P1** |
| **Operações em massa**                         | Listas simples                       | atribuir, classificar, excluir, mudar status e exportar N empresas de uma vez             |     **P1** |
| **Qualidade da base**                          | Métricas de ETL dispersas            | dashboard de freshness, rejeições, cobertura CNAE, dados ausentes e erros                 |     **P1** |
| **Janela de manutenção**                       | Não definida                         | aviso, duração, manutenção programada/emergencial e impacto no uptime                     |     **P1** |
| **SLA mensurável**                             | Temos 99,5% interno                  | fórmula, fonte de medição, exclusões e período de apuração                                |     **P1** |
| **Suporte com resolução**                      | Só tempo de resposta                 | `opened`, `ack`, `resolved`, `closed`, restoration time e violação de SLA                 |     **P1** |
| **Compatibilidade browser**                    | “navegador moderno”                  | matriz Chrome/Edge/Firefox/Safari suportados                                              |     **P1** |
| **Acessibilidade comprovada**                  | WCAG 2.1 AA especificada             | testes automatizados + teclado + leitor + relatório de homologação                        |     **P1** |
| **Dicionário de exportação**                   | CSV/XLSX definidos                   | schema versionado, definição de cada coluna e formato aberto                              |     **P1** |
| **Tela de versão do sistema**                  | Ausente                              | versão app, commit, competência RFB, ruleset e última carga                               |     **P1** |
| **Budget de providers**                        | Não existe                           | chamadas, cache hit, custo acumulado e teto mensal                                        |     **P1** |
| **Vulnerabilidades em produção**               | SAST previsto                        | registro CVE, severidade, componente, prazo de correção e exceção                         |     **P1** |
| **Alertas de competência**                     | Apenas recomendado                   | empresas novas/alteradas que passaram a casar com pesquisa salva                          |     **P2** |

### 1. A lacuna mais séria que encontrei é a reprodutibilidade histórica

Hoje temos `saved_list`, `prospect_score`, `rule_set_version` e versão RFB, o que é um bom começo.  Mas ainda falta garantir matematicamente que uma lista criada em, por exemplo, **10/03/2027** possa ser reconstruída posteriormente exatamente como era naquele dia.

Isso importa muito para fiscalização.

Uma empresa pode ter:

`CNAE A → CNAE B`

`ATIVA → BAIXADA`

`porte ME → EPP`

ou uma regra CFQ pode mudar.

Ferramentas empresariais maduras guardam histórico dessas alterações. A BigDataCorp, por exemplo, possui dataset específico para histórico de mudanças de razão social, regime tributário e CNAE. ([BigDataCorp Docs][5])

Eu acrescentaria:

```text
prospect_snapshot

id
tenant_id
establishment_id

source_version
rule_set_version
score_version

registration_status_at_snapshot
primary_cnae_at_snapshot
company_size_at_snapshot

score_at_snapshot
factors_json

created_at
created_by
```

Assim o CRQ-V consegue demonstrar:

> “Na data em que essa empresa foi selecionada, esses eram os dados cadastrais e essa era a regra utilizada.”

Isso é muito melhor do que recalcular tudo dois anos depois com a base atual e descobrir que o passado sofreu atualização automática. Humanos já reescrevem memória muito bem sem ajuda do PostgreSQL.

## 2. O motor regulatório precisa de governança de norma, não somente versão

Hoje `regulatory_rule` guarda fonte, padrão CNAE, peso, justificativa e vigência.

Eu ampliaria para:

```text
source_document
source_url
source_sha256

norm_number
norm_article
norm_annex
norm_item

published_at
effective_from
effective_to

status:
DRAFT
REVIEWED
ACTIVE
RETIRED
SUPERSEDED

created_by
reviewed_by
approved_by

approval_at
change_reason
superseded_by
```

Isso evita uma situação particularmente divertida: uma IA editar silenciosamente o peso de um CNAE e seis meses depois ninguém saber por que uma fábrica apareceu na fila de fiscalização.

## 3. Há campos oficiais da Receita que ainda não estamos aproveitando

O modelo atual já traz a maior parte dos dados realmente necessários: CNPJ, matriz/filial, razão social, fantasia, situação, abertura, CNAEs, endereço, telefone, e-mail, capital e porte.

Mas a própria API oficial CNPJ oferece também **situação especial e data da situação especial**, e nos serviços mais completos informações sobre **Simples e MEI/SIMEI**. ([Serviços e Informações do Brasil][6])

Eu incluiria no estabelecimento/empresa:

```text
simples_optant
simples_start_date
simples_end_date

simei_optant
simei_start_date
simei_end_date

special_status
special_status_date
```

Não incluiria QSA por padrão. Nossa decisão atual de deixar quadro societário fora do MVP continua correta. A API oferece isso, mas “estar disponível” não significa “devemos colecionar tudo como um esquilo digital”. A LGPD e o objetivo contratual recomendam minimização.

## 4. Precisamos de uma verdadeira lista de supressão

Econodata possui filtros negativos e exclusão por tags. ([Econodata][2]) Para vendas isso evita prospectar a mesma empresa. Para o CRQ-V isso é ainda mais importante.

Exemplos:

```text
REGISTERED
EXEMPT
RECENTLY_INSPECTED
OUT_OF_SCOPE
DUPLICATE
FALSE_POSITIVE
DO_NOT_REPROSPECT
```

E a tabela deveria guardar:

```text
reason_code
reason_text
created_by
created_at
expires_at
source
evidence_ref
```

Isso evita que toda nova competência da Receita coloque novamente na fila uma empresa que um fiscal já analisou e descartou justificadamente.

## 5. Importação da base interna do CRQ-V merece virar requisito formal

Nosso README menciona integração futura com a base interna e o modelo já tem `tenant_company_state`.

Mas falta uma especificação de **bulk import segura**.

Produtos concorrentes já oferecem importação de clientes e gestão das bases existentes. ([EmpresAqui][7]) Para nosso caso, isso deveria ser:

```text
upload
→ detectar colunas
→ mapear
→ validar CNPJ
→ normalizar
→ procurar duplicatas
→ dry-run
→ relatório de erros
→ confirmação humana
→ importação
→ audit_event
```

Isso é P0 na minha leitura, porque sem a base do CRQ-V podemos encontrar empresas novas, mas não conseguimos evitar retrabalho sobre empresas que a autarquia já conhece.

## 6. Propriedade dos dados e saída contratual estão fracas

O benchmark oficial do Governo Federal para SaaS recomenda que o contrato deixe clara a propriedade da Administração sobre dados, backups e logs, defina portabilidade, estratégia de saída e limite o uso secundário das informações, inclusive para treinamento ou otimização de IA. ([Serviços e Informações do Brasil][4])

Outros termos de referência públicos seguem a mesma lógica. Um TR do DER-MG, por exemplo, exige extração integral sem custo adicional e exportação em SQL, CSV, JSON ou XML ao longo do contrato e após seu encerramento. ([DER MG][8]) Outro edital do Cofen exigiu disponibilização integral, migração no encerramento e backups periódicos. ([Cofen][9])

Nosso `CONTRACT-EXIT` deveria portanto produzir não apenas “apagar dados”, mas antes:

```text
CRQV-export-YYYYMMDD/
    companies.csv
    lists.csv
    list_items.csv
    inspections.csv
    notes.csv
    audit.csv
    rules.json
    saved_searches.json
    metadata.json
    checksums.sha256
```

E o `metadata.json` deve dizer schema, versão, encoding, datas e versões utilizadas.

A ePING recomenda que CSV venha acompanhado do leiaute dos campos, e adota padrões abertos de intercâmbio. ([Eping][10]) Portanto eu adicionaria também um **data dictionary versionado**.

## 7. A auditoria precisa ser resistente a adulteração

Hoje nosso `audit_event` tem ator, ação, entidade, `request_id`, metadata e data.

É bom, mas para um sistema que vai apoiar fiscalização eu reforçaria:

```text
event_id
tenant_id
actor_id
actor_role

action
entity_type
entity_id

request_id
correlation_id

result
reason

before_hash
after_hash

event_hash
previous_event_hash

ip_address
user_agent

created_at
```

A aplicação jamais deveria fazer `UPDATE` ou `DELETE` normal nesses eventos.

Não é exigência literal do Pregão 0005/2026, mas licitações públicas de software frequentemente tratam logs como instrumento de auditoria. Um TR federal, por exemplo, exige solução com características que permitam auditoria e acesso a logs de eventos; também explicita proteção contra CSRF, XSS e injection. ([Serviços e Informações do Brasil][11])

## 8. Incidente LGPD tem campos que ainda não modelamos

Aqui encontramos um ponto normativo concreto.

A ANPD exige que o controlador mantenha registro de incidentes de segurança envolvendo dados pessoais, inclusive daqueles não comunicados, **por no mínimo cinco anos**. O registro deve conter data de conhecimento, circunstâncias, natureza/categoria dos dados, titulares afetados, avaliação de risco, medidas de mitigação, comunicação e, quando não houver comunicação, a justificativa. ([Serviços e Informações do Brasil][12])

Portanto `incident` precisa incluir, quando envolver dados pessoais:

```text
personal_data_incident
awareness_at
data_categories
estimated_subjects
risk_assessment
possible_damage
mitigation_actions
anpd_notified
anpd_notification_at
subjects_notified
non_notification_reason
retention_until
```

Isso merece entrar na SPEC, não ficar escondido num runbook.

## 9. Manutenção e mudança de versão precisam de política

O TR do CRQ-V exige funcionamento durante a vigência e manutenção dos acessos e suporte. 

Além disso, a minuta proíbe alteração não prevista sem consentimento prévio do CRQ-V. Isso torna **change management** importante.

Outros contratos públicos especificam explicitamente aviso prévio de manutenção, horário da janela e procedimento para exceções. Um TR federal, por exemplo, previa comunicação com 72 horas de antecedência para manutenção preventiva e atualização. ([Serviços e Informações do Brasil][11])

Não copiaria “72 horas” para nosso contrato como obrigação, porque o CRQ-V não estabeleceu isso. Mas criaria internamente:

```text
release
change_request
maintenance_window

release.version
release.commit_sha
release.image_digest
release.database_revision

change.type
change.reason
change.risk
change.approval_required
change.approval_reference

rollback_plan
maintenance_start
maintenance_end
users_notified_at
```

## 10. Nosso SLA de 99,5% está incompleto

Temos meta de disponibilidade e alertas.

Falta definir **como se calcula**.

Por exemplo:

```text
availability =
(total_minutes - unavailable_minutes)
/
(total_minutes - excluded_maintenance_minutes)
```

E determinar:

```text
measurement_source
measurement_timezone
scheduled_maintenance
emergency_maintenance
provider_dependency
partial_outage
start_detection
end_detection
```

Sem isso, “99,5%” é só um número bonito com gravata.

## 11. Falta uma matriz real de browsers e ambiente

A nossa matriz diz “navegador moderno”.  Isso é vago.

Outros TRs públicos chegam a identificar Chrome, Edge, Firefox e Safari como browsers suportados. ([Serviços e Informações do Brasil][11])

Eu definiria oficialmente:

```text
Chrome: current + previous
Edge: current + previous
Firefox: current + previous
Safari: current + previous
JavaScript: required
Resolution minimum supported
Tablet breakpoint
Timezone: America/Sao_Paulo
Locale: pt-BR
Encoding: UTF-8
```

## 12. Acessibilidade: já temos a intenção, falta evidência

Nossa SPEC já define **WCAG 2.1 AA**, teclado, contraste e labels.

A pesquisa em padrões governamentais sugere completar isso com **eMAG** e uma rotina de homologação. O próprio material de boas práticas do Governo recomenda que a empresa entregue relatório gerado por ferramenta automática e que a fiscalização valide os resultados. ([Serviços e Informações do Brasil][13])

Então incluiria no CI/E2E:

```text
axe-core
Playwright accessibility checks
keyboard-only navigation
focus order
accessible names
contrast
screen-reader smoke test
```

Não precisa transformar o produto em uma tese sobre ARIA. Precisa demonstrar que pessoas conseguem usá-lo.

## 13. Precisamos controlar o custo das APIs

Esse ponto nasce diretamente da realidade econômica do edital.

O TR final estima **R$ 4.800 pelos 12 meses**, R$ 400 mensais. 

Então qualquer provider pago precisa ter:

```text
provider_usage

provider
request_count
cache_hits
cache_misses
cost_estimate
monthly_budget
budget_threshold
blocked_after_limit
period
```

Isso protege justamente a arquitetura enxuta que já escolhemos.

## 14. Um dashboard de qualidade dos dados seria mais útil que vários recursos de IA

Criaria uma área administrativa mostrando:

```text
Competência RFB atual
Data da última ingestão
Total estabelecimentos RS
Total ativos
CNPJs rejeitados
CNAEs desconhecidos
Registros sem município
Registros sem porte
Rules sem match
Última verificação provider
Provider error rate
Import duration
```

Essa tela vale mais operacionalmente que enfiar um LLM no meio da fiscalização só porque 2026 aparentemente exige que todo botão tenha uma IA morando atrás dele.

## 15. Há recursos dos concorrentes que eu NÃO colocaria agora

Dos concorrentes encontrei decisores, contatos pessoais, LinkedIn, saúde financeira, dívidas, faturamento presumido, NCM, organograma, nível de atividade estimado e filtros de presença digital. ([Econodata][2])

Para o CRQ-V:

**Simples/MEI, matriz/filial, situação especial, histórico cadastral e filtros negativos** têm utilidade clara.

**QSA, decisores, redes sociais, faturamento estimado, dívidas e organogramas** não deveriam entrar no MVP sem uma necessidade formal do CRQ-V.

**NCM** é interessante tecnicamente porque pode ajudar a detectar atividade com produtos químicos que o CNAE sozinho não captura, mas ele requer outra fonte de dados. Eu o deixaria como pesquisa P2.

**Busca por linguagem natural** também pode existir no futuro, traduzindo “indústrias químicas pequenas abertas nos últimos 2 anos perto de Caxias” para filtros estruturados, mas não deve atrasar o produto obrigatório.

---

# A conclusão da auditoria mudou

Antes eu dizia: **não crie outra SPEC, fortaleça a 0018**.

Depois desta pesquisa mais profunda, agora há conteúdo genuinamente novo suficiente para justificar **uma segunda SPEC**.

Eu separaria assim:

**`SPEC-0018-FULL-IMPLEMENTATION-COMPLIANCE.md`**
Implementa tudo aquilo que já sabíamos que precisava existir.

**`SPEC-0019-CONTRACTUAL-DATA-GOVERNANCE-HARDENING.md`**
Incorpora os novos achados desta auditoria recursiva:

> rastreabilidade documental, snapshots históricos, governança das regras CFQ, histórico cadastral, importação CRQ-V, supressões, propriedade e portabilidade dos dados, audit trail resistente a alteração, incidentes ANPD, change/release management, SLA mensurável, acessibilidade verificável, dependências externas, controle de custos e estratégia formal de saída.

Essa 0019 **não seria mais documentação repetida sobre o mesmo produto**. Ela cobre dimensões que nossas SPECs atuais realmente não tratam de forma suficiente.

E tem um achado que eu colocaria em **P0 imediatamente**: criar um `PROCUREMENT-MANIFEST` com hash e versão de cada documento oficial. O edital diz que existe Anexo IV, mas a página oficial atual não o publica.  ([CRQV][1]) Se amanhã aparecer uma retificação ou esse anexo surgir no site, o projeto precisa conseguir dizer exatamente **qual conjunto documental originou cada requisito e cada release**.

Isso transforma o CRQ-V-IA de “software que parece cumprir o edital” em **software capaz de demonstrar tecnicamente, historicamente e documentalmente por que cumpre o edital**. Para um sistema voltado à fiscalização pública, essa diferença é considerável.

[1]: https://crqv.org.br/licitacao/view/109/pregao-eletronico-00052026?utm_source=chatgpt.com "CRQ-V | PREGÃO ELETRÔNICO 0005/2026"
[2]: https://help.econodata.com.br/pt/article/como-funcionam-os-filtros-da-plataforma-x25v4a/?utm_source=chatgpt.com "Como funcionam os filtros da plataforma | Econodata"
[3]: https://www.empresaqui.com.br/?utm_source=chatgpt.com "Listas de Empresas Atualizadas | Prospecção B2B - EmpresAqui"
[4]: https://www.gov.br/governodigital/pt-br/contratacoes-de-tic/legislacao/modelo-de-contratacao-de-software-e-servicos-em-nuvem/vigentes/portaria-sgd-mgi-no-5-950-de-26-de-outubro-de-2023?utm_source=chatgpt.com "Portaria SGD/MGI nº 5.950, de 26 de outubro de 2023 — Governo Digital"
[5]: https://docs.bigdatacorp.com.br/plataforma/reference/empresas-historico-de-dados-basicos?utm_source=chatgpt.com "Histórico de Dados Básicos"
[6]: https://www.gov.br/conecta/catalogo/apis/consulta-cnpj/swagger_api_cnpj.md/swagger_view?utm_source=chatgpt.com "API Docs"
[7]: https://www.empresaqui.com.br/pesquisa-de-empresas?utm_source=chatgpt.com "Pesquisa de empresas: filtre por CNAE, região, porte e +!"
[8]: https://der.mg.gov.br/files/2704/-2301520-0000022026/36750/ANEXO-I-%E2%80%93-Termo-de-Referencia---SEI-132367654.pdf?preview=1&utm_source=chatgpt.com "SEI/GOVMG - 132367654 - Termo de Referência"
[9]: https://www.cofen.gov.br/wp-content/uploads/2021/11/Edital-de-Pregao-Eletronico-no-27-2021.pdf?utm_source=chatgpt.com "COMISSÃO DE LICITAÇÃO DO COFEN"
[10]: https://eping.governoeletronico.gov.br/?utm_source=chatgpt.com "Padrões de Interoperabilidade de Governo Eletrônico"
[11]: https://www.gov.br/gestao/pt-br/acesso-a-informacao/licitacoes-e-contratos/licitacoes-e-contratacoes-diretas/central-de-compras-seges/ate-2022/pregoes/2021/arquivos/pe-18-2021/02-18243288_termo_de_referencia___s_cont_c_d_exc__d_10024_19_.html?utm_source=chatgpt.com "SEI/ME - 18243288 - Termo de Referência - S Cont c/D Exc (D 10024/19)"
[12]: https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/documentos/rcis___anonimizado_final_ocultado_2_parte3.pdf?utm_source=chatgpt.com "IV  
DO PROCEDIMENTO REGISTRO DE INCIDENTES DE SEG"
[13]: https://www.gov.br/governodigitallogin/pt-br/acessibilidade-e-usuario/acessibilidade-digital/modelo-de-acessibilidade?utm_source=chatgpt.com "Modelo de Acessibilidade — Governo Digital"


# SPEC-0020 — Contractual Data Governance, Traceability and Operational Hardening

Status: REQUIRED
Priority: P0
Repository: JoseRFJuniorLLMs/CRQ-V-IA
Target branch: main

Depends on:
- SPEC-0000 through SPEC-0018
- ARCHITECTURE.md
- DATA-MODEL.md
- REQUIREMENTS-MATRIX.md
- HABILITATION-CHECKLIST.md
- official documents of Pregão Eletrônico CRQ-V nº 0005/2026
- Processo CRQ-V nº 1729/2026

Type:
Governance / Compliance / Data Integrity / Contractual Operations / Auditability

---

# 1. PURPOSE

This specification hardens CRQ-V-IA for actual contractual operation.

SPEC-0018 is responsible for transforming the repository into an executable product.

SPEC-0019 is responsible for ensuring that the executable product is:

- traceable;
- historically reproducible;
- auditable;
- contractually governable;
- capable of proving which data and rules produced each result;
- capable of surviving regulatory and cadastral changes;
- capable of importing and reconciling CRQ-V internal data;
- capable of controlled contractual exit;
- capable of producing evidence for inspection, audit and contract management.

This specification MUST NOT replace implementation required by SPEC-0018.

It adds governance and operational guarantees around that implementation.

---

# 2. PRINCIPLE

Every relevant result produced by CRQ-V-IA must answer:

1. Which source data were used?
2. Which source version was used?
3. Which regulatory rule was used?
4. Which rule version was used?
5. Which software version produced the result?
6. When was the result produced?
7. Who triggered or approved the action?
8. Can the same result be reconstructed later?

If any of these questions cannot be answered for a material fiscal prospecting action, traceability is incomplete.

---

# 3. PROCUREMENT MANIFEST

Create:

docs/procurement/PROCUREMENT-MANIFEST.yaml

The manifest SHALL register every official procurement document used as a source of requirements.

Schema:

procurement:
  id: CRQ-V-0005-2026
  process: 1729/2026

documents:
  - id:
    type:
    title:
    source_url:
    local_reference:
    publication_date:
    retrieved_at:
    sha256:
    version:
    supersedes:
    superseded_by:
    active:
    notes:

Document types:

- EDITAL
- TERMO_REFERENCIA
- PROPOSTA_MODELO
- CONTRATO_MINUTA
- ETP
- ANEXO
- RETIFICACAO
- ESCLARECIMENTO
- IMPUGNACAO
- RESPOSTA
- ATA
- OTHER

Never silently replace one document with another.

Every replacement or amendment SHALL create a new manifest entry.

---

# 4. MISSING PROCUREMENT DOCUMENTS

Create:

docs/procurement/MISSING-DOCUMENTS.md

Current known pending item:

- ANEXO IV — Modelos de Referência.

Do not invent its content.

Status values:

- MISSING
- REQUESTED
- RECEIVED
- SUPERSEDED
- NOT_APPLICABLE

Fields:

document
expected_source
detected_from
status
first_detected_at
last_checked_at
impact
action_required

A missing document SHALL prevent the project from claiming complete documentary verification.

---

# 5. REQUIREMENT TRACEABILITY

Upgrade REQUIREMENTS-MATRIX.md.

Every requirement SHALL have:

requirement_id
source_document
source_section
source_page
source_hash
requirement_text
classification
implementation_status
implementation_files
test_files
evidence_files
first_commit
last_verified_commit
acceptance_status
notes

Classification:

MANDATORY
CONTRACTUAL
SECURITY
LGPD
OPERATIONAL
INTERNAL_QUALITY
OPTIONAL
COMPETITIVE

Status:

NOT_STARTED
IMPLEMENTING
IMPLEMENTED
TESTED
ACCEPTED
BLOCKED

No requirement may be marked ACCEPTED without objective evidence.

---

# 6. SOFTWARE RELEASE TRACEABILITY

Create database entity:

software_release

Fields:

id
version
commit_sha
git_tag
build_id
container_image
container_digest
database_revision
ruleset_version
release_type
created_at
deployed_at
deployed_by
approved_by
environment
rollback_release_id
change_request_id
status

release_type:

MAJOR
MINOR
PATCH
HOTFIX
DATA_ONLY
RULESET_ONLY
SECURITY

status:

BUILT
TESTED
APPROVED
DEPLOYED
ROLLED_BACK
RETIRED

Every production deployment SHALL be linked to exactly one release.

---

# 7. CONTRACTUAL BASELINE RELEASE

Before contractual delivery, create an immutable release tag.

Example:

v1.0.0-crqv-contract

The release SHALL identify:

- commit SHA;
- database schema revision;
- ruleset version;
- RFB dataset competence;
- container digest;
- dependency lockfiles;
- migration set;
- acceptance report;
- security report.

The proposal and contracted functionality should be associated with this baseline.

---

# 8. CHANGE MANAGEMENT

Create entity:

change_request

Fields:

id
title
description
reason
change_type
requested_by
requested_at
risk_level
affects_contract
affects_data
affects_rules
affects_security
requires_crq_approval
approval_reference
approved_by
approved_at
release_id
rollback_plan
status

change_type:

BUGFIX
FEATURE
SECURITY
DATA
REGULATORY
INFRASTRUCTURE
CONFIGURATION

status:

DRAFT
REVIEW
APPROVED
REJECTED
IMPLEMENTED
DEPLOYED
ROLLED_BACK

Material contractual changes SHALL be traceable to approval.

---

# 9. MAINTENANCE WINDOW

Create:

maintenance_window

Fields:

id
type
reason
scheduled_start
scheduled_end
actual_start
actual_end
services_affected
expected_impact
users_notified_at
notification_channel
approved_by
incident_id
status

type:

PLANNED
EMERGENCY
SECURITY

Maintenance exclusions from availability calculations MUST be explicitly recorded.

---

# 10. HISTORICAL REPRODUCIBILITY

Current-state data are insufficient for fiscal traceability.

Create:

prospect_snapshot

Fields:

id
tenant_id
establishment_id

source_version
source_competence
rule_set_version
software_release_id

legal_name
trade_name
registration_status
registration_status_date
primary_cnae
secondary_cnaes_json
company_size
capital_social
municipality
address_hash

regulatory_score
operational_score
final_score
tier
factors_json

created_at
created_by
trigger_type

trigger_type:

SEARCH
LIST_ADD
EXPORT
MANUAL_SNAPSHOT
INSPECTION_SELECTION

Snapshots SHALL be immutable.

---

# 11. SAVED LIST SNAPSHOTS

Adding a company to a fiscal work list SHALL preserve the relevant state at that time.

saved_list_item SHALL reference:

prospect_snapshot_id

Do not reconstruct historical list state exclusively from current company records.

---

# 12. COMPANY CHANGE HISTORY

Create:

company_change_event

Fields:

id
establishment_id
source_version_from
source_version_to
detected_at
field_name
old_value
new_value
change_type

change_type:

CREATED
UPDATED
REMOVED
REACTIVATED

Track at least:

- razão social;
- nome fantasia;
- situação cadastral;
- data da situação;
- CNAE principal;
- CNAEs secundários;
- porte;
- capital social;
- município;
- endereço;
- matriz/filial;
- opção Simples;
- opção SIMEI;
- situação especial.

---

# 13. FIRST-SEEN AND LAST-SEEN

Company and establishment records SHALL include:

first_seen_source_version
last_seen_source_version
first_seen_at
last_seen_at

This enables queries such as:

"Empresas que surgiram na base no último mês."

and:

"Empresas que passaram a possuir CNAE relevante."

---

# 14. SIMPLES, MEI AND SPECIAL STATUS

Extend company/establishment models with:

simples_optant
simples_start_date
simples_end_date

simei_optant
simei_start_date
simei_end_date

special_status
special_status_date

Fields SHALL only be displayed when source data support them.

Missing data SHALL be represented as UNKNOWN, never guessed.

---

# 15. RFB SOURCE PROVENANCE

Every field imported from RFB SHALL be traceable to:

source_dataset
source_version
source_file
source_file_sha256
import_job_id
imported_at

Where practical, preserve file-level provenance rather than row-level raw payload duplication.

---

# 16. RULE GOVERNANCE

Upgrade regulatory_rule.

Fields:

id
rule_set_version

norm_type
norm_number
norm_year

source_document
source_url
source_sha256

article
paragraph
inciso
item
annex

cnae_pattern
scope_type

base_weight
rationale

published_at
effective_from
effective_to

status

created_by
created_at
reviewed_by
reviewed_at
approved_by
approved_at

change_reason
superseded_by

status:

DRAFT
REVIEWED
APPROVED
ACTIVE
RETIRED
SUPERSEDED

---

# 17. RULE SET

Create:

regulatory_rule_set

Fields:

id
version
name
description
source_summary
created_at
approved_at
approved_by
status
previous_version
release_id

Only ACTIVE rule sets may be used in production.

Changing weights or CNAE mappings SHALL create a new rule set version.

Do not mutate a production rule set in place.

---

# 18. RULE DIFF

Implement:

GET /api/v1/rulesets/{version}/diff/{other_version}

Return:

added_rules
removed_rules
modified_rules
weight_changes
source_changes
effective_date_changes

This allows administrative review before deployment of new regulatory mappings.

---

# 19. INTERNAL CRQ-V DATA IMPORT

Create a first-class import subsystem.

Supported initial formats:

CSV
XLSX

Flow:

UPLOAD
→ PARSE
→ COLUMN_DETECTION
→ MAPPING
→ NORMALIZATION
→ CNPJ_VALIDATION
→ DUPLICATE_DETECTION
→ DRY_RUN
→ HUMAN_CONFIRMATION
→ IMPORT
→ AUDIT

Do not import directly into production records without dry-run.

---

# 20. CRQ-V IMPORT JOB

Create:

tenant_import_job

Fields:

id
tenant_id
filename
sha256
uploaded_by
uploaded_at
mapping_json
records_total
records_valid
records_invalid
records_duplicate
records_imported
dry_run
confirmed_by
confirmed_at
status
error_report_uri

status:

UPLOADED
ANALYZING
READY
INVALID
CONFIRMED
IMPORTING
COMPLETED
FAILED

---

# 21. IMPORT ERROR REPORT

For every rejected line, provide:

row_number
cnpj
field
value
error_code
error_message

Allow export as CSV.

---

# 22. TENANT COMPANY STATE

Extend tenant_company_state.

Fields:

tenant_id
establishment_id

crq_status
workflow_status

last_inspection_at
last_analysis_at

reason_code
reason_text

do_not_reprospect
suppression_until

source
evidence_reference

created_by
updated_by
created_at
updated_at

---

# 23. SUPPRESSION RULES

Create controlled suppression mechanism.

Reason codes:

REGISTERED
EXEMPT
RECENTLY_INSPECTED
OUT_OF_SCOPE
FALSE_POSITIVE
DUPLICATE
LEGAL_REVIEW
MANUAL_SUPPRESSION

Suppression SHALL be explainable and auditable.

Suppressed companies SHALL not disappear from the system.

They should be marked and excluded by default from new prospecting queues when configured.

---

# 24. BULK CNPJ LOOKUP

Add bulk lookup functionality.

Input:

- pasted CNPJs;
- CSV;
- XLSX.

Capabilities:

validate
normalize
deduplicate
match
show missing
show inactive
show prospect score
export result

Recommended limit SHALL be configurable.

---

# 25. BULK OPERATIONS

Authorized users SHALL be able to perform controlled bulk operations:

add to list
assign inspector
set priority
change workflow status
suppress
remove suppression
export

Every bulk operation SHALL:

- require explicit confirmation;
- record actor;
- record affected count;
- generate audit event;
- preserve operation identifier.

---

# 26. AUDIT LOG HARDENING

audit_event SHALL be append-only.

Extend schema:

event_id
tenant_id
actor_user_id
actor_role

action
entity_type
entity_id

request_id
correlation_id

result
reason

before_hash
after_hash

metadata_json

ip_address
user_agent

event_hash
previous_event_hash

software_release_id
created_at

Application code SHALL NOT expose standard update/delete operations for audit_event.

---

# 27. AUDIT HASH CHAIN

Recommended implementation:

event_hash = SHA256(
    previous_event_hash
    + canonical_event_payload
)

The hash chain provides tamper evidence.

It does not replace database security.

Canonical serialization MUST be deterministic.

---

# 28. AUDIT VERIFICATION

Create command:

python -m app.audit.verify_chain

And endpoint restricted to ADMIN:

GET /api/v1/admin/audit/integrity

Return:

events_checked
first_event
last_event
broken_links
status

status:

VALID
INVALID

---

# 29. DATA CLASSIFICATION

Implement classification:

PUBLIC
INTERNAL
CRQ_CONFIDENTIAL
PERSONAL_DATA

Examples:

PUBLIC:
public RFB corporate data.

INTERNAL:
operational platform metadata.

CRQ_CONFIDENTIAL:
fiscal lists;
inspection planning;
internal notes;
suppression reasons;
inspection history.

PERSONAL_DATA:
data subject to LGPD where applicable.

Classification SHALL influence:

logging
export
retention
access
telemetry
backup
incident handling

---

# 30. NO SECONDARY USE

CRQ_CONFIDENTIAL and PERSONAL_DATA SHALL NOT be used for:

- model training;
- marketing;
- profiling unrelated to the contract;
- external analytics;
- third-party enrichment without authorization;
- LLM prompts sent to external providers.

Any future exception requires documented approval and legal basis.

---

# 31. EXTERNAL DEPENDENCY REGISTER

Create:

docs/operations/EXTERNAL-DEPENDENCIES.md

And optionally entity:

external_dependency

Fields:

name
provider
purpose
data_sent
data_received
data_classification
hosting_region
backup_region
contract_owner
cost_model
monthly_budget
criticality
fallback
exit_strategy

Examples:

cloud hosting
object storage
CNPJ provider
email
monitoring

---

# 32. DATA RESIDENCY

System configuration SHALL explicitly identify:

primary_region
backup_region
object_storage_region

Do not silently migrate CRQ-V confidential data to another jurisdiction.

Any change SHALL generate a change_request.

---

# 33. PROVIDER USAGE CONTROL

Create:

provider_usage

Fields:

provider
period
request_count
cache_hits
cache_misses
success_count
error_count
rate_limit_count
cost_estimate
monthly_budget
warning_threshold
hard_limit

This is especially important because the contracted value is low and external API costs must remain controlled.

---

# 34. PROVIDER CIRCUIT BREAKER

External provider failures SHALL NOT make core prospecting unavailable.

Implement states:

CLOSED
OPEN
HALF_OPEN

Fallback:

online provider unavailable
→ use latest RFB dataset
→ show provenance
→ show "not verified in real time"

---

# 35. DATA QUALITY DASHBOARD

Create administrative view:

/admin/data-quality

Show at least:

current RFB competence
last successful import
number of RS establishments
number active
number inactive
invalid CNPJs
unknown CNAEs
records without municipality
records without company size
records without primary CNAE
rule matches
unmatched relevant records
provider error rate
import duration
import rejected records
source age

Do not hide quality failures.

---

# 36. DATA QUALITY METRICS

Create:

data_quality_metric

Fields:

source_version
metric
value
threshold
status
measured_at

status:

OK
WARNING
FAIL

Critical thresholds SHALL prevent automatic publication when appropriate.

---

# 37. PUBLICATION GATE

New RFB competence SHALL NOT automatically become production if critical validation fails.

Flow:

INGESTED
→ VALIDATED
→ QUALITY_CHECK
→ READY
→ APPROVED
→ PUBLISHED

Allow manual approval when configured.

---

# 38. PORTABILITY

CRQ-V SHALL be able to obtain its contractual data in open formats.

Minimum formats:

CSV
JSON

Optional:

SQL dump

Provide machine-readable schema descriptions.

---

# 39. DATA DICTIONARY

Create:

docs/data/DATA-DICTIONARY.md

For every exported field document:

field_name
description
type
nullable
source
example
classification
version_introduced
deprecated_since

Exports SHALL include schema version.

---

# 40. CONTRACT EXIT PACKAGE

Implement command:

crqvia export-contract --tenant crq-v

Output:

CRQV-export-YYYYMMDD/
    README.txt
    metadata.json
    companies.csv
    establishments.csv
    lists.csv
    list_items.csv
    saved_searches.json
    tenant_company_state.csv
    notes.csv
    audit.csv
    rules.json
    incidents.csv
    users.csv
    data-dictionary.json
    checksums.sha256

Do not include password hashes or secrets.

---

# 41. CONTRACT EXIT METADATA

metadata.json SHALL contain:

tenant
generated_at
software_version
commit_sha
database_revision
rfb_source_version
rule_set_version
schema_version
encoding
timezone
file_list
record_counts

---

# 42. CONTRACT EXIT VERIFICATION

After export:

calculate SHA-256
verify all files
record export in audit
allow authorized CRQ-V representative to confirm receipt

Only after contractual authorization proceed with deletion.

---

# 43. DATA DELETION WORKFLOW

Statuses:

EXPORT_PENDING
EXPORT_GENERATED
EXPORT_CONFIRMED
DELETION_APPROVED
DELETION_RUNNING
DELETION_VERIFIED
CLOSED

Deletion SHALL respect legal retention obligations.

Do not blindly delete logs or records subject to mandatory retention.

---

# 44. SECURITY INCIDENT RECORD

Extend incident model:

id
tenant_id

incident_type
severity

detected_at
awareness_at
contained_at
resolved_at

personal_data_incident

data_categories
estimated_subjects
affected_systems

risk_assessment
possible_damage

mitigation_actions
root_cause

crq_notified_at

anpd_notification_required
anpd_notified_at

subjects_notification_required
subjects_notified_at

non_notification_reason

retention_until

status

---

# 45. INCIDENT EVIDENCE

Each incident SHALL support attachment/reference to:

timeline
logs
screenshots
affected release
affected source version
corrective action
preventive action
communication evidence

---

# 46. SLA CALCULATION

Define measurable availability.

availability_percentage =

(total_period_minutes - unavailable_minutes)
/
(total_period_minutes - excluded_minutes)
* 100

Store:

measurement_period
measurement_source
total_minutes
excluded_minutes
unavailable_minutes
availability_percentage

Do not calculate uptime from application self-report only.

Prefer independent external health monitoring when available.

---

# 47. OUTAGE DEFINITION

Define:

FULL_OUTAGE
PARTIAL_OUTAGE
DEGRADED
EXTERNAL_PROVIDER_FAILURE

Core service outage SHOULD include inability to:

- authenticate;
- search;
- access company results;
- access essential fiscal lists.

Failure of optional functionality should not necessarily equal full outage.

---

# 48. SUPPORT SLA METRICS

Ticket SHALL record:

opened_at
acknowledged_at
work_started_at
service_restored_at
resolved_at
closed_at

Metrics:

time_to_ack
time_to_restore
time_to_resolve

Internal targets from SPEC-0015 remain goals unless contractual values supersede them.

---

# 49. BROWSER SUPPORT MATRIX

Create:

docs/operations/BROWSER-SUPPORT.md

Initial support policy:

Chrome:
current + previous major

Edge:
current + previous major

Firefox:
current + previous major

Safari:
current + previous major

Define also:

language: pt-BR
encoding: UTF-8
timezone display: America/Sao_Paulo
desktop priority
tablet support for critical workflows

Browser versions SHALL be re-evaluated periodically.

---

# 50. ACCESSIBILITY VALIDATION

Current WCAG goals SHALL become testable.

Implement:

axe-core
Playwright accessibility smoke tests
keyboard-only navigation checks
focus-order checks
accessible-name checks

Manual acceptance SHALL include:

login
search
filters
company profile
lists
exports

Create:

docs/acceptance/ACCESSIBILITY-REPORT.md

---

# 51. APPLICATION VERSION DISPLAY

Every UI SHALL expose, at minimum through an "About/System" screen:

application_version
commit_sha_short
deployment_date
RFB competence
rule_set_version
last_data_update

This makes incident reports and fiscal evidence reproducible.

---

# 52. VERSION API

Create:

GET /api/v1/system/version

Example:

{
  "application_version": "1.2.0",
  "commit": "abc1234",
  "database_revision": "42",
  "rfb_competence": "2027-03",
  "rule_set": "CFQ-339-v3",
  "deployed_at": "..."
}

Endpoint SHALL NOT expose secrets or infrastructure-sensitive information.

---

# 53. SAVED SEARCH ALERTS

Optional P2 feature.

Saved queries may be periodically evaluated against new source versions.

Generate alert when:

- new company matches;
- company changes CNAE and starts matching;
- company reactivates and matches;
- previously suppressed item becomes eligible after suppression expiry.

Do not automatically create an inspection decision.

---

# 54. MATRIX / BRANCH RELATIONSHIP

Use CNPJ root to group headquarters and branches.

Expose:

headquarters_cnpj
branch_count
is_headquarters

Allow filter:

HEADQUARTERS_ONLY
BRANCHES_ONLY
ALL

Do not collapse branches when address-level fiscal activity matters.

---

# 55. NEGATIVE FILTERS

Search engine SHALL support exclusions:

exclude CNAE
exclude municipality
exclude status
exclude saved list
exclude CRQ status
exclude suppressed entities

This is required for efficient fiscal prospecting.

---

# 56. SEARCH EXPLAINABILITY

Every search result SHOULD be capable of exposing:

matched_filters
matched_rules
score_factors
source_version
rule_set_version

Debug-level explanation may be restricted to authorized users.

---

# 57. REGULATORY REVIEW QUEUE

Create queue for ambiguous cases:

REVIEW_REQUIRED

Reasons:

textual activity ambiguity
multiple conflicting CNAEs
rule requiring human interpretation
missing source data

The system must prefer human review over fabricated certainty.

---

# 58. MODEL / AI GOVERNANCE

If ML or LLM features are enabled:

model_version
training_dataset_version
feature_set_version
evaluation_report
approved_by
deployed_at

Store explanation separately from regulatory rules.

ML score SHALL NOT overwrite regulatory score.

External LLMs SHALL NOT receive CRQ_CONFIDENTIAL data.

---

# 59. VULNERABILITY MANAGEMENT

Create:

security_vulnerability

Fields:

id
source
cve
component
version
severity
detected_at
fixed_version
fixed_at
status
risk_acceptance_reason
accepted_by
expires_at

status:

OPEN
MITIGATED
FIXED
ACCEPTED
FALSE_POSITIVE

Critical vulnerabilities SHALL block release unless formally accepted.

---

# 60. SBOM RETENTION

Each production release SHALL retain an SBOM.

Supported format:

CycloneDX
or
SPDX

SBOM SHALL be linked to:

software_release_id
container_digest
commit_sha

---

# 61. DEPENDENCY LICENSING

CI SHOULD identify dependency licenses.

Reject or review dependencies incompatible with the product's licensing or contractual use.

Generate:

THIRD-PARTY-NOTICES.md

---

# 62. CONFIGURATION GOVERNANCE

Production configuration SHALL be versioned where safe.

Never store:

passwords
tokens
API keys
private certificates

in Git.

Configuration changes affecting behavior SHALL generate audit or change records.

---

# 63. SECRET ROTATION

Document and test rotation procedure for:

database credentials
JWT/session secrets
provider API credentials
object-storage keys
email credentials

Rotation SHALL not require source-code changes.

---

# 64. BACKUP TRACEABILITY

Every backup SHALL record:

backup_id
started_at
completed_at
database_revision
software_release
source_version
size
sha256
storage_location
encrypted
restore_tested_at

A backup that has never been restored successfully SHALL not be considered fully verified.

---

# 65. RESTORE EVIDENCE

Periodic restore test SHALL generate:

docs/acceptance/RESTORE-REPORT-<date>.md

Containing:

backup used
environment
restore duration
validation queries
record counts
errors
status

---

# 66. OBSERVABILITY DATA CLASSIFICATION

Logs and traces MUST NOT contain:

passwords
tokens
authorization headers
full sensitive payloads
CRQ confidential notes

CNPJ may appear only where operationally justified.

Prefer IDs and hashes in telemetry.

---

# 67. CORRELATION IDs

Every API request SHALL receive:

request_id

Distributed/background actions SHALL also carry:

correlation_id

Export, ingestion, provider verification and audit records should share correlation identifiers.

---

# 68. OPERATIONAL EVENT TIMELINE

For incidents, imports, releases and exports, timestamps SHALL use:

UTC internally

Display:

America/Sao_Paulo

Store timestamps with timezone information.

---

# 69. TIME SYNCHRONIZATION

Production hosts and containers SHOULD use reliable synchronized time.

Audit integrity depends on timestamps.

Detect unreasonable clock drift where technically possible.

---

# 70. CONTRACTUAL REPORT

Generate monthly report:

docs/reporting/monthly/

Contents:

availability
incidents
support tickets
RFB source version
imports
ruleset version
software releases
provider usage
backup status
restore test status
security findings
data quality
change requests

This can support contract fiscalization.

---

# 71. EVIDENCE IMMUTABILITY

Acceptance evidence SHOULD contain:

generated_at
commit_sha
software_release_id
test_run_id
source_version
rule_set_version

Do not regenerate old evidence silently.

Create new evidence version instead.

---

# 72. PROCUREMENT RETRIEVAL CHECK

Provide script:

scripts/check-procurement-documents.py

It SHOULD compare known official procurement documents against PROCUREMENT-MANIFEST.

Detect:

new documents
changed content
missing content
new hashes

Do not automatically accept changed documents as authoritative without review.

---

# 73. PROCUREMENT CHANGE ALERT

When a procurement document changes:

status = REVIEW_REQUIRED

Generate report with:

document
old_hash
new_hash
detected_at
possible affected requirements

This is particularly important before bid submission and contracting.

---

# 74. DOCUMENT SOURCE OF TRUTH

Original procurement documents SHALL be retained outside normal editable source documentation.

Suggested structure:

docs/procurement/sources/

Do not manually modify source PDFs or official text snapshots.

Derived documents SHALL live separately.

---

# 75. REQUIREMENT DIFF

Create utility:

scripts/requirements-diff.py

Compare:

previous requirement matrix
current requirement matrix

Detect:

added requirements
removed requirements
changed source references
changed acceptance criteria

---

# 76. ACCEPTANCE HARDENING

Acceptance report SHALL include:

functional requirement
source clause
implementation file
test
test result
evidence
release
source data version
rule version

PASS requires evidence.

NOT_TESTED is preferable to a fabricated PASS.

---

# 77. PERFORMANCE REPRODUCIBILITY

Performance tests SHALL record:

dataset size
RFB competence
database configuration
software release
hardware/container resources
query mix
concurrency
results

Without environment metadata, performance results are not reproducible.

---

# 78. BASELINE PERFORMANCE DATASET

Create a repeatable benchmark dataset representative of RS.

It SHOULD contain:

large municipalities
small municipalities
multiple CNAEs
active/inactive companies
matrix/branches
multiple company sizes

Do not benchmark exclusively with synthetic tiny datasets.

---

# 79. LARGE EXPORT SAFETY

For large exports:

run asynchronously
limit concurrent exports
show progress
expire files
audit download
avoid memory exhaustion

Export SHALL never block normal search operations.

---

# 80. RATE LIMIT GOVERNANCE

Configure separate limits for:

authentication
company search
provider verification
exports
admin operations

Rate limits SHALL be configurable per tenant/environment.

---

# 81. ADMINISTRATIVE SEPARATION

ADMIN permission SHOULD NOT automatically imply ability to alter regulatory rules without explicit rule-governance permission.

Recommended permissions:

USER_ADMIN
RULE_VIEW
RULE_EDIT
RULE_APPROVE
AUDIT_VIEW
DATA_IMPORT
DATA_PUBLISH
SECURITY_ADMIN

Avoid one universal super-role for routine operations.

---

# 82. FOUR-EYES CONTROL

Recommended for:

publishing a new rule set
publishing a new RFB competence after warnings
deleting tenant data
contract exit
approving critical vulnerability exception

Requester and approver SHOULD be different users where practical.

---

# 83. DATA EXPORT PERMISSIONS

Differentiate:

EXPORT_BASIC
EXPORT_CONFIDENTIAL
EXPORT_AUDIT

A normal inspector SHOULD NOT automatically be allowed to export all audit data.

---

# 84. DOWNLOAD AUDIT

Every download of:

export file
contract-exit package
audit extract

SHALL record:

actor
file
timestamp
IP/context
file hash

---

# 85. EXPIRED EXPORT CLEANUP

Background job SHALL delete expired temporary exports.

Record:

created_at
expires_at
deleted_at

Deletion SHALL preserve audit metadata without preserving the export contents.

---

# 86. TENANT ISOLATION TESTS

Automated tests SHALL verify:

Tenant A cannot query Tenant B lists.

Tenant A cannot fetch Tenant B exports.

Tenant A cannot access Tenant B notes.

Tenant A cannot use IDs to bypass access control.

Even if initial deployment has one tenant, isolation architecture must be tested.

---

# 87. DATA MIGRATION TESTS

Schema migrations SHALL test:

upgrade
rollback where supported
data preservation
index creation
large-table migration behavior

A migration that destroys historical snapshots is unacceptable.

---

# 88. DISASTER RECOVERY

Document:

maximum tolerable outage
target RTO
target RPO
restore procedure
communication procedure

Keep targets compatible with the contract economics.

Do not design an unnecessarily expensive multi-region architecture unless required.

---

# 89. OPERATIONAL READINESS REVIEW

Before production launch, perform ORR.

Checklist:

application
database
backup
restore
monitoring
alerts
security
support
incident communication
provider fallbacks
data import
rule approval
release baseline
contract exit
documentation
acceptance evidence

Create:

docs/acceptance/OPERATIONAL-READINESS-REVIEW.md

---

# 90. GO-LIVE GATE

Production go-live SHALL require:

SPEC-0018 mandatory functionality implemented.

SPEC-0019 P0 controls implemented.

Acceptance report generated.

Critical security issues resolved.

Backup successfully restored.

Two-user concurrency validated.

RFB source imported.

Rule set approved.

Support channel active.

Monitoring active.

No unresolved documentary change affecting mandatory functionality.

---

# 91. PRIORITY CLASSIFICATION

P0:

procurement manifest
requirement traceability
contractual baseline
release management
historical snapshots
rule governance
CRQ-V import
suppression
audit hardening
contract exit
incident governance
data quality gates
backup verification

P1:

browser matrix
accessibility evidence
provider budgets
bulk operations
historical change UI
data residency
advanced SLA reporting

P2:

saved-search alerts
NCM research
natural-language filter builder
advanced route planning
optional ML/LLM features

P0 SHALL be completed before optional AI enhancements.

---

# 92. NON-GOALS

This SPEC does NOT require:

automatic fiscal decisions
automatic legal classification
scraping CAPTCHA-protected websites
social-network harvesting
mandatory QSA ingestion
personal profiling
marketing functionality
sales-lead functionality
expensive enterprise infrastructure

---

# 93. AGENT RULES

The implementation agent SHALL:

read existing code before modifying it;

preserve prior specifications unless conflict is proven;

implement controls rather than only documenting them;

create tests for material features;

never fabricate official procurement requirements;

never fabricate Anexo IV;

never invent regulatory rules;

never infer missing RFB values;

never overwrite historical snapshots;

never mutate active rulesets in place;

never mark acceptance PASS without executed evidence.

---

# 94. REQUIRED AGENT OUTPUT PER PHASE

For each implementation phase provide:

COMPLETED
What was implemented.

FILES
Files changed.

DATABASE
Migrations added.

TESTS
Commands executed and results.

EVIDENCE
Acceptance evidence produced.

RISKS
Open risks.

BLOCKERS
External blockers.

NEXT
Next implementation step.

COMMIT
Commit SHA.

---

# 95. DEFINITION OF DONE

SPEC-0019 is complete only when:

procurement documents are versioned and hashed;

requirements link to implementation and tests;

production releases are identifiable;

historical prospecting state can be reconstructed;

regulatory rules are versioned and approved;

CRQ-V data can be safely imported;

suppression prevents avoidable reprospecting;

audit history is append-only and integrity-checkable;

incidents support LGPD evidence;

external dependencies are documented;

provider usage and cost can be monitored;

data quality is visible;

bad source imports can be blocked;

contract data can be exported in open formats;

contract exit has been tested;

backup restore has been tested;

accessibility evidence exists;

browser compatibility is documented;

application version is visible;

monthly operational evidence can be produced;

the system can explain:

WHAT happened
WHO did it
WHEN it happened
WHICH data were used
WHICH rule was used
WHICH software version was used
WHY the result was produced.

If any P0 item remains only documented and not implemented where implementation is required:

SPEC-0019 REMAINS OPEN.