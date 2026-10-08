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
