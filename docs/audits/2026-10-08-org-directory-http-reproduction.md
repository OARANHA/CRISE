# PR #22 — Reprodução HTTP sintética do diretório organizacional

**Data:** 2026-10-08. **Base:** `feat/brightbean-upstream-import` @ `f39f053e136f30acc456fa70a4b6b001990c63ba`.
**Status:** casos de regressão escritos; execução HTTP/PostgreSQL e comportamento observado **PENDENTES de CI**. Este documento não afirma exploração reproduzida.

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

- **REAL NOW:** PRs #19, #20, #21 integradas na branch de importação; PR #2 ainda draft para `main`; `main` permanece sem BrightBean.
- **PROVEN EVIDENCE (estática):** `apps/client_portal/views_admin.py::invite_client` solicita `OrgMembership.MEMBER`; `apps/members/views.py::member_list` usa `@require_org_role("member")` e lê todo `OrgMembership` da organização, com vínculos de todos os workspaces não arquivados; `templates/members/partials/member_row.html` renderiza nomes, e-mails e nomes de workspaces.
- **GAP:** ainda não há reprodução por resposta HTTP autenticada, nem identidade persistente distinguindo funcionário interno de cliente externo. A ADR-0003 e a ADR-0004 continuam propostas.
- **REUSE GATE:** `OrgMembership`, `WorkspaceMembership`, `require_org_role` e testes HTTP Django já existem. Não criar novo RBAC, tenancy ou migração.
- **DECISION:** adicionar testes *red-first* sem alterar produção. Apenas uma falha real comprovada justifica avaliar correção mínima e sua compatibilidade com papéis internos; caso a correção dependa de política não aprovada, submeter a decisão à revisão humana.

## Cenário e verificações

`apps/members/tests/test_client_directory_boundaries.py` usa exclusivamente `example.invalid` e nomes sintéticos.

- O1: workspace A (observador `MEMBER/CLIENT`, operador `MEMBER/EDITOR`), workspace B (outro cliente) e funcionário interno com vínculos A+B.
- O2: workspace C com cliente próprio.
- Controles positivos: owner/admin O1 consultam o diretório completo; funcionário com A+B mantém acesso; cliente C não recebe dados de O1.
- Negativos: usuário A não recebe nome/e-mail do cliente B nem nome do workspace B, inclusive HTMX e após revogação de A; conta sem organização é bloqueada; anônimo redirecionado; operações de administração por cliente são negadas.
- A negativa exige filtrar **query e resposta**, não só ocultar elementos do template. A resposta 403/404 sem dados também satisfaz o limite de confidencialidade, mas restringir a interface de funcionários internos seria regressão a avaliar.

## Escopo e limites

A rota `/members/` é um endpoint Django HTML; caminhos administrativos de HTMX estão sob `apps/members/urls.py` e `require_org_role("admin")`. Inspeção dirigida dos módulos REST `apps/api/routers/me.py`, `accounts.py` e MCP `handlers.py`, `tools.py` não identificou endpoint de listagem de membros organizacionais equivalente. **Isso não substitui inventário completo das superfícies de autorização.**

**Testes locais:** não executados (repositório completo não disponível no executor local). **CI da PR #22:** verificar uma única vez após comunicação `green`/`red` do operador, correlacionando head SHA. Falha dos negativos é esperada na implementação original, mas **não deve ser declarada observada antes da execução**.

**Próximo gate:** analisar relatório de testes do SHA da PR, registrar evidência HTTP e então decidir a menor correção backend sem aprovar tenancy. Não realizar deploy, integração em `main` ou uso de dados reais.
