# ADR-0003 — Deliberação técnica de isolamento (não normativa)

**Data da inspeção:** 2026-10-08 (America/Sao_Paulo). **Status:** PROPOSTA PARA DECISÃO, NÃO ACEITA. **Tipo:** revisão estática de código + síntese de testes sintéticos existentes; nenhuma alteração de runtime, nenhuma migração e nenhum novo teste executado.
**Referência de runtime:** `feat/brightbean-upstream-import` @ `63e0c854e199945435a9c42d5cfe2acfc62611b5`. **Base documental desta proposta:** PR #30 @ `855b7765cf09589d04038fb3092300adfb6c2ae4` (CI #37867551502, 5/5 success, PR ABERTA/não integrada). `main` @ `f6883b747ce1a6ae6a6968948da5225332ed4f2f`; PR #2 Draft.

## REAL NOW → PROVEN EVIDENCE

1. `apps/members/models.py`: `OrgMembership` é único por `(user, organization)` e `WorkspaceMembership` por `(user, workspace)`; `effective_permissions` usa papel base ou `CustomRole`, sem atributo confiável de vínculo profissional interno/externo.
2. `apps/members/middleware.py::RBACMiddleware`: em rotas globais escolhe a primeira organização (`OrgMembership.first()`) independentemente do `last_workspace_id`. Em URLs com `workspace_id`, `process_view` valida a associação específica e reatribui o contexto. Os **quatro testes de caracterização M11** comprovam os limites observados, não homologam multi-organização.
3. `apps/media_library/managers.py::for_workspace_with_shared`: `workspace_id=NULL` + mesma organização compartilha mídia editorial. `apps/media_library/views.py::shared_library_index` é org-scoped; `apps/organizations/views.py::workspaces_view` lista workspaces da organização para papel `member`. Esse desenho não é isolamento absoluto entre workspaces.
4. `apps/members/views.py::member_list` já restringe a leitura de membros/workspaces por participação compartilhada para papel org `member`. Não repetir como vulnerabilidade aberta sem considerar a correção existente; **outras rotas org-scoped** continuam a exigir inventário.
5. `apps/approvals/comments.py::get_comments_for_post`, `apps/approvals/views.py::{add_comment,comment_attachment}`: a restrição de `INTERNAL` considera papel literal `CLIENT`, não afiliação do operador. Os **dez testes sintéticos M10** demonstram que `EDITOR` externo e interno hoje leem raiz/reply e baixam anexos internos, e que EDITOR externo pode escrever nota interna. **M10 permanece aberto**.
6. `apps/client_portal/decorators.py::portal_approval_required` revalida `approve_posts`; `portal_auth_required` exige sessão portal e vínculo atual, mas não prova afiliação externa por si só. `apps/client_portal/services.py::generate_magic_link` exige papel `CLIENT`; um editor externo pode precisar do fluxo editorial comum.
7. `apps/api/auth.py::VirtualMembership` transporta permissões, workspace e ator, sem identidade `internal/external`; `apps/api/routers/posts.py::_can_view_internal_notes` usa `create_posts` (risco M09). API, MCP, sessões e workers precisam da mesma regra no backend.
8. `apps/members/services.py::accept_invitation` é capaz de criar `OrgMembership` em outra organização; isso **não prova** navegação, páginas globais, convites, tarefas e OAuth multi-org seguros. Funções de serviço com owner org-wide exigem análise no contexto tenant.

**Fontes complementares:** [auditoria M10](2026-10-08-m10-actor-affiliation-architecture-gate.md), [auditoria M11](2026-10-08-m11-multi-org-context-characterization.md), [matriz ator-recurso](2026-10-08-authorization-actor-resource-matrix.md), [ADR-0004](../decisions/ADR-0004-private-evidence-storage.md).

## GAPS → REUSE GATE

