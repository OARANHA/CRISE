# Índice da documentação viva — VIGIAFAST

**Entrada principal:** [PROJECT_SOURCE](PROJECT_SOURCE.md) define autoridade e ordem de leitura; [AGENTS.md](../AGENTS.md) estabelece regras de execução. Este índice orienta, mas **não cria autoridade superior** às ADRs aceitas ou à evidência real do código/CI.

| Necessidade | Fonte |
| --- | --- |
| Situação verificada, SHA, PRs e lacunas | [CANONICAL_STATE.md](CANONICAL_STATE.md) |
| Continuidade curta entre sessões | [MEMORY.md](../MEMORY.md) |
| Regras de operação e interpretação | [Doutrina](doutrina/README.md) |
| Decisões arquiteturais e status | [ADRs](decisions/) — verificar o cabeçalho de cada ADR |
| Arquitetura e componentes-alvo | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Limites e riscos de segurança | [SECURITY.md](SECURITY.md) |
| Integrações e alcance real das redes sociais | [INTEGRATIONS.md](INTEGRATIONS.md) |
| Planejamento por fase | [ROADMAP.md](ROADMAP.md) |
| Evidências detalhadas e auditorias | [Auditorias](audits/) · [Matriz de autorização PR #21](audits/2026-10-08-authorization-actor-resource-matrix.md) · [Reprodução HTTP PR #22](audits/2026-10-08-org-directory-http-reproduction.md) · [Afiliação e gate de decisão M10](audits/2026-10-08-m10-actor-affiliation-architecture-gate.md) · [Contexto multi-organização M11](audits/2026-10-08-m11-multi-org-context-characterization.md) · [Deliberação ADR-0003 (proposta)](audits/2026-10-08-adr0003-tenancy-deliberation.md) |
| Registros anteriores, inclusive PRs já concluídas | [Histórico](historico/README.md) |
| Procedimentos para agentes | [Skills VIGIAFAST](../.agents/skills/README.md) |

## Contrato da documentação viva

1. **Estado atual é um snapshot curto e datado**, não um diário. Revise e substitua afirmações superadas somente depois de verificar o GitHub. Descreva o SHA do **momento observado**; não invente estado pós-merge.
2. **Histórico é append-only**: PRs, commits e CI são a trilha primária. Snapshots antigos vão a `docs/historico/` quando necessário, identificados como não normativos.
3. **ADRs propostas não autorizam implementação/produção.** Uma ADR aceita orienta decisões; alterações duráveis exigem revisão explícita.
4. **Skills são receitas operacionais, não prova de execução** e não substituem testes, RBAC ou autorização. Um agente só as utiliza se sua ferramenta as reconhecer/carregar.
5. **No mesmo PR**, ajustar `CANONICAL_STATE.md` e `MEMORY.md` apenas com fatos verificados; atualizar documentos temáticos e ADRs quando a mudança exigir. Identificar `proposto`, `implementado`, `testado`, `operacional`.
6. **Nunca** registrar segredos, dados reais de clientes ou evidências privadas no GitHub público; respeitar a AGPL-3.0 do BrightBean.

## Auditoria rápida de desatualização

- Comparar SHAs e estados de PR do snapshot com o GitHub; marcar diferenças.
- Procurar afirmações como "CI pendente", "não testado" ou "PR aberta" sem data/evidência.
- Conferir se a capacidade documentada existe no código e se testes relevantes a cobrem.
- Conferir se os links locais e status das ADRs estão coerentes.
- Atualizar por PR e **não** fazer polling contínuo.
