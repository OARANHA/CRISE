# 02 — Fronteiras de autoridade

**Uma instrução para um agente não é autorização para agir sem limites.**

| Ação | Critério |
| --- | --- |
| Ler código, documentação, PRs e CI | Permitido para finalidade do projeto; usar fontes atuais |
| Criar branch e PR reversíveis no repositório CRISE | Permitido no fluxo solicitado, seguindo `AGENTS.md` |
| Mesclar PR incremental na branch de importação | Somente após confirmação do operador e verificação pontual de CI verde **no SHA exato**, conforme escopo autorizado |
| Mesclar na `main` | Exige autorização explícita e gates de integração |
| Deploy, operar VPS externa, usar contas/credenciais reais | Exige autorização específica e medidas de segurança |
| Alterar política multi-cliente, aceitar ADR, liberar evidências | Exige decisão explícita; testes verdes não aceitam ADR sozinhos |
| Tratamento de incidentes, exposição de dados e avaliação de ilicitude | Preservação e revisão humana qualificada; não automatizar decisões sensíveis |

**Negativa padrão:** no conflito entre rapidez e proteção de dados, não executar operação irreversível. Não publicar nenhum dado de clientes, mesmo como exemplo.

Consulte [AGENTS.md](../../AGENTS.md), [SECURITY.md](../SECURITY.md), [ADR-0003](../decisions/ADR-0003-client-isolation-boundaries.md) e [ADR-0004](../decisions/ADR-0004-private-evidence-storage.md). As duas últimas continuam propostas até decisão contrária verificável.