| Alternativa | Reuso BrightBean | Vantagem | Gaps / riscos não resolvidos | Avaliação |
| --- | --- | --- | --- | --- |
| **A — uma organização por cliente** | `Organization`, `Workspace`, memberships, roles, convites, portal, mídia editorial por organização, REST/MCP existentes | Contém ativos org-shared no domínio de um cliente; separa configurações organizacionais e administração de cada cliente | M11 (`.first()` e contexto global), operadores internos multi-org, seleção de contexto, cross-org jobs/relatórios, autorização `INTERNAL` M10, revogação, duplicação de conta social e UX central | **Preferência condicional para deliberar**; não pronta para rollout |
| **B — uma organização VIGIAFAST com workspace por cliente** | Menor esforço inicial de alternância e operações internas | Equipe vê workspaces sob um mesmo contexto de organização | Mídia org-shared, listagem global de workspaces, configurações/membros org-scoped, regras owner org-wide, fanout de webhooks e outras rotas com escopo de organização; M10 permanece | Não recomendar como padrão de isolamento sem auditoria/hardening transversal comprovados |
| **C — coordenação central VIGIAFAST separada** | Pode apenas agregar navegação/atribuições em cima do BrightBean | Uma interface pt-BR para a equipe que opera muitos clientes | Se criada como superusuário ou organização com dados copiados, vira bypass intercliente; maior custo e nova superfície de autorização | **Complemento opcional à A**, não substituto de tenant e não segunda fonte de permissões |

**Deliberação técnica recomendada, ainda não aprovada:** escolher **A (uma organização por cliente)** como fronteira lógica padrão, com um ou mais workspaces do próprio cliente para usos editoriais; adicionar posteriormente uma camada **C de coordenação central** para equipe VIGIAFAST que mostre somente organizações/workspaces dos quais o funcionário é membro e escopo autorizado. Não usar uma organização operacional única como repositório de dados de todos os clientes. Isso **não equivale a isolamento físico, RLS do banco ou homologação multi-tenant**.

**Limite essencial:** A não corrige sozinha M10; cliente EDITOR em sua organização continuaria lendo dado `INTERNAL` daquele cliente. A também não corrige M11, nem substitui controles por recurso e classe de informação.

## Contrato a votar para a ADR (não implementado)

1. **Tenant:** `Organization` do cliente delimita recursos org-scoped; `Workspace` delimita edição/canais/equipe por contexto do cliente. Compartilhamento de mídia editorial pode continuar **dentro** do tenant; nenhuma mídia de cliente A será implicitamente de B. Materiais reputacionais/evidências privadas dependem de ADR-0004 e storage privado, jamais da mídia pública.
2. **Equipe interna:** `User` único pode possuir múltiplos `OrgMembership` e `WorkspaceMembership` atribuídos com justificativa e revogação. A tela de coordenação apenas oferece seleção de contextos *autorizados*; não passa dados privados por sessão, cache, relatório ou serviço cross-tenant sem novo check. Uma organização VIGIAFAST interna, se necessária para operações próprias, não concede acesso aos clientes.
3. **Contexto:** resolver `active_org` a partir de workspace autorizado ou escolha explícita validada em toda requisição; para rotas globais sem workspace, rejeitar contexto ausente/ambíguo e nunca escolher `.first()` arbitrariamente. Garantir consistência `workspace.organization_id == active_org.id`; revogação e workspace arquivado invalidam contexto anterior. Revisar org-wide owners, funções de exclusão, convites, calendário transversal e tarefas.
4. **Afiliação por vínculo:** proposta de extensão de `WorkspaceMembership` com `internal`, `external` ou `unclassified` independente de `EDITOR`, `CLIENT`, `is_staff`, `OrgRole` e `CustomRole`. **Não** autodeclarada em convite, signup, portal, OAuth ou API; valores legados `unclassified` até verificação humana de identidade e autorização da equipe.
5. **Autoridade e auditoria:** somente administradores VIGIAFAST explicitamente delegados podem conferir/revogar `internal`, sem autoelevação, sob evento auditável com ator, vínculo, transição, data/hora, justificativa e escopo; reclassificação e offboarding revisados. Owner de uma organização de cliente não se torna certificador de funcionário VIGIAFAST.
6. **Autorização por recurso:** permitir dado `INTERNAL` apenas se ator autenticado, membership **atual** no workspace do objeto, permissão de ação apropriada, `affiliation=internal` **verificada** e concessão expressa à classe de dado. `internal` isolado não é superpermissão. `external` e `unclassified` não recebem `INTERNAL` automaticamente por `EDITOR`/`create_posts`. Revalidar para serviço, HTTP/HTMX, download UUID, REST/MCP, jobs, cache, exportações e resposta de IA.
7. **Legados:** inventariar memberships e vínculos profissionais usando fonte confiável; preparar classificação supervisionada e plano de reversão. Nunca backfill `OWNER/MANAGER/EDITOR => internal`. Antes de ativar negação para contas existentes, simular impacto nos fluxos editoriais e concluir provisionamento de equipe interna, sem abrir exceção genérica que exponha `INTERNAL`.
8. **Portal e edição:** observar e operar são experiências separadas; papel `CLIENT` tem fluxo de magic link, mas cliente `EDITOR` usa funcionalidades editoriais concedidas sem ganhar automaticamente direitos sobre notas reservadas. Revalidar aprovação com `portal_approval_required`; preservar recursos BrightBean e a AGPL-3.0.

