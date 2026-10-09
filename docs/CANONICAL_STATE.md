# VIGIAFAST — estado canônico verificável

**Snapshot:** 2026-10-08, revisão direta do GitHub antes da reconciliação da PR #28. Revalidar SHA/CI após qualquer novo commit. **Sem deploy, clientes reais ou homologação.**

## REAL NOW

| Referência | Estado verificado |
| --- | --- |
| `main` | `f6883b747ce1a6ae6a6968948da5225332ed4f2f`; importação não integrada |
| `feat/brightbean-upstream-import` | `16be52b3ced02ce25881ce4dc3c98c1cff75a1d7` (após merge PR #29) |
| [PR #2](https://github.com/OARANHA/CRISE/pull/2) | Aberta/Draft para `main`; não autorizada para merge |
| [PR #27](https://github.com/OARANHA/CRISE/pull/27) | Integrada à branch de importação; documentação de afiliação M10 |
| [PR #29](https://github.com/OARANHA/CRISE/pull/29) | Integrada **somente** à importação; regra Wandora JEV.1 registrada em `AGENTS.md`, `docs/PROJECT_SOURCE.md`, `MEMORY.md` |
| [CI pós-merge PR #29](https://github.com/OARANHA/CRISE/actions/runs/37864930016) | `completed / success`, 5/5 no SHA `16be52b3...` |
| [PR #28](https://github.com/OARANHA/CRISE/pull/28) | Testes M11 e auditoria; **reconciliação de conflitos em sua própria branch**, sem merge na importação |
| [CI original PR #28](https://github.com/OARANHA/CRISE/actions/runs/37863411779) | `completed / success`, 5/5 no SHA antigo `a98b35a...`. **Não valida SHA novo da reconciliação** |

## PROVEN EVIDENCE

- BrightBean Studio Django/Python/PostgreSQL AGPL-3.0 presente apenas na branch da PR #2; recursos existentes preservados, sem homologação.
- M10: PR #26 acrescentou testes de caracterização; EDITOR externo continua capaz de ler comentários/replies/anexos `INTERNAL` no comportamento atual. PR #27 comparou alternativas de afiliação sem implementar alteração. **M10 NÃO CORRIGIDO**.
- M11: `OrgMembership` aceita múltiplas organizações por usuário, mas `RBACMiddleware.__call__` escolhe organização global via `.first()` separadamente de `last_workspace_id`; URL explícita com `workspace_id` revalida membership. Quatro testes de caracterização, sem mudança runtime. [Auditoria M11](audits/2026-10-08-m11-multi-org-context-characterization.md).
- `MediaAssetManager.for_workspace_with_shared` permite compartilhamento editorial por organização, não autoriza compartilhamento de evidências privadas. M09 (`Post.internal_notes`) permanece risco separado.
- Wandora JEV.1 é **camada consultiva** obrigatória quando disponível, conforme `AGENTS.md`; julgamento probabilístico não substitui código, testes, doutrina ou autorização. PR #29 integrada.

## GAPS → REUSE GATE → DECISION

1. ADR-0001/0002 ACEITAS; [ADR-0003](decisions/ADR-0003-client-isolation-boundaries.md) e [ADR-0004](decisions/ADR-0004-private-evidence-storage.md) **PROPOSTAS/NÃO ACEITAS**.
2. A topologia de clientes e afiliação confiável `internal/external/unclassified` independente de role são propostas a deliberar; não implementar política INTERNAL nem migração sem decisão explícita.
3. Reusar `User`, `OrgMembership`, `WorkspaceMembership`, `CustomRole`, middleware, convites e editor BrightBean; não refazer RBAC.
4. **Próximo gate:** conferir a CI no novo SHA da PR #28 depois da reconciliação de conflitos, por aviso `green`/`red` do operador. A CI original não vale para esse novo SHA. Merge da PR #28 exige autorização específica.
5. Sem merge em `main` ou PR #2, deploy, dados reais, alteração de outro sistema, aprovação automática de ADR ou polling contínuo.
