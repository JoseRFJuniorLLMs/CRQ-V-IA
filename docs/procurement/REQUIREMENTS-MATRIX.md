# Matriz de aderência ao Pregão Eletrônico nº 0005/2026

| ID | Requisito | Implementação proposta | Evidência de aceite |
|---|---|---|---|
| TR-001 | Identificar empresas com potencial de atuação na área da Química no RS | Motor regulatório CNAE + Resolução CFQ 339/2025 + score explicável | Busca retorna empresas do RS e exibe motivo da seleção |
| TR-002 | Filtros por setor | CNAE principal/secundário, divisão, grupo, classe, subclasses e categorias regulatórias | Demonstração funcional |
| TR-003 | Filtros por região | UF, município, região imediata/intermediária, CEP e listas salvas | Demonstração funcional |
| TR-004 | Filtros por porte | Campo de porte da RFB, capital social e faixas configuráveis | Demonstração funcional |
| TR-005 | Outros parâmetros de fiscalização | situação cadastral, data de abertura, CNAE secundário, risco, score, fonte, última atualização | Demonstração funcional |
| TR-006 | Verificar situação cadastral de CNPJ | Base aberta RFB + adaptador Conecta gov.br/Serpro para consulta on-demand | Tela da empresa mostra situação, fonte e timestamp |
| TR-007 | 2 acessos simultâneos | Licença lógica sem limite inferior a 2; teste concorrente com 2 sessões independentes | Teste de aceitação |
| TR-008 | LGPD | Minimização, RBAC, logs, criptografia, retenção e resposta a incidentes | Checklist de segurança e LGPD |
| TR-009 | Disponibilidade adequada | Health checks, monitoramento, backups, deploy redundante quando contratado | Relatório de disponibilidade |
| TR-010 | Suporte durante vigência | Canal de suporte, classificação de incidentes, registro de tickets e SLA interno | Plano de suporte |
| TR-011 | Solução digital sem infraestrutura local específica | Aplicação web responsiva e hospedada em cloud | Acesso por navegador moderno |
| TR-012 | Entrega após formalização | Provisionamento automatizado de tenant, usuários e credenciais | Checklist de onboarding |
| TR-013 | Credenciais e orientações de uso | Convite de usuários + manual + tour inicial | Manual e e-mail de ativação |
| TR-014 | Comunicação de falhas | Incidentes operacionais com aviso ao fiscal do contrato | Log de incidentes e modelo de comunicação |
| TR-015 | Dados em formato eletrônico | Exportação CSV/XLSX/PDF e listas salvas | Exportação funcional |
| TR-016 | 12 meses | Configuração de contrato/tenant com vigência e renovação | Tela administrativa |

## Critérios internos de qualidade

Além do mínimo editalício, o projeto adota metas internas de engenharia para reduzir risco de rejeição:

- P95 de buscas comuns abaixo de 1,5 s na base do RS.
- 99,5% de disponibilidade mensal, excluídas janelas previamente comunicadas.
- Backup diário, RPO alvo de 24 h e RTO alvo de 4 h.
- Toda empresa exibida com `source_updated_at`, `source_name` e `rule_version`.
- Nenhuma classificação regulatória sem justificativa legível por humano.
