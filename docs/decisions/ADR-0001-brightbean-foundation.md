# ADR-0001 — BrightBean como fundação integral

**Data:** 2026-10-08. **Status:** Aceita como direção de produto; execução pendente.

## Contexto
O VIGIAFAST precisa de dashboard, autenticação, multi-workspaces, RBAC, publicação, inbox, analytics, API e MCP para equipe interna com múltiplos clientes. O BrightBean Studio oferece código aberto dessas áreas em Django/Python/PostgreSQL, evitando reconstrução desnecessária.

## Decisão
Usar a base open source integral do BrightBean Studio como ponto de partida; preservar funcionalidades existentes, histórico/origem e condições AGPL-3.0; evoluir a experiência para VIGIAFAST em pt-BR e adicionar módulos próprios para descoberta, crise, evidência e IA.

## Regras
- Não desabilitar/remover capacidades preexistentes sem ADR posterior, justificativa e testes.
- Não tratar integração com contas autorizadas como capacidade de pesquisar todos os posts de terceiros.
- Importação deverá fixar commit de origem e permitir rastrear mudanças do upstream.
- Funcionalidades comerciais/servidores privados não presentes no código aberto não são presumidas livres ou implementadas.

## Consequências
+ Economia de implementação, interfaces e módulos reaproveitados.
- AGPL-3.0 exige cumprimento de atribuição e oferta de código correspondente nas hipóteses previstas; avaliar no contexto da operação.
- Necessita revisão de segurança, multi-tenancy e tradução antes de uso real.

## Estado de execução
Não implementada nesta ADR. Ver `docs/CANONICAL_STATE.md` e histórico Git.