## Menor slice funcional **somente após decisão explícita**

**Slice A1 (M11, pré-requisito para usar A):** corrigir de modo incremental o contexto da organização ativa em rotas globais para usuários multi-org, mantendo `OrgMembership` / `WorkspaceMembership` e as funções originais. Sem selecionar organização por `.first()` e sem confiar em `last_workspace_id` sem checagem; fornecer escolha segura e simplificada de cliente para equipe interna. Testes sintéticos para A e C em organizações separadas, ausência/expiração/troca de contexto, URL com workspace, revogação, navegação, calendário global, convites, sessões/API e regressões de usuário single-org. **Não implementar este slice enquanto ADR-0003 estiver proposta.**

**Slice A2 (M10, PR posterior e separada):** afiliação verificada + caminho administrativo/auditoria + migração conservadora `unclassified` + predicado de autorização por classe e regressões adversariais para comentários raiz/reply, anexos por UUID e escrita interna, mantendo edição normal por externos; depois ampliar a API, MCP, inbox e M09 em slices separados, sem habilitar produção parcialmente.

**Critérios negativos para liberação operacional:** operador A jamais acessa ID/UUID/bytes/notas/identidades/conta social de B, mesmo com link direto ou cache; externo `EDITOR` não lê/escreve `INTERNAL`; revogação é efetiva em sessão/token; nenhum anexo de evidência em `media_library/`; testes de compatibilidade do BrightBean e revisão de licenças. A/B na mesma organização continuam fixtures úteis para comprovar riscos da opção B; C em organização separada comprova a outra topologia. Não usar clientes reais antes de homologação.

## Parecer Wandora JEV.1 (consultivo)

- Ferramenta: `jev_route_task`, provider `typesafe`, modelo retornado `jev-1.13.0`; tarefa: escolher o próximo caminho de deliberação entre A/B/C com as restrições do VIGIAFAST.
- Retorno registrado: `route=deep_review`, `confidence=0.76`, `probabilities.deep_review=0.82`, `probabilities.block=0.16`, `probabilities.proceed_fast=0.01` (demais 0.01). **Interpretação:** aprofundar revisão antes de adotar política; não seleciona por si só a topologia A e não equivale a autorização.
- **Decisão técnica independente:** recomendar A condicionalmente a partir dos filtros e escopos inspecionados; manter ADR proposta e bloquear runtime, merge e deploy até decisão humana e regressões.

## Estado da execução desta análise

- Leitura estática do repositório e consulta pontual à CI da PR #30; inspeção dos testes M10/M11 já versionados. **Não foram executados novos testes locais ou em ambiente runtime** nesta análise documental; green da PR #30 valida apenas o SHA daquela PR.
- Nenhum cliente, segredo, token, URL de postagem real ou dado pessoal usado.
- A integração da PR #30 e a aceitação ADR-0003 são gates distintos; esta nota não autoriza nenhum dos dois.
