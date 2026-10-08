# VIGIAFAST — memória operacional resumida

**Não é fonte autônoma de verdade.** Ler [docs/PROJECT_SOURCE.md](docs/PROJECT_SOURCE.md) → [AGENTS.md](AGENTS.md) → [estado canônico](docs/CANONICAL_STATE.md) → ADRs → código/testes/PRs. Revalidar GitHub em toda retomada.

## Produto e limites

- CRISEDIGITAL/VIGIAFAST: inicialmente nove clientes, sem limite rígido; equipe interna, clientes observadores e clientes operadores. Interface pretendida pt-BR.
- BrightBean Studio integral (Django, PostgreSQL, Python), AGPL-3.0. Preservar autenticação, editor, calendário, portal, inbox, analytics, API/MCP e recursos preexistentes.
- Não confundir contas sociais conectadas com descoberta pública de terceiros. Obsei e Bellingcat Auto Archiver **não integrados**. Dados sensíveis e evidências privados fora de `media_library/`; revisão humana em análise jurídica/reputacional.

## Fotografia pontual de 08/10/2026 — confirmar novamente

- `main`: `f6883b7`. Branch de importação após PR #20: `fba74835fb00e14bcaf80e5bf4ef535f9b0d6069`. PR #19 e #20 integradas; PR #2 ainda draft para `main`.
- CI #37814988489 da PR #20 concluída com sucesso no head `d2e9eb0`; **não usar para atestar CI da PR #21**.
- A [matriz documental da PR #21](docs/audits/2026-10-08-authorization-actor-resource-matrix.md) inventaria papéis e exposição por classe de dado; **testes T01–T10 são planejados, não executados nesta entrega**.
- Riscos prioritários: org MEMBER vê diretório de membros de toda O1; EDITOR externo herda acesso a dados INTERNAL; mídia org-shared; fanout Meta em contas duplicadas; portal/sessão pós-mudança de papel; contexto multi-org.
- ADR-0003/0004 permanecem **PROPOSTAS, NÃO ACEITAS**. Nenhuma homologação de isolamento integral, armazenamento privado de evidências ou deploy.

## Próximo gate

Aguardar operador informar `green` ou `red` da PR #21 no SHA exato; **não fazer polling**. Depois realizar testes negativos sintéticos da matriz e priorizar correções **em PRs próprias**, mantendo tenancy pendente de decisão humana. Nenhuma mudança na `main`.
