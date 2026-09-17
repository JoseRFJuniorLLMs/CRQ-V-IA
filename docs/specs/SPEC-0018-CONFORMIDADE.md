Fiz uma nova auditoria cruzando a **branch `main` atual do `CRQ-V-IA`** com o Edital, Termo de Referência, Modelo de Proposta, minuta de contrato e ETP. A conclusão mudou bastante quando olhamos o repositório como **produto executável**, e não como projeto de arquitetura.

**Sim, falta coisa. E a principal lacuna é objetiva: neste momento o repositório contém uma especificação muito boa do produto, mas praticamente não contém o produto.**

O edital é o Pregão Eletrônico nº 0005/2026, Processo nº 1729/2026, para software especializado de prospecção e identificação de empresas potencialmente sujeitas à fiscalização.  O TR deixa ainda mais explícito que a solução deve funcionar durante 12 meses e servir ao Departamento de Fiscalização e Autuação. 

### 1. O achado mais importante: não há aplicação implementada

No GitHub, `apps/api/` contém **apenas um README dizendo que FastAPI/SQLAlchemy/Alembic estão previstos**.  O mesmo ocorre em `apps/web/`, que contém apenas um README dizendo que Next.js será implementado.  E `services/ingest/` também contém somente um README descrevendo o pipeline futuro.

O próprio README principal é correto e não tenta fingir o contrário: registra o status como **“Fase inicial de especificação e arquitetura”**.

Também não encontrei `package.json`, aplicação Next.js, aplicação FastAPI, migrations Alembic, models, endpoints, testes ou pipeline de ingestão. O `docker-compose` atual sobe somente um PostgreSQL/PostGIS.  E o GitHub Actions atualmente apenas verifica se alguns Markdown existem, sem compilar, testar ou executar a aplicação.

Isso é crítico porque o TR determina que **o objeto só será recebido se atender integralmente às especificações técnicas**, podendo a Administração rejeitar a solução total ou parcialmente. 

### 2. Cruzamento requisito por requisito

| Área                        | Exigência dos anexos                                     | O que há hoje                       | O que falta                                    |
| --------------------------- | -------------------------------------------------------- | ----------------------------------- | ---------------------------------------------- |
| Prospecção de empresas      | Identificar empresas com potencial na área química no RS | SPEC completa                       | **Motor executável**                           |
| Pesquisa                    | Setor, região, porte e outros critérios                  | SPEC completa                       | **Frontend + API + banco/indexação**           |
| CNPJ                        | Verificar situação cadastral perante RFB                 | Estratégia de providers             | **Provider funcional e demonstrável**          |
| 2 acessos simultâneos       | Obrigatório                                              | Teste especificado                  | **Auth, sessões e teste real**                 |
| Plataforma durante 12 meses | Obrigatório                                              | Modelado                            | **Ambiente produção operacional**              |
| Licença/assinatura          | Deve garantir acesso no período                          | Parcialmente modelado               | **Gestão de vigência/tenant**                  |
| Sem infraestrutura no CRQ-V | Ambiente tecnológico da contratada                       | Arquitetura prevista                | **Cloud efetivamente implantada**              |
| Suporte                     | Durante toda a vigência                                  | SPEC de suporte                     | **Canal real, tickets e responsável**          |
| Comunicação de falhas       | Comunicação ao fiscal                                    | SPEC genérica                       | **Fluxo operacional + contato + evidência**    |
| LGPD                        | Obrigatória                                              | Boa SPEC                            | **Controles efetivamente implantados**         |
| Confidencialidade           | Pesquisas/listas/fiscalização devem ficar restritas      | Parcial na SPEC                     | **Isolamento e política específica**           |
| Exclusão de dados           | Encerrada finalidade/contrato                            | Política prevista                   | **Rotina de encerramento e prova de exclusão** |
| Treinamento/orientação      | Previsto no ETP                                          | Manual/tour previsto                | **Treinamento formal + evidência**             |
| Exportação eletrônica       | Esperada                                                 | SPEC CSV/XLSX                       | **Implementação**                              |
| Disponibilidade             | Adequada durante contrato                                | SLO definido                        | **Monitoramento real**                         |
| Backup/restore              | Boa prática necessária para continuidade                 | SPEC                                | **Rotina e teste real**                        |
| Aceite                      | Atendimento integral                                     | Script definido                     | **Relatório executado**                        |
| Atestado técnico            | Obrigatório na habilitação                               | Checklist                           | **Documento externo da empresa**               |
| Proposta comercial          | Modelo oficial                                           | Checklist                           | **Proposta preenchida/assinada**               |
| Operação contratual         | NF + regularidade                                        | Parcial                             | **Checklist mensal completo**                  |
| Preposto                    | Previsto na minuta contratual                            | Não encontrei especificação própria | **Designação e processo operacional**          |

Os principais requisitos funcionais estão corretamente capturados na matriz do projeto: prospecção, filtros, CNPJ, dois acessos, LGPD, disponibilidade, suporte, cloud, onboarding e exportação.  Então **não precisamos reinventar a arquitetura**. Precisamos começar a convertê-la em software.

### 3. Há requisitos que precisam ficar mais explícitos nas SPECs

O TR exige pelo menos dois acessos simultâneos e determina que a solução seja fornecida por licença, assinatura ou modalidade equivalente durante todo o contrato.  A SPEC de autenticação cobre muito bem a simultaneidade, inclusive prevendo um teste com duas sessões independentes.  Mas falta modelar claramente a **vigência contratual**, data de ativação, expiração, renovação, bloqueio pós-contrato e exportação/devolução dos dados no encerramento.

Outro detalhe importante: o TR proíbe **qualquer forma de subcontratação**.  Só que nossa arquitetura prevê opcionalmente Serpro, object storage, cloud/PaaS e outros serviços externos. Isso não significa automaticamente subcontratação, mas eu documentaria expressamente uma arquitetura de dependências onde a contratada continua sendo integralmente responsável e nenhum terceiro assume a execução do objeto. Melhor matar essa discussão antes que alguém no processo descubra o prazer ancestral de interpretar uma palavra contra o fornecedor.

### 4. O CNPJ precisa deixar de depender de uma condição que talvez não aconteça

Hoje a SPEC diz que o **Conecta gov.br** será usado “quando o CRQ-V fornecer credenciais”, e o Serpro seria opcional.

