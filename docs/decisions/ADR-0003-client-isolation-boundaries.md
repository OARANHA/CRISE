# ADR-0003 — Limites de isolamento entre clientes

**Data:** 2026-10-08  
**Status:** **Proposta — NÃO ACEITA**. Exige validação de código, testes e decisão explícita antes de usar dados reais.

## Contexto
O VIGIAFAST prevê inicialmente nove clientes e funcionários que administram contas, menções, ocorrências e relatórios sem permitir acesso indevido de um cliente aos dados de outro. O BrightBean já tem `Organization`, `Workspace`, `OrgMembership`, `WorkspaceMembership`, chaves de API associadas a um único workspace e filtros na inbox.

A [PR #6](https://github.com/OARANHA/CRISE/pull/6) comprovou 16 cenários sintéticos em inbox REST/MCP/HTMX e emissão de chave: o cliente A não acessou mensagens dos clientes B (outro workspace na mesma organização) e C (outra organização).

**Mas:** `apps/media_library/managers.py::MediaAssetManager.for_workspace_with_shared` inclui mídias com `workspace_id IS NULL` e `organization_id` correspondente. A API `apps/api/routers/media.py` reutiliza esse filtro. Portanto, *workspaces diferentes de uma mesma organização não garantem isolamento absoluto de toda a mídia*: existe compartilhamento organizacional intencional no produto original. Não se pode assumir que um workspace == um tenant totalmente isolado.

O middleware original `apps/members/middleware.py` também descreve suporte a **uma organização por usuário na v1**. Colocar cada cliente em uma organização separada exigiria validação especial para funcionários que administram mais de um cliente.

## Opções a avaliar
1. **Uma organização da empresa + um workspace por cliente:** facilita operador centralizado, mas exige política explícita sobre ativos organizacionais compartilhados e testes de vazamento.
2. **Uma organização por cliente:** tende a reforçar fronteira dos ativos org-shared, mas exige evolução comprovada de acesso multi-organização para equipe interna; maior impacto sobre o BrightBean.
3. **Operador central + tenants de domínio separados:** possível no futuro, porém só com arquitetura, segurança e migrações aprovadas; não reconstruir RBAC antes de avaliar a base.

## Proposta de trabalho, não decisão de implantação
- Manter, **para fins de teste**, clientes sintéticos A/B na mesma organização e C em outra.
- Testar ativos privados por workspace versus ativos org-shared. Reproduzir o compartilhamento existente, quantificar seu impacto e definir se deve ser negado por padrão na experiência VIGIAFAST.
- Manter **evidências, capturas e dados reputacionais privados** em storage segregado por cliente, nunca na mídia pública de publicação, nem compartilhados por organização por padrão.
- Operadores acessam dados de clientes distintos **somente quando** possuem escopo/permissão explícitos.
- Decisões jurídicas/reputacionais sempre com revisão humana. Não incluir dados reais em testes.
- Estabelecer gate de regressão REST, MCP, HTMX, workers, armazenamento e relatórios antes de aceitar ADR.

## Gate para aceitar
Exigir teste negativo demonstrando que usuário sem permissão de B não acessa listagem, UUID, download, anotação ou relatórios de B, mesmo conhecendo identificadores. Se houver compartilhamento intencional, defini-lo como uma concessão específica, auditável e **nunca aplicável a evidências privadas**.

## Consequências e riscos
- Reutilização da base reduz custo mas exige compatibilização com modelo de compartilhamento atual.
- Até completar os testes e decisão, **proibido tratar a aplicação como homologada para nove clientes reais**.

## Referências
- [Matriz de isolamento](../audits/2026-10-08-client-isolation-matrix.md)
- `apps/media_library/managers.py`
- `apps/api/routers/media.py`
- `apps/members/middleware.py`
- [PR #6](https://github.com/OARANHA/CRISE/pull/6)
