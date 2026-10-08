# VIGIAFAST — memória operacional resumida

**Memória de continuidade; NÃO é fonte autônoma de verdade.** Ver sempre [docs/PROJECT_SOURCE.md](docs/PROJECT_SOURCE.md) e [docs/CANONICAL_STATE.md](docs/CANONICAL_STATE.md). O estado do GitHub pode avançar depois deste arquivo.

## Produto
- **CRISEDIGITAL / VIGIAFAST:** plataforma reputacional para nove clientes iniciais, expansível, equipe interna e usuários de clientes (observadores e futuros operadores).
- **Base:** BrightBean Studio integral, Django/Python/PostgreSQL, AGPL-3.0 e notices preservados. Interface pretendida em português brasileiro.
- **Fontes:** contas conectadas são diferentes de descoberta de menções de terceiros. Integrações Obsei/Auto Archiver e coleta pública ainda não operacionais. Não prometer cobertura ilimitada.
- **Segurança:** dados por cliente, LGPD, revisão humana para classificações sensíveis, evidências fora da mídia editorial pública.

## Como continuar
1. Ler fonte e regras: `docs/PROJECT_SOURCE.md` → `AGENTS.md`.
2. Reconciliar `main`, branch de importação, PRs, SHAs e CI **pontualmente**.
3. Consultar [snapshot canônico](docs/CANONICAL_STATE.md), [ADRs](docs/decisions/), documentação temática e código/testes relevantes.
4. Reutilizar BrightBean antes de criar recursos. Trabalhar em branch, PR e testes; atualizar snapshot e memória.
5. Não fazer polling contínuo de CI: operador informa `green`/`red`. Não mesclar `main`, implantar ou usar dados reais sem autorização específica.

## Última situação verificada nesta organização documental (2026-10-08)
- `main`: `f6883b7`; branch de importação: `0bf37c5` após a PR #19, antes da integração desta PR documental.
- PR #2 segue draft para `main`; PR #19 integrada (merge `0bf37c5`) com [CI #37809392150](https://github.com/OARANHA/CRISE/actions/runs/37809392150) verde: **2.439 passed / 1 skipped**, sete testes novos. A PR #20 teve CI anterior verde em `3367e10`, mas exige CI no commit reconciliado.
- PRs #18 e #19 integradas; somente cenários sintéticos cobertos foram comprovados. Nenhuma homologação de isolamento total.
- ADR-0003 e ADR-0004 são **propostas, não aceitas**.

[Histórico detalhado anterior](docs/historico/2026-10-08-memoria-anterior.md). Referências atuais devem ser verificadas em GitHub, não inferidas da memória.
