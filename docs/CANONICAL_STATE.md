# VIGIAFAST — estado canônico verificável

**Snapshot:** 2026-10-08. O conteúdo é pontual e deve ser reconciliado com GitHub antes de qualquer ação.

## REAL NOW — repositório e integrações

| Referência | Estado observado |
| --- | --- |
| `main` | `f6883b747ce1a6ae6a6968948da5225332ed4f2f` — BrightBean não integrado |
| `feat/brightbean-upstream-import` | `da900ea4f6a65963538e5defe7c081122e78dece` — merge PR #24 |
| [PR #2](https://github.com/OARANHA/CRISE/pull/2) | Aberta em Draft; base `main`; não integrar automaticamente |
| PRs #19–#24 | Integradas somente à branch de importação |
| [PR #24](https://github.com/OARANHA/CRISE/pull/24) | Merge confirmado no SHA `da900ea4f6a65963538e5defe7c081122e78dece` |
| CI da PR #24 | Pré-merge: registrada como aprovada no handoff anterior; CI **pós-merge não verificada** nesta retomada |
| Branch de trabalho | `fix/client-comment-visibility-gate` — slice M24 proposto; CI ainda não verificada |
| Deploy/homologação | Nenhum autorizado ou comprovado; sem clientes reais |

## PROVEN EVIDENCE

- Base BrightBean Studio (Django/Python/PostgreSQL, AGPL-3.0) preservada na branch de importação com editor, calendário, aprovação, inbox, analytics, portal, mídias, API/MCP e RBAC. Presença no código não equivale a homologação funcional completa.
- [PR #22 / auditoria de diretório](audits/2026-10-08-org-directory-http-reproduction.md): defesa do diretório `/members/` por vínculo de workspace para org members; 14 regressões sintéticas documentadas e CI aprovada no respectivo SHA.
- [PR #24 / aprovação em sessão ativa](audits/2026-10-08-portal-approval-live-permissions.md): `portal_approval_required` reutiliza `WorkspaceMembership.effective_permissions` nas quatro ações POST de aprovação, incluindo revogação/downgrade. Não refazer essa correção.
- **Novo slice em revisão:** [auditoria M24](audits/2026-10-08-client-internal-comment-visibility.md) comprova por inspeção fluxo de `visibility=internal` não autorizado de `CLIENT` para `PostComment`; branch dedicada adiciona gate de escrita e oito testes HTTP sintéticos. **Testes ainda não executados/CI pendente de comunicação manual.** O risco foi identificado por leitura estática, não por exploração HTTP executada.

## GAPS → REUSE GATE → DECISION

1. [ADR-0001](decisions/ADR-0001-brightbean-foundation.md) e [ADR-0002](decisions/ADR-0002-canonical-documentation.md) são **aceitas**. [ADR-0003](decisions/ADR-0003-client-isolation-boundaries.md) e [ADR-0004](decisions/ADR-0004-private-evidence-storage.md) seguem **propostas/não aceitas**.
2. Identidade funcionário interno × cliente operador ainda não é atributo confiável; `EDITOR` externo e classes internas requerem política aprovada e testes específicos. Não alterar tenancy ou interpretação de `EDITOR` no slice M24.
3. Mídia org-shared, possível fanout Meta por conta duplicada, REST/MCP, notificações, downloads e armazenamento privado de evidências seguem sem homologação global. Proibido colocar evidências privadas em `media_library/`.
4. A próxima ação é aguardar `green`/`red` informado pelo operador **para a branch M24**, validar uma única vez Pytest, Ruff, Mypy, Gitleaks e Docker no SHA exato, revisar resultados e pedir autorização explícita para qualquer merge.
5. Não realizar deploy, uso de clientes reais, coleta social, alteração da VPS ou integração da PR #2 à `main` sem autorização específica.
