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
