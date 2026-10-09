# VIGIAFAST — memória operacional resumida

**Não é fonte de verdade.** Retomada obrigatória: `docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/CANONICAL_STATE.md` → `MEMORY.md` → ADRs → código, testes, Git e CI.

## Produto / reuso
- CRISEDIGITAL / VIGIAFAST: funcionários internos + operadores dos clientes; nove clientes iniciais, com crescimento; interface pt-BR.
- Reusar integralmente BrightBean Studio Django/Python/PostgreSQL, AGPL-3.0: editor, calendário, aprovação, portal, inbox, analytics, mídia editorial, API/MCP e RBAC.
- Obsei / Bellingcat Auto Archiver são candidatos. Sem deploy, dados reais, monitoramento público homologado ou evidências privadas implementadas.

## Estado observado em 2026-10-08
- `main` @ `f6883b747ce1a6ae6a6968948da5225332ed4f2f`, intacta; PR #2 aberta/Draft para `main`.
- `feat/brightbean-upstream-import` @ `648050ab37525cd596e69b61a600ea09a1503886`, merge PR #31 somente nessa branch. PR #31 CI pré-merge [#37871818043](https://github.com/OARANHA/CRISE/actions/runs/37871818043) GREEN 5/5 em `7ce2acd...`; pós-merge em `648050ab...` não verificada aqui.
- PR #26: 10 casos de caracterização M10; PR #27: estudo de afiliação; PR #29: regra consultiva JEV.1 integrada; PR #28: 4 casos sintéticos M11 e auditoria integrados somente à branch de importação.
- ADR-0001 e 0002 **ACEITAS**; ADR-0003 e 0004 **PROPOSTAS/NÃO ACEITAS**.
- [PR #30](https://github.com/OARANHA/CRISE/pull/30) integrada somente à importação em `1e02089...`, CI pós-merge GREEN 5/5. [PR #31](https://github.com/OARANHA/CRISE/pull/31) também **integrada somente à importação** em `648050ab...`, sem aceitar ADR-0003.
- Programa V1 **sem demonstração**: [issue #32](https://github.com/OARANHA/CRISE/issues/32) e tarefas [#33 segurança](https://github.com/OARANHA/CRISE/issues/33), [#34 UX](https://github.com/OARANHA/CRISE/issues/34), [#35 monitoramento](https://github.com/OARANHA/CRISE/issues/35), [#36 infra/QA](https://github.com/OARANHA/CRISE/issues/36); [plano de execução](docs/V1_EXECUTION_PLAN.md) em PR documental, não implica quatro agentes já rodando.

## Riscos / próximo gate
- **M10 aberto:** EDITOR externo continua indistinguível do interno para leitura de comentários, respostas e anexos `INTERNAL`. Afiliação `internal/external/unclassified` por `WorkspaceMembership` é uma **proposta condicional**, não implementada. Não liberar operadores reais como EDITOR.
- **M11 caracterizado:** `OrgMembership` permite multi-org, mas `RBACMiddleware.__call__` usa `.first()` e `last_workspace_id` independentemente, podendo produzir contexto global divergente. A PR #28 confirmou casos sintéticos, **não a operação multi-org completa**.
- M09 (`Post.internal_notes`) e mídia org-shared seguem riscos; evidências privadas dependem da ADR-0004.
- **Deliberação técnica (NÃO ACEITA):** [nota ADR-0003](docs/audits/2026-10-08-adr0003-tenancy-deliberation.md) recomenda **uma organização por cliente** para conter compartilhamento org-wide existente; coordenação interna com memberships explícitas. Aprovação humana da topologia/autoridade e da afiliação `internal/external/unclassified` continua necessária. Depois, menor slice M11 (contexto multi-org); M10 em PR separada, sem política antes da decisão.
- **JEV.1:** consultar em decisões técnicas/arquiteturais como camada consultiva quando disponível; nunca substitui testes, políticas, revisão ou autorização. Sem polling contínuo de CI; usuário comunica `green`/`red`. Sem merge não autorizado, `main` ou deploy.
