# SPEC-0014 — Testes e aceite

## Testes obrigatórios

### Funcionais

1. Buscar por CNPJ.
2. Buscar por nome.
3. Filtrar por CNAE.
4. Filtrar por município.
5. Filtrar por porte.
6. Combinar filtros.
7. Exibir situação cadastral.
8. Exibir fonte/timestamp.
9. Exibir justificativa do score.
10. Salvar consulta.
11. Criar lista.
12. Exportar CSV/XLSX.
13. Usar duas sessões simultâneas.
14. Consultar CNPJ on-demand com provider mock/real homologação.
15. Registrar auditoria.

### Segurança

- brute-force/rate limit;
- controle horizontal de acesso;
- CSRF/XSS/SQLi;
- exposição de secrets;
- exportação por usuário sem permissão;
- sessão revogada.

### Desempenho

Base representativa do RS. Rodar teste com pelo menos 20 usuários virtuais e duas consultas simultâneas contínuas.

### Resiliência

- banco reinicia;
- provider CNPJ fica indisponível;
- worker falha no meio da importação;
- storage retorna erro;
- rollback de competência.

## Pacote de aceite

- matriz de requisitos preenchida;
- vídeo curto de demonstração;
- relatório de testes;
- relatório de segurança;
- manual de usuário;
- manual de operação;
- evidência de backup/restore;
- evidência de 2 acessos simultâneos.
