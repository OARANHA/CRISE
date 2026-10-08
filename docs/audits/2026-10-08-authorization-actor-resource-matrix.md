# PR #21 — Matriz de autorização: identidade × papel × ação × recurso × escopo

**Data da inspeção:** 2026-10-08. **Base examinada:** `feat/brightbean-upstream-import` @ `fba74835fb00e14bcaf80e5bf4ef535f9b0d6069`.
**Natureza:** análise estática + plano de testes sintéticos. **Nenhum teste novo foi executado nesta entrega; nenhuma rota ou política foi modificada.**
**Autoridade:** complemento técnico à [ADR-0003](../decisions/ADR-0003-client-isolation-boundaries.md), que continua **PROPOSTA/NÃO ACEITA**. Não é homologação.

## 1. Contrato de atores e escopo

- **Identidade/afiliação (política VIGIAFAST ainda não representada como atributo confiável):** funcionário interno, cliente observador, cliente operador e serviço autorizado. Não confundir `User.is_staff` (Django admin) ou `OrgMembership.org_role` com prova de vínculo empregatício VIGIAFAST.
- **Papel/escopo existente:** `OrgMembership` por usuário+organização; `WorkspaceMembership` por usuário+workspace com `workspace_role` e `CustomRole.permissions`; `Workspace.organization` delimita organização. Um usuário pode ter vários vínculos a workspaces, mas um papel base por vínculo. Papel `EDITOR` não informa se a pessoa é interna ou do cliente.
- **Operação permitida (política-alvo, não implementada):** exige **identidade aprovada + associação ao recurso/cliente + capacidade por ação + classe de dado + estado de sessão/token**, verificadas no backend e não apenas na navegação.
- **Referências de teste:** A e B são workspaces distintos na organização O1; C é workspace da organização O2; I_A é funcionário interno explicitamente associado a A; O_A é cliente observador de A (`CLIENT`); E_A e T_A são clientes operadores de A (`EDITOR` e `CONTRIBUTOR`); I_AB tem associações explícitas a A e B; X_A é usuário removido de A. Criar somente fixtures sintéticas.

## 2. Inventário de reuso confirmado no código

| Capacidade preservada | Implementação verificada | Limite para o produto |
| --- | --- | --- |
| Identidade e vínculos | `apps/accounts/models.py::User`; `apps/organizations/models.py::Organization`; `apps/workspaces/models.py::Workspace`; `apps/members/models.py::{OrgMembership,WorkspaceMembership,CustomRole}` | Não há identidade persistente `internal/customer` própria do VIGIAFAST; `CustomRole` dá permissões, não afiliação |
| Hierarquias e permissões | `apps/members/models.py::BUILTIN_ROLE_PERMISSIONS`; `apps/members/decorators.py::{require_org_role,require_workspace_role,require_permission}` | `require_workspace_role` compara a ordem de papéis, inclusive `CLIENT > VIEWER`; sua docstring menciona equivalência custom, mas o código compara somente `workspace_role` |
| Contexto | `apps/members/middleware.py::RBACMiddleware` | A organização global é escolhida por `.first()`; URLs de workspace resolvem vínculo específico; multi-organização ainda não é fluxo comprovado |
| Editor / calendário / aprovações | `apps/composer/views.py`; `apps/calendar/views.py`; `apps/approvals/{views,comments,services}.py` | Alguns caminhos filtram informação interna apenas quando papel literal é `CLIENT` ou `VIEWER`; `EDITOR` externo exige fronteira de dados adicional |
| Portal | `apps/client_portal/{decorators,services,views,views_admin}.py` | Link mágico novo exige papel `CLIENT`; sessão pré-existente pode persistir após troca de papel; `portal_reports` é placeholder |
| Inbox / analytics | `apps/inbox/views.py`; `apps/analytics/views.py`; `apps/api/routers/{inbox,analytics}.py` | `EDITOR` inclui `use_inbox`, `reply_from_inbox` e `view_analytics`; inbox de equipe inclui notas internas; testar exposição por classe de dado |
| Mídia editorial | `apps/media_library/managers.py::for_workspace_with_shared`; `apps/media_library/views.py`; `apps/api/routers/media.py`; `apps/mcp/handlers.py` | `workspace_id=NULL` e mesma organização são compartilhados intencionalmente; prefixo `media_library/` é público para publicação, jamais para evidências |
| Chaves API e MCP | `apps/api_keys/{services,views}.py`; `apps/api/auth.py::{ApiKeyAuth,McpAuth}`; `apps/mcp/handlers.py` | Token restringe workspace, contas e permissões; OAuth MCP seleciona workspace ativo; teste de revogação e troca de contexto permanece necessário |
| Webhook Meta | `apps/social_accounts/models.py`; `apps/inbox/webhooks.py::_process_meta_events` | Mesmo identificador nativo em workspaces distintos da mesma org pode replicar eventos, comprovado em teste existente |

