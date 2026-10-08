# Estado canônico verificável — VIGIAFAST

**Reconciliado em:** 2026-10-08. **Fonte:** GitHub `OARANHA/CRISE` e logs de GitHub Actions.
Este arquivo é um **snapshot atual**, não um diário cumulativo. Atualize o que mudou na mesma PR e preserve o histórico em commits/ADRs/auditorias. Antes de trabalhar, confira o estado real das branches e PRs.

## REAL NOW

- **`main`:** contém fundação documental [PR #1](https://github.com/OARANHA/CRISE/pull/1), merge `f6883b747ce1a6ae6a6968948da5225332ed4f2f`. Ainda **não** contém a aplicação.
- **Branch de importação:** `feat/brightbean-upstream-import`, commit `1b0436980c618e9931b1dc78aa6c818bc4849abd` no início desta reconciliação.
- **[PR #2](https://github.com/OARANHA/CRISE/pull/2):** aberta, **draft**, base `main`, sem merge.
- **Importação upstream:** snapshot completo dos **874 arquivos versionados** de `brightbeanxyz/brightbean-studio@96ccc1e88fefa171c4e5ca981dc9f289bdf60d39`, com verificação byte a byte no [bootstrap #37728568048](https://github.com/OARANHA/CRISE/actions/runs/37728568048). Histórico upstream referenciado por URL/SHA, mas não copiado integralmente como histórico Git; preservar AGPL-3.0 e notices.
- **Deploy/produção:** nenhum. **Dados ou credenciais de clientes reais:** nenhum neste repositório. Não houve coleta real Instagram/TikTok/Facebook.

## PROVEN EVIDENCE — testes e merges

| PR | Entrega na branch de importação | Evidência |
| --- | --- | --- |
| [#3](https://github.com/OARANHA/CRISE/pull/3) | CI original (Ruff, Mypy, Pytest/PostgreSQL, Docker sem push e Gitleaks), commit `a9d397bf34c699b50b4237142cc50b905e3b105f` | [Run #37728858063](https://github.com/OARANHA/CRISE/actions/runs/37728858063), 2.337 passed / 1 skipped |
| [#4](https://github.com/OARANHA/CRISE/pull/4) | Restrições de Caddy/Compose, commit `4d5f9d400eab88ae80ca58b3087fc6537249c41b` | [Run #37729909304](https://github.com/OARANHA/CRISE/actions/runs/37729909304), cinco jobs verdes, smoke test Caddy público 200/privado 404 |
| [#5](https://github.com/OARANHA/CRISE/pull/5) | IP do login/API atrás de proxies confiáveis, commit `82bc2138999160edfd547cfcb1efbee7c8d187ac` | [Run #37730766539](https://github.com/OARANHA/CRISE/actions/runs/37730766539), 2.348 passed / 1 skipped |
| [#6](https://github.com/OARANHA/CRISE/pull/6) | 16 casos de isolamento da inbox REST/MCP/HTMX e emissão de chave, commit `1b0436980c618e9931b1dc78aa6c818bc4849abd` | [Run #37763047990](https://github.com/OARANHA/CRISE/actions/runs/37763047990), **2.364 passed / 1 skipped / 822 warnings**, cinco jobs verdes |

**Escopo validado na #6:** cliente A autorizado; clientes B (workspace diferente na mesma organização) e C (outra organização) ocultos ou bloqueados para operações de inbox e chaves API avaliadas. Só cenários sintéticos; **não extrapolar para todos os dados dos nove clientes**.

## GAPS — gates ainda abertos

1. **Política de isolamento para os 9 clientes:** BrightBean tem assets organizacionais compartilhados (`MediaAsset.workspace IS NULL`). `for_workspace_with_shared` torna esses assets acessíveis aos workspaces da mesma organização. Antes de definir um workspace por cliente, decidir como proibir que mídia, anexos, evidências e relatórios de um cliente apareçam para outro. Ver [ADR-0003](decisions/ADR-0003-client-isolation-boundaries.md), **proposta**, não aceita.
2. **Cobertura de segurança restante:** teste adversarial em posts, mídia, permissões, OAuth/MCP, UI, webhooks, tarefas, cache, relatórios, downloads, revogação e storage. O resultado da inbox não cobre tudo isso.
3. **Mídias confidenciais/evidências:** storage privado isolado, controle de acesso, hashes, origem, horários, trilha de manuseio e política LGPD **ainda não implementados**.
4. **Infraestrutura real:** configuração de proxies confiáveis, segredos únicos, backend de cache compartilhado e hardening sob concorrência exigem homologação. A CI de Compose/Caddy não substitui teste do ambiente de produção.
5. **Inteligência e captura:** Obsei, Auto Archiver e fontes externas ainda não integrados; nenhuma descoberta universal de comentários ou publicações de terceiros comprovada.
6. **Produto e experiência:** branding VIGIAFAST, interface pt-BR, gestão de ocorrências e relatórios por cliente ainda são entregas futuras.

## REUSE GATE → DECISION → NEXT ACTION

- **Reuse:** manter Django/Python/PostgreSQL e as capacidades do BrightBean já verificadas. Não reconstruir autorização ou inbox já existentes.
- **Decisão atual:** PR #2 **permanece em rascunho**, sem deploy. A arquitetura exata de isolamento ainda não foi aceita.
- **PR #8 em revisão (CI ainda não confirmada):** testes sintéticos A/B/C para leitura e edição de posts, acesso REST/MCP à mídia privada e comprovação de mídia org-shared existente. Se a política atual contrariar a privacidade exigida, corrigir por uma PR própria após avaliar dependências.
- **Esta revisão documental:** não alterar funcionalidade; aguardar CI da PR documental e comunicado do operador (green/red), sem polling.
- **Depois:** validar OAuth/MCP, workers e demais caminhos, revisar ADR-0003, iniciar UX VIGIAFAST gradualmente sem eliminar os módulos BrightBean.

## Regras imutáveis

Não usar dados reais antes de concluir os gates, não executar deploy nem operações em outros sistemas sem autorização. Nunca armazenar tokens, posts, nomes, evidências ou relatórios reais dos clientes no Git público. Não declarar um teste como aprovado sem log/commit verificável.

## PR #8 — primeira CI vermelha por importação (2026-10-08)
- [Run #37766160766](https://github.com/OARANHA/CRISE/actions/runs/37766160766): falha apenas em `ruff check`, regra `I001` (import block un-sorted) no novo arquivo `apps/api/tests/test_post_media_client_boundaries.py`. O `ruff format --check` não chegou a executar; build Docker skipped.
- **Pytest aprovou 2.380 casos, 1 skipped e 838 warnings**, incluindo **16/16 cenários novos** de segurança para posts, mídia e mídia organizacional compartilhada. Mypy e Gitleaks passaram.
- O workflow temporário `format-post-media-once.yml` aplica `ruff check --fix --select I` e `ruff format` usando a **mesma versão 0.15.9** da CI, verifica o resultado e remove a si próprio no commit bot. Nenhuma alteração em código de produção.
- **A execução e o commit automático ainda não estão confirmados.** O GitHub pode deixar a CI sobre um commit criado por `github-actions[bot]` como `action_required`; nesse caso uma alteração por conector GitHub precisará disparar nova validação. Não afirmar green antes de evidências. Sem polling, merge ou deploy.

## PR #8 — formatação corrigida; CI integral pendente (2026-10-08)
- [Workflow de correção #37767396264](https://github.com/OARANHA/CRISE/actions/runs/37767396264) **success**: `ruff==0.15.9` executou `ruff check --fix --select I`, `ruff format`, `ruff check` e `ruff format --check`; todos aprovaram o arquivo novo. Commit gerado: `a057fba3ff508423d479f5838859a326aeb5db7e` (`github-actions[bot]`). O workflow temporário foi removido no mesmo commit.
- [Run de CI #37767401425](https://github.com/OARANHA/CRISE/actions/runs/37767401425) foi iniciada no commit **anterior** `0521f8d487decd45c3acd77c4f81092101118242`: red por I001, enquanto Pytest, Mypy e Gitleaks passaram; Docker skipped. **Não representa o código corrigido**.
- [Run #37767422744](https://github.com/OARANHA/CRISE/actions/runs/37767422744) no commit `a057fba3...` terminou `action_required`, sem jobs, disparada pelo bot. Portanto **não existe ainda CI integral comprovada do commit formatado**.
- O próximo commit documental foi solicitado pelo conector GitHub, para disparar a CI no mesmo código formatado. Sem modificação de código, sem deploy, sem merge. Conferir o próximo resultado somente após comunicação `green`/`red`/`action_required`.

## Próximo gate OAuth/MCP — PR #9 pendente de validação
- [PR #8](https://github.com/OARANHA/CRISE/pull/8) **integrada** em `feat/brightbean-upstream-import`, commit `46546e22ac4f1836de1fe7b1a0b4d3228a77ce4b`.
- [Run CI #37768145395](https://github.com/OARANHA/CRISE/actions/runs/37768145395): Ruff, Mypy, Pytest/PostgreSQL, Docker build sem push e Gitleaks **success**. Pytest: 2.380 passed, 1 skipped, 838 warnings, 16 novos casos de posts/mídia aprovados.
- PR #9 **proposta**: regressões adicionais com OAuth e API keys: troca de workspace, cliente com perfil Viewer, tentativa de acessar mensagens de B/C, remoção de participação e redução de permissões. `apps/api/auth.py` possui resolvedor e interseção de permissões próprios do BrightBean; **não reconstruir**.
- **Ainda não existe CI validada para a PR #9**. CI verde da #8 não comprova isolamento OAuth em todas as situações.
- ADR-0003 continua proposta; a visibilidade de `MediaAsset.workspace_id = NULL` entre workspaces da mesma organização está demonstrada e não deve ser usada para evidências confidenciais.

## PR #9 — primeira CI falhou somente no Ruff format (2026-10-08)
- [Run #37769541281](https://github.com/OARANHA/CRISE/actions/runs/37769541281), commit `b269dbf155b161514a6383405d3e0ddea53317e4`: Ruff lint, Mypy, Pytest/PostgreSQL e Gitleaks **aprovados**. Pytest: **2.390 passed, 1 skipped, 848 warnings**, incluindo **10/10 casos novos OAuth/MCP**. Docker build `skipped` devido a `ruff format --check` reprovar **um arquivo**: `apps/api/tests/test_oauth_workspace_isolation.py`.
- Tentativa de executar Ruff localmente neste ambiente foi bloqueada por ausência de pacote e acesso ao índice de pacotes. Formatação deve ocorrer pelo workflow temporário `format-oauth-boundaries-once.yml`, fixado em `ruff==0.15.9`, que verifica e grava apenas o arquivo de testes e remove o próprio workflow no mesmo commit do bot.
- **Este workflow ainda não foi validado**. Commits do `github-actions[bot]` podem produzir CI `action_required`; nesse caso um commit normal, sem alteração da lógica dos testes, terá de solicitar nova execução.
- PR #9 **não mesclar** sem cinco jobs da CI real aprovados sobre commit corrigido. Nenhum deploy ou alteração na main. Aguardar green/red/action_required do operador, sem polling.

## PR #9 — correção Ruff concluída; validação integral ainda não realizada (2026-10-08)
- [Workflow de formatação #37770295100](https://github.com/OARANHA/CRISE/actions/runs/37770295100) **success**: executou `ruff check --fix --select I`, `ruff format`, `ruff check` e `ruff format --check` com **Ruff 0.15.9**. O commit `0642e15e7ca5a5e11287e3772f739d7e13984d78` foi enviado por `github-actions[bot]` e removeu o workflow temporário.
- [CI #37770299933](https://github.com/OARANHA/CRISE/actions/runs/37770299933) falhou em formatação porque avaliou o **commit anterior** `290c7a27cdadd2828969a7e70ed282c4e2d34ea5`. No SHA anterior, Ruff lint, Mypy, Pytest e Gitleaks passaram. Pytest: **2.390 passed, 1 skipped, 848 warnings**, dos quais **10/10** cenários novos OAuth/MCP verdes; Docker build skipped.
- [CI #37770322477](https://github.com/OARANHA/CRISE/actions/runs/37770322477) sobre o SHA corrigido `0642e15...` está concluída como **action_required**, com **zero jobs**, originada por `github-actions[bot]`. **Não houve CI completa sobre a versão corrigida**.
- Um commit documental separado via conector GitHub é utilizado para provocar uma execução `pull_request` normal sem alterar código/testes. **Aguardamos comunicação green/red do operador** antes de consultar esse novo resultado, sem polling.
- PR #9 não integrada; PR #2 ainda draft fora da main. Nenhum deploy, segredo ou dado real.

## PR #9 validada; PR #10 — credenciais aquecidas em cache (2026-10-08)
- PR #9 integrada na branch de importação em `0c07b97047e92573553a1bd6f8fff1b3a44c2eb2`. [Run CI #37771059913](https://github.com/OARANHA/CRISE/actions/runs/37771059913): cinco jobs success, **2.390 passed, 1 skipped, 848 warnings**, **10/10** cenários OAuth/MCP aprovados.
- **PR #10 proposta, CI pendente:** sete regressões com token API **previamente utilizado** e linha de credencial em cache; testar revogação, remoção/redução de permissões, modificações M2M allowlist nos dois sentidos, exclusão de membership e vencimento, em REST/MCP. Reutiliza o código de `apps/api_keys/services.py` e `apps/api_keys/signals.py`, sem alterar código de produção.
- Cache de testes Django não equivale a uma validação real de Redis com múltiplos processos. Esse gate seguirá aberto. Sem merge na `main`, sem deploy, contas sociais reais ou dados de clientes. Aguardar green/red do operador sem polling.

## PR #10 aprovada; PR #11 proposta — roteamento dos webhooks da Meta (2026-10-08)
- [PR #10](https://github.com/OARANHA/CRISE/pull/10) integrada na branch de importação (`78c18b4318147bab0472cf3fb7b798c9c71b05c2`). [CI #37773171776](https://github.com/OARANHA/CRISE/actions/runs/37773171776): cinco jobs verdes, **2.397 testes aprovados, 1 ignorado, 855 avisos**, 7/7 regressões com API keys e cache Django previamente aquecido.
- **PR #11 proposta; CI pendente:** três testes sintéticos sobre eventos Meta em dois workspaces da mesma organização ou de organizações diferentes. Código existente `apps/inbox/webhooks.py::_process_meta_events` filtra `account_platform_id` e permite múltiplas contas/workspaces com o mesmo identificador nativo quando os segredos correspondem. `SocialAccount` possui unicidade `(workspace, platform, account_platform_id)`, não global.
- **Risco do produto:** a mesma página social conectada em workspaces de clientes distintos na mesma organização recebe o mesmo evento de webhook em ambos. Esse comportamento pode ser legítimo na base BrightBean, mas não autoriza compartilhar mensagens ou evidências privadas do VIGIAFAST. Não alterar roteamento sem avaliação de compatibilidade e decisão na ADR-0003.
- Testes da PR #11 ainda **não validados**. Regras originais e operações externas intactas. PR #2 permanece draft; sem merge em main, deploy ou dados reais. Aguardar green/red informado pelo operador; sem polling.

## PR #11 — CI vermelha somente em Ruff format (2026-10-08)
- [Run #37775101149](https://github.com/OARANHA/CRISE/actions/runs/37775101149) no SHA `d6c587156edb7b4e4f80b1824d8d3deb552dd1ef`: Pytest **2.400 passed / 1 skipped / 858 warnings**, incluindo **3/3 casos novos Meta webhook**. Ruff `check`, Mypy, Gitleaks aprovados. Ruff `format --check` acusou 1 arquivo (`apps/inbox/tests/test_webhooks.py`); Docker build skipped.
- Criado workflow **temporário de execução única** `format-meta-webhook-once.yml`, que usa Ruff **0.15.9**, formata/testa apenas o arquivo afetado e remove o próprio workflow no commit automático. Os testes demonstram que ID nativo repetido na mesma organização gera mensagens nos dois workspaces: risco da arquitetura, **não** autorização para compartilhar mensagens privadas.
- **Resultado da correção verificado:** [formatador #37777934154](https://github.com/OARANHA/CRISE/actions/runs/37777934154) passou com Ruff 0.15.9 (`ruff check`, `ruff format`, `ruff format --check`), gerando commit do bot `f32523a5b5012611da91a8dc58719e80de74d010`. No mesmo commit, o workflow temporário foi removido. [CI vermelha #37777938776](https://github.com/OARANHA/CRISE/actions/runs/37777938776) foi executada no **SHA anterior** `40010073717c3c21962e071e5d15f296c12c4aa6`, não no código corrigido. Pytest aprovou 2.400 casos (3 novos), 1 skipped e 858 avisos; Ruff check, Mypy e Gitleaks passaram. [CI #37777968456](https://github.com/OARANHA/CRISE/actions/runs/37777968456) no SHA corrigido retornou **action_required, sem jobs**, por ter sido originada por `github-actions[bot]`. Portanto a **CI completa do commit corrigido continua pendente**; novo commit apenas documental pelo conector GitHub solicita execução normal. Não mesclar até cinco jobs success no head exato, e não fazer polling.
- PR #2 continua draft sem merge na main; sem deploy ou dados reais.

## PR #11 aprovada; PR #12 proposta — inbox em tarefas de fundo (2026-10-08)
- [PR #11](https://github.com/OARANHA/CRISE/pull/11) integrada em `feat/brightbean-upstream-import`, commit `613f767d7fa0c59f657dc4d74f9b29fb02b8e2e2`. [CI #37778759366](https://github.com/OARANHA/CRISE/actions/runs/37778759366): cinco jobs success, **2.400 passed, 1 skipped, 858 warnings**, três novos cenários Meta/webhook aprovados.
- **PR #12 proposta, CI pendente:** cinco regressões de `InboxSyncEngine`: varredura dos três clientes fictícios sem chamada externa, mensagens com mesmo ID remoto em workspaces distintos, atualização que não toca outros clientes, notificações restritas ao workspace de origem e idempotência de notificações.
- O código de `apps/inbox/tasks.py` usa `social_account` como chave do upsert e `workspace` para selecionar destinatários das notificações; não reconstruir nem alterar esse fluxo antes de verificar testes.
- **Riscos ainda abertos:** a mesma conta nativa repetida na mesma organização pode receber webhook em mais de um workspace; Redis multiworker, filas e storage de evidências confidenciais não estão homologados. ADR-0003 continua proposta. Sem dados de clientes reais, sem deploy e sem merge na main.

## PR #12 validada; PR #13 proposta — notificações de responsáveis revogados (2026-10-08)
- [PR #12](https://github.com/OARANHA/CRISE/pull/12) integrada na branch de importação, commit `250a88f5a780715f1a82d8327ada4e28e8445bbd`; [CI #37784489968](https://github.com/OARANHA/CRISE/actions/runs/37784489968): cinco jobs success, **2.405 passed, 1 skipped, 858 warnings**; cinco casos de tarefas de fundo passaram.
- **Achado de revisão estática:** `apps/inbox/views.py::assign_message` valida associação do responsável ao workspace no momento da atribuição, mas `apps/inbox/tasks.py::_notify_new_message` e `_notify_sla_overdue` notificavam `message.assigned_to` sem validar se essa associação ainda existe. Após desligamento, a FK `InboxMessage.assigned_to` persiste, criando risco de envio de corpo de mensagem/identificadores ao usuário removido.
- **PR #13 proposta; CI PENDENTE:** `_notification_users` reutiliza `WorkspaceMembership` para validar responsável atual. Se não pertencer ao workspace, notifica apenas owners/managers atuais do workspace de origem (mesmo fallback de mensagens sem responsável). Adiciona **oito cenários parametrizados sintéticos**: responsável válido, responsável somente em outro cliente da mesma/outra organização e funcionário desligado, para novo evento e SLA. Preserva rotas, autenticação e esquema.
- **Limites:** não altera o controle de atribuição pelo usuário, não garante ausência de corrida entre validação e entrega por filas externas, nem resolve o compartilhamento de contas Meta ou mídia organizacional. ADR-0003 permanece proposta. Sem deploy, dados reais ou merge na main; aguardar green/red sem polling.

## PR #13 validada; gate documental de evidências privadas, PR #14 proposta (2026-10-08)
- [PR #13](https://github.com/OARANHA/CRISE/pull/13) integrada à branch de importação: merge `fc12754fcc2c328c0d01ac92a288c14792381bab`. [CI #37787128260](https://github.com/OARANHA/CRISE/actions/runs/37787128260) cinco jobs success; **2.413 passed, 1 skipped, 858 warnings**, incluindo **8/8 regressões** de destinatários de notificação da inbox.
- **Inspeção do código:** `MediaAsset.file` grava em `media_library/`, e Caddy/`PUBLIC_MEDIA_PREFIXES` permitem acesso público anônimo a esse prefixo porque redes sociais precisam baixar mídia de publicações. Uma tela de download autenticada não protege a URL direta do mesmo arquivo. `for_workspace_with_shared` também expõe mídia org-shared para workspaces da mesma organização.
- **PR #14 proposta, documentação apenas, CI pendente:** nova [ADR-0004](docs/decisions/ADR-0004-private-evidence-storage.md), status **PROPOSTA/NÃO ACEITA**, formaliza contrato de armazenamento privado e separados de mídias públicas, com RBAC por workspace, download autorizado, hash, proveniência, auditoria e revisão humana. **Não foi implementado nenhum componente de evidência**.
- ADR-0003 continua proposta; decisões de tenancy e armazenamento exigem revisão explícita. Não ligar contas/clientes reais, não alterar `main`, não fazer deploy. Aguardar green/red do operador sem polling da PR #14.

## PR #14 integrada; proposta de clientes observadores/operadores na ADR-0003, PR #15 (2026-10-08)
- [PR #14](https://github.com/OARANHA/CRISE/pull/14) integrada em `feat/brightbean-upstream-import`, merge `7ed877a27175d8aa9967ffa0d5894338d4ef0845`. [CI #37789363791](https://github.com/OARANHA/CRISE/actions/runs/37789363791): cinco jobs aprovados, **2.413 passed / 1 skipped / 858 warnings**. **ADR-0004 continua PROPOSTA, nenhum storage privado implementado.**
- **Requisito de produto confirmado na conversa:** aproveitar integralmente as funcionalidades do clone BrightBean, permitir crescimento além dos 9 clientes iniciais e operar dois tipos de cliente no produto: observador (portal) e colaborador/operador (ferramentas permitidas do workspace), além de funcionários internos multi-cliente.
- **Verificação de código:** `apps/client_portal` já contém dashboard, convites por link mágico, fila/aprovações, posts publicados e atividade. `portal_reports` apenas renderiza template. `generate_magic_link` exige CLIENT, `portal_auth_required` verifica sessão+participação, e `portal_approval_queue` filtra comentários internos condicionalmente a `workspace_role=CLIENT`. `WorkspaceMembership` e `CustomRole` são candidatos ao reuso; `RBACMiddleware` assume uma organização por usuário na v1.
- **PR #15 proposta (CI ainda NÃO consultada):** documentação ADR-0003, arquitetura, segurança e roadmap definindo personas internas, clientes observadores e clientes operadores, sem prometer que uma combinação de papéis já seja segura. **Nenhuma mudança funcional** ou aprovação de ADRs.
- **Gates:** testes cruzados A/B/C para acesso cliente, edição, comentários internos, aprovação, convites, sessão revogada, relatórios, arquivos e módulos originais; evitar org-shared privado e o fanout de webhook Meta. ADR-0003 e ADR-0004 continuam **NÃO ACEITAS**; PR #2 ainda draft em `main`; nenhum deploy/dado real. Aguardar `green`/`red` do operador sem polling.

## PR #15 integrada; PR #16 proposta — comentários internos no portal (2026-10-08)
- [PR #15](https://github.com/OARANHA/CRISE/pull/15) integrada em `feat/brightbean-upstream-import`, merge `3fc4b56d4f7e5bb8f83a2dbe75f20c025386e264`. [CI #37799250321](https://github.com/OARANHA/CRISE/actions/runs/37799250321): cinco jobs success, **2.413 passed, 1 skipped, 858 warnings**. A ADR-0003 ainda é PROPOSTA.
- **Risco observado em código:** `portal_approval_queue` filtra comentários internos somente quando `workspace_role == CLIENT`; após uma promoção a EDITOR mantendo sessão de portal, a página poderia exibir comentários internos. Seus `Prefetch("replies")` traziam também respostas internas. Além disso `approvals.views.comment_attachment` verifica apenas associação ao workspace e permite ao papel CLIENT solicitar por URL direta o anexo de comentário interno se souber os UUIDs.
- **PR #16 proposta, ainda sem CI:** manter o portal sempre filtrado para comentários e replies EXTERNAL, independentemente do papel do usuário na sessão; negar anexo interno a `WorkspaceRole.CLIENT` por UUID direto, preservando anexo externo e leitura interna para editor autorizado. Seis testes novos sintéticos no portal e nos anexos; proteção não cobre ainda operadores externos promovidos a papéis de equipe em rotas internas — pendente de política formal da ADR-0003.
- Sem autenticação real, novas APIs, migração, infraestrutura, coleta externa, deploy, dados de cliente, merge na main ou aceitação de ADRs. Aguardar `green`/`red`, sem polling.

## PR #16 integrada; PR #17 proposta — exclusão cruzada de comentários (2026-10-08)
- [PR #16](https://github.com/OARANHA/CRISE/pull/16) integrada na branch de importação em `821d2202c66a644236ab84f5548a6af54b8cfb0a`. [CI #37803584176](https://github.com/OARANHA/CRISE/actions/runs/37803584176): cinco jobs success, **2.419 passed, 1 skipped, 864 warnings**, seis regressões novas aprovadas.
- **Lacuna encontrada em código:** `apps/approvals/comments.py::delete_comment` consultava `PostComment` por UUID sem verificar `post__workspace`. Um autor ou moderador legitimamente autorizado no workspace A poderia tentar excluir um comentário de outro workspace B/C se conhecesse o ID, porque `delete_comment` usava o workspace A apenas para calcular permissão. `approvals.views.delete_comment` também não cruzava o UUID do `post_id` da URL com o comentário antes de apagá-lo.
- **PR #17 proposta; CI NÃO VERIFICADA:** filtra a exclusão pelo workspace do comentário no serviço, e exige que o `post_id` da URL corresponda a um `Post` do workspace e ao `PostComment`. Sete testes sintéticos negativos/positivos: autor B via URL A, UUID de post incorreto em B, gestor A tentando excluir B/C por serviço, autor B legítimo, gestor B legítimo, colaborador B sem moderação.
- **Riscos ainda abertos:** `get_comments_for_post` pré-carrega replies internas para papel CLIENT em rotas de equipe; atribuição CLIENT→EDITOR ainda exige decisão de identidade/permissões na ADR-0003; compartilhamento de mídia/Meta webhook e storage privado não homologados. ADR-0003/ADR-0004 NÃO ACEITAS. Sem dado real, deploy ou merge da PR #2 na main; aguardar green/red sem polling.

## PR #17 validada; PR #18 proposta — respostas de comentários internos (2026-10-08)
- [PR #17](https://github.com/OARANHA/CRISE/pull/17) integrada à branch de importação em merge `5c29183f599b5a61b6e7e64c18fc9c5c1a7ec418`. [CI #37805298794](https://github.com/OARANHA/CRISE/actions/runs/37805298794): cinco jobs success, **2.428 passed, 1 skipped, 871 warnings**. Sete novos métodos de teste de exclusão, mais dois herdados e reexecutados.
- **Falha de privacidade observada em código:** `apps/approvals/comments.py::get_comments_for_post` excluía comentários raiz INTERNAL para usuários com `WorkspaceRole.CLIENT`, mas `Prefetch("replies")` buscava replies de qualquer `visibility`, incluindo INTERNAL. A rota HTMX `apps/approvals/views.py::add_comment` renderiza a consulta do serviço; outras rotas de edição/exclusão também a reutilizam.
- **PR #18 proposta, CI ainda NÃO verificada:** o serviço filtra `Prefetch("replies")` por EXTERNAL para papel CLIENT, preservando todas as respostas para papéis de equipe. Quatro testes sintéticos: raiz/reply externa do cliente, editor enxerga internas, downgrade editor→CLIENT, resposta HTTP HTMX sem exibir resposta interna.
- **Limites:** papel EDITOR de funcionário externo continua indistinguível de funcionário interno em outras rotas; identidade e política de acesso dependem da ADR-0003. A correção proposta não resolve armazenamento privado, org-shared, webhooks Meta repetidos nem autorização em todos os módulos. ADR-0003/ADR-0004 NÃO ACEITAS, PR #2 draft, `main` inalterada, sem deploy; aguardar green/red, sem polling.
