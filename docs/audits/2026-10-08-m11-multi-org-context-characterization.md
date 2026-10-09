# M11 — caracterização de contexto multi-organização do BrightBean

**Data:** 2026-10-08. **Base inspecionada:** `feat/brightbean-upstream-import` @ `20fcb3aae63ffc2763939818f36b70841ce1ed0d`.
**Status:** TESTES PROPOSTOS, NÃO EXECUTADOS NESTA INSPEÇÃO. **Não é correção de multi-organização, isolamento ou M10.**
**Escopo:** documentação e testes sintéticos em `apps/members/tests/test_m11_multi_org_context_characterization.py`; nenhum código de aplicação ou migração alterados.

## REAL NOW / PROVEN EVIDENCE

- [PR #27](https://github.com/OARANHA/CRISE/pull/27) integrada somente à branch de importação no SHA `20fcb3...`; [CI pós-merge #37862079868](https://github.com/OARANHA/CRISE/actions/runs/37862079868) terminou `completed/success`, cinco jobs no mesmo SHA.
- `apps/members/models.py`: `OrgMembership` possui unicidade `(user, organization)`, **não unicidade por usuário**; `WorkspaceMembership` possui `(user, workspace)`. O modelo aceita múltiplas associações a organizações para um usuário.
- `apps/members/services.py::accept_invitation` usa `OrgMembership.objects.get_or_create(user=user, organization=invitation.organization)` e associa workspaces. O caminho de convite permite adicionar associação a outra organização no nível da persistência, mas não prova uma experiência multi-org completa ou segura.
- `apps/members/middleware.py::RBACMiddleware.__call__` escolhe a organização global usando `OrgMembership.objects.filter(user=...).first()`. Separadamente, lê `last_workspace_id` para o workspace corrente. **Com duas organizações, os dois contextos podem divergir**; o comentário original do middleware declara suporte a uma organização por usuário na v1.
- `RBACMiddleware.process_view` resolve URL com `workspace_id` usando membership específica; reatribui organização e associação ao workspace da URL. A ausência de membership lança `PermissionDenied`.
- `apps/organizations/views.py::cross_workspace_calendar` utiliza `request.org` para filtrar workspaces. Uma organização global escolhida sem seleção explícita pode alterar a experiência de quem atende clientes em organizações distintas.
- [ADR-0003](../decisions/ADR-0003-client-isolation-boundaries.md) segue PROPOSTA/NÃO ACEITA. [ADR-0004](../decisions/ADR-0004-private-evidence-storage.md) segue PROPOSTA/NÃO ACEITA. M10 continua não corrigido.

## Cenários desta PR — documentação do comportamento, não aprovação de política

| ID | Teste sintético | Comportamento existente esperado |
| --- | --- | --- |
| M11-01 | Operador pertence às organizações O1 e O2; `last_workspace_id` aponta à que não é escolhida por `.first()` | `request.org` e `request.workspace.organization` **divergem** em página global |
| M11-02 | Mesmo operador acessa URL explícita de workspace em O2 | `process_view` escolhe vínculo e organização O2 |
| M11-03 | Mesmo operador tenta workspace sem membership, embora esteja associado à organização | `PermissionDenied` |
| M11-04 | Membership do workspace é revogada entre duas verificações | `process_view` nega a verificação seguinte |

Os quatro testes caracterizam o middleware **diretamente**, sem autenticar no navegador nem exercitar todos os endpoints globais. Se aprovados na CI, provarão apenas os casos acima, não o funcionamento global do produto. São complementares às regressões anteriores de isolamento A/B/C e à caracterização M10 da PR #26.

## Tradeoff relevante para ADR-0003

**Alternativa A — uma organização compartilhada com workspace por cliente:** preserva melhor a navegação global atual, mas `MediaAssetManager.for_workspace_with_shared` permite compartilhamento editorial organizacional entre A/B; diretórios, integrações e demais endpoints exigem auditoria. Workspaces não são barreiras universais de tenant. É preciso decidir quais recursos nunca poderão usar escopo organizacional.

**Alternativa B — uma organização por cliente:** oferece fronteira organizacional explícita para mecanismos que fazem compartilhamento dentro da organização. Contudo, `OrgMembership` multi-org no banco **não basta**: páginas globais, seleção de organização, convite, contexto de API/MCP, permissões, sessão e experiência de funcionário multi-cliente precisam revisão e testes. Não afirmar isolamento completo sem evidência transversal.

**Alternativa C — controle central VIGIAFAST + organizações de clientes:** separação mais nítida de responsabilidades, mas introduz camada de coordenação adicional, que deve ser justificada pelo reuso e não reconstruída antecipadamente.

**Recomendação de engenharia para deliberação:** se o requisito prioritário for separação forte entre empresas independentes, avaliar **uma organização por cliente**, mantendo funcionário interno com memberships explícitas e ampliando somente o necessário para seleção de organização em rotas globais. Isto é **recomendação condicional, não decisão aceita**; o custo de adaptar fluxos atuais e a preservação do BrightBean devem ser aprovados explicitamente. Independentemente da opção, afiliação confiável separada do role continua necessária para corrigir M10.

## REUSE GATE / DECISION

Preservar a autenticação Django, `OrgMembership`, `WorkspaceMembership`, `CustomRole`, serviços de convite, middleware e editor. Não criar novo modelo de tenant, não migrar contas, não alterar a política de mídia editorial, não integrar a PR #2 e não implantar nada.

**Gate de decisão humana:** escolher a topologia de clientes para ADR-0003; aprovar ou rejeitar afiliação `internal/external/unclassified` por membership; definir autoridade de classificação, migração supervisionada e autorização por classe de dados. Só depois implementar controle M10 no runtime, com regressões de preservação das funções BrightBean e A/B/C. 

**Verificações ainda pendentes:** CI desta nova PR sobre SHA exato (Pytest, Ruff, Mypy, Gitleaks, Docker), testes HTTP completos de navegação multi-org, sessões/portal, API keys/MCP e classificação/negativa de INTERNAL. Não fazer polling; operador informa `green`/`red`.
