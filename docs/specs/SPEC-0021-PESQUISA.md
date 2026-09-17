Vasculhei o site atual do CRQ-V, o Pregão Eletrônico nº 0005/2026, páginas de Registro de Pessoa Jurídica, AFT, regularidade, a regulamentação usada pelo Conselho e cruzei isso com o **código atual** do `JoseRFJuniorLLMs/CRQ-V-IA`, não apenas com o README. A conclusão mudou bastante em relação ao “100% conforme” que está hoje no repositório.

**O projeto está conceitualmente muito bem alinhado com o que o CRQ-V quer, mas eu não o apresentaria hoje como 100% aderente ou pronto para homologação.** Há alguns problemas P0 que podem fazer a solução encontrar empresas erradas, deixar empresas relevantes de fora ou apresentar informação cadastral como verificada quando ela não foi verificada.

O pregão está realmente aberto, publicado em **10/09/2026**, e o objeto é exatamente “software especializado para prospecção e identificação de empresas potencialmente sujeitas à fiscalização do CRQ-V”. O PNCP registra 12 meses, R$ 400/mês e total estimado de R$ 4.800. ([CRQV][1])

### Auditoria CRQ-V × CRQ-V-IA

| Área                          | O que o CRQ-V precisa                                  | O que existe hoje                                                                                | Parecer                                                       |
| ----------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| Prospecção de empresas do RS  | Universo real de empresas potencialmente fiscalizáveis | `seed_rs_companies.py` com empresas demonstrativas inseridas manualmente                         | 🔴 **P0**                                                     |
| CNAE principal                | Pesquisa/classificação                                 | Implementado                                                                                     | 🟢                                                            |
| CNAEs secundários             | Devem entrar na pesquisa                               | Armazenados e classificados, mas o filtro `/prospects?cnae=` consulta **somente `primary_cnae`** | 🔴                                                            |
| Divisão/grupo CNAE            | O próprio levantamento do TR prevê hierarquia CNAE     | Não há filtro efetivo por divisão/grupo                                                          | 🟠                                                            |
| Município                     | Filtro geográfico                                      | Implementado                                                                                     | 🟢                                                            |
| Bairro/CEP                    | Segmentação territorial                                | Campos existem, mas não são filtros da API                                                       | 🟠                                                            |
| Microrregião/região           | Planejamento territorial                               | Não modelado                                                                                     | 🟠                                                            |
| Porte                         | ME/EPP/Demais                                          | Implementado                                                                                     | 🟢                                                            |
| Capital social                | Informação disponível                                  | Implementado                                                                                     | 🟢                                                            |
| Data de abertura              | Critério de prospecção                                 | Campo existe, mas falta filtro próprio                                                           | 🟠                                                            |
| Situação cadastral            | Ativa/baixada/inapta/suspensa                          | Campo + live check                                                                               | 🔴 **live check precisa correção**                            |
| Matriz/filial                 | Muito útil para fiscalização                           | Campo existe, falta filtro/agregação                                                             | 🟠                                                            |
| Listas/roteiros               | Trabalho dos fiscais                                   | Implementado                                                                                     | 🟢                                                            |
| CSV/XLSX                      | Saída eletrônica                                       | Implementado                                                                                     | 🟢                                                            |
| 2 acessos simultâneos         | Obrigatório no TR                                      | Implementado/testado em aplicação                                                                | 🟢, mas falta teste real de carga                             |
| Auditoria                     | Rastreabilidade                                        | Existe                                                                                           | 🟢/🟠                                                         |
| LGPD                          | Obrigatória                                            | Boa estrutura inicial                                                                            | 🟠, não dá para declarar conformidade integral só pelo código |
| Enquadramento CFQ             | Identificar empresas sujeitas                          | Motor existe, mas cobertura normativa é incompleta                                               | 🔴 **P0**                                                     |
| RT/AFT                        | Essencial para saber situação real perante CRQ         | Praticamente não modelado                                                                        | 🟠                                                            |
| Atualização periódica da base | Necessária para uma prospecção real                    | Não encontrei ETL real da base empresarial do RS                                                 | 🔴 **P0**                                                     |

