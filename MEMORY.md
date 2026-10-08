# VIGIAFAST — memória operacional resumida

**A memória não substitui o GitHub.** Ordem: `docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/CANONICAL_STATE.md` → este arquivo → ADRs → código e CI.

## Produto
- CRISEDIGITAL/VIGIAFAST: plataforma em pt-BR, inicialmente nove clientes, sem limite fixo, com equipe interna e usuários externos autorizados.
- Reutilizar integralmente BrightBean Studio (Django/Python/PostgreSQL, AGPL-3.0), sem prometer descoberta irrestrita nas redes sociais. Obsei e Bellingcat Auto Archiver não foram integrados.
- Evidências privadas nunca em `media_library/`. Não realizar coleta real, deploy ou homologação sem autorização.

## GitHub — reconciliação em 08/10/2026
- `main`: `f6883b747ce1a6ae6a6968948da5225332ed4f2f`.
- Importação BrightBean: `feat/brightbean-upstream-import` @ `da900ea4f6a65963538e5defe7c081122e78dece`.
- PRs #19–#24 integradas na branch de importação. PR #2 continua **aberta/Draft** sobre `main`, sem autorização de merge.
- PR #22 corrigiu diretório `/members/`; PR #24 corrigiu revalidação de `approve_posts` para sessões de portal, já integrada. CI pós-merge da PR #24 ainda não consultada neste ciclo por regra de comunicação manual.
- ADR-0001/0002 aceitas; ADR-0003/0004 propostas, não aceitas.

## Slice atual
- `fix/client-comment-visibility-gate`: fechamento pontual do cenário M24 (`CLIENT` forjando comentário `internal` no POST); preserva `external` e papéis da equipe.
- [Auditoria de código e testes previstos](docs/audits/2026-10-08-client-internal-comment-visibility.md). Oito regressões HTTP sintéticas criadas, mas **não executadas neste chat**; CI ainda sem confirmação.
- Regra: usuário informa `green`/`red`; uma única consulta da CI no SHA correspondente, com JEV consultivo. Nunca merge automaticamente nem alterar `main`, VPS ou dados reais.
