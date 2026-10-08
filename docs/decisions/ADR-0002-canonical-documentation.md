# ADR-0002 — Documentação canônica independente de chats

**Data:** 2026-10-08. **Status:** Aceita.

## Contexto
Sessões de IA e handoffs podem perder contexto ou refletir estados antigos; decisões e memória apenas em chat comprometem rastreabilidade e continuidade.

## Decisão
GitHub `OARANHA/CRISE` é a fonte persistente e auditável do projeto. `docs/PROJECT_SOURCE.md` indica ordem de leitura; `AGENTS.md` define regras; `MEMORY.md` guarda memória técnica resumida; `docs/CANONICAL_STATE.md` registra estado comprovado; ADRs documentam decisões; arquitetura/integrações/segurança/roadmap registram desenho e limites.

## Política de atualização
- Toda entrega atualiza documentação correlata no mesmo PR; alterações relevantes devem apresentar SHA, testes e estado.
- Chats são contexto temporário, não autoridade. Na retomada, reconciliar Git, CI, código e docs.
- Informações internas ou pessoais de clientes nunca vão ao repositório público.
- Manter distinção explícita entre **proposto**, **em construção**, **testado** e **operacional**.

## Consequências
+ Continuidade independente de conversas e de um fornecedor de IA.
+ Histórico auditável e revisão técnica facilitada.
- Exige disciplina de revisão de documentação em cada alteração funcional.
