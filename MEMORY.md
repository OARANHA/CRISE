# VIGIAFAST — memória operacional resumida

**Não é fonte de verdade.** Ordem: `docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/CANONICAL_STATE.md` → esta memória → ADRs → código/testes/CI.

## Produto / reuso
- CRISEDIGITAL / VIGIAFAST: nove clientes inicialmente, escalável, operação interna e operadores externos; interface pt-BR.
- Preservar integralmente BrightBean Studio Django/Python/PostgreSQL, AGPL-3.0: editor, calendário, aprovações, portal, inbox, analytics, mídia editorial, API/MCP, RBAC.
- Obsei e Bellingcat Auto Archiver são candidatos; dados privados, monitoramento de terceiros e evidências não estão homologados.

## Estado observado 2026-10-08
- `main`: `f6883b747ce1a6ae6a6968948da5225332ed4f2f` (preservada); PR #2 segue Draft.
- `feat/brightbean-upstream-import`: `16be52b3ced02ce25881ce4dc3c98c1cff75a1d7`; PR #29 integrada, [CI pós-merge #37864930016](https://github.com/OARANHA/CRISE/actions/runs/37864930016) GREEN 5/5 nesse SHA.
- PR #28 tem quatro testes sintéticos M11 e auditoria; CI original [#37863411779](https://github.com/OARANHA/CRISE/actions/runs/37863411779) GREEN no SHA `a98b35a...`, mas reconciliação com PR #29 **exige CI nova** antes de qualquer integração. Nenhum merge da PR #28 autorizado.
- ADR-0001/0002 aceitas; ADR-0003/0004 propostas e **não aceitas**.

## Segurança e próximo gate
- M10 **não corrigido**: EDITOR interno e externo indistinguíveis para `INTERNAL`. Afiliação verificada independente de role continua somente proposta; sem atribuir EDITOR a operadores reais enquanto não houver política testada.
- M11 caracteriza que `RBACMiddleware` pode discordar entre `request.org` global e organização do `last_workspace_id` para operador multi-org. Não muda runtime nem valida toda interface. Topologia por cliente ainda depende da decisão ADR-0003.
- M09 (`Post.internal_notes`) separado; ADR-0004 para evidências privadas pendente. Sem dados reais, deploy ou `main`.
- **Wandora JEV.1**: consultar como camada consultiva para decisões técnicas/arquiteturais quando disponível (AGENTS.md e PROJECT_SOURCE.md); não substitui políticas, testes ou autorização. Indisponibilidade declarada; nunca inventar parecer.
- Não fazer polling de CI: operador informa `green`/`red` e revisamos o SHA exato. Próximo passo: testar PR #28 reconciliada; merge requer autorização específica.