Isso é um risco de aceite. O TR simplesmente exige que a plataforma possibilite verificar a situação cadastral perante a Receita Federal.  Não diz que o CRQ-V tem obrigação de fornecer credencial de API.

Portanto o produto precisa funcionar **mesmo que o CRQ-V não forneça absolutamente nenhuma credencial externa**. A base aberta da RFB pode ser a fonte padrão, com competência e timestamp claramente expostos, e um provider on-demand adicional pode melhorar a atualidade. Mas o requisito mínimo não pode ficar bloqueado esperando uma integração concedida pelo contratante.

### 5. LGPD está bem desenhada, mas falta transformar política em controle

Essa parte das SPECs ficou boa. A SPEC prevê minimização, RBAC, menor privilégio, MFA, logs, TLS, criptografia de backups, retenção e fluxo de incidentes.

Só que o TR vai além de uma menção genérica à LGPD. Ele determina proteção técnica e administrativa, acesso restrito, **confidencialidade inclusive das pesquisas, listas de empresas e informações de fiscalização**, comunicação de incidentes sem demora injustificada e eliminação/destinação legal dos dados após o encerramento da finalidade. 

Eu adicionaria ao modelo uma classificação específica como `CRQ_CONFIDENTIAL`, impediria que listas internas aparecessem em logs ou telemetria indevida e criaria uma rotina formal de **contract exit**: exportação autorizada, revogação de contas, eliminação dos dados, retenções legais e emissão de relatório final.

### 6. Falta treinamento formal

O ETP é explícito: deve haver **orientação ou capacitação dos usuários quanto às funcionalidades do software**. 

O projeto prevê manual e tour inicial, o que ajuda, mas eu colocaria uma entrega objetiva:

`Treinamento inicial CRQ-V + manual PDF/HTML + gravação opcional + lista de presença/aceite + credenciais entregues`.

Isso vira uma prova fácil de cumprimento em vez de uma conversa do tipo “mas vocês explicaram como usar?”, porque aparentemente nossa espécie decidiu que até explicar onde fica o botão de pesquisa precisa deixar vestígio documental.

### 7. Comunicação operacional precisa ser contratual, não apenas técnica

O TR determina comunicação ao fiscal quando houver indisponibilidade ou falha.  E a minuta diz que a Administração terá gestor e fiscal específicos e que as comunicações formais podem ocorrer por e-mail. 

Além disso, a minuta exige que a contratada disponha de **preposto** para intermediar a execução. 

O repo precisa portanto de algo como `CONTRACT-OPERATIONS.md` contendo preposto, e-mail oficial de suporte, e-mail de incidentes, contatos do fiscal/gestor, modelo de aviso de indisponibilidade, modelo de restabelecimento e registro das comunicações.

### 8. A CI atual não protege nada que será efetivamente contratado

A SPEC de deployment promete lint, unit tests, typecheck, SAST, dependency scan, build, SBOM, staging e smoke tests.

O CI real só testa a existência de arquivos Markdown.

Quando a implementação começar, o pipeline precisa efetivamente executar testes de backend/frontend, migrations, testes do ETL, scanners de dependências, secret scanning, build dos containers, SBOM e smoke test.

A SPEC de aceite já fornece uma base excelente, incluindo buscas, filtros, CNPJ, duas sessões, auditoria, segurança, desempenho e resiliência.  O problema é simples: **nenhum desses testes existe ainda como código**.

### 9. Falta completar a camada administrativo-contratual

O Modelo de Proposta exige preço, prazo de execução, validade, garantia do objeto, dados completos da empresa/contato e dados bancários.  

A minuta contratual vincula a solução ao TR e à proposta apresentada.  Portanto eu faria o repo guardar uma **release imutável da solução ofertada**, por exemplo `v1.0.0-crqv-bid`, porque aquilo que você declarar tecnicamente na proposta vai te vincular depois.

Durante o contrato, a NF é mensal e devem acompanhar **cinco CNDs: Federal/INSS, FGTS, Trabalhista, Estadual e Municipal**. 

O checklist atual do GitHub tem Federal, FGTS, Municipal e CNDT, mas **não lista explicitamente a Fazenda Estadual**.  Isso precisa ser corrigido.

Também vale criar um checklist mensal de faturamento contendo empenho, modalidade/processo, Simples Nacional quando aplicável, NF, cinco CNDs e comprovante de disponibilidade mensal.

### 10. O atestado técnico continua sendo uma dependência externa crítica

O TR exige atestados de fornecimento similar, de complexidade tecnológica e operacional equivalente ou superior, e permite diligência sobre contrato, endereço e local de execução. 

Nenhuma quantidade de Rust, Python, IA ou entusiasmo arquitetural gera retrospectivamente um atestado de capacidade técnica. Esse documento precisa existir **fora do repositório**.

Há ainda uma cláusula condicional dizendo que, se o objeto for considerado serviço técnico especializado, poderá ser exigido registro profissional e responsável com ART/AFT.  O checklist atual deveria incluir explicitamente esse item como **“verificar aplicabilidade”**.

### 11. Há uma divergência documental que sua checklist já pegou corretamente

O Edital fala em balanço do **último exercício social**.  Já o TR pede os **dois últimos exercícios sociais**. 

Também existe diferença na base do patrimônio líquido de 10%: há redações usando valor estimado e valor proposto. Isso não é problema do software, mas é risco real de habilitação. A abordagem atual do checklist, preparar a documentação mais abrangente e buscar esclarecimento se necessário, é prudente.

### 12. Encontrei ainda um documento que está faltando nesta auditoria

O Edital afirma que fazem parte dele **quatro anexos**:

Anexo I, Termo de Referência; Anexo II, Modelo de Proposta; Anexo III, Minuta de Contrato; e **Anexo IV, Modelos de Referência**. 

Você anexou o Edital, TR, Modelo de Proposta, Contrato e ETP. O ETP é identificado expressamente como **Estudo Técnico Preliminar do Processo 1729/2026**, não como Anexo IV. 

Portanto **não dá para declarar auditoria documental 100% fechada enquanto o Anexo IV não for obtido**. É exatamente o tipo de arquivo aparentemente inofensivo que depois contém três declarações obrigatórias em fonte tamanho 10 escondidas no fim do mundo.

### O que eu faria agora, na ordem

