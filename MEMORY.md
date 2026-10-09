# VIGIAFAST — memória operacional resumida

**Não é fonte de verdade.** Consultar `docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/CANONICAL_STATE.md` → este arquivo → ADRs → código/testes/CI.

## Produto
- CRISEDIGITAL / VIGIAFAST: operação interna e operadores dos clientes; nove clientes iniciais, sem limites artificiais; interface pt-BR.
- Base integral BrightBean Studio Django/Python/PostgreSQL, AGPL-3.0; preservar editor, calendário, portal, inbox, analytics, mídia editorial, API/MCP e RBAC.
- Obsei/Bellingcat Auto Archiver são candidatos. Sem monitoramento real de terceiros, dados reais, storage privado de evidências ou deploy.

## Estado observado em 2026-10-08
- `main` @ `f6883b747ce1a6ae6a6968948da5225332ed4f2f`, intacta.
- `feat/brightbean-upstream-import` @ `20fcb3aae63ffc2763939818f36b70841ce1ed0d`: PR #27 integrada; [CI pós-merge #37862079868](https://github.com/OARANHA/CRISE/actions/runs/37862079868), cinco jobs success nesse SHA.
- PR #2 segue aberta/Draft para `main`.
- ADR-0001 e ADR-0002 aceitas; ADR-0003 e ADR-0004 propostas/não aceitas.

## Gates de segurança
- M10 continua **não corrigido**: EDITOR de equipe e EDITOR externo ainda compartilham acesso a comentários, replies e anexos INTERNAL. PR #26 testou o comportamento, não resolveu. PR #27 registrou [proposta de afiliação confiável](docs/audits/2026-10-08-m10-actor-affiliation-architecture-gate.md).
- Novo slice M11 em branch separada: quatro testes sintéticos para caracterizar a seleção da organização global no middleware. `OrgMembership` pode ter múltiplas organizações para usuário; o middleware global usa `.first()` e `last_workspace_id` separadamente, com possível divergência. [Auditoria M11](docs/audits/2026-10-08-m11-multi-org-context-characterization.md). **CI M11 ainda não verificada; não há mudança de runtime.**
- A decisão de tenancy da ADR-0003 continua bloqueada até autorização humana: organização por cliente ou organização compartilhada; afiliação interna/externa independente do papel, política de classes de dados e migração supervisionada. M09 (`Post.internal_notes`) e ADR-0004 (storage privado) permanecem separados.
- Sem merge automático, deploy, alterações à `main` ou dados reais. Operador avisa `green`/`red` para conferência única no SHA exato.