Permissões base reutilizáveis de `apps/members/models.py`:
`create_posts`, `edit_others_posts`, `approve_posts`, `publish_directly`,
`manage_social_accounts`, `view_analytics`, `use_inbox`, `reply_from_inbox`,
`manage_workspace_settings`, `upload_media`, `edit_media`, `delete_media`, `manage_media`.
O papel `CLIENT` tem `approve_posts` e `view_analytics`; `EDITOR` tem `create_posts`, `view_analytics`, `use_inbox` e `reply_from_inbox`; `CONTRIBUTOR` tem `create_posts`, mas não inbox/analytics. Estes são **defaults de papel**, não decisões de liberar classes de dados ao cliente.

## 3. Matriz ator × ação × recurso × escopo × decisão esperada

**Legenda:** P = permitir com condição indicada; N = negar; G = gate/decisão humana pendente. Resultados são **esperados pelo VIGIAFAST**, não alegações de que todas as rotas já cumprem o contrato. Para N, aceitar 403, 404 ou redirecionamento seguro sem conteúdo/efeitos; verificar HTTP conforme endpoint.

| ID | Identidade / papel | Ação → recurso / classe de dado | Escopo | Esperado | Situação e referência |
| --- | --- | --- | --- | --- | --- |
| M01 | I_A / EDITOR | Criar/editar post editorial | A | P | `create_posts`, `composer/views.py::compose/save_post` |
| M02 | I_A / EDITOR | Consultar/editar post por UUID | B ou C | N | Middleware + `Post.objects.for_workspace`; regressão transversal pendente |
| M03 | I_AB / EDITOR | Trabalhar em post editorial | A e B atribuídos | P | Vínculos explícitos; rever troca de workspace |
| M04 | O_A / CLIENT | Consultar fila e publicados no portal | A, dados externos | P | `client_portal/views.py::portal_approval_queue/portal_published` |
| M05 | O_A / CLIENT | Ler portal / post por UUID de B/C | B ou C | N | `portal_workspace`, filtros de Post; teste direto |
| M06 | O_A / CLIENT | Aprovar item pendente do portal | A | P, com direito de aprovação atual | Portal checa sessão+vínculo; ação não revalida `approve_posts` |
| M07 | O_A / CLIENT revogado | Aprovar ou ler portal em sessão aberta | A | N | `portal_auth_required` revalida vínculo; testar transição, sessão e role |
| M08 | E_A / EDITOR, cliente | Editar conteúdo autorizado | A | P | `create_posts`; fluxo de login/permissão cliente operador não homologado |
| M09 | E_A / EDITOR, cliente | Ler `internal_notes` de post | A | N | **Divergência potencial:** `composer/views.py` e `api/routers/posts.py` associam acesso a papel/`create_posts` |
| M10 | E_A / EDITOR, cliente | Ler comentário interno/reply/anexo interno | A | N | **Divergência potencial:** `approvals/comments.py::get_comments_for_post` e `approvals/views.py::comment_attachment` negam somente papel literal `CLIENT` |
| M11 | O_A / CLIENT | Ler comentário/reply interno no portal | A | N | `client_portal/views.py` filtra EXTERNAL de forma incondicional; testes existentes |
| M12 | T_A / CONTRIBUTOR, cliente | Criar conteúdo, sem aprovar/publicar | A | P só ao criar | `BUILTIN_ROLE_PERMISSIONS`; negativos para `approve_posts`/`publish_directly` |
| M13 | E_A / EDITOR, cliente | Ler ou responder inbox/DM sensível | A | G (padrão N até autorização específica por classe) | Default EDITOR permite inbox e reply; `inbox/views.py::_detail_context` inclui notas internas |
| M14 | O_A / CLIENT | Ler/responder inbox de equipe | A/B/C | N | Default CLIENT não tem `use_inbox`/`reply_from_inbox` |
| M15 | I_A / permissão `view_analytics` | Ver analytics de conta permitida | A | P | `api/routers/analytics.py` valida permissão e allowlist |
| M16 | O_A / CLIENT | Analytics editorial autorizado | A | P só classes liberadas | Papel tem `view_analytics`; conferir rotas de UI sem decorator explícito |
| M17 | Qualquer cliente de A | Consultar analytics, inbox ou calendário por UUID B/C | B/C | N | Testes negativos em HTTP, HTMX, REST e MCP |
| M18 | I_A / papel editorial | Ler mídia exclusiva de workspace | A | P segundo permissão | `media_library/views.py` e `api/routers/media.py` |
| M19 | O_A ou E_A / cliente | Ler mídia org-shared não autorizada | O1, fora de A | N na política-alvo | **Divergência existente:** `for_workspace_with_shared` e `shared_library_index` |
| M20 | O_A ou E_A / cliente | Listar pessoas/workspaces de B | O1 | N | **Divergência por inspeção:** `members/views.py::member_list` permite org `member` e lista toda O1 |
| M21 | O_A ou E_A / cliente | Emitir/editar API key para B | B | N | `api_keys/services.py` exige `manage_api_keys` org e vínculo ao workspace |
| M22 | I_A / token de A | Buscar post/inbox/analytics com identificador de B | B/C | N | `api/routers` + `mcp/handlers.py`; testes existentes parciais |
| M23 | X_A / token API/OAuth revogado/desvinculado | Continuar lendo/escrevendo | A | N | `api/auth.py` e `api_keys/services.py`; testar cache, sessão e concorrência |
| M24 | Usuário de A / CLIENT ou EDITOR | Criar comentário `INTERNAL` forjado | A | N para cliente externo | `approvals/views.py::add_comment` recebe `visibility` do POST; verificação de identidade pendente |
| M25 | Qualquer cliente | Ler/baixar evidência reputacional confidencial | A/B/C | N até módulo e autorização aprovados | ADR-0004 não implementada; nunca usar `media_library/` |
| M26 | Serviço webhook Meta | Vincular mensagem à conta cliente correta | A sem contaminar B/C | P somente vínculo autorizado | `inbox/webhooks.py`; fanout de ID duplicado exige decisão |
| M27 | Org `member` externo | Administrar convites, papéis e outras contas de O1 | O1 | N | `members/views.py` restringe POSTs a admin; leitura `member_list` não é restrita |
| M28 | Cliente de A | Usar credencial ou seleção de workspace de outra org | C/O2 | N | `RBACMiddleware` e `McpAuth`; uma org por usuário na v1 |