1. **Implementar o monorepo real**, com `apps/web`, `apps/api`, `services/ingest`, schemas/migrations e testes.
2. Implementar primeiro o fluxo completo **login → busca → filtros → empresa → situação CNPJ → lista → exportação**.
3. Implementar ingestão RFB/RS + CNAE + motor de regras, sem depender de credencial fornecida pelo CRQ-V.
4. Implementar dois acessos simultâneos, RBAC, auditoria, TLS, retenção, exclusão e resposta a incidentes.
5. Criar deploy de homologação/produção, monitoramento, backup e restore.
6. Acrescentar **treinamento, preposto, contract-exit, comunicação ao fiscal e operação mensal** às SPECs.
7. Corrigir o checklist para incluir **CND Estadual, ART/AFT quando aplicável e pacote mensal de faturamento**.
8. Obter o **Anexo IV** e fazer a última varredura antes de congelar uma release de licitação.

Então o quadro real é: **a engenharia de requisitos está forte e o desenho cobre quase todo o TR; o código executável ainda está essencialmente em zero**. Não precisamos de mais vinte documentos conceituais agora. Precisamos começar a transformar `SPEC-0000` a `SPEC-0017` em código, testes e evidências. Só depois disso eu colocaria o selo interno de **“pronto para homologação do CRQ-V”**.


Fiz uma nova auditoria cruzando a **branch `main` atual do `CRQ-V-IA`** com o Edital, Termo de Referência, Modelo de Proposta, minuta de contrato e ETP. A conclusão mudou bastante quando olhamos o repositório como **produto executável**, e não como projeto de arquitetura.

**Sim, falta coisa. E a principal lacuna é objetiva: neste momento o repositório contém uma especificação muito boa do produto, mas praticamente não contém o produto.**

O edital é o Pregão Eletrônico nº 0005/2026, Processo nº 1729/2026, para software especializado de prospecção e identificação de empresas potencialmente sujeitas à fiscalização.  O TR deixa ainda mais explícito que a solução deve funcionar durante 12 meses e servir ao Departamento de Fiscalização e Autuação. 

### 1. O achado mais importante: não há aplicação implementada

No GitHub, `apps/api/` contém **apenas um README dizendo que FastAPI/SQLAlchemy/Alembic estão previstos**.  O mesmo ocorre em `apps/web/`, que contém apenas um README dizendo que Next.js será implementado.  E `services/ingest/` também contém somente um README descrevendo o pipeline futuro.

O próprio README principal é correto e não tenta fingir o contrário: registra o status como **“Fase inicial de especificação e arquitetura”**.

Também não encontrei `package.json`, aplicação Next.js, aplicação FastAPI, migrations Alembic, models, endpoints, testes ou pipeline de ingestão. O `docker-compose` atual sobe somente um PostgreSQL/PostGIS.  E o GitHub Actions atualmente apenas verifica se alguns Markdown existem, sem compilar, testar ou executar a aplicação.

Isso é crítico porque o TR determina que **o objeto só será recebido se atender integralmente às especificações técnicas**, podendo a Administração rejeitar a solução total ou parcialmente. 

### 2. Cruzamento requisito por requisito

| Área                        | Exigência dos anexos                                     | O que há hoje                       | O que falta                                    |
| --------------------------- | -------------------------------------------------------- | ----------------------------------- | ---------------------------------------------- |
| Prospecção de empresas      | Identificar empresas com potencial na área química no RS | SPEC completa                       | **Motor executável**                           |
| Pesquisa                    | Setor, região, porte e outros critérios                  | SPEC completa                       | **Frontend + API + banco/indexação**           |
| CNPJ                        | Verificar situação cadastral perante RFB                 | Estratégia de providers             | **Provider funcional e demonstrável**          |
| 2 acessos simultâneos       | Obrigatório                                              | Teste especificado                  | **Auth, sessões e teste real**                 |
| Plataforma durante 12 meses | Obrigatório                                              | Modelado                            | **Ambiente produção operacional**              |
| Licença/assinatura          | Deve garantir acesso no período                          | Parcialmente modelado               | **Gestão de vigência/tenant**                  |
| Sem infraestrutura no CRQ-V | Ambiente tecnológico da contratada                       | Arquitetura prevista                | **Cloud efetivamente implantada**              |
| Suporte                     | Durante toda a vigência                                  | SPEC de suporte                     | **Canal real, tickets e responsável**          |
| Comunicação de falhas       | Comunicação ao fiscal                                    | SPEC genérica                       | **Fluxo operacional + contato + evidência**    |
| LGPD                        | Obrigatória                                              | Boa SPEC                            | **Controles efetivamente implantados**         |
| Confidencialidade           | Pesquisas/listas/fiscalização devem ficar restritas      | Parcial na SPEC                     | **Isolamento e política específica**           |
| Exclusão de dados           | Encerrada finalidade/contrato                            | Política prevista                   | **Rotina de encerramento e prova de exclusão** |
| Treinamento/orientação      | Previsto no ETP                                          | Manual/tour previsto                | **Treinamento formal + evidência**             |
| Exportação eletrônica       | Esperada                                                 | SPEC CSV/XLSX                       | **Implementação**                              |
| Disponibilidade             | Adequada durante contrato                                | SLO definido                        | **Monitoramento real**                         |
| Backup/restore              | Boa prática necessária para continuidade                 | SPEC                                | **Rotina e teste real**                        |
| Aceite                      | Atendimento integral                                     | Script definido                     | **Relatório executado**                        |
| Atestado técnico            | Obrigatório na habilitação                               | Checklist                           | **Documento externo da empresa**               |
| Proposta comercial          | Modelo oficial                                           | Checklist                           | **Proposta preenchida/assinada**               |
| Operação contratual         | NF + regularidade                                        | Parcial                             | **Checklist mensal completo**                  |
| Preposto                    | Previsto na minuta contratual                            | Não encontrei especificação própria | **Designação e processo operacional**          |

Os principais requisitos funcionais estão corretamente capturados na matriz do projeto: prospecção, filtros, CNPJ, dois acessos, LGPD, disponibilidade, suporte, cloud, onboarding e exportação.  Então **não precisamos reinventar a arquitetura**. Precisamos começar a convertê-la em software.

### 3. Há requisitos que precisam ficar mais explícitos nas SPECs

O TR exige pelo menos dois acessos simultâneos e determina que a solução seja fornecida por licença, assinatura ou modalidade equivalente durante todo o contrato.  A SPEC de autenticação cobre muito bem a simultaneidade, inclusive prevendo um teste com duas sessões independentes.  Mas falta modelar claramente a **vigência contratual**, data de ativação, expiração, renovação, bloqueio pós-contrato e exportação/devolução dos dados no encerramento.

