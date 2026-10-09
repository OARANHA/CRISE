# VIGIAFAST — estado canônico verificável

**Snapshot:** 2026-10-08, após consulta pontual ao GitHub. Reconciliar antes de agir. **Sem deploy, dados reais ou homologação de clientes.**

## REAL NOW

| Referência | Estado confirmado |
| --- | --- |
| `main` | `f6883b747ce1a6ae6a6968948da5225332ed4f2f`; BrightBean não integrado |
| `feat/brightbean-upstream-import` | `20fcb3aae63ffc2763939818f36b70841ce1ed0d` |
| [PR #2](https://github.com/OARANHA/CRISE/pull/2) | Aberta e Draft para `main`; não integrada |
| [PR #27](https://github.com/OARANHA/CRISE/pull/27) | Integrada somente à branch de importação, merge `20fcb3aae63ffc2763939818f36b70841ce1ed0d` |
| [CI pós-merge #37862079868](https://github.com/OARANHA/CRISE/actions/runs/37862079868) | `completed / success`, 5/5 (Pytest, Mypy, Ruff, Gitleaks e Docker) no SHA do merge #27 |
| Slice em preparação M11 | [Caracterização multi-organização](audits/2026-10-08-m11-multi-org-context-characterization.md) e quatro testes sintéticos em branch separada; **CI própria não verificada**, sem mudança de runtime |

## PROVEN EVIDENCE

- BrightBean Studio Django/Python/PostgreSQL, AGPL-3.0, importado na branch da PR #2; editor, calendário, portal, inbox, analytics, mídia editorial, API/MCP e RBAC existentes preservados. Código/CI sintética não equivale a homologação.
- PRs #22, #24 e #25 contêm controles pontuais de diretório, aprovações e clientes `CLIENT`. [M10](audits/2026-10-08-m10-editor-internal-visibility.md) foi **caracterizado** na PR #26; dez testes sintéticos demonstram que EDITOR interno e EDITOR externo permanecem indistinguíveis para conteúdo INTERNAL. **M10 NÃO CORRIGIDO.**
- [PR #27](https://github.com/OARANHA/CRISE/pull/27) documentou [proposta de afiliação](audits/2026-10-08-m10-actor-affiliation-architecture-gate.md): `WorkspaceMembership` registra papel/permissões, mas não afiliação verificada independente do role. Proposta condicional: `internal/external/unclassified` por vínculo, concedida por autoridade confiável e avaliada com ação/recurso/cliente/classe de dado.
- Novo diagnóstico estático M11: `OrgMembership` aceita múltiplas organizações para um usuário; `RBACMiddleware.__call__` usa `OrgMembership.objects.filter(user=...).first()` em páginas globais e `last_workspace_id` separadamente. O contexto de organização pode divergir do workspace atual. `process_view` resolve organização da URL com workspace explícito. **Testes sintéticos adicionados, sem resultado de CI ainda**.
- Compartilhamento `MediaAsset` por organização permanece no código original; não representa isolamento garantido entre workspaces. M09 (`Post.internal_notes`) é risco separado. Armazenamento de evidências privadas ainda não foi implementado.

## GAPS → REUSE GATE → DECISION

1. ADR-0001/0002 **ACEITAS**. [ADR-0003](decisions/ADR-0003-client-isolation-boundaries.md) e [ADR-0004](decisions/ADR-0004-private-evidence-storage.md) **PROPOSTAS/NÃO ACEITAS**.
2. É preciso decidir entre organização compartilhada com workspaces e organizações separadas por cliente. A segunda melhora a fronteira de mídia organizacional, mas depende de contexto multi-org e fluxo central adequados; a primeira exige limites adicionais para mídias compartilhadas e dados entre clientes.
3. Reusar `User`, `OrgMembership`, `WorkspaceMembership`, `CustomRole`, middleware, sessões, convites, RBAC, editor e portal. Não reconstruir nem modificar política sem aprovação.
4. Próximo gate: validar CI da caracterização M11 (operador avisa `green`/`red`); depois deliberar explicitamente topologia, afiliação e política de INTERNAL da ADR-0003, antes de implementar M10 em runtime.
5. Sem merge na `main`, merge da PR #2, deploy, dados reais, alteração de outras aplicações ou polling contínuo. Merge de PR incremental somente com autorização expressa.
