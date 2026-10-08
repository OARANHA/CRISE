# 2026-10-08 — Comentários internos forjados por papel CLIENT (M24)

**Base examinada:** `feat/brightbean-upstream-import` @ `da900ea4f6a65963538e5defe7c081122e78dece`.
**Slice:** `fix/client-comment-visibility-gate`; PR de revisão, sem merge/deploy.
**Estado da evidência:** fluxo de dados comprovado por leitura do código; testes HTTP sintéticos adicionados, **execução ainda pendente**. Não afirmar exploração executada.

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

- **Ator:** usuário com `WorkspaceMembership.workspace_role=CLIENT`, membro somente do workspace A; post editorial no próprio A.
- **Ação malformada:** `POST approvals:add_comment` com `visibility=internal` (em vez de `external`).
- **Recurso/dado:** `PostComment.visibility`, que controla a classificação da conversa entre equipe e cliente.
- **Evidência estática:** `apps/approvals/views.py::add_comment` exige papel mínimo `viewer` e recebe `visibility` do formulário; `apps/approvals/comments.py::create_comment` grava o valor sem verificar permissão do autor. O papel `CLIENT` supera `viewer` na hierarquia atual. Logo, o fluxo existente permitia que CLIENT solicitasse criação de comentário marcado `internal`; a reprodução HTTP antes da correção não foi executada.
- **Reuso:** `request.workspace_membership`, `WorkspaceMembership.WorkspaceRole.CLIENT`, constantes `PostComment.Visibility`, roteamento, serviços e middleware do BrightBean; nenhum modelo, migration ou RBAC novo.
- **Decisão restrita:** para `CLIENT`, aceitar criação de comentário apenas com `visibility=external` (inclusive valor padrão). Negar `internal` e valores inválidos com HTTP 403 antes de criar comentário ou notificar terceiros. Papéis editoriais existentes não mudam.

## Regressões sintéticas adicionadas

`apps/approvals/test_client_comment_visibility_gate.py`: oito testes HTTP de (1) CLIENT → internal negado/sem persistência; (2) valor inesperado negado; (3) external permitido; (4) external como padrão; (5) EDITOR mantém internal; (6) downgrade EDITOR→CLIENT na sessão existente; (7) acesso por UUID de B, outro workspace da mesma organização; (8) acesso a C, outra organização.

**Execução local:** não realizada; sem checkout completo nem ambiente Django/PostgreSQL disponível neste chat. **CI da branch:** esperar comunicação manual `green`/`red`, conferir uma vez no SHA exato, sem polling. Não há conclusão de testes presumida.

## Riscos residuais e limites

- A distinção confiável entre funcionário interno e cliente operador `EDITOR` permanece pendente da ADR-0003; a regra implementada cobre somente o papel `CLIENT`.
- Outras operações sobre comentários, replies, anexos, mídia organizacional, API/MCP e inbox não foram homologadas por este slice.
- Não modificar licença, portal, postagens ou políticas de evidências privadas; ADR-0003 e ADR-0004 seguem propostas.
- Nenhum dado real de clientes, API externa, coleta social, deploy ou merge foi empregado nesta etapa.
