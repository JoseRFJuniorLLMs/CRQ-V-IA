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