O modelo atual já guarda CNPJ, razão social, nome fantasia, porte, capital, matriz/filial, situação cadastral, abertura, CNAE principal/secundários, endereço, telefone, e-mail, score, justificativa e estado interno CRQ-V. Isso é uma base bastante boa.

Só que a API de busca revela uma divergência importante com a própria matriz de conformidade: o repositório declara filtro por CNAE principal **e secundário**, bairro e CEP, mas a implementação efetiva aceita `q`, `cnae`, `city`, `status`, `size`, `tier`, `crq_status` e `min_score`; e `cnae` é aplicado apenas sobre `Establishment.primary_cnae`.

### O maior problema: a base de empresas

Aqui está o ponto que mais me preocuparia numa homologação.

O sistema não está atualmente prospectando o universo empresarial do Rio Grande do Sul. O `seed_rs_companies.py` contém um conjunto manual de empresas de demonstração como “PETROQUÍMICA SUL BRASIL S.A.”, “TINTAS E RESINAS DO SUL LTDA.”, “BIOEFLUENTES RS” etc.

Isso serve muito bem para demonstrar a interface. **Não atende a finalidade material do contrato**, que é descobrir empresas que o CRQ-V ainda precisa encontrar.

Curiosamente, o `relatorio.md` antigo já havia identificado exatamente a solução correta: baixar e processar os dados públicos da Receita, cruzar Empresas + Estabelecimentos + CNAEs e filtrar `UF = RS`. Depois o código evoluiu, mas essa parte fundamental acabou substituída por seed demonstrativo.

Eu colocaria como P0 um pipeline parecido com:

`Dados Abertos CNPJ/RFB → estabelecimento RS → CNAE principal/secundários → normalização → RN CFQ → deduplicação → comparação com base CRQ-V → ranking → prospecção`

E cada carga precisa ter **competência/data da fonte**, por exemplo `2026-08`, para que uma fiscalização possa posteriormente demonstrar qual informação existia naquela data.

### O segundo problema crítico: o “Receita Federal ao vivo”

Esse precisa ser corrigido antes de mostrar o sistema em homologação.

Hoje ele tenta BrasilAPI e Minha Receita. Até aí, razoável como intermediários. O problema vem depois.

Se os dois serviços falharem, o código retorna:

`success = true`
`registration_status = ATIVA`
`source = "Base Cadastral RFB / CRQ-V Local Cache"`

e ainda informa que a consulta foi “simulada com sucesso”.

Isso é perigoso. Uma queda de internet pode transformar uma empresa baixada em **“ATIVA confirmada”**.

O retorno correto deveria ser algo como:

```text
verification_status = UNAVAILABLE
success = false
cached = true/false
cached_status = ...
cached_at = ...
provider = ...
```

Nunca fabricar `ATIVA`.

Pior, o teste automatizado não detecta o problema porque apenas verifica se `live_data["success"] is True`. Como o fallback sempre devolve `true`, o teste passa até quando nenhuma consulta real funcionou.

Esse teste precisa simular separadamente: BrasilAPI OK, fallback secundário OK, timeout total, CNPJ inexistente, CNPJ baixado, resposta inconsistente e cache expirado.

### O motor CFQ 339 está incompleto

Aqui encontrei a maior diferença entre “parece correto” e “é regulatoriamente correto”.

O `cfq_rules.py` contém uma tabela manual relativamente pequena concentrada em indústria química, fertilizantes, defensivos, cosméticos, tintas, saneamento, laboratório, curtume, bebidas e alguns comércios.

