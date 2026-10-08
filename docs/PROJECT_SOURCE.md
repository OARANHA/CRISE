# VIGIAFAST — fonte canônica do projeto

**Projeto:** CRISEDIGITAL. **Produto:** VIGIAFAST. **Repositório:** https://github.com/OARANHA/CRISE
**Idioma:** português brasileiro. **Situação:** código-base em branch de importação; ainda não testado ou homologado.

## Leitura obrigatória ao iniciar qualquer trabalho
1. Este arquivo: `docs/PROJECT_SOURCE.md`.
2. `AGENTS.md`: regras de execução e segurança.
3. `docs/CANONICAL_STATE.md`: estado comprovado, lacunas e próximo passo.
4. `MEMORY.md`: contexto de continuidade entre sessões.
5. `docs/decisions/`: decisões arquiteturais (ADRs) aceitas.
6. `docs/ARCHITECTURE.md`, `docs/INTEGRATIONS.md`, `docs/SECURITY.md` e `docs/ROADMAP.md`.
7. Código-fonte, testes, Git, PRs e workflows pertinentes ao trabalho.

## Regra de autoridade
- **Estado implementado:** só pode ser afirmado com evidência de arquivos/SHAs, execução de testes ou ambiente observado. Código e comportamento testado prevalecem sobre uma descrição desatualizada.
- **Decisões arquiteturais:** ADR com status Aceita prevalece até que outra ADR a substitua. Propostas não são implementações.
- **Estado operacional:** `docs/CANONICAL_STATE.md` resume evidências verificadas; divergências exigem revalidação e correção documental.
- **Memória:** `MEMORY.md` sintetiza contexto; não substitui evidência, ADR nem código.
- **Chats e resumos da IA não são fonte de verdade.** Nenhuma ação deve ser repetida só porque outro chat informou que aconteceu.

## Ritual de retomada
1. Consultar leitura obrigatória e reconciliar main, branch, SHA, PRs e status de CI **uma vez**.
2. Declarar: **REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION**.
3. Verificar antes de construir se o BrightBean ou componente escolhido já implementa a capacidade.
4. Fazer mudança pequena, testável e reversível em branch separada; atualizar documentação no mesmo PR.
5. Registrar no `MEMORY.md` o que mudou, no `CANONICAL_STATE.md` o que está comprovado e em ADR qualquer decisão durável.
6. Não fazer polling de CI: o responsável informa quando estiver pronto.

## Limites explícitos
Não realizar deploy, mexer em outras aplicações/VPS, apagar dados ou executar operações destrutivas sem autorização específica. Nunca publicar dados de clientes ou credenciais neste repositório público.

## Documentação de origens
BrightBean Studio: https://github.com/brightbeanxyz/brightbean-studio — referência de código, licença AGPL-3.0; SHA de base sob avaliação: `96ccc1e88fefa171c4e5ca981dc9f289bdf60d39` (main observado em 2026-10-08). **Importado somente na branch da PR #2, não integrado à main nem homologado.** Ver `docs/INTEGRATIONS.md`.
