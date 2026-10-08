---
name: vigiafast-retomar
description: "Use ao retomar qualquer tarefa do VIGIAFAST para reconciliar estado de Git, PRs, CI, ADRs e lacunas antes de agir."
---

# Retomada com estado comprovado

1. Leia `docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/CANONICAL_STATE.md` → `MEMORY.md`; depois ADRs relevantes.
2. Confirme `main`, `feat/brightbean-upstream-import`, branch, SHAs e PRs relevantes no GitHub. Não confiar em status de chats ou snapshots antigos.
3. Verifique CI apenas quando necessário, **uma vez**, relacionando execução concluída ao SHA exato. O operador avisa `green`/`red`; não fazer polling.
4. Abra código e testes da função solicitada; diferencie implementado, testado e operacional.
5. Apresente `REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION` em poucas linhas e prossiga só dentro do escopo autorizado.
6. Se estiver faltando autorização para deploy, merge na `main`, uso de credenciais/dados reais ou decisão de ADR, **pare e solicite autorização específica**.

**Saída:** referenciar estado real, lacuna principal, próximo slice e gates. Não reexecutar ações por causa de relatos anteriores.
