# M10 — proposta de afiliação confiável e autorização por classe de dado

**Data:** 2026-10-08. **Base de código revisada:** `feat/brightbean-upstream-import` @ `e5f9ec7c6568729bc26220f1ab44b156bc7d6477`.
**Natureza:** inspeção estática e proposta técnica; **nenhuma alteração no comportamento de produção** nesta entrega.
**Autoridade:** insumo para [ADR-0003](../decisions/ADR-0003-client-isolation-boundaries.md), ainda **PROPOSTA / NÃO ACEITA**. A [ADR-0004](../decisions/ADR-0004-private-evidence-storage.md) também não foi aceita.

## REAL NOW → PROVEN EVIDENCE

- `main` @ `f6883b747ce1a6ae6a6968948da5225332ed4f2f`; branch de importação @ `e5f9ec7c6568729bc26220f1ab44b156bc7d6477`. A PR #2 permanece aberta e Draft para `main`.
- [PR #26](https://github.com/OARANHA/CRISE/pull/26) integrada **somente** à branch de importação no SHA `e5f9ec7...`. [CI pós-merge #37858665680](https://github.com/OARANHA/CRISE/actions/runs/37858665680): `completed/success`, cinco jobs concluídos com sucesso (Pytest, Mypy, Ruff, Gitleaks e Docker), no mesmo SHA. São dez testes sintéticos de **caracterização**, não regressões que provem a confidencialidade dos dados.
- `apps/accounts/models.py::User` possui `is_staff`, campo administrativo Django, mas nenhum atributo de afiliação VIGIAFAST/cliente.
- `apps/members/models.py::OrgMembership` representa vínculo com organização e papel `owner/admin/member`; `WorkspaceMembership` representa vínculo por usuário/workspace, `workspace_role`, `custom_role` e `effective_permissions`. Não há atributo confiável que separe funcionário interno de operador externo com mesmo papel funcional.
- `apps/members/middleware.py::RBACMiddleware` revalida membership por workspace na URL, mas em páginas globais obtém a organização com `.first()` e documenta pressuposto de uma organização por usuário na v1. Não usar como garantia de multi-organização.
- `apps/approvals/comments.py::get_comments_for_post` filtra raiz e resposta INTERNAL apenas quando `workspace_role == CLIENT`; `apps/approvals/views.py::comment_attachment` também bloqueia o arquivo INTERNAL somente para `CLIENT`. `add_comment` bloqueia escrita INTERNAL somente para `CLIENT`. EDITOR interno e EDITOR externo são indistinguíveis nessas rotas.
- `apps/client_portal/views.py::portal_approval_queue` restringe raiz/reply a EXTERNAL incondicionalmente na sessão de portal. `apps/client_portal/services.py::generate_magic_link` requer CLIENT, enquanto `portal_auth_required` verifica sessão e associação atual sem exigir o papel CLIENT. A experiência portal não define afiliação do ator para outras superfícies.
- `apps/api/routers/posts.py::_can_view_internal_notes` baseia leitura de `Post.internal_notes` em `create_posts`: risco **M09**, tratado em slice separado; incluído aqui como dependência de política. `apps/api/auth.py` cria `VirtualMembership` de permissões para API key e MCP; será preciso propagar afiliação confiável ou avaliar cada ação sobre membership real.
- `apps/media_library/managers.py::for_workspace_with_shared` torna mídia editorial de organização visível entre workspaces da mesma organização; isso não autoriza compartilhamento de evidências privadas nem valida o tenancy da ADR-0003.

## GAPS → REUSE GATE

**Reuso obrigatório:** manter `User`, `OrgMembership`, `WorkspaceMembership`, `CustomRole`, sessões Django, middleware, permissões `create_posts` etc., editor, calendário, aprovações, portal, REST e MCP. Reutilizar o escopo por workspace e os filtros de comentários existentes como pontos de integração; não criar um segundo RBAC.

**Lacuna exata:** o mesmo `WorkspaceMembership.workspace_role=EDITOR` pode representar I_A (funcionário da VIGIAFAST) ou E_A (operador do cliente). `effective_permissions` concede capacidade de editar, não autorização para consultar dado INTERNAL. Uma mudança no template não protegeria GET/POST diretos, anexos por UUID, API nem MCP.

## Comparação de alternativas

| Alternativa | Reuso / impacto | Risco e avaliação |
| --- | --- | --- |
| Usar `User.is_staff`, `workspace_role` ou `CustomRole` como identidade | Nenhuma migração | **Descartar:** `is_staff` indica administração Django; role/custom role descreve capacidade, não afiliação. Mantém o desvio M10. |
| Adicionar afiliação a `OrgMembership` | Campo e migração relativamente pequenos | Afiliação por organização não representa, sozinha, autorização a recurso e cliente específicos; depende da decisão de tenancy e da revisão do fluxo multi-org. |
| **Adicionar afiliação independente a `WorkspaceMembership`** | Reutiliza o vínculo já resolvido em cada URL, sem novos papéis nem reconstruir RBAC; exige campo/migração, fluxo de atribuição seguro e predicado de acesso | **Preferência técnica condicional:** expressa status interno/externo por vínculo; não deve ser preenchido automaticamente a partir de EDITOR/OWNER nem manipulado pelo próprio usuário. Não resolve por si só tenancy global nem media org-shared. |
| Entidade específica de afiliação/contrato de trabalho | Proveniência e histórico potencialmente mais ricos | Maior número de junções, rotas e migrações antes de existir necessidade demonstrada. Reavaliar se houver identidade global ou consultorias multi-organização com regras distintas. |

## Contrato preferido para deliberação — **PROPOSTO, NÃO IMPLEMENTADO**

1. Separar **afiliação por vínculo** (`internal`, `external`, `unclassified`) do papel funcional `workspace_role` e da concessão `custom_role`. `internal` significa **afiliação VIGIAFAST verificada para aquele workspace**, não `is_staff` e não o nome do papel.
2. A classificação só pode ser gravada por fluxo administrativo confiável, com auditoria de quem classificou, quando, qual workspace e por qual fundamento autorizado; convite, link mágico, formulário, login OAuth ou usuário externo não podem se autodeclarar `internal`. Incluir revisão de atribuições existentes e reclassificação privilegiada.
3. Usuários legados devem começar **não classificados** para fins de liberação de INTERNAL. Nenhuma migração deve converter automaticamente todo OWNER/MANAGER/EDITOR em funcionário interno. Planejar levantamento e backfill supervisionado **antes** de habilitar política de leitura, para preservar trabalho legítimo.
4. Decisão de autorização sensível deve considerar, no servidor, `actor` autenticado + membership **atual** e escopo do `resource.workspace_id` + `action` e `effective_permissions` + `classification` do dado + afiliação verificada + eventual concessão específica à classe de dados. `external` ou `unclassified` não leem INTERNAL só porque possuem `create_posts`. O status `internal`, isoladamente, também não concede acesso a tudo.
5. Centralizar a decisão em serviço/predicado de autorização reutilizável; adaptar serviço de comentários, views HTMX e streaming de anexos, depois outras superfícies (M09, inbox, calendário, REST/MCP) conforme inventário. Evitar depender apenas de decorators de interface ou campos de sessão. Revalidar membership e revogação durante sessão/token ativo. Não expor classificação interna ao cliente.
6. Preservar operações BrightBean de edição, calendário e aprovação quando autorizadas. Distinguir mídia **editorial pública** de **evidências confidenciais**: a segunda categoria depende da ADR-0004 e de storage próprio, nunca `media_library/`.
7. Decisão sobre **uma organização com workspaces de clientes versus organizações separadas** continua na ADR-0003. O campo proposto não homologaria qualquer das topologias.

## Matriz mínima de validação posterior (fixtures 100% sintéticas)

| Caso | Capacidade editorial | Dados internos / URL direta |
| --- | --- | --- |
| I_A = funcionário interno classificado, EDITOR de A | Edição e aprovação conforme permissões; não elevar automaticamente | Permitido **somente** se capacidade específica e classe autorizadas em A |
| E_A = operador externo classificado, EDITOR de A | Editar em A conforme permissão | Negar comentários INTERNAL raiz/reply, escrita INTERNAL, anexos INTERNAL por UUID e `internal_notes` |
| O_A = cliente observador CLIENT de A | Portal e aprovação autorizados | Negar INTERNAL independentemente da tela |
| T_A = operador externo CONTRIBUTOR de A | Criar conforme permissão, sem aprovação adicional | Negar INTERNAL |
| I_AB = funcionário interno com memberships explícitos A e B | A e B conforme os respectivos vínculos | Sem acesso a C; afiliação e permissão avaliadas por vínculo |
| Usuário A tentando recurso B (mesma org O1) ou C (outra org O2) | Negar ação não atribuída | Negar lista/UUID/download/API/MCP, inclusive media privada |
| Mudança EDITOR→CLIENT, externalização ou remoção da membership durante sessão/API key | Reavaliar permissões atuais | Negar imediatamente nas próximas requisições |
| Sessão de portal ainda ativa após alteração de papel | Somente fluxo com autorização vigente | Sempre filtrar comentários e replies INTERNAL |

**Gates técnicos:** testes HTTP/HTMX, serviço, downloads raiz/reply, alterações em sessão, REST, MCP, custom roles, conteúdo editorial, mídia org-shared, operações multi-workspace; regressão para funcionalidades BrightBean preexistentes. O inventário transversal ainda não substitui estes testes.

## DECISION e menor slice seguro

**Decisão desta entrega:** documentar proposta, corrigir snapshot canônico da PR #26 e **parar no gate arquitetural**. Nenhuma política, modelo Django, migração, API, template, job, servidor ou dado real foi modificado.

**Gate explícito para implementar M10:** aceitar (ou revisar) a representação de afiliação e fonte de confiança, decidir o tenancy na ADR-0003, definir quais classes INTERNAL podem ser lidas por funcionário interno e garantir um caminho seguro para memberships legadas. Aceitação da ADR-0003 exige autorização humana específica; aprovação de PR documental e CI verde não a substituem.

**Próximo slice após decisão:** campo de afiliação não classificado por padrão + migração compatível + serviço de autorização por classe de dado + testes adversariais focais para comentários/attachments, em uma PR isolada; expansão REST/MCP/M09 em slices distintos. Não realizar rollout real antes da auditoria transversal, da ADR-0004 quando aplicável, nem de autorização operacional.