## 4. Riscos por prioridade — evidência estática versus prova pendente

1. **ALTA — Diretório organizacional em organização compartilhada.** `apps/client_portal/views_admin.py::invite_client` cria convite de `OrgMembership.MEMBER`; `apps/members/views.py::member_list` aceita `require_org_role("member")` e busca todos os membros de O1 e seus workspaces. `config/urls.py` monta `/members/`. **Reprodução sintética proposta:** associar cliente A à O1 como MEMBER/CLIENT; adicionar usuário de B; autenticar A; GET `/members/`; verificar se identificadores, nomes ou e-mails de B são renderizados. Impacto: inventário organizacional e identificação de usuários de outros clientes. Inspeção indica rota permissiva; **HTTP ainda não executado**.
2. **ALTA — Identidade externa com EDITOR/CONTRIBUTOR não é modelada.** `apps/approvals/comments.py::get_comments_for_post`, `apps/approvals/views.py::comment_attachment`, `apps/calendar/views.py`, `apps/composer/views.py` e `apps/api/routers/posts.py` condicionam dados internos a `workspace_role` ou `create_posts`. **Reprodução sintética proposta:** criar E_A externo com EDITOR; comentário interno com anexo e `Post.internal_notes` em A; testar UI, URL por UUID, REST e MCP. Papel de edição **não** equivale à autorização de ver dados internos. Não afirmar vazamento real sem teste HTTP.
3. **ALTA — Biblioteca organizacional acessível entre workspaces.** `apps/media_library/managers.py::for_workspace_with_shared`, `apps/media_library/views.py::shared_library_index` com `@require_org_role("member")`. **Comportamento intencional BrightBean**, reprovado como padrão para dados internos de clientes. Criar mídia sintética org-shared e comprovar visibilidade A/B; não alterar mídia editorial sem política aprovada.
4. **ALTA — Fanout Meta quando mesma conta nativa consta em A/B.** `apps/social_accounts/models.py` limita unicidade a `(workspace,platform,account_platform_id)`; `apps/inbox/webhooks.py::_process_meta_events` pode encaminhar mesmo evento a ambos. Já existe teste `apps/inbox/tests/test_webhooks.py::test_repeated_native_id_inside_org_fans_out_to_both_workspaces`; **não realizar coleta real**.
5. **MÉDIA/ALTA — Sessão de portal e aprovação após mudança de papel.** `portal_auth_required` revalida qualquer membership mas não `workspace_role=CLIENT`; `portal_approve` chama serviço sem teste de permissão de aprovação. PR #16 filtra comentários externos mesmo se usuário virou EDITOR, e PR #19 invalida **links ainda não usados** após mudança, porém sessão emitida anteriormente pode persistir. Testar sessão ativa + downgrade + POST de aprovação, sem inferir exploit até executar.
6. **MÉDIA — Hierarquia/custom role e contexto multi-org.** `require_workspace_role` usa comparação de papel literal; `CustomRole.permissions` não é considerado nesse decorator; `RBACMiddleware` usa primeira `OrgMembership` em rotas globais. Avaliar regressão com papéis customizados, usuário em O1+O2 e `last_workspace_id` obsoleto.
7. **MÉDIA — Autorização de comentário externo.** `approvals/views.py::add_comment` obtém `visibility` de entrada POST e exige papel hierárquico mínimo `viewer`; verificar com CLIENT/EDITOR externo se pode criar INTERNAL e como isso aparece em notificações/replies.

