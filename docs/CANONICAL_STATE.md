# VIGIAFAST — estado canônico verificável

**Snapshot pontual:** 2026-10-08. Atualizar após cada PR integrada; confirmar o estado real no GitHub ao retomar. **Não sincronizado automaticamente.**

## REAL NOW — GitHub reconciliado em 08/10/2026

| Referência | Estado verificado |
| --- | --- |
| `main` | `f6883b747ce1a6ae6a6968948da5225332ed4f2f`; BrightBean não integrado |
| `feat/brightbean-upstream-import` | `f39f053e136f30acc456fa70a4b6b001990c63ba` (após merge PR #21) |
| [PR #2](https://github.com/OARANHA/CRISE/pull/2) | Aberta, draft para `main`; **não integrar** nesta fase |
| [PR #19](https://github.com/OARANHA/CRISE/pull/19) | Integrada na branch de importação |
| [PR #20](https://github.com/OARANHA/CRISE/pull/20) | Integrada na branch de importação |
| [PR #21](https://github.com/OARANHA/CRISE/pull/21) | Integrada; head `1c45f4a6d32a010361d9a38511918286138dd2a9`; merge `f39f053e136f30acc456fa70a4b6b001990c63ba` |
| [CI PR #21](https://github.com/OARANHA/CRISE/actions/runs/37819894602) | `completed/success` no head exato `1c45f4a6d32a010361d9a38511918286138dd2a9` |
| [CI PR #22 anterior](https://github.com/OARANHA/CRISE/actions/runs/37824566462) | head `cf2fab265135d20af294f0388bf0c2fa2c73e58c`: 2447 pass, 4 fail, 1 skip; Ruff format falhou; mypy/gitleaks aprovados |
| [CI PR #22 correção](https://github.com/OARANHA/CRISE/actions/runs/37827220652) | head `6468bbc2cf955324d93565e1b0ab262f484fbec5`: Pytest, mypy e gitleaks **aprovados**, Ruff lint aprovado, **Ruff format reprovou 2 arquivos**, Docker skipped |
| Deploy | Nenhum autorizado/comprovado; sem homologação para clientes reais |

## PROVEN EVIDENCE — capacidades e limites

- BrightBean importado mantém Django/Python/PostgreSQL e os fluxos de editor/publicação, calendário, inbox, analytics, aprovações, portal, autenticação/RBAC, mídia e API/MCP. Não reconstruir.
- [Matriz PR #21](audits/2026-10-08-authorization-actor-resource-matrix.md): revisão **estática** de identidade × papel × ação × recurso × escopo; nenhuma regressão nova executada neste slice documental, nenhuma política alterada.
- `OrgMembership`/`WorkspaceMembership`/`CustomRole` já dão permissões por papel, mas não representam de modo confiável a distinção entre funcionário interno VIGIAFAST e operador do cliente com papel `EDITOR`.
- Na hipótese de organização única, `/members/` permite a `OrgMembership.MEMBER` consultar diretório e vínculos de toda organização; convite de cliente cria esse papel. Exposição **reproduzida pelos quatro testes de confidencialidade na CI inicial**; correção de escopo no backend passou Pytest na CI posterior, mas ainda sem CI geral verde.
- Mídia org-shared e fanout de identificador Meta duplicado continuam riscos conhecidos. PRs #6–#19 provam somente cenários localizados.
- `portal_reports` é placeholder, sem relatório reputacional operacional.
- ADR-0001 e ADR-0002 **aceitas**; [ADR-0003](decisions/ADR-0003-client-isolation-boundaries.md) e [ADR-0004](decisions/ADR-0004-private-evidence-storage.md) **propostas, NÃO ACEITAS**.

## Reprodução HTTP em andamento — PR #22

- [Diagnóstico HTTP e correção por workspace](audits/2026-10-08-org-directory-http-reproduction.md): teste sintético confirmou falhas da política anterior; correção mínima `MEMBER` baseada em `WorkspaceMembership` passou os testes Pytest no head `6468bbc2`, restando formatação Ruff; novo commit de formatação requer CI nova.
- Confirmar correção no novo SHA antes de integrar; não alterar tenancy, autenticação ou modelo RBAC sem autoridade.

## GAPS → REUSE GATE → DECISION

1. Primeiro executar cenários sintéticos A/B na mesma organização e C em outra (T01–T10 da matriz), sobretudo diretório organizacional, classes INTERNAL, papel de cliente editor, portal ativo/revogado, API/MCP, webhooks, mídia e notificações.
2. Preservar o BrightBean e a AGPL-3.0; qualquer vulnerabilidade reproduzida pede PR funcional pequena **separada** da matriz.
3. Sem aprovação de tenancy, sem evidências privadas em `media_library/`, sem clientes reais, coleta social, deploy ou integração da PR #2 à `main`.
4. A PR #21 foi integrada e a CI de seu head concluiu com sucesso. A PR #22 introduziu casos HTTP sintéticos T01/T10: execução inicial reproduziu quatro falhas esperadas e revelou falha de Ruff format; a correção passou Pytest na CI seguinte, mas Ruff format reprovou dois arquivos; correção de formato requer nova CI. Sem polling.

**Histórico anterior:** Git/PR #19–#20 e [arquivo anterior](historico/2026-10-08-estado-canonico-anterior.md). Documentos históricos não são autoridade para estado atual.
