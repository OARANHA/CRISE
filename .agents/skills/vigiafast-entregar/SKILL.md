---
name: vigiafast-entregar
description: "Use para concluir uma tarefa do VIGIAFAST via branch, PR, testes e confirmação pontual de GitHub Actions, sem deploy ou merge na main."
---

# Entrega reversível por PR

1. Verifique base/branch/SHA reais e mantenha uma alteração pequena por PR; preserve outras PRs em curso.
2. Inclua regressões sintéticas relevantes. Identifique testes executados e não executados; use Ruff, Mypy, Pytest/PostgreSQL, Gitleaks e Docker quando o pipeline exigir.
3. Registre na PR intenção, módulos reutilizados, riscos, critérios de aceite, SHA, estado de CI e próximo passo.
4. Não alegue `green` antes de verificar os cinco trabalhos concluídos no **head SHA exato**. Não fazer polling; aguarde o operador informar `green`/`red`.
5. Um merge incremental na branch de importação segue o fluxo previamente autorizado após validação. `main`, deploy, fontes reais e operações destrutivas dependem de aprovação explícita.
6. Atualize documentos canônicos com fatos constatados, e não com previsões. Na saída informe PR, commit, resultados e lacunas.

**Nunca:** apagar avisos AGPL, expor segredos/dados reais, aceitar automaticamente ADR-0003/ADR-0004 ou confundir teste em CI com ambiente homologado.
