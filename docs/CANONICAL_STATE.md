# VIGIAFAST — estado canônico verificável

**Snapshot pontual:** 2026-10-08. Evidências verificadas no GitHub; este arquivo não se atualiza sozinho. Reconciliar o estado real antes de executar ações.

## REAL NOW — referências e CI

| Referência | Estado confirmado |
| --- | --- |
| `main` | `f6883b747ce1a6ae6a6968948da5225332ed4f2f`; BrightBean ainda não integrado |
| `feat/brightbean-upstream-import` | `9beba79939d90242c3f6c7cee508f35f5ecafd77` (merge PR #22) |
| [PR #2](https://github.com/OARANHA/CRISE/pull/2) | Aberta, Draft, base `main`; head atualizado com a branch de importação, **não integrar** nesta fase |
| PRs #19, #20 e #21 | Integradas anteriormente na branch de importação; PR #21 merge `f39f053e136f30acc456fa70a4b6b001990c63ba` |
| [PR #22](https://github.com/OARANHA/CRISE/pull/22) | **Integrada** em `feat/brightbean-upstream-import`; head `5545b297c80b7cbeecb0c0d2331d8b2e10843acf`; merge `9beba79939d90242c3f6c7cee508f35f5ecafd77` |
| [CI PR #22](https://github.com/OARANHA/CRISE/actions/runs/37831790876) | `completed/success` no head `5545b297c80b7cbeecb0c0d2331d8b2e10843acf` |
| [CI pós-merge](https://github.com/OARANHA/CRISE/actions/runs/37833488194) | `completed/success` no merge `9beba79939d90242c3f6c7cee508f35f5ecafd77` |
| Testes da CI pós-merge | Pytest, Ruff, Mypy, Gitleaks e Docker build: **todos sucesso** |
| Deploy | Nenhum autorizado/comprovado; **sem homologação com clientes reais** |

## PROVEN EVIDENCE — implementação limitada

- BrightBean Studio preservado na branch de importação: aplicação Django/Python/PostgreSQL e recursos preexistentes de publicação, editor, calendário, aprovações, inbox, analytics, portal, autenticação/RBAC, mídia e API/MCP. O clone **não** foi integrado à `main`.
- [Matriz de autorização PR #21](audits/2026-10-08-authorization-actor-resource-matrix.md) fornece análise estática para outras superfícies, não um selo de isolamento global.
- [PR #22 / auditoria HTTP](audits/2026-10-08-org-directory-http-reproduction.md): quatro regressões sintéticas demonstraram exposição do diretório `/members/` entre clientes da mesma organização. Correção backend restringe `OrgMembership.MEMBER` aos usuários e vínculos dos workspaces ativos que compartilha, mais a própria identidade. `OWNER/ADMIN` mantêm visão organizacional.
- O arquivo `apps/members/tests/test_client_directory_boundaries.py` cobre **14 testes HTTP sintéticos**, incluindo A/B na mesma organização, C em outra, CLIENT/EDITOR, HTMX, revogação e equipe. A CI completa passou no head e após o merge.
- Os testes **não comprovam** isolamento multi-cliente de toda a aplicação, identidade permanente funcionário/cliente, nem segurança de evidências privadas.

## GAPS → REUSE GATE → DECISION

1. **Modelo de clientes:** [ADR-0003](decisions/ADR-0003-client-isolation-boundaries.md) permanece **PROPOSTA / NÃO ACEITA**. `WorkspaceMembership` e `OrgMembership` são reutilizados; `EDITOR` não identifica de forma confiável funcionário interno versus operador do cliente.
2. **Evidências:** [ADR-0004](decisions/ADR-0004-private-evidence-storage.md) permanece **PROPOSTA / NÃO ACEITA**. Não colocar evidências confidenciais em `media_library/`; armazenamento privado ainda não implementado.
3. **Riscos adicionais:** mídias compartilhadas no escopo organizacional, fanout Meta em contas duplicadas, portal após mudança de papel/revogação, APIs/MCP, workers, notificações e downloads exigem investigação e regressões sintéticas específicas. `portal_reports` não é relatório reputacional completo.
4. **Próxima decisão:** selecionar um único risco não coberto da [matriz PR #21](audits/2026-10-08-authorization-actor-resource-matrix.md), reproduzir por testes sintéticos e propor uma PR pequena reutilizando BrightBean. Não presumir que aceitar ADRs ou ampliar permissões decorra da CI verde da PR #22.
5. **Operação:** não realizar deploy, coleta real de terceiros, homologação de clientes, integração da PR #2 à `main`, alterações em VPS ou operações destrutivas sem autorização específica. O operador informa CI `green`/`red`; **não fazer polling**.

**Decisão deste slice:** sincronização **somente documental** com resultados comprovados da PR #22; nenhum código, permissão, ADR ou arquitetura alterado. Histórico detalhado de falhas intermediárias permanece na [auditoria](audits/2026-10-08-org-directory-http-reproduction.md) e no GitHub.