Outro detalhe importante: o TR proíbe **qualquer forma de subcontratação**.  Só que nossa arquitetura prevê opcionalmente Serpro, object storage, cloud/PaaS e outros serviços externos. Isso não significa automaticamente subcontratação, mas eu documentaria expressamente uma arquitetura de dependências onde a contratada continua sendo integralmente responsável e nenhum terceiro assume a execução do objeto. Melhor matar essa discussão antes que alguém no processo descubra o prazer ancestral de interpretar uma palavra contra o fornecedor.

### 4. O CNPJ precisa deixar de depender de uma condição que talvez não aconteça

Hoje a SPEC diz que o **Conecta gov.br** será usado “quando o CRQ-V fornecer credenciais”, e o Serpro seria opcional.

Isso é um risco de aceite. O TR simplesmente exige que a plataforma possibilite verificar a situação cadastral perante a Receita Federal.  Não diz que o CRQ-V tem obrigação de fornecer credencial de API.

Portanto o produto precisa funcionar **mesmo que o CRQ-V não forneça absolutamente nenhuma credencial externa**. A base aberta da RFB pode ser a fonte padrão, com competência e timestamp claramente expostos, e um provider on-demand adicional pode melhorar a atualidade. Mas o requisito mínimo não pode ficar bloqueado esperando uma integração concedida pelo contratante.

### 5. LGPD está bem desenhada, mas falta transformar política em controle

Essa parte das SPECs ficou boa. A SPEC prevê minimização, RBAC, menor privilégio, MFA, logs, TLS, criptografia de backups, retenção e fluxo de incidentes.

Só que o TR vai além de uma menção genérica à LGPD. Ele determina proteção técnica e administrativa, acesso restrito, **confidencialidade inclusive das pesquisas, listas de empresas e informações de fiscalização**, comunicação de incidentes sem demora injustificada e eliminação/destinação legal dos dados após o encerramento da finalidade. 

Eu adicionaria ao modelo uma classificação específica como `CRQ_CONFIDENTIAL`, impediria que listas internas aparecessem em logs ou telemetria indevida e criaria uma rotina formal de **contract exit**: exportação autorizada, revogação de contas, eliminação dos dados, retenções legais e emissão de relatório final.

### 6. Falta treinamento formal

O ETP é explícito: deve haver **orientação ou capacitação dos usuários quanto às funcionalidades do software**. 

O projeto prevê manual e tour inicial, o que ajuda, mas eu colocaria uma entrega objetiva:

`Treinamento inicial CRQ-V + manual PDF/HTML + gravação opcional + lista de presença/aceite + credenciais entregues`.

Isso vira uma prova fácil de cumprimento em vez de uma conversa do tipo “mas vocês explicaram como usar?”, porque aparentemente nossa espécie decidiu que até explicar onde fica o botão de pesquisa precisa deixar vestígio documental.

### 7. Comunicação operacional precisa ser contratual, não apenas técnica

O TR determina comunicação ao fiscal quando houver indisponibilidade ou falha.  E a minuta diz que a Administração terá gestor e fiscal específicos e que as comunicações formais podem ocorrer por e-mail. 

Além disso, a minuta exige que a contratada disponha de **preposto** para intermediar a execução. 

O repo precisa portanto de algo como `CONTRACT-OPERATIONS.md` contendo preposto, e-mail oficial de suporte, e-mail de incidentes, contatos do fiscal/gestor, modelo de aviso de indisponibilidade, modelo de restabelecimento e registro das comunicações.

### 8. A CI atual não protege nada que será efetivamente contratado

A SPEC de deployment promete lint, unit tests, typecheck, SAST, dependency scan, build, SBOM, staging e smoke tests.

O CI real só testa a existência de arquivos Markdown.

Quando a implementação começar, o pipeline precisa efetivamente executar testes de backend/frontend, migrations, testes do ETL, scanners de dependências, secret scanning, build dos containers, SBOM e smoke test.

A SPEC de aceite já fornece uma base excelente, incluindo buscas, filtros, CNPJ, duas sessões, auditoria, segurança, desempenho e resiliência.  O problema é simples: **nenhum desses testes existe ainda como código**.

### 9. Falta completar a camada administrativo-contratual

O Modelo de Proposta exige preço, prazo de execução, validade, garantia do objeto, dados completos da empresa/contato e dados bancários.  

A minuta contratual vincula a solução ao TR e à proposta apresentada.  Portanto eu faria o repo guardar uma **release imutável da solução ofertada**, por exemplo `v1.0.0-crqv-bid`, porque aquilo que você declarar tecnicamente na proposta vai te vincular depois.

Durante o contrato, a NF é mensal e devem acompanhar **cinco CNDs: Federal/INSS, FGTS, Trabalhista, Estadual e Municipal**. 

O checklist atual do GitHub tem Federal, FGTS, Municipal e CNDT, mas **não lista explicitamente a Fazenda Estadual**.  Isso precisa ser corrigido.

Também vale criar um checklist mensal de faturamento contendo empenho, modalidade/processo, Simples Nacional quando aplicável, NF, cinco CNDs e comprovante de disponibilidade mensal.

### 10. O atestado técnico continua sendo uma dependência externa crítica

O TR exige atestados de fornecimento similar, de complexidade tecnológica e operacional equivalente ou superior, e permite diligência sobre contrato, endereço e local de execução. 

Nenhuma quantidade de Rust, Python, IA ou entusiasmo arquitetural gera retrospectivamente um atestado de capacidade técnica. Esse documento precisa existir **fora do repositório**.

Há ainda uma cláusula condicional dizendo que, se o objeto for considerado serviço técnico especializado, poderá ser exigido registro profissional e responsável com ART/AFT.  O checklist atual deveria incluir explicitamente esse item como **“verificar aplicabilidade”**.

### 11. Há uma divergência documental que sua checklist já pegou corretamente

O Edital fala em balanço do **último exercício social**.  Já o TR pede os **dois últimos exercícios sociais**. 

Também existe diferença na base do patrimônio líquido de 10%: há redações usando valor estimado e valor proposto. Isso não é problema do software, mas é risco real de habilitação. A abordagem atual do checklist, preparar a documentação mais abrangente e buscar esclarecimento se necessário, é prudente.

### 12. Encontrei ainda um documento que está faltando nesta auditoria

O Edital afirma que fazem parte dele **quatro anexos**:

