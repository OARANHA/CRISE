# 03 — Provas, tempo e atualização

**Ritual obrigatório ao retomar:** `REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION`.

1. Registrar data e SHAs de `main`, staging e branch de trabalho. Verificar estado atual das PRs relacionadas.
2. Para dizer "passou", encontrar execução de CI concluída com sucesso **no SHA exato** e identificar trabalhos aprovados; uma CI de commit anterior não comprova o atual.
3. Separar evidência de leitura estática, teste sintético e validação operacional real. Não inferir produção ou integração de redes por CI de aplicação.
4. Usar [CANONICAL_STATE](../CANONICAL_STATE.md) como fotografia, **não como diário**. Antes de publicar mudança, substituir status vencidos e registrar apenas estado comprovado.
5. Usar `MEMORY.md` como orientação curta e `docs/historico/` para snapshots passados. PRs e logs GitHub mantêm a trilha completa, inclusive falhas.
6. Esperar o operador comunicar `green` ou `red`. **Nunca fazer polling contínuo**. Conferir uma vez, corrigir se necessário e deixar o próximo ciclo ao operador.

**Obrigação de honestidade:** status são `proposto`, `implementado sem validação`, `testado no cenário X` ou `operacional com autorização`. "Tudo pronto" não é evidência. Nunca afirmar que uma execução planejada já ocorreu.
