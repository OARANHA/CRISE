# Segurança pontual — ações de aprovação com sessão de portal ativa

**Data:** 2026-10-08. **Base:** `feat/brightbean-upstream-import` @ `e142acdaf0902a53040498c43abeb02c9fcbe936`.
**Estado:** correção e regressões propostas em branch de revisão, **sem execução local de Django/PostgreSQL, sem resultado de CI desta mudança e sem merge**.
**Matriz:** M06/M07, T05 e T09 em `2026-10-08-authorization-actor-resource-matrix.md`. ADR-0003/0004 continuam propostas.

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

- **Comportamento identificado por inspeção estática:** `apps/client_portal/decorators.py::portal_auth_required` verifica sessão e existência de `WorkspaceMembership`, mas não `approve_posts`. Em `apps/client_portal/views.py`, os POSTs `portal_approve`, `portal_request_changes`, `portal_reject` e `portal_request_hold` chamam serviços sem verificar permissão atual. Os serviços de `apps/approvals/services.py` realizam transições de status, sem gate de RBAC próprio. A leitura estática indica que uma sessão emitida quando o papel era CLIENT poderia continuar acionando transições após downgrade a EDITOR ou VIEWER, mantendo a associação.
- **Impacto:** ação editorial de aprovação/suspensão fora das permissões atuais do usuário, mesmo sem cruzar workspaces. Não é uma evidência de exploração em produção.
- **Reuso:** `WorkspaceMembership.effective_permissions` já contempla `BUILTIN_ROLE_PERMISSIONS` e `CustomRole.permissions`. As ações de equipe em `apps/approvals/views.py` já exigem `approve_posts`.
- **Decisão do slice:** criar `portal_approval_required`, compondo `portal_auth_required` com checagem de `request.portal_membership.effective_permissions["approve_posts"]`. Aplicar apenas nos quatro POSTs do portal, sem alterar listagem, papéis, modelos de tenancy ou serviços editoriais.
- **Testes propostos:** em `apps/client_portal/test_portal_approval_permissions.py`, sessão ativa com papel CLIENT alterado para EDITOR/VIEWER; `CustomRole` sem permissão; `CustomRole` com permissão; quatro ações permitidas para CLIENT; UUID de post em B (mesma organização) ou C (outra); revogação de membership. Testes negativos verificam HTTP e **ausência de mutação/ApprovalAction**. Todos os atores e publicações são sintéticos.
- **Riscos residuais:** identidade persistente interna versus externa, leitura de dados internos por EDITOR, org-shared media, endpoints REST/MCP e portal em outros fluxos. Este slice não aprova ADR-0003/0004 nem substitui testes globais.

## Validação e gates

Leitura estática do código comprovada. O código de regressão ainda depende de Pytest/PostgreSQL, Ruff, Mypy, Gitleaks e Docker no SHA efetivo da PR. **Não afirmar teste executado nem CI verde para a nova alteração antes da execução verificada.** Não realizar deploy, acesso a clientes reais ou merge automático. Manter `main` e a PR #2 intocadas.