Anexo I, Termo de Referência; Anexo II, Modelo de Proposta; Anexo III, Minuta de Contrato; e **Anexo IV, Modelos de Referência**. 

Você anexou o Edital, TR, Modelo de Proposta, Contrato e ETP. O ETP é identificado expressamente como **Estudo Técnico Preliminar do Processo 1729/2026**, não como Anexo IV. 

Portanto **não dá para declarar auditoria documental 100% fechada enquanto o Anexo IV não for obtido**. É exatamente o tipo de arquivo aparentemente inofensivo que depois contém três declarações obrigatórias em fonte tamanho 10 escondidas no fim do mundo.

### O que eu faria agora, na ordem

1. **Implementar o monorepo real**, com `apps/web`, `apps/api`, `services/ingest`, schemas/migrations e testes.
2. Implementar primeiro o fluxo completo **login → busca → filtros → empresa → situação CNPJ → lista → exportação**.
3. Implementar ingestão RFB/RS + CNAE + motor de regras, sem depender de credencial fornecida pelo CRQ-V.
4. Implementar dois acessos simultâneos, RBAC, auditoria, TLS, retenção, exclusão e resposta a incidentes.
5. Criar deploy de homologação/produção, monitoramento, backup e restore.
6. Acrescentar **treinamento, preposto, contract-exit, comunicação ao fiscal e operação mensal** às SPECs.
7. Corrigir o checklist para incluir **CND Estadual, ART/AFT quando aplicável e pacote mensal de faturamento**.
8. Obter o **Anexo IV** e fazer a última varredura antes de congelar uma release de licitação.

Então o quadro real é: **a engenharia de requisitos está forte e o desenho cobre quase todo o TR; o código executável ainda está essencialmente em zero**. Não precisamos de mais vinte documentos conceituais agora. Precisamos começar a transformar `SPEC-0000` a `SPEC-0017` em código, testes e evidências. Só depois disso eu colocaria o selo interno de **“pronto para homologação do CRQ-V”**.


# SPEC-0018 — Implementação Integral do CRQ-V-IA e Conformidade com o Pregão 0005/2026

Status: REQUIRED
Priority: P0
Repository: JoseRFJuniorLLMs/CRQ-V-IA
Target branch: main
Scope: implementação completa do produto executável
Supersedes: nenhum documento anterior
Depends on:
- SPEC-0000 até SPEC-0017
- ARCHITECTURE.md
- DATA-MODEL.md
- REQUIREMENTS-MATRIX.md
- HABILITATION-CHECKLIST.md

---

# 1. OBJETIVO

Transformar o repositório CRQ-V-IA de um conjunto de especificações e arquitetura em uma aplicação completa, executável, testável e implantável, capaz de atender tecnicamente ao Pregão Eletrônico CRQ-V nº 0005/2026.

O agente deverá implementar o produto e não apenas gerar novas especificações.

Ao final desta SPEC deverá existir uma solução funcional contendo:

- frontend web;
- backend API;
- banco de dados;
- migrations;
- pipeline de ingestão;
- motor regulatório;
- consulta cadastral CNPJ;
- autenticação;
- controle de acesso;
- suporte a múltiplos usuários;
- observabilidade;
- auditoria;
- exportações;
- ambiente de homologação;
- testes;
- CI/CD;
- documentação operacional;
- pacote de evidências de aceite.

---

# 2. REGRA PRINCIPAL

O agente NÃO deverá considerar a tarefa concluída se houver apenas:

- README;
- pseudocódigo;
- interfaces vazias;
- mocks sem implementação de produção;
- TODOs;
- endpoints retornando valores fixos;
- páginas estáticas simulando dados;
- componentes sem integração;
- migrations não executáveis;
- testes marcados como skip;
- scripts não executados;
- configurações não verificadas.

A definição de pronto exige software executável.

---

# 3. FONTES NORMATIVAS DO PRODUTO

O agente deverá tratar como requisitos obrigatórios:

1. Pregão Eletrônico nº 0005/2026;
2. Processo CRQ-V nº 1729/2026;
3. Termo de Referência;
4. Estudo Técnico Preliminar;
5. Minuta de Contrato;
6. Modelo de Proposta Comercial;
7. SPECs já existentes no repositório.

Em caso de conflito entre uma decisão arquitetural interna e exigência do edital/TR, prevalece a exigência contratual.

Nenhuma funcionalidade deverá transformar score, CNAE, regra ou modelo de IA em decisão automática de fiscalização, autuação ou obrigatoriedade jurídica.

---

# 4. RESULTADO DE NEGÓCIO

O CRQ-V deverá conseguir utilizar a plataforma para:

1. autenticar usuários;
2. pesquisar empresas;
3. filtrar empresas;
4. localizar empresas no Rio Grande do Sul;
5. identificar empresas potencialmente relacionadas à área da Química;
6. consultar situação cadastral do CNPJ;
7. entender por que uma empresa apareceu no resultado;
8. criar listas de empresas;
9. priorizar empresas;
10. exportar resultados;
11. compartilhar trabalho entre fiscais;
12. utilizar pelo menos dois acessos simultaneamente;
13. manter histórico e auditoria;
14. utilizar a plataforma sem instalar infraestrutura local específica;
15. receber suporte;
16. continuar utilizando a solução durante toda a vigência contratual.

---

# 5. STACK OBRIGATÓRIA

Manter a arquitetura já aprovada no projeto.

## 5.1 Frontend

- Next.js;
- TypeScript;
- React;
- App Router;
- autenticação integrada à API;
- layout responsivo;
- acessibilidade;
- componentes reutilizáveis.

## 5.2 Backend

- Python;
- FastAPI;
- SQLAlchemy 2;
- Alembic;
- Pydantic;
- PostgreSQL.

## 5.3 Banco

- PostgreSQL 16;
- PostGIS;
- pg_trgm;
- índices adequados para busca empresarial.

## 5.4 ETL

- Python;
- Polars;
- DuckDB quando conveniente;
- processamento batch/streaming.

## 5.5 Infraestrutura

- Docker;
- Docker Compose;
- containers OCI;
- produção em cloud/PaaS ou infraestrutura equivalente.

Evitar dependências obrigatórias de:

- Kafka;
- Elasticsearch;
- Redis;
- Kubernetes.

Somente introduzir componentes adicionais quando houver benefício técnico comprovado.

---

# 6. ESTRUTURA FINAL DO REPOSITÓRIO

Criar e implementar:

