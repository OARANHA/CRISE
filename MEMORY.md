# MEMORY.md — memória técnica persistente do VIGIAFAST

> Contexto público e sintético. Este arquivo traz **o estado atual**, não todo o histórico. Detalhes verificáveis em [docs/CANONICAL_STATE.md](docs/CANONICAL_STATE.md), ADRs e PRs. Chats **não** são fonte de verdade.

## Produto e missão
- Projeto **CRISEDIGITAL**; produto **VIGIAFAST**; código: [OARANHA/CRISE](https://github.com/OARANHA/CRISE).
- Plataforma interna de monitoramento/gestão de crise para inicialmente **9 clientes**, com controle de acesso por cliente; painel 100% em português brasileiro.
- Instagram, TikTok, Facebook e outras fontes públicas **quando tecnicamente e legalmente viáveis**. Contas conectadas/autorizadas são diferentes de publicações de terceiros.
- Base integral **BrightBean Studio** Django/Python/PostgreSQL, licença AGPL-3.0. Não recriar recursos existentes.
- Possíveis integrações futuras, **ainda não operacionais**: Obsei, Bellingcat Auto Archiver, OpenMagpie, 4CAT, Zeeschuimer.

## Estado em 2026-10-08
- **`main`:** documentação canônica da PR #1; código da aplicação ainda **não mesclado**.
- **PR #2:** importação BrightBean em `feat/brightbean-upstream-import`, **draft**. Upstream fixado em `96ccc1e88fefa171c4e5ca981dc9f289bdf60d39`; 874 arquivos comparados byte a byte em [Actions #37728568048](https://github.com/OARANHA/CRISE/actions/runs/37728568048).
- **PRs #3, #4, #5, #6:** integradas à branch de importação (CI, Caddy/DB, IP de proxies e 16 regressões de isolamento da inbox). Head após #6: `1b0436980c618e9931b1dc78aa6c818bc4849abd`.
- **Última CI verificada:** [run #37763047990](https://github.com/OARANHA/CRISE/actions/runs/37763047990) no SHA `006f2e765a42ddebec8fd2bae7359121fd3b82af`: cinco trabalhos verdes; **2.364 passed / 1 skipped / 822 warnings**, incluindo **16/16** testes inter-cliente.
- **Nenhum deploy**, nenhuma conta social real conectada e nenhum cliente real cadastrado no repositório.

## Pendências críticas
1. **Isolamento completo:** hipótese de 1 workspace por cliente **não aceita**. MediaAsset com `workspace_id=NULL` é compartilhado com a organização; verificar efeito nos nove clientes, política de mídias e evidências. [ADR-0003](docs/decisions/ADR-0003-client-isolation-boundaries.md) em proposta.
2. Ampliar teste adversarial de posts, mídia, arquivos, tarefas, cache, MCP/OAuth, relatórios e papéis.
3. Armazenamento **privado** de evidências, LGPD, hashes, origens, retenção, auditoria.
4. Integrações de inteligência/arquivamento, busca de menções e classificação contextual pt-BR.
5. Transformação incremental de interface BrightBean em **VIGIAFAST** preservando funcionalidades.

## Próximo trabalho
- Revisar e testar a proposta da PR documental de reconciliação; **não tratar CI nova como verde até verificar**.
- PR #8 de testes A/B/C em **posts e mídia** criada, aguardando CI. A suíte descreve o acesso organizacional compartilhado existente sem autorizar evidências privadas nesse espaço. Corrigir isolamentos falhos somente após evidências e análise de dependências.
- Não mesclar a PR #2 na `main` nem implantar com dados reais antes de encerrar gates essenciais e obter autorização.

## Operação de agentes
Leia `docs/PROJECT_SOURCE.md` → `AGENTS.md` → estado canônico → memória → ADRs → código/testes. Trabalhe com branches/PRs, resultados comprovados e atualize estes arquivos em cada slice. Não monitorar CI em loop; o operador avisa **green/red**.

## PR #8 — primeira CI vermelha por importação (2026-10-08)
- [Run #37766160766](https://github.com/OARANHA/CRISE/actions/runs/37766160766): falha apenas em `ruff check`, regra `I001` (import block un-sorted) no novo arquivo `apps/api/tests/test_post_media_client_boundaries.py`. O `ruff format --check` não chegou a executar; build Docker skipped.
- **Pytest aprovou 2.380 casos, 1 skipped e 838 warnings**, incluindo **16/16 cenários novos** de segurança para posts, mídia e mídia organizacional compartilhada. Mypy e Gitleaks passaram.
- O workflow temporário `format-post-media-once.yml` aplica `ruff check --fix --select I` e `ruff format` usando a **mesma versão 0.15.9** da CI, verifica o resultado e remove a si próprio no commit bot. Nenhuma alteração em código de produção.
- **A execução e o commit automático ainda não estão confirmados.** O GitHub pode deixar a CI sobre um commit criado por `github-actions[bot]` como `action_required`; nesse caso uma alteração por conector GitHub precisará disparar nova validação. Não afirmar green antes de evidências. Sem polling, merge ou deploy.

## CI PR #8 — ação pendente após formatação concluída (2026-10-08)
- Formatador real aprovado: [Actions #37767396264](https://github.com/OARANHA/CRISE/actions/runs/37767396264), bot commit `a057fba3ff508423d479f5838859a326aeb5db7e`.
- CI red [#37767401425](https://github.com/OARANHA/CRISE/actions/runs/37767401425) rodou o commit **anterior**, não é regressão comprovada.
- [#37767422744](https://github.com/OARANHA/CRISE/actions/runs/37767422744) no bot commit foi `action_required` sem jobs.
- Atualizar PR #8 pelo conector GitHub apenas em docs para pedir CI normal. Esperar resultado real, sem polling/merge/deploy.

## PR #8 validada; novo gate OAuth/MCP (2026-10-08)
- PR #8 integrada na branch de importação `46546e22ac4f1836de1fe7b1a0b4d3228a77ce4b`. [CI #37768145395](https://github.com/OARANHA/CRISE/actions/runs/37768145395) com 5 jobs verdes; 2.380 testes aprovados, 1 ignorado. Os 16 novos casos de posts/mídia passaram.
- PR #9 proposta de testes da autenticação OAuth/MCP e revogação/permissões por workspace. Nenhum deploy, cliente real ou aprovação integral de isolamento. Aguardar CI (green/red), sem polling.

## PR #9 — primeira CI falhou somente no Ruff format (2026-10-08)
- [Run #37769541281](https://github.com/OARANHA/CRISE/actions/runs/37769541281), commit `b269dbf155b161514a6383405d3e0ddea53317e4`: Ruff lint, Mypy, Pytest/PostgreSQL e Gitleaks **aprovados**. Pytest: **2.390 passed, 1 skipped, 848 warnings**, incluindo **10/10 casos novos OAuth/MCP**. Docker build `skipped` devido a `ruff format --check` reprovar **um arquivo**: `apps/api/tests/test_oauth_workspace_isolation.py`.
- Tentativa de executar Ruff localmente neste ambiente foi bloqueada por ausência de pacote e acesso ao índice de pacotes. Formatação deve ocorrer pelo workflow temporário `format-oauth-boundaries-once.yml`, fixado em `ruff==0.15.9`, que verifica e grava apenas o arquivo de testes e remove o próprio workflow no mesmo commit do bot.
- **Este workflow ainda não foi validado**. Commits do `github-actions[bot]` podem produzir CI `action_required`; nesse caso um commit normal, sem alteração da lógica dos testes, terá de solicitar nova execução.
- PR #9 **não mesclar** sem cinco jobs da CI real aprovados sobre commit corrigido. Nenhum deploy ou alteração na main. Aguardar green/red/action_required do operador, sem polling.

## PR #9 — formatador aprovado; action_required em commit bot (2026-10-08)
- [Formatter #37770295100](https://github.com/OARANHA/CRISE/actions/runs/37770295100) success; SHA do bot `0642e15e7ca5a5e11287e3772f739d7e13984d78`, com workflow temporário removido.
- [CI #37770299933](https://github.com/OARANHA/CRISE/actions/runs/37770299933) red de commit anterior; Pytest, Mypy, Gitleaks e Ruff lint verdes (2.390 testes passed, 1 skipped, 848 warnings, incluindo dez casos OAuth/MCP).
- [CI #37770322477](https://github.com/OARANHA/CRISE/actions/runs/37770322477) action_required no bot commit e sem jobs. Um commit de docs pelo conector solicitará nova CI; **aguardar green/red**. Não mesclar a PR #9 antes dos cinco jobs aprovados.

## PR #9 validada; PR #10 — credenciais aquecidas em cache (2026-10-08)
- PR #9 integrada na branch de importação em `0c07b97047e92573553a1bd6f8fff1b3a44c2eb2`. [Run CI #37771059913](https://github.com/OARANHA/CRISE/actions/runs/37771059913): cinco jobs success, **2.390 passed, 1 skipped, 848 warnings**, **10/10** cenários OAuth/MCP aprovados.
- **PR #10 proposta, CI pendente:** sete regressões com token API **previamente utilizado** e linha de credencial em cache; testar revogação, remoção/redução de permissões, modificações M2M allowlist nos dois sentidos, exclusão de membership e vencimento, em REST/MCP. Reutiliza o código de `apps/api_keys/services.py` e `apps/api_keys/signals.py`, sem alterar código de produção.
- Cache de testes Django não equivale a uma validação real de Redis com múltiplos processos. Esse gate seguirá aberto. Sem merge na `main`, sem deploy, contas sociais reais ou dados de clientes. Aguardar green/red do operador sem polling.

## PR #10 integrada — próximo gate webhook (2026-10-08)
- `feat/brightbean-upstream-import` após PR #10: `78c18b4318147bab0472cf3fb7b798c9c71b05c2`; [CI #37773171776](https://github.com/OARANHA/CRISE/actions/runs/37773171776), cinco jobs aprovados, **2.397 passed / 1 skipped**, sete casos novos de credenciais em cache.
- PR #11 de regressões Meta para páginas com IDs nativos distintos/repetidos: documentar roteamento por organização/workspace, sem mudar código original. **Pendente CI**.
- Compartilhamento organizacional de mídia e compartilhamento de webhooks por mesma conta nativa são riscos a decidir, não capacidades aprovadas para evidências confidenciais. ADR-0003 segue PROPOSTA.
- Sem deploy, sem merge na main. Operador informa green/red; não fazer polling.

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
