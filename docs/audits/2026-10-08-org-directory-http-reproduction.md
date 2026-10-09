# PR #22 — Reprodução HTTP sintética do diretório organizacional

**Data:** 2026-10-08. **Base:** `feat/brightbean-upstream-import` @ `f39f053e136f30acc456fa70a4b6b001990c63ba`.
**Status final verificado:** falha reproduzida com cenários sintéticos; correção backend e regressões integradas pela PR #22 na branch de importação em `9beba79939d90242c3f6c7cee508f35f5ecafd77`, após CI verde no head e CI verde pós-merge. Nenhuma execução em produção.

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

- **REAL NOW:** PRs #19–#22 integradas na branch de importação; PR #22 merge `9beba79939d90242c3f6c7cee508f35f5ecafd77`. PR #2 continua Draft para `main`; `main` permanece sem BrightBean.
- **PROVEN EVIDENCE (estática):** `apps/client_portal/views_admin.py::invite_client` solicita `OrgMembership.MEMBER`; `apps/members/views.py::member_list` usa `@require_org_role("member")` e lê todo `OrgMembership` da organização, com vínculos de todos os workspaces não arquivados; `templates/members/partials/member_row.html` renderiza nomes, e-mails e nomes de workspaces.
- **PROVEN EVIDENCE (CI):** workflow [#37824566462](https://github.com/OARANHA/CRISE/actions/runs/37824566462), head `cf2fab265135d20af294f0388bf0c2fa2c73e58c`: pytest 4 falhas, 2447 aprovações, 1 skip; Ruff formatação reprovou arquivo de testes, lint aprovado; mypy/gitleaks aprovados. Falhas de confidencialidade foram esperadas no comportamento anterior.
- **PROVEN EVIDENCE (CI pós-correção):** [#37827220652](https://github.com/OARANHA/CRISE/actions/runs/37827220652), head `6468bbc2cf955324d93565e1b0ab262f484fbec5`: Pytest, mypy, gitleaks e Ruff lint concluídos com sucesso; Ruff format reprovou os dois arquivos Python alterados; Docker skipped. A lógica passou os testes, mas a CI total **não** passou.
- **PROVEN EVIDENCE (CI formato):** [#37830781888](https://github.com/OARANHA/CRISE/actions/runs/37830781888), head `36b67be9b0a1b43db378f67932c037f362d3f7ee`: Pytest, mypy, gitleaks e Ruff lint aprovados; Ruff format reprovou **somente** `apps/members/tests/test_client_directory_boundaries.py`; Docker skipped. Corrigida disposição de chamada `_member` em `test_member_without_workspace_sees_only_own_identity`, não alterando asserções.
- **PROVEN EVIDENCE (CI final):** [#37831790876](https://github.com/OARANHA/CRISE/actions/runs/37831790876), no head `5545b297c80b7cbeecb0c0d2331d8b2e10843acf`, e [CI pós-merge #37833488194](https://github.com/OARANHA/CRISE/actions/runs/37833488194), no merge `9beba79939d90242c3f6c7cee508f35f5ecafd77`: `completed/success`, com Pytest, Ruff, Mypy, Gitleaks e Docker build aprovados.
- **GAP:** identidade persistente de funcionário interno versus cliente externo, outras superfícies de autorização e ADR-0003/ADR-0004 seguem pendentes; CI verde não prova isolamento global.
- **REUSE GATE:** `OrgMembership`, `WorkspaceMembership`, `require_org_role` e testes HTTP Django já existem. Não criar novo RBAC, tenancy ou migração.
- **DECISION:** aplicar escopo já existente de `WorkspaceMembership` apenas para `OrgMembership.MEMBER`, preservando diretório integral para `OWNER/ADMIN`. Permitir que membro veja sua identidade e usuários com workspace explícito em comum, sem exibir vínculos a outros workspaces. Não criar identidade interna nova nem selecionar tenancy.

## Cenário e verificações

`apps/members/tests/test_client_directory_boundaries.py` usa exclusivamente `example.invalid` e nomes sintéticos.

- O1: workspace A (observador `MEMBER/CLIENT`, operador `MEMBER/EDITOR`), workspace B (outro cliente) e funcionário interno com vínculos A+B.
- O2: workspace C com cliente próprio.
- Controles positivos: owner/admin O1 consultam o diretório completo; funcionário com A+B mantém acesso; cliente C não recebe dados de O1.
- Negativos: usuário A não recebe nome/e-mail do cliente B nem nome do workspace B, inclusive HTMX e após revogação de A; conta sem organização é bloqueada; anônimo redirecionado; operações de administração por cliente são negadas.
- A negativa exige filtrar **query e resposta**, não só ocultar elementos do template. A resposta 403/404 sem dados também satisfaz o limite de confidencialidade, mas restringir a interface de funcionários internos seria regressão a avaliar.

## Correção mínima proposta após CI vermelha

`apps/members/views.py::member_list` passa a aplicar ao papel organizacional `MEMBER`:
1. `org_workspaces`: somente workspaces ativos associados ao usuário, dentro da organização atual;
2. `memberships`: somente o próprio usuário ou usuários com participação em um desses workspaces, com `distinct()`;
3. `workspace_memberships` exibidos: limitados aos workspaces visíveis ao leitor;
4. `OWNER/ADMIN`: diretório organizacional e funcionalidades de administração originais permanecem sem alteração.

A regra é de **escopo de recurso** reaproveitando memberships BrightBean, não de inferência de vínculo trabalhista. Um cliente em A pode ver um funcionário que participa de A+B, mas não o nome do workspace B. Sem workspace atual, só pode ver a própria identidade. Esse recorte exige regressão de UI e perfis internos antes de aprovação.

## Escopo e limites

A rota `/members/` é um endpoint Django HTML; caminhos administrativos de HTMX estão sob `apps/members/urls.py` e `require_org_role("admin")`. Inspeção dirigida dos módulos REST `apps/api/routers/me.py`, `accounts.py` e MCP `handlers.py`, `tools.py` não identificou endpoint de listagem de membros organizacionais equivalente. **Isso não substitui inventário completo das superfícies de autorização.**

**Testes locais do executor:** não executados. **CI inicial:** quatro testes negativos falharam, reproduzindo exposição; ver SHA acima. **CI final do head e pós-merge:** todos os cinco jobs aprovados nos SHAs documentados; não afirmar homologação de toda a plataforma. Execução de testes em produção: nenhuma.

**Próximo gate:** revisar compatibilidade da regra com papéis internos e escolher novo cenário adversarial da matriz PR #21, por PR separada; **não aprovar tenancy** por consequência da PR #22. Não realizar deploy, integração em `main` ou uso de dados reais.