apps/
  web/
    src/
    components/
    app/
    lib/
    tests/
    package.json
    Dockerfile

  api/
    app/
      api/
      auth/
      core/
      db/
      models/
      schemas/
      services/
      repositories/
      security/
      audit/
      exports/
    migrations/
    tests/
    pyproject.toml
    alembic.ini
    Dockerfile

services/
  ingest/
    src/
      download/
      normalize/
      transform/
      regulatory/
      publish/
    tests/
    pyproject.toml
    Dockerfile

infra/
  docker-compose.yml
  docker-compose.prod.yml
  env/
  scripts/
  monitoring/

docs/
  operations/
  security/
  acceptance/
  procurement/

scripts/
  bootstrap.sh
  seed.sh
  ingest-rfb.sh
  test-all.sh
  backup.sh
  restore.sh

---

# 7. BANCO DE DADOS

Implementar migrations reais para pelo menos:

## 7.1 company

Campos mínimos:

- id
- cnpj_base
- razao_social
- natureza_juridica
- capital_social
- porte
- ente_federativo
- source_version
- created_at
- updated_at

## 7.2 establishment

- id
- company_id
- cnpj
- nome_fantasia
- matriz_filial
- situacao_cadastral
- data_situacao_cadastral
- motivo_situacao
- data_inicio_atividade
- cnae_principal
- tipo_logradouro
- logradouro
- numero
- complemento
- bairro
- cep
- uf
- municipio_codigo
- municipio_nome
- latitude
- longitude
- source_updated_at

## 7.3 cnae

- codigo
- descricao
- secao
- divisao
- grupo
- classe
- subclasse

## 7.4 establishment_cnae

Relacionar CNAEs secundários.

## 7.5 regulatory_rule

- id
- version
- source
- rule_type
- cnae
- weight
- description
- valid_from
- valid_to
- active

## 7.6 prospect_score

- establishment_id
- regulatory_score
- operational_score
- final_score
- explanation_json
- rule_version
- calculated_at

## 7.7 user

- id
- email
- password_hash
- role
- active
- created_at
- last_login

## 7.8 tenant

Preparar aplicação para tenant CRQ-V.

## 7.9 saved_list

## 7.10 saved_list_item

## 7.11 saved_search

## 7.12 audit_event

## 7.13 incident

## 7.14 cnpj_verification

## 7.15 contract_configuration

Campos:

- start_date
- end_date
- status
- simultaneous_access_limit
- retention_policy
- support_email
- tenant_id

---

# 8. PIPELINE DE DADOS RFB

Implementar pipeline de produção para Dados Abertos CNPJ.

Fluxo:

DOWNLOAD
→ VERIFY
→ EXTRACT
→ NORMALIZE
→ FILTER RS
→ STAGING
→ VALIDATE
→ INDEX
→ PUBLISH
→ AUDIT

O pipeline deverá:

- identificar automaticamente a competência;
- baixar arquivos;
- validar tamanho;
- gerar SHA-256;
- detectar corrupção;
- descompactar;
- interpretar encoding;
- carregar Empresas;
- carregar Estabelecimentos;
- carregar CNAEs;
- carregar Municípios;
- carregar Simples quando necessário;
- filtrar RS antecipadamente;
- carregar staging;
- executar validação;
- publicar atomicamente.

Nunca expor dados parcialmente importados.

---

# 9. VERSIONAMENTO DOS DADOS

Cada carga deverá possuir:

source_version
source_date
source_url
source_hash
import_started_at
import_finished_at
record_count
status

Somente uma versão poderá estar marcada como produção.

Implementar rollback para competência anterior.

---

# 10. MOTOR REGULATÓRIO

Implementar SPEC-0003 integralmente.

Entrada:

- CNAE principal;
- CNAEs secundários;
- porte;
- situação cadastral;
- data de abertura;
- localização;
- dados internos CRQ-V quando disponíveis.

Saída:

{
  "score": 82,
  "classification": "HIGH",
  "reasons": [
    {
      "type": "CNAE_PRIMARY",
      "rule": "...",
      "weight": 60
    }
  ],
  "rule_version": "...",
  "calculated_at": "..."
}

O motor deverá ser:

- determinístico;
- versionado;
- explicável;
- reproduzível;
- auditável.

Nenhum resultado poderá afirmar:

- "empresa irregular";
- "empresa obrigada ao registro";
- "empresa deve ser autuada".

Usar terminologia:

- potencial;
- indício;
- prioridade;
- possibilidade de fiscalização;
- requer análise humana.

---

# 11. BUSCA

Criar endpoint:

GET /api/v1/companies/search

Filtros obrigatórios:

- CNPJ;
- razão social;
- nome fantasia;
- CNAE;
- CNAE principal;
- CNAE secundário;
- município;
- região;
- CEP;
- porte;
- situação cadastral;
- data de abertura;
- score mínimo;
- categoria regulatória.

Permitir combinação AND/OR onde aplicável.

Implementar:

- paginação;
- ordenação;
- facets;
- cursor pagination;
- busca textual tolerante.

Meta:

P95 inferior a 1,5 segundo em consultas usuais na base RS.

---

# 12. PERFIL DA EMPRESA

Criar:

GET /api/v1/companies/{cnpj}

Tela deverá mostrar:

- CNPJ;
- situação;
- razão social;
- nome fantasia;
- endereço;
- município;
- porte;
- capital social;
- CNAE principal;
- CNAEs secundários;
- abertura;
- fonte;
- competência da fonte;
- última verificação;
- score;
- fatores do score;
- regra regulatória relacionada.

Separar claramente:

"Dado cadastral"

de:

"Análise de prospecção".

---

# 13. CONSULTA CNPJ

O requisito não poderá depender de credenciais fornecidas pelo CRQ-V.

Implementar provider interface:

CnpjProvider.verify()

Providers:

1. RFBBatchProvider
2. ConectaGovProvider
3. SerproProvider

RFBBatchProvider é obrigatório e sempre disponível.

Conecta e Serpro são opcionais.

Se provider online falhar:

- retornar informação da competência RFB;
- informar que não houve confirmação em tempo real;
- não falhar a tela inteira.

---

# 14. AUTENTICAÇÃO

Implementar autenticação real.

Requisitos:

- Argon2id;
- tokens/sessões seguras;
- refresh/revogação;
- rate limit;
- lock progressivo;
- audit log;
- recuperação de senha.

Perfis:

ADMIN
COORDINATOR
INSPECTOR
READ_ONLY

---

# 15. ACESSOS SIMULTÂNEOS

Implementar e testar pelo menos dois usuários simultaneamente.

Teste obrigatório:

Usuário A:
- login;
- busca;
- abre empresa;
- salva lista.

Usuário B simultaneamente:
- login;
- busca diferente;
- exportação;
- abre empresa.

Nenhum usuário poderá:

- derrubar sessão do outro;
- bloquear consultas;
- compartilhar estado indevidamente.

---

# 16. FRONTEND

Criar telas:

/login
/dashboard
/companies
/companies/[cnpj]
/lists
/lists/[id]
/saved-searches
/admin/users
/admin/data
/admin/rules
/admin/audit
/support

Dashboard deverá exibir:

- empresas prospectadas;
- empresas por município;
- empresas por porte;
- empresas por categoria;
- competência dos dados;
- data última atualização;
- top CNAEs;
- status da plataforma.

Não inventar métricas sem dados.

---

# 17. LISTAS DE FISCALIZAÇÃO

Status:

NEW
REVIEWING
SELECTED
DISMISSED
EXPORTED
INSPECTED

Permitir:

- adicionar;
- remover;
- comentar;
- atribuir;
- ordenar;
- exportar;
- registrar histórico.

---

# 18. EXPORTAÇÃO

Implementar:

CSV
XLSX

PDF pode ser implementado na segunda etapa.

Exportação deve conter:

- CNPJ;
- empresa;
- município;
- porte;
- CNAE;
- situação;
- score;
- justificativa;
- competência;
- timestamp;
- fonte.

Toda exportação deverá gerar audit_event.

---

# 19. LGPD

Implementar controles reais.

Não coletar por padrão:

- CPF;
- dados sociais;
- dados de sócios sem necessidade;
- dados pessoais sem finalidade contratual.

Implementar:

- RBAC;
- criptografia TLS;
- secrets fora do código;
- logs protegidos;
- retenção configurável;
- expiração de exports;
- trilha de auditoria;
- incidente de segurança.

---

# 20. CLASSIFICAÇÃO CRQ_CONFIDENTIAL

Criar classificação interna:

PUBLIC
INTERNAL
CRQ_CONFIDENTIAL

Classificar como CRQ_CONFIDENTIAL:

- listas de fiscalização;
- critérios internos;
- comentários;
- informações fornecidas pelo CRQ-V;
- dados sobre ações fiscalizatórias;
- histórico de inspeção.

Esses dados não deverão:

- aparecer em telemetria;
- aparecer em logs de aplicação;
- ser enviados para LLM externo;
- ser usados para treinamento;
- ser compartilhados entre tenants.

---

# 21. CONTRACT EXIT

Implementar procedimento de término de contrato.

Etapas:

1. gerar exportação autorizada;
2. desabilitar usuários;
3. revogar credenciais;
4. revogar tokens;
5. preservar apenas dados legalmente necessários;
6. apagar dados contratuais;
7. apagar exports;
8. emitir relatório de encerramento.

Criar:

docs/operations/CONTRACT-EXIT.md

---

# 22. SUPORTE

Criar sistema mínimo de tickets.

Campos:

- id;
- requester;
- severity;
- subject;
- description;
- opened_at;
- status;
- resolution;
- resolved_at.

Severidades:

P1
P2
P3
P4

Implementar canal de suporte configurável.

---

# 23. INCIDENTES

Criar workflow:

DETECTED
ACKNOWLEDGED
MITIGATING
RESOLVED
CLOSED

Campos:

- início;
- impacto;
- serviços afetados;
- causa;
- ações;
- resolução;
- comunicação ao CRQ-V.

Gerar modelo de comunicação.

---

# 24. PREPOSTO E OPERAÇÃO CONTRATUAL

Criar:

docs/operations/CONTRACT-OPERATIONS.md

Incluir:

- responsável/preposto;
- e-mail de suporte;
- contato operacional;
- fiscal do contrato;
- gestor do contrato;
- fluxo de incidente;
- fluxo de comunicação;
- onboarding;
- desligamento;
- faturamento;
- manutenção de habilitação.

Nenhum dado pessoal deverá ser hard-coded.

Usar variáveis/configuração.

---

# 25. TREINAMENTO

Criar pacote de treinamento.

Arquivos:

docs/training/USER-GUIDE.md
docs/training/ADMIN-GUIDE.md
docs/training/QUICKSTART.md

O agente deve preparar também roteiro de treinamento inicial de 30 a 60 minutos.

Conteúdo:

- login;
- pesquisa;
- filtros;
- leitura de score;
- criação de listas;
- exportação;
- consulta de CNPJ;
- boas práticas LGPD.

---

# 26. INFRAESTRUTURA

Atualizar docker-compose.

Serviços mínimos:

postgres
api
web
worker

Cada serviço deverá possuir:

- health check;
- restart policy;
- logs;
- volume quando necessário.

Criar Dockerfile de produção.

---

# 27. BACKUP

Criar scripts:

scripts/backup.sh
scripts/restore.sh

Backup deverá abranger:

- PostgreSQL;
- configuração;
- artifacts necessários.

Nunca incluir secrets em backup público.

Criar teste automatizado de restore.

---

# 28. OBSERVABILIDADE

Endpoints:

/health/live
/health/ready
/metrics

Monitorar:

- latência;
- erros;
- disponibilidade;
- conexões DB;
- versão RFB;
- última importação;
- falha de ingestão;
- providers CNPJ;
- disco;
- filas.

---

# 29. CI

Substituir atual CI de documentos.

Pipeline obrigatório:

1. markdown/spec validation
2. frontend install
3. frontend lint
4. frontend typecheck
5. frontend tests
6. backend lint
7. backend typecheck
8. backend unit tests
9. ingest tests
10. migrations test
11. integration tests
12. dependency scan
13. secret scan
14. SAST
15. Docker build
16. SBOM
17. smoke test

Pipeline deve falhar se qualquer etapa crítica falhar.

---

# 30. TESTES

Criar testes reais.

## Unit

Cobrir:

- score;
- regras;
- providers;
- filtros;
- permissões;
- exports.

## Integration

Cobrir:

- API + PostgreSQL;
- migrations;
- autenticação;
- busca;
- listas;
- audit log.

## E2E

Cobrir:

- login;
- pesquisa;
- filtros;
- empresa;
- lista;
- exportação;
- dois usuários.