Só que o Anexo I da RN 339 é **enorme**. Inclui atividades que não parecem “indústria química” à primeira vista: alimentos, produtos do fumo, madeira, celulose/papel, borracha, plástico, minerais não metálicos, metalurgia e muitas outras. O próprio texto chega, por exemplo, a fabricação de farinha, amidos, açúcar, café, panificação, vinagre, fermentos, madeira tratada, celulose, vidro, cimento, cerâmica, siderurgia etc. ([CRQMG][2])

Então hoje ocorre isto:

**RN 339 oficial → centenas de enquadramentos**
**CRQ-V-IA → subconjunto selecionado manualmente**

Resultado: há risco grande de **falso negativo**.

Existe ainda uma questão jurídica mais delicada. O art. 3º da RN 339 diz que o registro é obrigatório quando a **atividade básica ou serviço prestado a terceiros** está relacionada no Anexo I. Já o art. 4º diz que, quando a atividade básica não é química e a empresa apenas possui atividade de apoio/secundária que demanda conhecimento químico, o registro é facultativo, embora devam existir profissionais habilitados. ([CRQMG][2])

Seu algoritmo atual simplesmente reduz o peso do CNAE secundário para 85% e pode elevar a classificação. Isso não representa adequadamente essa distinção.

Eu substituiria o simples:

`HIGH / MEDIUM / LOW`

por duas dimensões independentes:

```text
fiscal_priority:
HIGH | MEDIUM | LOW

regulatory_status:
MANDATORY_REGISTRATION
CHEMICAL_SUPPORT_ACTIVITY
SERVICE_TO_THIRD_PARTIES
MANUAL_REVIEW
OUT_OF_SCOPE
```

E cada decisão deveria guardar:

```text
cnae
cnae_role                 # PRIMARY / SECONDARY
norm_number
norm_article
norm_annex
norm_item
legal_effect
rule_version
source_sha256
effective_from
rationale
```

Isso transforma seu motor de uma heurística elegante em um **motor regulatório auditável**.

### Os campos oficiais do próprio CRQ-V mostram outra oportunidade

O formulário atual de Registro de Pessoa Jurídica do CRQ-V pede razão social, CNPJ/CPF, telefone, e-mail, e-mail de cobrança, endereço, bairro, cidade, CEP, UF, **Inscrição Estadual, número de empregados, natureza da atividade, Responsável Técnico, número de registro do RT e conselho vinculado**. ([CRQV][3])

Você já cobre boa parte dos dados empresariais. Mas não cobre bem:

| Campo CRQ-V                   | CRQ-V-IA              |
| ----------------------------- | --------------------- |
| Razão social                  | ✅                     |
| CNPJ                          | ✅                     |
| Telefone/e-mail               | ✅                     |
| Endereço/bairro/cidade/CEP/UF | ✅                     |
| Capital social                | ✅                     |
| Inscrição Estadual            | ❌                     |
| Número de empregados          | ❌                     |
| Natureza da atividade         | ⚠️ inferida pelo CNAE |
| Responsável Técnico           | ❌                     |
| Registro CRQ do RT            | ❌                     |
| Conselho vinculado            | ❌                     |
| AFT                           | ❌                     |

Nem todos esses campos precisam vir de uma base pública. E eu **não tentaria coletar tudo indiscriminadamente**, porque a função do produto é prospecção, não montar o cadastro universal da humanidade. Billing email, CPF de sócio e coisas semelhantes nem deveriam entrar na prospecção sem uma razão específica.

Mas dados de **registro CRQ, RT e AFT** seriam extremamente valiosos se vierem por importação da base interna do CRQ-V.

O próprio CRQ-V diz que empresas cuja atividade principal envolve química ou que prestam esses serviços precisam de registro e profissional habilitado. ([CRQV][4]) A AFT comprova a responsabilidade técnica e atualmente possui validade máxima de um ano; o Conselho inclusive atualizou o layout da AFT em setembro de 2026. ([CRQV][5])

Então o cruzamento ideal seria:

```text
RFB diz que existe
        +
RN/CFQ diz que tem potencial
        +
CRQ-V diz que não está registrada
        +
CRQ-V diz que não possui AFT vigente
        =
ALTA PRIORIDADE REAL DE FISCALIZAÇÃO
```

