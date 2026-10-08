# VIGIAFAST — memória operacional resumida

**Não é fonte autônoma de verdade.** Ler [docs/PROJECT_SOURCE.md](docs/PROJECT_SOURCE.md) → [AGENTS.md](AGENTS.md) → [estado canônico](docs/CANONICAL_STATE.md) → ADRs → código/testes/PRs. Revalidar GitHub em toda retomada.

## Produto e limites

- CRISEDIGITAL/VIGIAFAST: inicialmente nove clientes, sem limite rígido; equipe interna, clientes observadores e clientes operadores. Interface pretendida pt-BR.
- BrightBean Studio integral (Django, PostgreSQL, Python), AGPL-3.0. Preservar autenticação, editor, calendário, portal, inbox, analytics, API/MCP e recursos preexistentes.
- Não confundir contas sociais conectadas com descoberta pública de terceiros. Obsei e Bellingcat Auto Archiver **não integrados**. Dados sensíveis e evidências privados fora de `media_library/`; revisão humana em análise jurídica/reputacional.

## Fotografia de 08/10/2026 — confirmar ao retomar

- `main` `f6883b7`; importação `f39f053e136f30acc456fa70a4b6b001990c63ba` (PRs #19–#21 integradas); PR #2 continua draft para `main`.
- CI PR #21 run `37819894602`: `completed/success` no head `1c45f4a6d32a010361d9a38511918286138dd2a9`. **Não prova T01–T10.**
- PR #22 em teste: `apps/members/tests/test_client_directory_boundaries.py` adiciona negativas HTTP sintéticas para `/members/`, HTMX, A/B em O1, C em O2, CLIENT/EDITOR, revogação e controles positivos de equipe. **Resultados ainda pendentes de CI**. Ver [auditoria](docs/audits/2026-10-08-org-directory-http-reproduction.md).
- Riscos adicionais de classes INTERNAL, mídia org-shared, fanout Meta e portal revogado permanecem no [inventário PR #21](docs/audits/2026-10-08-authorization-actor-resource-matrix.md).
- ADR-0003 e ADR-0004 **PROPOSTAS/NÃO ACEITAS**; sem tenancy aprovado, evidências privadas ou deploy.

## Próximo gate

Aguardar operador comunicar `green` ou `red` da PR #22; conferir pontualmente CI no head exato, sem polling. Reproduzir ou descartar exposição HTTP e só então considerar correção mínima backend, preservando BrightBean e papéis internos. Nunca modificar `main`.
