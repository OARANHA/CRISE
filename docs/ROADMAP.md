# Roadmap — VIGIAFAST

Roadmap é planejamento, **não comprovação de recursos entregues**. Manter status e PRs vinculados a cada fase.

## Fase 0 — Fundamentos documentais
- [x] Criar README público sem dados sensíveis.
- [x] Integrar documentação canônica e memória na main pela PR #1 (`f6883b747ce1a6ae6a6968948da5225332ed4f2f`).
- [ ] Estabelecer critérios objetivos de aceite e matriz de risco.

## Fase 1 — Importar e preservar BrightBean
- [x] Copiar snapshot integral para a branch de importação com upstream fixado e avisos de licença; **merge pendente**.
- [x] Baseline em CI: 2.337 passed, 1 skipped; lint, tipos, migrações, Docker e Gitleaks verdes.
- [ ] Validar comportamento real de RBAC, workspaces, inbox e API/MCP.
- [x] CI baseline da PR #3 validada e integrada à branch de importação.
- [ ] Validar PR #4: mídia privada no Caddy e segredos/portas no Compose.

## Fase 2 — Operação simples para equipe
- [ ] Rebrand total da interface para VIGIAFAST em pt-BR, sem remover funcionalidade original.
- [ ] Cadastro multi-cliente, termos monitorados, prioridades e responsáveis.
- [ ] Módulo de ocorrências, notas, atribuições e histórico auditável.

## Fase 3 — Inteligência e evidências
- [ ] Prova de conceito Obsei com classificação contextual pt-BR e revisão humana.
- [ ] Prova de conceito Auto Archiver com hashes e storage protegido.
- [ ] Alertas e relatórios por cliente, sem vazamento inter-tenant.

## Fase 4 — Descoberta pública validada
- [ ] Pesquisa de menções por nome/variações em fontes públicas e APIs permitidas.
- [ ] Monitoramento de URLs conhecidas e coleta documentada de comentários disponíveis.
- [ ] Matriz por rede: cobertura, disponibilidade, limites, custo, LGPD e testes.

## Fase 5 — Homologação / produção
- [ ] Auditoria, backups/restauração, retenção, observabilidade e testes com dados sintéticos.
- [ ] Autorizações específicas para credenciais reais e deploy isolado.
- [ ] Treinamento da equipe e operação supervisionada.

**Regra:** nenhuma fase avança por descrição em chat; anexar PR/commit, testes e evidências em `docs/CANONICAL_STATE.md`.

## Checkpoints complementares — outubro/2026
- [x] PR #4, hardening Caddy e Compose validado e integrado na branch de importação.
- [ ] PR #5, resolver IP por proxy confiável e regressões — aguardar CI.
- [ ] Gate: autorização e vazamento entre clientes via UI, API, MCP, workers, cache, arquivos e evidências.

## Gate de isolamento — PR #6 (a validar)
- [x] PR #5 corrigida e aprovada na CI da branch de importação: 2.348 passed, 1 skipped.
- [ ] Executar testes adversariais da PR #6 (clientes sintéticos A/B/C, REST/MCP/HTMX).
- [ ] Expandir testes para posts, mídia, workers, cache, notificações, OAuth e evidências.
- [ ] Definir arquitetura oficial: nove clientes como workspaces distintos em uma organização; validar com ADR.
