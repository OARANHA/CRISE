# VIGIAFAST — estado canônico verificável

**Snapshot pontual:** 2026-10-08. Atualizar após cada PR integrada; confirmar o estado real no GitHub ao retomar. **Não sincronizado automaticamente.**

## REAL NOW — GitHub confirmado antes da PR #21

| Referência | Estado comprovado |
| --- | --- |
| `main` | `f6883b747ce1a6ae6a6968948da5225332ed4f2f`; BrightBean não integrado |
| `feat/brightbean-upstream-import` | `fba74835fb00e14bcaf80e5bf4ef535f9b0d6069`; base da inspeção da matriz |
| [PR #2](https://github.com/OARANHA/CRISE/pull/2) | Aberta, draft, direcionada à `main`; **não integrar** nesta fase |
| [PR #19](https://github.com/OARANHA/CRISE/pull/19) | Integrada à branch de importação; merge `0bf37c52b73e4d08996017e081c47138dd568ac8` |
| [PR #20](https://github.com/OARANHA/CRISE/pull/20) | Integrada à branch de importação; merge `fba74835fb00e14bcaf80e5bf4ef535f9b0d6069` |
| [CI da PR #20 #37814988489](https://github.com/OARANHA/CRISE/actions/runs/37814988489) | Concluída com sucesso no head `d2e9eb0833def2d1da74471957b034ec6ac7a9ba`; cinco jobs, conforme validação anterior |
| Deploy | Nenhum deploy autorizado ou comprovado; não homologado para clientes reais |

## PROVEN EVIDENCE — capacidades e limites

- BrightBean importado mantém Django/Python/PostgreSQL e os fluxos de editor/publicação, calendário, inbox, analytics, aprovações, portal, autenticação/RBAC, mídia e API/MCP. Não reconstruir.
- [Matriz PR #21](audits/2026-10-08-authorization-actor-resource-matrix.md): revisão **estática** de identidade × papel × ação × recurso × escopo; nenhuma regressão nova executada neste slice documental, nenhuma política alterada.
- `OrgMembership`/`WorkspaceMembership`/`CustomRole` já dão permissões por papel, mas não representam de modo confiável a distinção entre funcionário interno VIGIAFAST e operador do cliente com papel `EDITOR`.
- Na hipótese de organização única, `/members/` permite a `OrgMembership.MEMBER` consultar diretório e vínculos de toda organização; convite de cliente cria esse papel. É **risco baseado em código**, ainda sem reprodução HTTP sintética nesta PR.
- Mídia org-shared e fanout de identificador Meta duplicado continuam riscos conhecidos. PRs #6–#19 provam somente cenários localizados.
- `portal_reports` é placeholder, sem relatório reputacional operacional.
- ADR-0001 e ADR-0002 **aceitas**; [ADR-0003](decisions/ADR-0003-client-isolation-boundaries.md) e [ADR-0004](decisions/ADR-0004-private-evidence-storage.md) **propostas, NÃO ACEITAS**.

## GAPS → REUSE GATE → DECISION

1. Primeiro executar cenários sintéticos A/B na mesma organização e C em outra (T01–T10 da matriz), sobretudo diretório organizacional, classes INTERNAL, papel de cliente editor, portal ativo/revogado, API/MCP, webhooks, mídia e notificações.
2. Preservar o BrightBean e a AGPL-3.0; qualquer vulnerabilidade reproduzida pede PR funcional pequena **separada** da matriz.
3. Sem aprovação de tenancy, sem evidências privadas em `media_library/`, sem clientes reais, coleta social, deploy ou integração da PR #2 à `main`.
4. A PR #21 é documental e aguarda CI no **seu próprio head**, comunicada pelo operador (sem polling). Não interpretar sua CI como execução dos testes adversariais planejados.

**Histórico anterior:** Git/PR #19–#20 e [arquivo anterior](historico/2026-10-08-estado-canonico-anterior.md). Documentos históricos não são autoridade para estado atual.
