# Roadmap — VIGIAFAST

**Status atualizado em 2026-10-08.** Planejado ≠ entregue; o código BrightBean importado ainda está na PR #2, não na `main`.

## Fase 0 — Fundação canônica
- [x] README e documentação de projeto na `main` (PR #1).
- [x] AGENTS, MEMORY, fonte canônica e ADRs iniciais definidos.
- [ ] Validar a atualização de estado/memória e política de isolamento (ADR-0003 proposta).

## Fase 1 — Aproveitar o BrightBean
- [x] Importar snapshot de 874 arquivos com SHA upstream, licença e comparação byte a byte (PR #2 **draft**).
- [x] CI original: Ruff, Mypy, Pytest/PostgreSQL, Docker build sem push e Gitleaks (PR #3).
- [x] Restringir mídia privada no Caddy e remover configurações demonstrativas do PostgreSQL em Compose (PR #4; smoke tests em CI).
- [x] Unificar identificação de IP do login/API atrás de proxies confiáveis (PR #5).
- [x] Executar 16 testes de isolamento da inbox REST/MCP/HTMX e API keys com clientes A/B/C (PR #6, 16/16 aprovados, 2.364 testes na suíte).
- [x] PR #8: 16 novos casos em posts e mídia A/B/C aprovados na CI (2.380 testes no total); compartilhamento org-shared comprovado, privacidade de evidências ainda pendente.
- [ ] PR #9: validar novos testes de papéis, troca de workspace OAuth/MCP, offboarding e restrição de API keys (CI pendente).
- [x] PR #9: CI aprovada para 10 cenários OAuth/MCP, permissões e offboarding; 2.390 passed / 1 skipped.
- [ ] PR #10: validar sete regressões de API keys com cache já preenchido, revogação e alterações de escopo (CI pendente).
- [ ] Cobrir depois Redis multiworker, tarefas, webhooks, relatórios, downloads e storage privado de evidências.
- [ ] Escolher formalmente o modelo multi-cliente; preservar as capacidades originais e remover riscos de vazamento antes de produção.
- [ ] Integrar PR #2 à `main` somente após revisão dos gates relevantes e autorização.

## Fase 2 — Interface operacional
- [ ] Evoluir o BrightBean com branding **VIGIAFAST**, totalmente em pt-BR, sem remover autenticação, publicação, inbox e analytics existentes.
- [ ] Cadastro/gestão multi-cliente, termos e variantes, ocorrências, responsáveis, alertas e relatórios por cliente.

## Fase 3 — Inteligência e evidências
- [ ] Validar Obsei em pt-BR com revisão humana.
- [ ] Avaliar Auto Archiver, armazenamento privado, hashes e proveniência.
- [ ] Alertas, severidade, histórico e relatórios isolados por cliente.

## Fase 4 — Descoberta externa
- [ ] Conectores de fontes públicas com matriz de acesso, comentários, custos e limites reais.
- [ ] Distinção clara entre contas sociais conectadas e conteúdo de terceiros.
- [ ] Ferramentas opcionais OpenMagpie, 4CAT, Zeeschuimer somente após avaliação técnica/legal.

## Fase 5 — Homologação
- [ ] Revisão LGPD, permissões e credenciais, logs, retenção, backups e testes de restauração.
- [ ] Testes de segurança com múltiplos clientes fictícios e revisão humana das classificações sensíveis.
- [ ] Deploy **somente com autorização específica**. Nunca colocar evidências/clientes reais no GitHub público.

Progresso se comprova por PR, SHA e CI; status atualizado em `docs/CANONICAL_STATE.md`, nunca só em conversas.
