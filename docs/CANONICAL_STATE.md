# VIGIAFAST — estado canônico verificável

**Snapshot:** 2026-10-08, após verificação pontual do GitHub. Sempre reconciliar estado atual antes de agir. **Sem deploy, homologação ou dados de clientes reais.**

## REAL NOW

| Referência | Estado comprovado |
| --- | --- |
| `main` | `f6883b747ce1a6ae6a6968948da5225332ed4f2f` — BrightBean ainda não integrado |
| `feat/brightbean-upstream-import` | `648050ab37525cd596e69b61a600ea09a1503886` (merge PR #31) |
| [PR #2](https://github.com/OARANHA/CRISE/pull/2) | Aberta, Draft, destino `main`; sem autorização de merge |
| [PR #26](https://github.com/OARANHA/CRISE/pull/26) | Integrada à importação; dez caracterizações sintéticas M10; **não corrige M10** |
| [PR #27](https://github.com/OARANHA/CRISE/pull/27) | Integrada à importação; estudo de afiliação independente de role |
| [PR #29](https://github.com/OARANHA/CRISE/pull/29) | Integrada à importação; regra Wandora JEV.1 consultiva em `AGENTS.md`, `PROJECT_SOURCE.md` e memória |
| [PR #28](https://github.com/OARANHA/CRISE/pull/28) | Integrada **somente à importação**; merge SHA `63e0c854e199945435a9c42d5cfe2acfc62611b5`; quatro caracterizações sintéticas M11 |
| [CI pós-merge PR #28 #37866908923](https://github.com/OARANHA/CRISE/actions/runs/37866908923) | Histórico: `completed / success` no SHA `63e0c854...`; **5/5** |
| [PR #30](https://github.com/OARANHA/CRISE/pull/30) | **Integrada apenas à importação**; merge `1e02089d97b72bd5ac2dd8d626a83c6e34d8094c`; [CI pós-merge #37871185545](https://github.com/OARANHA/CRISE/actions/runs/37871185545) `completed/success`, **5/5 no merge SHA** |

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
4. **PR #31 (Draft, documental):** [nota de opções A/B/C](audits/2026-10-08-adr0003-tenancy-deliberation.md) recomenda **uma organização por cliente** como hipótese de decisão. A PR #31 aponta para a branch de importação, sem merge nem CI pós-atualização do seu head confirmada. ADR-0003 **não aceita**; após aprovação, slice M11 primeiro, depois M10, em PRs funcionais separadas.
5. **Limites:** não dar `EDITOR` a operadores reais enquanto M10 não for resolvido e testado; não fazer merge de PR #2 na `main`, deploy, operações destrutivas, uso de dados reais ou coleta real de redes; merge incremental somente com autorização específica; sem polling contínuo de CI.

## UX em revisão (não integrado)

- [Issue #34](https://github.com/OARANHA/CRISE/issues/34): slice funcional de shell/login e dashboard inicial em pt-BR em branch `feat/vigiafast-ux-login-ptbr-v1-20261008`; [auditoria e limites](audits/2026-10-08-ux-vigiafast-access-first-slice.md). Dois testes sintéticos versionados; CI da branch ainda sem resultado confirmado. Não alegar idioma completo ou homologação.
