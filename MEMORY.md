# VIGIAFAST — memória operacional resumida

**Não é fonte de verdade.** Ordem de leitura: `docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/CANONICAL_STATE.md` → esta memória → ADRs → código/testes/CI.

## Produto e reuso
- CRISEDIGITAL / VIGIAFAST: equipe interna e operadores de clientes, inicialmente nove, escalável; interface pt-BR.
- Reusar integralmente BrightBean Studio Django/Python/PostgreSQL (AGPL-3.0): editor, calendário, aprovações, portal, inbox, analytics, API/MCP, RBAC.
- Obsei e Bellingcat Auto Archiver são candidatos. Coleta pública de terceiros, armazenamento de evidências privadas e relatórios reputacionais completos **não estão homologados/implementados**.

## Estado observado em 2026-10-08
- `main`: `f6883b747ce1a6ae6a6968948da5225332ed4f2f`, preservada.
- `feat/brightbean-upstream-import`: `e5f9ec7c6568729bc26220f1ab44b156bc7d6477`; PR #26 integrada somente nessa branch.
- [CI pós-merge PR #26](https://github.com/OARANHA/CRISE/actions/runs/37858665680): GREEN no SHA acima, cinco jobs success. Dez testes de **caracterização** M10 aprovados; **não corrigem M10**.
- PR #2 aberta e Draft para `main`. ADR-0001/0002 aceitas; ADR-0003/0004 propostas e **não aceitas**. Nenhum deploy autorizado.

## Próximo gate: identidade, permissão e classe de dado (M10)
- `WorkspaceMembership` registra papel e permissões; não registra afiliação confiável entre funcionário VIGIAFAST e operador do cliente. `EDITOR` de ambos acessa comentários, replies e anexos `INTERNAL` nas rotas caracterizadas.
- Auditoria de alternativas e proposta de menor impacto: [docs/audits/2026-10-08-m10-actor-affiliation-architecture-gate.md](docs/audits/2026-10-08-m10-actor-affiliation-architecture-gate.md). Afiliação independente, não inferida de `is_staff` nem do role, e predicado por ator, ação, recurso, cliente e confidencialidade; **somente PROPOSTO**.
- Próximo trabalho de runtime depende de decisão explícita sobre ADR-0003, autoridade para classificar usuários legados e política de acesso INTERNAL. A ADR-0004 continua necessária para storage privado. M09 (`Post.internal_notes`) separado.
- Sem dados reais, deploy, merge sem autorização ou polling de CI. Operador comunica `green`/`red` para verificar uma única execução no SHA da nova PR.
