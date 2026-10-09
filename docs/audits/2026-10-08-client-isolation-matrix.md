# VIGIAFAST — matriz inicial de isolamento entre clientes

**Data:** 2026-10-08  
**Status:** **16/16 casos aprovados** na [CI #37763047990](https://github.com/OARANHA/CRISE/actions/runs/37763047990), 2.364 passed / 1 skipped / 822 warnings, cinco jobs verdes; [PR #6](https://github.com/OARANHA/CRISE/pull/6) integrada à branch de importação no commit `1b0436980c618e9931b1dc78aa6c818bc4849abd`. **Não constitui auditoria completa.**

## Modelo alvo

Para os nove clientes iniciais, a hipótese operacional é **uma organização da equipe com um workspace por cliente**. Também precisamos isolar organizações completamente distintas. Essa hipótese precisa de decisão formal antes de ativar dados reais.

O BrightBean possui `Organization`, `Workspace`, `OrgMembership`, `WorkspaceMembership`, chaves API limitadas por workspace e contas sociais, e `InboxMessage.workspace`. Aproveitamos esses recursos existentes, sem redesenhar autenticação.

## Matriz de testes da PR #6

| Superfície | Mesmo cliente A | Cliente B: mesma organização, workspace diferente | Cliente C: outra organização |
| --- | --- | --- | --- |
| REST inbox lista | A permitido | B oculto | C oculto |
| REST inbox leitura por UUID | A permitido | 404 | 404 |
| REST criar rascunho em mensagem alheia | — | 404, sem gravação | 404, sem gravação |
| REST editar, apagar ou enviar rascunho alheio | — | 404, sem efeito | 404, sem efeito |
| MCP listar e buscar inbox | A permitido | oculto/erro | oculto/erro |
| HTMX acessar inbox por workspace ID | — | 403 | 403 |
| Emitir API key com conta social alheia | — | proibido | proibido |

Os testes usam exclusivamente organizações, usuários, contas e comentários **sintéticos**, criados no banco efêmero de testes.

## Gates que continuam abertos mesmo que a CI da PR #6 fique verde

- Outros endpoints de UI, REST e MCP: posts, mídia, permissões customizadas, portal do cliente, relatórios e notificações.
- Processadores em segundo plano, filas, webhook, cache, resultados de IA, índices e arquivos.
- Comportamento de organizações diferentes, troca de workspace e revogação de acesso.
- Testes adversariais com usuário pertencente a dois clientes, papéis Viewer/Client e administrador limitado.
- Decidir/implementar storage privado de evidências; mídia de publicação pública **não é** storage confidencial.
- Homologação LGPD, configuração real de proxy confiável, taxa e retenção.

## Critério de aceite

Nenhuma informação de B/C aparece quando a chave ou sessão só está autorizada em A. Operações por identificadores UUID alheios são recusadas sem efeitos colaterais nem envio às redes sociais. Registrar resultado real da CI, sem inferir segurança total.

## Regressões posteriores e limite dos processos assíncronos
- PR #8: posts e mídia REST/MCP; 16 casos aprovados; mídia org-shared continua visível entre workspaces da mesma organização.
- PR #9: OAuth/MCP, mudança de workspace e offboarding; 10 casos aprovados.
- PR #10: cache Django aquecido, revogação e alterações de escopo; 7 casos aprovados.
- PR #11: Meta webhook com mesmo ID de página entre workspaces; três casos aprovados; duplicação de mensagens entre clientes da mesma organização é comportamento observado e **risco não aceito para produção**.
- PR #12 **proposta, CI pendente:** `InboxSyncEngine` com duplicação de ID remoto e notificações selecionadas por workspace. Não substituir homologação de filas reais nem aceitar a ADR-0003.

## PR #12 comprovada; PR #13 proposta
- PR #12: `InboxSyncEngine` separa mensagens com ID remoto igual por conta e mantém notificações comuns por workspace. [CI #37784489968](https://github.com/OARANHA/CRISE/actions/runs/37784489968): cinco jobs verdes, 2.405 passed/1 skipped.
- Lacuna detectada: `InboxMessage.assigned_to` continua apontando para funcionário após remoção da participação, e notificações de evento/SLA não revalidavam sua associação ao workspace antes de enviar detalhes.
- PR #13 (CI pendente): validar destinatário por `WorkspaceMembership` no despacho e aplicar fallback para owners/managers atuais do workspace. Oito cenários parametrizados, sem dados reais ou rede externa.
