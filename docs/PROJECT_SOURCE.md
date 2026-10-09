# VIGIAFAST — fonte canônica do projeto

**Projeto:** CRISEDIGITAL. **Produto:** VIGIAFAST. **Repositório:** https://github.com/OARANHA/CRISE
**Idioma:** português brasileiro. **Situação:** código-base importado na branch de revisão, com CI e regressões sintéticas aprovadas em PRs específicas; aplicação ainda não homologada nem integrada à `main`.

## Leitura obrigatória ao iniciar qualquer trabalho
1. Este arquivo: `docs/PROJECT_SOURCE.md`.
2. `AGENTS.md`: regras de execução e segurança.
3. `docs/CANONICAL_STATE.md`: estado comprovado, lacunas e próximo passo.
4. `MEMORY.md`: contexto curto de continuidade (não histórico cumulativo).
5. `docs/decisions/`: verificar o status de cada ADR; apenas as **aceitas** determinam decisões arquiteturais.
6. `docs/README.md`: índice; `docs/doutrina/README.md`: procedimentos complementares; `docs/ARCHITECTURE.md`, `docs/INTEGRATIONS.md`, `docs/SECURITY.md`, `docs/ROADMAP.md` conforme tarefa.
7. Código-fonte, testes, Git, PRs e workflows pertinentes ao trabalho. Opcionalmente carregar uma skill em `.agents/skills/` se o agente suportar o padrão.

## Regra de autoridade
- **Estado implementado:** só pode ser afirmado com evidência de arquivos/SHAs, execução de testes ou ambiente observado. Código e comportamento testado prevalecem sobre uma descrição desatualizada.
- **Decisões arquiteturais:** ADR com status Aceita prevalece até que outra ADR a substitua. Propostas não são implementações.
- **Estado operacional:** `docs/CANONICAL_STATE.md` resume evidências verificadas; divergências exigem revalidação e correção documental.
- **Memória:** `MEMORY.md` sintetiza contexto; não substitui evidência, ADR nem código. Snapshots em `docs/historico/` são históricos, nunca fontes de status atual.
- **Chats e resumos da IA não são fonte de verdade.** Nenhuma ação deve ser repetida só porque outro chat informou que aconteceu.

## Ritual de retomada
1. Consultar leitura obrigatória e reconciliar main, branch, SHA, PRs e status de CI **uma vez**.
2. Declarar: **REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION**.
3. Verificar antes de construir se o BrightBean ou componente escolhido já implementa a capacidade.
4. Fazer mudança pequena, testável e reversível em branch separada; atualizar documentação no mesmo PR.
5. Manter `MEMORY.md` como resumo curto e `CANONICAL_STATE.md` como snapshot atualizado; preserve fatos históricos em Git/PRs ou `docs/historico/`, e decisões duráveis em ADR.
6. Não fazer polling de CI: o responsável informa quando estiver pronto.

## Limites explícitos
Não realizar deploy, mexer em outras aplicações/VPS, apagar dados ou executar operações destrutivas sem autorização específica. Nunca publicar dados de clientes ou credenciais neste repositório público.

## Documentação de origens
BrightBean Studio: https://github.com/brightbeanxyz/brightbean-studio — referência de código, licença AGPL-3.0; SHA de base sob avaliação: `96ccc1e88fefa171c4e5ca981dc9f289bdf60d39` (main observado em 2026-10-08). **Importado somente na branch da PR #2, não integrado à main nem homologado.** Ver `docs/INTEGRATIONS.md`.


## Apoio de decisão obrigatório quando disponível

A pedido do responsável pelo projeto (2026-10-08), usar **Wandora JEV.1** como camada de apoio em decisões de arquitetura, segurança e execução do VIGIAFAST. Aplicar a regra operacional descrita em `AGENTS.md`, mantendo rastreabilidade do resultado. O JEV fornece julgamentos probabilísticos, não autoridade: não substitui `REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION`, revisão de código, testes, ADR aceita nem autorização explícita. Quando indisponível, documentar o limite e não simular seu uso.