**Vulnerabilidade comprovada por exploração:** nenhuma nesta PR. Os itens acima são observações estáticas, incompatibilidades de política ou comportamento sintético já documentado; qualquer correção deve ser isolada em PR própria, sem alterações oportunistas de RBAC.

## 5. Testes adversariais planejados (não executados na PR #21)

| Conjunto | Cenário / asserção | Base de teste para ampliar |
| --- | --- | --- |
| T01 | Cliente A `MEMBER+CLIENT` GET `/members/`: nenhuma identidade, associação ou convite de B/C; controle positivo para interno autorizado | `apps/members/tests/test_role_hierarchy.py`; novo teste de leitura |
| T02 | Cliente A GET `/organizations/media/shared/` e picker API/MCP: negar mídia não autorizada de B/org-shared; confirmar mídia autorizada A | `apps/media_library/tests/test_security.py`; `apps/api/tests/test_post_media_client_boundaries.py` |
| T03 | E_A editor externo: comentário INTERNAL raiz/reply, anexo e `internal_notes` não aparecem via calendário, composer, HTMX, REST, MCP, UUID direto; I_A positivo | `apps/approvals/test_client_reply_visibility.py`; `test_comment_attachment.py`; `apps/api/tests/test_post_media_client_boundaries.py` |
| T04 | Papel externo CLIENT, EDITOR, CONTRIBUTOR e custom: POST comentário `visibility=internal`, acesso a download, ação aprovação, publicação e inbox | `apps/approvals/test_security.py`; `apps/client_portal/tests.py` |
| T05 | O_A sessão portal já iniciada → papel alterado/removido, workspace arquivado, usuário desativado: ações negadas e sem alteração de estado | `apps/client_portal/test_revoked_magic_links.py`; `apps/client_portal/tests.py` |
| T06 | Cookie de sessão, API key e OAuth MCP, com A/B/C e `last_workspace_id` alternado: negar B/C por UUID e pós-revogação | `apps/api/tests/test_cross_client_isolation.py`; `test_oauth_workspace_isolation.py`; `apps/mcp/tests/test_oauth_auth.py` |
| T07 | Duas contas Meta com mesmo ID remoto em O1: evidenciar fanout; outras orgs/segredos separados; exigir regra autorizada antes de dados reais | `apps/inbox/tests/test_webhooks.py` |
| T08 | Revogação em notificações/workers, cache aquecido, cron, exportações e relatórios: não entregar payload de B/C a A nem após offboarding | `apps/inbox/tests/test_notification_membership_boundaries.py`; acrescentar casos |
| T09 | Não regressão dos papéis internos: publisher, editor, calendário, inbox, analytics, aprovação, portal, mídia, REST/MCP e licenças continuam funcionais | Suítes existentes, CI no SHA exato |
| T10 | Cliente observador tenta `/members/` e recursos globais via login de portal; políticas negam metadados intercliente inclusive no mesmo O1 | Novo teste de rota + URL direta |

