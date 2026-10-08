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
