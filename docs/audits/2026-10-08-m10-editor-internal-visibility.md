# M10 — comentários e anexos internos sob papel EDITOR (caracterização)

**Data:** 2026-10-08. **Base inspecionada:** `feat/brightbean-upstream-import` @ `84139275e16efcd2201191275b24cc9ea3513fa6`.
**Status:** divergência entre política-alvo VIGIAFAST e identidade efetivamente persistida; **NÃO CORRIGIDA**. Testes de caracterização propostos nesta branch; execução Pytest/CI ainda não verificada. Apenas dados sintéticos.

## Ator × ação × recurso × escopo

- I_A: funcionário VIGIAFAST de A (identidade **conceitual**), papel EDITOR, acesso interno esperado.
- E_A: operador de cliente A (identidade **conceitual**), também EDITOR, restrição a dados internos **desejada, mas não implementável com segurança apenas pelo papel**.
- O_A: observador de A, papel CLIENT; acesso somente a comentários externos.
- B: outro workspace na mesma O1; C: workspace em O2; sem membership, acesso deve ser recusado.
- Recursos: comentário INTERNAL raiz, reply INTERNAL em raiz EXTERNAL, anexos de ambos e URL conhecida por UUID.

## REAL NOW e evidência no código

1. `apps/members/models.py::WorkspaceMembership`: registra role e `custom_role`; não há campo confiável de origem interna/externa. `effective_permissions` não representa a classe de confidencialidade de comentários.
2. `apps/approvals/comments.py::get_comments_for_post`: filtra raízes INTERNAL e replies INTERNAL **somente quando** o role literal é CLIENT. EDITOR recebe ambos.
3. `apps/approvals/views.py::comment_attachment`: exige autenticação, vínculo ao workspace, post/comment corretos; bloqueia anexo INTERNAL **somente quando** role=CLIENT. Um EDITOR de A pode receber bytes de raiz ou reply de A por UUID conhecido.
4. `apps/approvals/views.py::add_comment`: bloqueia `visibility=internal` para CLIENT (PR #25), mas mantém escrita INTERNAL por EDITOR para preservar BrightBean.
5. `templates/approvals/partials/comment_list.html`: renderiza raízes e replies retornados pelo serviço; link de anexo raiz passa pela view privada. Um anexo de reply não é apresentado no template, mas a mesma rota de download aceita seu UUID.
6. `apps/client_portal/views.py::portal_approval_queue`: filtra EXTERNAL em raízes e replies independentemente do papel atual do usuário na sessão do portal.
7. `apps/members/middleware.py::RBACMiddleware`: resolve associação por workspace na URL. Ausência de membership B/C gera negação antes da view.
8. `apps/api/routers/posts.py` e `apps/mcp/handlers.py` expõem `Post.internal_notes` conforme `create_posts`, risco **M09 separado**; a inspeção focal de M10 não identificou contrato REST/MCP específico para `PostComment`. Isto não equivale a inventário completo das superfícies.

**Divergência central:** I_A e E_A estão representados de modo idêntico por EDITOR. Autorizar ou negar com base somente em EDITOR não resolve qual ator pertence ao time interno. O teste de E_A recebendo conteúdo INTERNAL é a **caracterização do comportamento existente**, não uma aprovação da política.

## Testes sintéticos nesta entrega

`apps/approvals/test_m10_editor_internal_visibility.py` cobre:

- Mesmo comportamento atual para I_A e E_A no serviço de listagem;
- Resposta HTMX do POST exibindo comentários e replies INTERNAL para EDITOR;
- GET por UUID de anexo de raiz/reply INTERNAL para EDITOR;
- Controle positivo de leitura da equipe e de anexo EXTERNAL por CLIENT;
- Filtro de raiz/reply e negação do anexo INTERNAL para CLIENT;
- Acesso por UUID a B (mesma organização) e C (organização diferente) sem membership;
- Post UUID incoerente no workspace A;
- Downgrade EDITOR→CLIENT na sessão atual, revogação da associação;
- Escrita INTERNAL por EDITOR como caracterização explícita da lacuna.

**Importante:** asserts intencionalmente descrevem o acesso atual de E_A a conteúdo interno para não produzir testes artificialmente verdes que pareçam provar confidencialidade. A lacuna permanece aberta mesmo se os testes de caracterização passarem. Não foram executadas operações HTTP fora de testes sintéticos; a execução real desses testes depende do CI/ambiente Django+PostgreSQL.

## REUSE GATE → DECISION

**Reusar:** Django sessions, `RBACMiddleware`, `WorkspaceMembership`, controles de rota por workspace, `get_comments_for_post`, portal e testes atuais. Sem mudar autenticação, tenancy, hierarchy, storage ou editor.

**Decisão desta entrega:** caracterizar e documentar M10, sem alterar regras de runtime. A ADR-0003 continua **PROPOSTA/NÃO ACEITA**; requer decisão humana sobre (1) afiliação de ator como domínio persistido, (2) política por classe de dado e ação, (3) sessões/API/MCP, (4) migração e controles de regressão. `User.is_staff` não é prova de vínculo interno. Não bloquear todo EDITOR — isso quebraria I_A e funcionalidades BrightBean.

**Risco residual:** a futura identidade E_A poderá ler/escrever notas internas no editor enquanto usar role EDITOR sem separação de identidade e classe de dado. Proibir concessão de editor a operadores externos **como controle operacional provisório** até decisão e implementação segura. Isso é orientação de rollout, não restrição no código.

**Gate posterior:** rodar testes no SHA da PR, informar resultado de Pytest, Ruff, Mypy, Gitleaks e Docker; revisar com operador; decidir ADR-0003 em etapa independente. Não fazer merge nem deploy automaticamente.