Isso é muito mais interessante que simplesmente “CNAE 20 = score 95”.

### Um problema documental que eu corrigiria imediatamente

Hoje o README e a SPEC-0018 afirmam **“100% conforme”**.

Ao mesmo tempo, o `relatorio.md` ainda afirma que o software está **“0% implementado”**, porque foi produzido antes da implementação atual.

Então o próprio repositório consegue simultaneamente estar 0% e 100% pronto. Uma façanha burocrático-quântica admirável, mas ruim numa licitação.

Eu removeria por enquanto o badge **“100% Conforme”** e usaria algo factual como **“Implementação alinhada ao Pregão 0005/2026, em validação de conformidade”** até fechar os P0.

### O que eu faria agora, em ordem

1. **Implementar ingestão real dos Dados Abertos do CNPJ/RFB**, filtrando todos os estabelecimentos do RS e atualizando por competência.
2. **Transformar integralmente o Anexo I da RN 339 em dados**, não em dezenas de regras hardcoded.
3. **Separar efeito jurídico de prioridade fiscal**, especialmente atividade básica x secundária x serviço a terceiros.
4. **Eliminar completamente o fallback falso `ATIVA/success=true`**.
5. Implementar filtros por **CNAE primário/secundário, seção/divisão/grupo/classe/subclasse, bairro, CEP, município, região, matriz/filial, data de abertura e faixa de capital**.
6. Criar importador CSV/XLSX da base interna do CRQ-V com registro da empresa, RT, AFT, última fiscalização e situações como dispensada/não fiscalizar novamente.
7. Adicionar **proveniência e temporalidade**: fonte, competência RFB, data de coleta, versão da norma, versão do motor e snapshot da seleção.
8. Criar testes regulatórios contra uma tabela-ouro do Anexo I e testes reais dos provedores, em vez de apenas testar que um endpoint devolveu HTTP 200.
9. Atualizar `relatorio.md`, `README.md` e `SPEC-0018` para refletirem o código real e só declarar conformidade quando houver evidência executável.
10. Na homologação, produzir um relatório automático mostrando para cada requisito: **TR → campo/API → tela → teste → evidência → commit**.

O ponto positivo é que **não é necessário jogar o projeto fora**. A arquitetura atual de Company/Establishment, API FastAPI, autenticação, listas, exportação, auditoria e frontend já entrega uma boa parte da estrutura. O que está faltando é justamente a camada que transforma uma demo convincente em **uma ferramenta fiscal confiável: dados reais, cobertura normativa integral e rastreabilidade da decisão**. A SPEC-0019, aliás, já percebe várias dessas necessidades de governança, snapshots, histórico, importação da base interna e supressão; ela está conceitualmente no caminho correto.

**Meu parecer para o estado atual:** o `CRQ-V-IA` **atende a forma e boa parte do fluxo funcional do Pregão 0005/2026, mas ainda não atende de maneira confiável a substância da prospecção**. Os três P0 são claros: **base real RFB do RS, RN 339 integral e consulta cadastral sem resultado fictício**. Resolvidos esses três, mais os filtros que já estão prometidos na documentação, aí o software fica muito mais defensável numa homologação técnica do CRQ-V.

[1]: https://crqv.org.br/?utm_source=chatgpt.com "CRQ-V"
[2]: https://crqmg.org.br/legislacao/read/357 "CRQMG"
[3]: https://www.crqv.org.br/uploads/servico/1836/SaLP93vRQa0a9ny8S4EJQLpllCDNAjua.pdf?utm_source=chatgpt.com "SERVIÇO PÚBLICO FEDERAL"
[4]: https://crqv.org.br/servico/view/22?utm_source=chatgpt.com "CRQ-V | Registro Pessoa Jurídica"
[5]: https://crqv.org.br/pagina/view/11?utm_source=chatgpt.com "CRQ-V | Informações"
