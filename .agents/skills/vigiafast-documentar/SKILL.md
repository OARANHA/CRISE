---
name: vigiafast-documentar
description: "Use ao preparar um PR ou uma retomada para atualizar a documentação viva, arquivar estados superados e identificar contradições."
---

# Documentação viva sem contradições

1. Leia `docs/README.md`, `docs/PROJECT_SOURCE.md` e `docs/CANONICAL_STATE.md`.
2. Confirme estado atual no GitHub; não propague linhas `CI pendente`, `PR aberta` ou `não testado` se os fatos mudaram.
3. Mantenha `docs/CANONICAL_STATE.md` **curto**, datado e com SHAs; mantenha `MEMORY.md` curto e orientado à continuidade.
4. Histórico antigo deve permanecer em Git/PRs e, quando houver snapshot longo a retirar, em `docs/historico/` como material **não canônico**.
5. Não reescreva ADR proposta como aceita; evite repetir regras de segurança e arquitetura em skills ou memória — referencie o arquivo de autoridade.
6. Verifique links relativos, frontmatter `name/description` das skills e se `AGENTS.md` aponta para a fonte correta.

**Saída:** arquivos atualizados, quais afirmações ficaram comprovadas, o que ainda depende de CI/revisão e onde está o histórico.
