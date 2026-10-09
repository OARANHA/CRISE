# UX VIGIAFAST — primeiro slice de acesso pt-BR (em revisão)

**Base observada:** `feat/brightbean-upstream-import` @ `648050ab37525cd596e69b61a600ea09a1503886` (PR #31 já integrada à importação). **Issue:** [#34](https://github.com/OARANHA/CRISE/issues/34). **Status:** proposta de código em branch própria; ainda não integrada, não homologada e sem deploy.

## Gate de reuso
Os templates `templates/base.html`, `templates/account/login.html` e `templates/accounts/dashboard.html` do BrightBean já implementam o layout, fluxo de login (django-allauth), formulário com CSRF, workspace e dashboard vazio. Modificá-los pontualmente evita reconstruir autenticação. Os avisos legais e o código AGPL-3.0 são preservados.

## Mudança delimitada
1. Shell: título de fallback VIGIAFAST, fallback da sidebar e bloco `html_lang` por tela, sem declarar o app inteiro traduzido.
2. Login: identidade textual VIGIAFAST, comunicação pt-BR, links e ações preservados, sem alterar URL, sessão, OAuth, campos ou políticas.
3. Página sem workspace: orientação e CTA em pt-BR; manter form POST com CSRF.
4. Dois testes de regressão sintéticos sob `apps/accounts/tests/test_vigiafast_auth_branding.py` cobrindo resposta HTTP, título, idioma localizado, textos, CSRF e POST existentes.

## Limites e lacunas
- Não representa o branding completo nem tradução 100%: sidebar, formulários automáticos do allauth, signup, relatórios e telas herdadas ainda podem exibir inglês/identidade BrightBean.
- Não altera credenciais, convites, filtros, RBAC, M10/M11/M09, modelos ou migrations; não presume a aprovação da ADR-0003.
- Ícones e assets existentes são preservados no repositório; logo textual evita afirmar existência de arte VIGIAFAST oficial.
- **Testes ainda não executados** nesta etapa; verificar no HEAD exato da PR (Pytest/Ruff/Mypy/Docker/Gitleaks) ao relato do operador. CI verde não comprova interface global traduzida.

Próxima etapa UX após a revisão: mapear sidebar, formulário allauth e telas mais usadas antes de traduzir o restante; tratar alterações visuais e termos legais separadamente.
