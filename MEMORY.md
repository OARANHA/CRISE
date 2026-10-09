# VIGIAFAST — memória operacional resumida

**Não é fonte de verdade.** Retomada obrigatória: `docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/CANONICAL_STATE.md` → `MEMORY.md` → ADRs → código, testes, Git e CI.

## Produto / reuso
- CRISEDIGITAL / VIGIAFAST: funcionários internos + operadores dos clientes; nove clientes iniciais, com crescimento; interface pt-BR.
- Reusar integralmente BrightBean Studio Django/Python/PostgreSQL, AGPL-3.0: editor, calendário, aprovação, portal, inbox, analytics, mídia editorial, API/MCP e RBAC.
- Obsei / Bellingcat Auto Archiver são candidatos. Sem deploy, dados reais, monitoramento público homologado ou evidências privadas implementadas.

## Estado observado em 2026-10-08
- `main` @ `f6883b747ce1a6ae6a6968948da5225332ed4f2f`, intacta; PR #2 aberta/Draft para `main`.
- `feat/brightbean-upstream-import` @ `63e0c854e199945435a9c42d5cfe2acfc62611b5`, após merge da PR #28. [CI pós-merge #37866908923](https://github.com/OARANHA/CRISE/actions/runs/37866908923) `completed/success`, **5/5** nesse SHA.
- PR #26: 10 casos de caracterização M10; PR #27: estudo de afiliação; PR #29: regra consultiva JEV.1 integrada; PR #28: 4 casos sintéticos M11 e auditoria integrados somente à branch de importação.
- ADR-0001 e 0002 **ACEITAS**; ADR-0003 e 0004 **PROPOSTAS/NÃO ACEITAS**.
- [PR #30](https://github.com/OARANHA/CRISE/pull/30) aberta/não integrada, head `855b7765cf09589d04038fb3092300adfb6c2ae4` e [CI #37867551502](https://github.com/OARANHA/CRISE/actions/runs/37867551502) GREEN 5/5 nesse SHA. Este registro de ADR é trabalho documental **posterior, empilhado sobre PR #30**, não integrado nem validado por aquela CI.

## Riscos / próximo gate
- **M10 aberto:** EDITOR externo continua indistinguível do interno para leitura de comentários, respostas e anexos `INTERNAL`. Afiliação `internal/external/unclassified` por `WorkspaceMembership` é uma **proposta condicional**, não implementada. Não liberar operadores reais como EDITOR.
- **M11 caracterizado:** `OrgMembership` permite multi-org, mas `RBACMiddleware.__call__` usa `.first()` e `last_workspace_id` independentemente, podendo produzir contexto global divergente. A PR #28 confirmou casos sintéticos, **não a operação multi-org completa**.
- M09 (`Post.internal_notes`) e mídia org-shared seguem riscos; evidências privadas dependem da ADR-0004.
- **Deliberação técnica (NÃO ACEITA):** [nota ADR-0003](docs/audits/2026-10-08-adr0003-tenancy-deliberation.md) recomenda **uma organização por cliente** para conter compartilhamento org-wide existente; coordenação interna com memberships explícitas. Aprovação humana da topologia/autoridade e da afiliação `internal/external/unclassified` continua necessária. Depois, menor slice M11 (contexto multi-org); M10 em PR separada, sem política antes da decisão.
- **JEV.1:** consultar em decisões técnicas/arquiteturais como camada consultiva quando disponível; nunca substitui testes, políticas, revisão ou autorização. Sem polling contínuo de CI; usuário comunica `green`/`red`. Sem merge não autorizado, `main` ou deploy.
