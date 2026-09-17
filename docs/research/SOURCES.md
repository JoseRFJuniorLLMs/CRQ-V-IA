# Fontes oficiais e pesquisa técnica

## 1. Documentos do Pregão Eletrônico nº 0005/2026

Documentos analisados na preparação do projeto:

- Edital do Pregão Eletrônico nº 0005/2026.
- Anexo I – Termo de Referência.
- Estudo Técnico Preliminar, Processo nº 1729/2026.
- Anexo II – Modelo de Proposta Comercial.
- Minuta do Contrato.

### Pontos relevantes extraídos

- Objeto: software especializado para prospecção de empresas com potencial de atuação na área da Química no Rio Grande do Sul.
- Vigência: 12 meses.
- Mínimo de 2 acessos simultâneos.
- Filtros mínimos: setor, região geográfica, porte e parâmetros compatíveis com fiscalização.
- Verificação de situação cadastral perante a Receita Federal, especialmente CNPJ.
- LGPD, disponibilidade e suporte técnico durante toda a vigência.
- Solução sem dependência de infraestrutura adicional específica no CRQ-V.
- Critério do certame: menor preço global.
- Participação exclusiva de ME/EPP, observadas as regras do edital.

## 2. Receita Federal

### Dados Abertos CNPJ

Fonte oficial: página “Cadastros” da Receita Federal, seção de Dados Abertos, com o Cadastro Nacional da Pessoa Jurídica.

Uso no projeto: descoberta em lote e atualização periódica de estabelecimentos, empresas, CNAEs, municípios e situação cadastral.

### Consulta oficial de CNPJ

O portal gov.br oferece serviço oficial de consulta de CNPJ e emissão de comprovante de inscrição e situação cadastral.

### Conecta gov.br / API CNPJ

O Catálogo de APIs Governamentais disponibiliza API de Consulta CNPJ para órgãos públicos, com endpoints Básica, QSA e Empresa. A integração exige adesão/credenciais institucionais.

Uso recomendado: verificação on-demand de empresas selecionadas para fiscalização, preservando a carga massiva na base aberta.

### Serpro Consulta CNPJ

Existe oferta comercial de API de Consulta CNPJ para pessoas jurídicas públicas e privadas. Deve permanecer como adaptador opcional para não introduzir custo variável obrigatório.

## 3. CONCLA / IBGE

A CNAE é a classificação oficial para atividades econômicas. A divisão 20 cobre fabricação de produtos químicos e a divisão 21 cobre produtos farmoquímicos e farmacêuticos, mas o universo de fiscalização do CRQ não se limita a essas divisões.

## 4. Sistema CFQ/CRQs

### Resolução CFQ nº 339/2025

Norma vigente de referência para o motor regulatório deste projeto. Consolida atividades econômicas sujeitas ao registro em CRQ e relaciona CNAEs no Anexo I.

A resolução estabelece três pontos fundamentais para o software:

1. CNAE é critério de identificação de atividades potencialmente fiscalizáveis.
2. Pessoas jurídicas cuja atividade básica ou serviço a terceiros esteja relacionado ao Anexo I são candidatas a registro, conforme a norma.
3. O enquadramento efetivo depende da confirmação da atividade pela fiscalização, logo a plataforma não deve “sentenciar” automaticamente.

### CRQ-V

O próprio CRQ-V informa que, quando a atividade principal da empresa envolve Química ou quando há prestação de serviço na área, podem existir obrigações de registro e responsabilidade técnica. A instituição também esclarece que sua função finalística inclui registro e fiscalização de empresas e profissionais no Rio Grande do Sul.

## 5. LGPD / ANPD

Referências:

- Lei nº 13.709/2018.
- Guia Orientativo da ANPD sobre agentes de tratamento e encarregado.
- Guia de Segurança da Informação para agentes de tratamento de pequeno porte.
- Materiais da ANPD sobre segurança, controle de acesso, minimização e resposta a incidentes.

Princípios adotados: finalidade, adequação, necessidade, segurança, prevenção, responsabilização e prestação de contas.

## 6. Decisões de arquitetura derivadas da pesquisa

- Não raspar a página pública da Receita Federal como mecanismo primário de produção.
- Usar Dados Abertos para carga em lote e API oficial para confirmação on-demand.
- Não ingerir QSA por padrão, pois não é necessário ao escopo mínimo e aumenta exposição de dados pessoais.
- Versionar as regras CNAE/CFQ para que mudanças normativas não exijam reescrever o software.
- Exibir sempre fonte, data de atualização e motivo do score.
- Separar “potencial de fiscalização” de “situação jurídica confirmada”.