Utilizar Playwright.

---

# 31. SEGURANÇA

Testar:

- SQL injection;
- XSS;
- CSRF;
- broken access control;
- IDOR;
- brute force;
- privilege escalation;
- secret exposure;
- insecure export;
- session reuse.

Nenhum segredo poderá estar no Git.

---

# 32. EVIDÊNCIAS DE ACEITE

Criar:

docs/acceptance/ACCEPTANCE-REPORT.md

Cada requisito deverá possuir:

ID
Requirement
Implementation
Test
Evidence
Status

Status:

PASS
FAIL
NOT_TESTED

Nunca marcar PASS sem evidência executada.

---

# 33. MATRIZ DE CONFORMIDADE

Atualizar REQUIREMENTS-MATRIX.md.

Adicionar colunas:

Implementation File
Test File
Evidence
Status

Não manter somente "implementação proposta".

Substituir progressivamente por implementação real.

---

# 34. CHECKLIST ADMINISTRATIVO

Atualizar HABILITATION-CHECKLIST.md.

Adicionar explicitamente:

- CND Estadual;
- CND Municipal;
- Federal/INSS;
- FGTS;
- CNDT;
- ART/AFT quando aplicável;
- responsável técnico quando aplicável;
- atestado técnico;
- contrato relacionado ao atestado disponível para diligência;
- proposta comercial;
- dados bancários;
- Simples Nacional;
- pacote mensal de faturamento.

Não tratar esses itens como código.

---

# 35. ANEXO IV

O edital referencia Anexo IV — Modelos de Referência.

O arquivo não está disponível no conjunto atual de documentos.

O agente NÃO deverá inventar seu conteúdo.

Criar:

docs/procurement/MISSING-DOCUMENTS.md

Registrar:

- Anexo IV pendente;
- impacto potencial;
- necessidade de auditoria quando obtido.

---

# 36. CUSTO

A arquitetura deverá continuar compatível com contrato de baixo valor.

Evitar serviços cloud caros.

Priorizar:

- PostgreSQL pequeno;
- app leve;
- worker leve;
- object storage;
- deployment simples.

Não introduzir infraestrutura de alta complexidade sem justificativa.

---

# 37. DEFINITION OF DONE

Esta SPEC somente estará concluída quando:

- frontend iniciar;
- backend iniciar;
- banco iniciar;
- migrations rodarem;
- ingest funcionar;
- dataset RS estiver carregado;
- busca funcionar;
- filtros funcionarem;
- CNPJ funcionar;
- score funcionar;
- dois usuários simultâneos funcionarem;
- listas funcionarem;
- exportação funcionar;
- audit log funcionar;
- LGPD controls existirem;
- CI passar;
- Docker build passar;
- testes passarem;
- backup passar;
- restore passar;
- documentação existir;
- acceptance report estiver preenchido com evidência real.

---

# 38. PROIBIÇÕES

O agente não poderá:

- substituir implementação por documentação;
- apagar SPECs existentes sem justificativa;
- alterar requisitos editalícios;
- inventar conteúdo do Anexo IV;
- automatizar decisão fiscal;
- coletar dados pessoais desnecessários;
- fazer scraping que contorne CAPTCHA;
- expor secrets;
- enviar dados CRQ_CONFIDENTIAL a serviços externos;
- criar dependência obrigatória de credenciais do CRQ-V para consulta básica de CNPJ;
- marcar requisito como concluído sem teste.

---

# 39. ORDEM DE EXECUÇÃO

Executar nesta ordem:

PHASE 1
Fundação do monorepo, API, web, DB, migrations.

PHASE 2
Ingestão RFB + CNAE + RS.

PHASE 3
Motor regulatório.

PHASE 4
Busca e filtros.

PHASE 5
Frontend funcional.

PHASE 6
Autenticação/RBAC.

PHASE 7
Listas e exports.

PHASE 8
Providers CNPJ.

PHASE 9
Auditoria/LGPD.

PHASE 10
Observabilidade/support.

PHASE 11
Testes/CI.

PHASE 12
Deploy/homologação.

PHASE 13
Pacote de evidências.

---

# 40. ENTREGA DO AGENTE

Ao finalizar cada fase, o agente deverá produzir:

## Completed

Lista objetiva de itens implementados.

## Files

Arquivos criados/modificados.

## Tests

Testes executados e resultados.

## Remaining

Pendências verdadeiras.

## Risks

Riscos encontrados.

## Commit

SHA do commit correspondente.

Não escrever "concluído" se testes não tiverem sido executados.

---

# 41. COMMIT STRATEGY

Criar commits pequenos e rastreáveis.

Exemplos:

feat(api): bootstrap FastAPI application

feat(db): add core company schema

feat(ingest): implement RFB establishment loader

feat(search): add prospect search filters

feat(auth): add RBAC authentication

feat(web): add company search UI

feat(export): add CSV and XLSX exports

feat(audit): implement immutable audit trail

test(e2e): verify two simultaneous users

docs(acceptance): add bid compliance evidence

---

# 42. RESULTADO FINAL ESPERADO

O repositório deverá deixar de ser:

"arquitetura de um possível produto"

e passar a ser:

"produto executável demonstrável ao CRQ-V".

O resultado deverá permitir que uma pessoa técnica clone o repositório e execute:

docker compose up --build

e obtenha:

- frontend funcionando;
- API funcionando;
- PostgreSQL funcionando;
- migrations aplicadas;
- usuário inicial;
- dataset de demonstração;
- busca funcional;
- filtros;
- score;
- listas;
- exportação;
- auditoria.

O ambiente de produção deverá utilizar configuração externa e secrets apropriados.

---

# 43. CRITÉRIO FINAL DO AGENTE

Antes de encerrar a tarefa, responder internamente:

1. O fiscal consegue pesquisar empresas?
2. Consegue filtrar por atividade?
3. Consegue filtrar por região?
4. Consegue filtrar por porte?
5. Consegue verificar CNPJ?
6. Dois usuários conseguem usar simultaneamente?
7. Existe explicação do motivo de prospecção?
8. Existe exportação?
9. Existe auditoria?
10. Existe suporte?
11. Existe monitoramento?
12. Existe proteção LGPD?
13. Existe backup?
14. Restore foi testado?
15. O sistema inicia do zero?
16. A CI passa?
17. Há evidência para cada requisito?

Se qualquer resposta obrigatória for NÃO:

A SPEC CONTINUA ABERTA.