# VIGIAFAST — memória operacional resumida

**Memória não é fonte de verdade.** Ao retomar, ler `docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/CANONICAL_STATE.md` → este arquivo → ADRs → código, testes e GitHub. Conferir o SHA atual; não reutilizar cegamente este snapshot.

## Produto e limites
- CRISEDIGITAL / VIGIAFAST: plataforma interna em pt-BR, inicialmente nove clientes, sem limite rígido, com equipe interna e usuários de clientes observadores/operadores.
- Base integral BrightBean Studio (Django, Python, PostgreSQL, AGPL-3.0). Preservar funções existentes; não confundir contas sociais conectadas com descoberta pública de terceiros. Obsei e Bellingcat Auto Archiver **não integrados**.
- Não usar `media_library/` para evidências privadas; classificação jurídico-reputacional exige revisão humana. Nenhum deploy ou homologação com clientes reais.

## GitHub verificado em 08/10/2026
- `main`: `f6883b747ce1a6ae6a6968948da5225332ed4f2f` (sem BrightBean); branch import `feat/brightbean-upstream-import`: `e142acdaf0902a53040498c43abeb02c9fcbe936`.
- PRs #19–#23 integradas **somente na branch de importação**. [PR #2](https://github.com/OARANHA/CRISE/pull/2) continua **Draft**, base `main`, **não integrada**.
- [PR #22](https://github.com/OARANHA/CRISE/pull/22): corrigiu `/members/` para membros organizacionais usando workspaces explicitamente associados, preservando o acesso `OWNER/ADMIN`. [Auditoria e 14 testes sintéticos](docs/audits/2026-10-08-org-directory-http-reproduction.md).
- CI [#37831790876](https://github.com/OARANHA/CRISE/actions/runs/37831790876) passou no head `5545b297`; CI pós-merge [#37833488194](https://github.com/OARANHA/CRISE/actions/runs/37833488194) passou no merge `9beba799`. Todos os cinco jobs da CI pós-merge concluíram com sucesso.
- [CI após PR #23](https://github.com/OARANHA/CRISE/actions/runs/37835321028): sucesso no SHA `e142acdaf0902a53040498c43abeb02c9fcbe936` (Pytest, Ruff, Mypy, Gitleaks e Docker).
- A CI verde é **localizada**: não prova tenancy global, segurança de evidências privadas, nem prontidão de produção.

## Próximo gate
- ADR-0003 (limites multi-cliente) e ADR-0004 (evidências privadas) seguem **PROPOSTAS / NÃO ACEITAS**.
- Slice isolado proposto: revalidar `approve_posts` em quatro ações POST do portal após downgrade de papel/sessão existente. Ver `docs/audits/2026-10-08-portal-approval-live-permissions.md`. Novos testes ainda não executados; aguardar `green`/`red` da CI da nova PR.
- O operador informa `green`/`red`; conferir CI **uma vez** no SHA da PR, sem polling, sem merges automáticos. Não modificar `main`, PR #2 ou VPS sem autorização.
