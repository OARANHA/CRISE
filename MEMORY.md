# VIGIAFAST — memória operacional resumida

**Não é fonte de verdade.** Consultar `docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/CANONICAL_STATE.md` → esta memória → ADRs → código/testes/CI.

## Produto
- CRISEDIGITAL / VIGIAFAST: inicialmente nove clientes com crescimento possível, funcionários internos e usuários de clientes; interface pt-BR.
- Preservar integralmente BrightBean Studio Django/Python/PostgreSQL (AGPL-3.0); não reconstruir editor, portal, aprovações, inbox, analytics, API/MCP, RBAC etc.
- Obsei e Bellingcat Auto Archiver são candidatos; não há coleta social real ou armazenamento privado de evidências implementado/homologado.

## Estado verificado em 08/10/2026
- `main`: `f6883b747ce1a6ae6a6968948da5225332ed4f2f`, preservada.
- Branch de importação: `feat/brightbean-upstream-import` @ `84139275e16efcd2201191275b24cc9ea3513fa6`.
- PRs #19–#25 integradas na branch de importação. PR #2 **aberta e Draft** para main, não integrada.
- PR #25: merge confirmado; CI pós-merge #37848566089 no SHA exato, 5/5 jobs success. Nenhum deploy conhecido ou autorizado.
- ADR-0001/0002 aceitas; ADR-0003/0004 propostas e não aceitas.

## Slice M10 — aguardando execução de testes
- [Auditoria M10](docs/audits/2026-10-08-m10-editor-internal-visibility.md): filtros de comentários/replies/anexos INTERNAL protegem CLIENT, mas não distinguem EDITOR interno versus EDITOR operador do cliente.
- Testes sintéticos de caracterização em branch separada, **sem alteração das permissões de produção**. Resultado CI do novo SHA ainda não verificado; um teste verde não resolve o desvio da política VIGIAFAST.
- Não conceder papel EDITOR a usuário de cliente real até política decidida e implementada. Sem dados reais, deploy, polling de CI ou merge sem autorização.
