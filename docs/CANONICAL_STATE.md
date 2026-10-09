# VIGIAFAST — estado canônico verificável

**Snapshot:** 2026-10-08, após verificação direta do GitHub. Reconciliar antes de cada novo ciclo. **Sem deploy, homologação ou clientes reais.**

## REAL NOW

| Referência | Estado comprovado |
| --- | --- |
| `main` | `f6883b747ce1a6ae6a6968948da5225332ed4f2f`, BrightBean não integrado |
| `feat/brightbean-upstream-import` | `e5f9ec7c6568729bc26220f1ab44b156bc7d6477` |
| [PR #2](https://github.com/OARANHA/CRISE/pull/2) | Aberta, Draft, base `main`; sem autorização para merge |
| [PR #26](https://github.com/OARANHA/CRISE/pull/26) | Integrada **somente** à branch de importação em 2026-10-08, merge commit `e5f9ec7...` |
| [CI pós-merge PR #26](https://github.com/OARANHA/CRISE/actions/runs/37858665680) | `completed / success`, SHA `e5f9ec7...`; cinco jobs success: Pytest, Ruff, Mypy, Gitleaks e Docker |
| [PR #28](https://github.com/OARANHA/CRISE/pull/28) | Aberta para branch de importação; head `a98b35a0d73bb3247f48e049ee157e29283a9b7e`; quatro testes sintéticos M11 de contexto multi-organização |
| [CI PR #28](https://github.com/OARANHA/CRISE/actions/runs/37863411779) | `completed / success`, 5/5 (Pytest, Ruff, Mypy, Gitleaks e Docker), validada no head `a98b35a...`; **sem merge** |
| Trabalho de processo atual | Regra consultiva Wandora JEV.1 adicionada a `AGENTS.md`, `docs/PROJECT_SOURCE.md` e `MEMORY.md` em branch isolada; CI desta proposta não verificada |

## PROVEN EVIDENCE

- BrightBean (Django/Python/PostgreSQL, AGPL-3.0) importado na branch da PR #2; editor, calendário, aprovações, inbox, analytics, portal, mídia editorial, API/MCP e RBAC originais preservados. Código existente/CI sintética não equivale a homologação de clientes reais.
- PR #22: defesa pontual do diretório organizacional; PR #24: autorização atual nas quatro ações de aprovação; PR #25: bloqueio de comentário INTERNAL forjado pelo papel CLIENT. Reutilizar; não refazer.
- [M10 — caracterização](audits/2026-10-08-m10-editor-internal-visibility.md): os dez testes sintéticos da PR #26 caracterizam o estado **ainda vulnerável** quando ator interno e operador externo usam EDITOR. A CI inicial [#37856628216](https://github.com/OARANHA/CRISE/actions/runs/37856628216) foi RED por duas falhas de conexão fechada em testes de streaming e formatação Ruff; correção dos testes, CI posterior e merge constam na PR #26. O acesso a comentários/replies/anexos INTERNAL por EDITOR **não foi corrigido**.
- `apps/members/models.py::WorkspaceMembership` contém papel funcional e permissões, mas não afiliação verificável `interno/externo`; `get_comments_for_post` e `comment_attachment` usam role CLIENT para ocultar INTERNAL. O portal filtra EXTERNAL independentemente do papel na sessão própria.
- `apps/api/routers/posts.py` usa `create_posts` para acesso a `Post.internal_notes` (**M09 separado**). `MediaAssetManager.for_workspace_with_shared` compartilha mídia editorial por organização; não usar esse caminho para evidências privadas.

## JEV — apoio consultivo

- Solicitação de 2026-10-08: consultar Wandora JEV.1 nas decisões técnicas/arquiteturais quando disponível; não delegar autorização, políticas ou avaliação de testes a julgamentos probabilísticos. Regra documentada nesta branch, **sem integração/CI própria confirmada**.
- JEV consultado nesta etapa (`jev_route_task` → `split_task`, confiança 0,48; `jev_guard_action` → `allow`, confiança 0,49). Foi decidido separar validação da PR #28 e nova PR documental. Parecer consultivo, não aprovação para merge.

## GAPS → REUSE GATE → DECISION

1. ADR-0001 e ADR-0002 **ACEITAS**. [ADR-0003](decisions/ADR-0003-client-isolation-boundaries.md) (tenancy/identidade) e [ADR-0004](decisions/ADR-0004-private-evidence-storage.md) (evidências privadas) **PROPOSTAS/NÃO ACEITAS**.
2. Afiliação verificada do ator independente do papel e autorização por classe de dado **não implementadas**. O M10 ainda permite que EDITOR externo acesse INTERNAL nas rotas caracterizadas.
3. Reusar Django sessions, `OrgMembership`, `WorkspaceMembership`, `CustomRole`, middleware, isolamento por workspace e mecanismos de permissões existentes; não reconstruir editor, portal ou RBAC.
4. **Proposta técnica, não decisão aceita:** afiliação `internal/external/unclassified` independente no vínculo de workspace, atribuída por autoridade confiável; sem inferência automática por papel; predicado central por ator, ação, recurso, workspace e confidencialidade. Ver [auditoria de alternativas](audits/2026-10-08-m10-actor-affiliation-architecture-gate.md).
5. **GATE:** antes de implementar classificação/migração/política, deliberar ADR-0003 (inclusive topologia multi-cliente, migração e acessos legados). ADR-0004 segue pendente. Até haver política testada, não conceder EDITOR a operadores de clientes reais.
6. Sem merge em `main`, sem integração da PR #2, sem deploy, sem dados reais, sem coleta social, sem polling de CI; merges de PRs incrementais somente com autorização expressa.