**Regra de execução:** usar fixtures A/B em O1 e C em O2, nenhum dado pessoal real, sem rede externa, verificar estado do banco e efeitos de background, 403/404 seguro conforme rota. CI de PR documental não executa automaticamente estes novos cenários, pois eles **não foram implementados**.

## 6. Alternativas de tenancy — ainda sem decisão

| Modelo | Reuso | Risco principal | Condição de escolha |
| --- | --- | --- | --- |
| O1 operacional única, workspace por cliente | Menor mudança na navegação e vínculo multi-cliente do BrightBean | Org MEMBER pode acessar recursos globais, org-shared e diretório; fanout Meta | Política por **identidade + dado** em todos os pontos; regressões completas e proibição de mistura confidencial |
| Organização separada para cada cliente | Fronteira mais forte para ativos organizacionais | `RBACMiddleware` global usa `.first()`; internos multi-org, billing e configurações exigem testes/evolução | Provar login, troca multi-org, API/MCP, jobs e UX sem reescrever autenticação |
| Domínios/instâncias segregados, controle operacional federado | Fronteira de implantação adicional | Custo, operação, sincronização, autenticação e publicação mais complexos | Exigir demonstração de necessidade e plano de migração operacional |

**Recomendação à ADR-0003 (não aprovação):** incluir definição formal de ator interno versus externo, classificação dos dados, lista de recursos globais a isolar, regra de contas sociais duplicadas, política de mídia org-shared e protocolo de revogação. Executar T01–T10 e auditoria rotas/serviços/filas antes de selecionar tenancy. Não usar `is_staff` como substituto automático da identidade de funcionário, nem reconstruir autenticação/RBAC sem evidência de insuficiência do BrightBean. A ADR-0004 permanece proposta e evidências privadas ficam **fora** de `media_library/`.

## 7. Gate para encerrar esta etapa

Esta PR entrega **documentação da matriz e planejamento de regressão**, sem testes novos e sem alteração de produção. A aceitação futura de ADR-0003 requer: decisão humana expressa; testes adversariais positivos e negativos executados; inventário completo de UI/HTMX/REST/MCP, storage, workers e webhooks; ausência de vazamento de identificadores/dados entre A/B/C; revogação comprovada; e homologação separada. A menor correção prioritária deverá ser discutida em **PR funcional independente** depois de confirmar T01 em ambiente sintético.

**Evidência histórica reaproveitada:** [PR #6](https://github.com/OARANHA/CRISE/pull/6), [PR #16](https://github.com/OARANHA/CRISE/pull/16) até [PR #19](https://github.com/OARANHA/CRISE/pull/19), [matriz de isolamento](2026-10-08-client-isolation-matrix.md), [reuso do portal](2026-10-08-client-portal-reuse-and-access.md), [fanout Meta](2026-10-08-meta-webhook-workspace-routing.md). Não inferir homologação a partir dessas PRs.
