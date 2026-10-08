# VIGIAFAST — estado canônico verificável

**Snapshot verificado:** 2026-10-08, a partir de leitura pontual do GitHub. **Não é sincronizado automaticamente**: na retomada, confirmar novamente SHAs, PRs e CI antes de afirmar qualquer status.

## REAL NOW (estado observado ANTES desta PR documental)

| Referência | Situação comprovada |
| --- | --- |
| `main` | `f6883b747ce1a6ae6a6968948da5225332ed4f2f`; fundação documental; BrightBean ainda não integrado |
| `feat/brightbean-upstream-import` | `2cd8878cf9dfba08d9c77ec3234b435b3859b378`; base de desenvolvimento, sem merge na main |
| [PR #2](https://github.com/OARANHA/CRISE/pull/2) | Aberta e draft, da branch de importação para `main`; não mesclada |
| [PR #18](https://github.com/OARANHA/CRISE/pull/18) | Integrada à branch de importação, merge `2cd8878cf9dfba08d9c77ec3234b435b3859b378` |
| [PR #19](https://github.com/OARANHA/CRISE/pull/19) | Aberta, não integrada; head `d94288b2685f9eb0878eda61017fac1e214ce3c9`; **CI desta PR não consultada neste trabalho** |
| Deploy / produção | Não houve deploy autorizado ou evidenciado neste trabalho; a aplicação não está homologada para dados reais |

**Último CI do código alterado inspecionado aqui:** [run #37807764663](https://github.com/OARANHA/CRISE/actions/runs/37807764663) da PR #18, no SHA `9428eb36c25fb7c7795c6fd5d44ce1fc8eda704d`: Ruff, Mypy, Pytest, Gitleaks e Docker build concluíram com sucesso; **2.432 passed, 1 skipped, 872 warnings**. Quatro regressões de visibilidade de comentários passaram. Isso **não é** evidência de CI da PR #19 ou de homologação global da branch.

## PROVEN EVIDENCE — o que existe

- O código importado preserva a base BrightBean (Django/Python/PostgreSQL), com publicação, calendário, inbox, analytics, aprovações, portal do cliente, API/MCP e gestão de workspaces; validar capacidades e restrições por rota e plataforma.
- As PRs [#16](https://github.com/OARANHA/CRISE/pull/16), [#17](https://github.com/OARANHA/CRISE/pull/17) e [#18](https://github.com/OARANHA/CRISE/pull/18) integraram **correções localizadas** de visibilidade do portal, escopo de exclusão e respostas internas de comentários. Não equivalem a isolamento multi-cliente completo.
- O portal tem convites, aprovações, publicações e histórico; `apps/client_portal/views.py::portal_reports` **apenas renderiza template**, sem relatório de crise pronto.
- A [ADR-0002](decisions/ADR-0002-canonical-documentation.md) está **aceita**. A [ADR-0003](decisions/ADR-0003-client-isolation-boundaries.md) e a [ADR-0004](decisions/ADR-0004-private-evidence-storage.md) permanecem **PROPOSTAS, NÃO ACEITAS**.

## GAPS — riscos e limites abertos

1. **Multi-cliente:** workspaces da mesma organização têm compartilhamento editorial de `MediaAsset` em nível organizacional; risco de eventos de mesma conta Meta em mais de um workspace. Não declarar isolamento total.
2. **Cliente operador:** `CLIENT` e `EDITOR` são papéis da mesma participação; um funcionário externo com papel editor ainda não é distinguido de membro interno em todas as superfícies. Exige política própria e regressões.
3. **Evidências:** storage privado, autorização de download, trilha de custódia, retenção LGPD e integridade verificável ainda não foram implementados.
4. **Fontes externas:** Obsei, Auto Archiver e descoberta de posts de terceiros ainda não integrados; cobertura Instagram/TikTok/Facebook não é irrestrita.
5. **Operação:** Redis sob múltiplos workers, revogação concorrente, uploads, relatórios, webhooks e verificações no ambiente final ainda requerem testes/homologação.
6. **Produto:** branding e interface integral pt-BR, gestão de ocorrências, relatórios de crise e experiências para clientes operadores são trabalho futuro.

## REUSE GATE → DECISION → NEXT ACTION

- Preservar funcionalidades BrightBean e avisos AGPL-3.0; pesquisar código/testes existentes antes de implementar.
- Aguardar comunicação `green`/`red` da PR #19; **não consultar CI em loop, não mesclar por suposição**.
- Antes de aceitar ADR-0003 ou conceder papel de editor a funcionário de cliente real, produzir matriz de acesso por identidade/ação/dado, testes negativos e resolver riscos compartilhados.
- Esta PR documental somente organiza leitura, doutrina e skills; não aprova ADRs, não inclui módulos de monitoramento, não faz deploy nem integra PR #2 à `main`.

**Histórico anterior:** [snapshot de estado](historico/2026-10-08-estado-canonico-anterior.md). Evidências completas continuam nos commits, PRs e logs da CI.
