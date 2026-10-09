# VIGIAFAST — estado canônico verificável

**Snapshot:** 2026-10-08, após verificação pontual do GitHub. Sempre reconciliar estado atual antes de agir. **Sem deploy, homologação ou dados de clientes reais.**

## REAL NOW

| Referência | Estado comprovado |
| --- | --- |
| `main` | `f6883b747ce1a6ae6a6968948da5225332ed4f2f` — BrightBean ainda não integrado |
| `feat/brightbean-upstream-import` | `63e0c854e199945435a9c42d5cfe2acfc62611b5` |
| [PR #2](https://github.com/OARANHA/CRISE/pull/2) | Aberta, Draft, destino `main`; sem autorização de merge |
| [PR #26](https://github.com/OARANHA/CRISE/pull/26) | Integrada à importação; dez caracterizações sintéticas M10; **não corrige M10** |
| [PR #27](https://github.com/OARANHA/CRISE/pull/27) | Integrada à importação; estudo de afiliação independente de role |
| [PR #29](https://github.com/OARANHA/CRISE/pull/29) | Integrada à importação; regra Wandora JEV.1 consultiva em `AGENTS.md`, `PROJECT_SOURCE.md` e memória |
| [PR #28](https://github.com/OARANHA/CRISE/pull/28) | Integrada **somente à importação**; merge SHA `63e0c854e199945435a9c42d5cfe2acfc62611b5`; quatro caracterizações sintéticas M11 |
| [CI pós-merge #37866908923](https://github.com/OARANHA/CRISE/actions/runs/37866908923) | `completed / success` no SHA exato `63e0c854...`; **5/5:** Pytest, Ruff, Mypy, Gitleaks, Docker |
| [PR #30](https://github.com/OARANHA/CRISE/pull/30) | **Aberta, não integrada**, head `855b7765cf09589d04038fb3092300adfb6c2ae4`; [CI #37867551502](https://github.com/OARANHA/CRISE/actions/runs/37867551502) `completed/success`, **5/5 no head** |

## PROVEN EVIDENCE

- BrightBean Studio Django/Python/PostgreSQL, licença AGPL-3.0, está na branch de importação ligada à PR #2; recursos existentes de editor, calendário, aprovações, portal, inbox, analytics, mídia, API/MCP e RBAC preservados. CI e testes sintéticos **não são homologação operacional**.
- **M10 aberto:** `WorkspaceMembership` não diferencia, de modo verificável e independente do role, funcionário interno VIGIAFAST de operador externo com `EDITOR`. Os testes da PR #26 caracterizam a visibilidade atual de comentários, respostas e anexos `INTERNAL` a ambos. PR #27 apenas propôs alternativas arquiteturais; não implementou correção.
- **M11 caracterizado:** testes sintéticos da PR #28 verificam a divergência possível entre `request.org` global e organização de `last_workspace_id` com usuário multi-org; o `process_view` revalida membership de URL explícita, nega workspace sem vínculo e nega acesso após revogação. Isso **não comprova operação multi-org completa** de interfaces, rotas globais, API/MCP ou clientes reais. Ver [auditoria M11](audits/2026-10-08-m11-multi-org-context-characterization.md).
- Compartilhamento de `MediaAsset` editorial por organização continua no BrightBean: workspaces da mesma organização não fornecem isolamento universal. M09 (`Post.internal_notes`) continua risco específico. Storage privado de evidências ainda requer decisão [ADR-0004](decisions/ADR-0004-private-evidence-storage.md).
- **Wandora JEV.1:** regra consultiva já integrada pela PR #29 e aplicável a decisões técnicas e arquiteturais quando disponível. Julgamentos probabilísticos não substituem código, testes, doutrina ou autorização humana.

## GAPS → REUSE GATE → DECISION

1. **ADRs:** ADR-0001 e ADR-0002 ACEITAS; [ADR-0003](decisions/ADR-0003-client-isolation-boundaries.md) e [ADR-0004](decisions/ADR-0004-private-evidence-storage.md) **PROPOSTAS / NÃO ACEITAS**.
2. **Gate prioritário:** deliberar topologia multi-cliente (organização por cliente vs. workspaces em organização compartilhada), afiliação verificada `internal/external/unclassified` separada do role, autoridade de classificação/auditoria, usuários legados e acesso a dados `INTERNAL`. **Não inferir aceitação da ADR por CI verde**.
3. **Reuso:** preservar `User`, `OrgMembership`, `WorkspaceMembership`, `CustomRole`, middleware, convites, sessões, editor, portal e filtros existentes; não reconstruir RBAC. Fazer inventário/experimentos de segurança com usuários sintéticos A/B/C antes de qualquer migração/política de runtime.
4. **Deliberação ADR-0003 documentada, não aceita:** [nota de opções A/B/C](audits/2026-10-08-adr0003-tenancy-deliberation.md) recomenda **uma organização por cliente**, condicionada a decisão explícita; interface central opcional sem acesso implícito. Gate funcional inicial proposto após aprovação: corrigir contexto multi-org M11; depois M10 afiliação e política `INTERNAL`, com PRs/testes separados. Nenhum runtime alterado.
5. **Limites:** não dar `EDITOR` a operadores reais enquanto M10 não for resolvido e testado; não fazer merge de PR #2 na `main`, deploy, operações destrutivas, uso de dados reais ou coleta real de redes; merge incremental somente com autorização específica; sem polling contínuo de CI.
