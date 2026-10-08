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
- [x] PR #9: CI aprovada para 10 cenários OAuth/MCP, permissões e offboarding; 2.390 passed / 1 skipped.
- [x] PR #10: sete regressões de API keys com cache preenchido aprovadas (CI #37773171776; 2.397 passed / 1 skipped).
- [x] PR #11: três cenários Meta webhook com ID nativo distinto/repetido aprovados (CI #37778759366; 2.400 passed / 1 skipped).
- [x] PR #12: cinco regressões de inbox em tarefas de fundo aprovadas (CI #37784489968; 2.405 passed / 1 skipped).
- [x] PR #13: notificação de responsáveis revogados/outro workspace corrigida e aprovada (CI #37787128260; 2.413 passed / 1 skipped, 8 novos testes).
- [ ] Cobrir depois Redis multiworker, demais tarefas, webhooks, relatórios, downloads e storage privado de evidências.
- [x] PR #15: requisitos para cliente observador/operador no portal (CI #37799250321 verde, documentação integrada; ADR-0003 ainda proposta).
- [ ] PR #16: proteção de comentários internos e anexos por URL no portal do cliente, seis casos sintéticos (CI pendente).
- [ ] Escolher formalmente o modelo multi-cliente; preservar as capacidades originais e remover riscos de vazamento antes de produção.
- [ ] Integrar PR #2 à `main` somente após revisão dos gates relevantes e autorização.

## Fase 2 — Interface operacional
- [ ] Evoluir o BrightBean com branding **VIGIAFAST**, totalmente em pt-BR, sem remover autenticação, publicação, inbox e analytics existentes.
- [ ] Cadastro/gestão multi-cliente, termos e variantes, ocorrências, responsáveis, alertas e relatórios por cliente.
- [ ] Reutilizar portal BrightBean para clientes observadores; validar cliente operador com editor/contributor/custom roles e preservar ocultação de comentários internos (sem prometer relatórios já prontos).
- [ ] Testes de autorização e desligamento na navegação cliente/operador antes de conceder trabalho dentro do workspace.

## Fase 3 — Inteligência e evidências
- [ ] Validar Obsei em pt-BR com revisão humana.
- [x] PR #14: proposta documental ADR-0004 integrada à branch de importação (CI #37789363791 aprovada); ADR ainda NÃO ACEITA, storage NÃO implementado.
- [ ] Avaliar Auto Archiver, implementar armazenamento privado após aceitação das ADRs, hashes e proveniência.
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
