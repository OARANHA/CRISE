# Estado canônico verificável — VIGIAFAST

**Data de referência:** 2026-10-08. Este snapshot deve ser reconciliado com Git e CI a cada nova sessão.

## REAL NOW — evidências
- GitHub: `OARANHA/CRISE` existente, público, inicialmente vazio; inicializado com `README.md` no commit `62744c16f5c94d4de0d40ac075423ea1382c2ac1`.
- A PR #1 da documentação canônica foi integrada à `main` no commit `f6883b747ce1a6ae6a6968948da5225332ed4f2f`.
- BrightBean Studio identificado em `brightbeanxyz/brightbean-studio`, licença AGPL-3.0, base `main` observada em `96ccc1e88fefa171c4e5ca981dc9f289bdf60d39`.

## Atualização da branch de importação
- Bootstrap de importação: [workflow de sucesso](https://github.com/OARANHA/CRISE/actions/runs/37728568048). O job confirmou `IMPORT_VALIDATED_FILES=874`, comparando os arquivos versionados do upstream byte a byte.
- A PR #2 encontra-se em rascunho, com o snapshot incluído no commit `b80322fd0d1386b0c13ef7891f98817b6d38d5d3` e sem merge na `main`.
- Snapshot original: `96ccc1e88fefa171c4e5ca981dc9f289bdf60d39`. Arquivos binários incluídos. README/CI originais preservados em docs/upstream.
- Importação em PR, não disponível em produção; validação CI da aplicação é etapa separada.

## O que NÃO está comprovado/implementado
- Os 874 arquivos foram importados com integridade, mas **a execução dos testes funcionais Django/PostgreSQL ainda precisa ser observada**.
- Nenhuma integração Obsei, Bellingcat, OpenMagpie, 4CAT ou conector de rede social foi implantada aqui.
- Nenhum teste da aplicação, teste real de API social, auditoria LGPD completa ou deploy foi executado neste repositório.
- Nenhum cliente, conta social, ocorrência, dado ou credencial real foi cadastrado aqui.

## Gaps
- Validação da importação por PR, teste do código original e estratégia de sincronização upstream (origem/SHA documentados).
- Validação funcional e segurança do código original, incluindo separação multiempresa.
- Mecanismo de descoberta de publicações de terceiros por nomes/variantes.
- Conectores testados com matriz explícita de capacidades e limitações.
- Fluxo de evidências e incidentes e classificação contextual brasileira.

## NEXT ACTION
1. Revisar a PR #3 de validação da base BrightBean e informar o resultado da CI (sem polling).
2. Se a CI estiver verde, revisar resultados de lint, mypy, pytest, migrações, build sem push e gitleaks; avaliar integração à PR #2 ainda em rascunho.
3. Corrigir os bloqueios de segurança de Compose e arquivos de mídia antes de deploy; executar depois testes explícitos de isolamento multi-cliente.
4. Não implantar e não usar dados reais até fechar os gates.

## Como atualizar
Registrar data, branch, SHA/PR, comando de teste e resultado, capacidades comprovadas e pendências. Nunca escrever 'funciona' somente porque o README de um fornecedor afirmou.

## Gates de segurança identificados em revisão estática
- `docker-compose.yml` expõe PostgreSQL na porta 5432 com senha de demonstração; `docker-compose.prod.yml` estende a configuração e define `DATABASE_URL` com senha demonstrativa. NÃO implantar assim.
- O `Caddyfile` serve todo `/media/*` diretamente, enquanto `config/urls.py` protege `comment_attachments/` via lista de caminhos públicos; verificar potencial acesso anônimo à mídia privada antes de deploy.
- Revisar cadeia de proxies e confiança em `HTTP_X_FORWARDED_FOR` no rate limit de login (`apps/accounts/middleware.py`).
- Relatório detalhado: `docs/audits/2026-10-08-brightbean-baseline.md`.

## Continuação comprovada 2026-10-08
- PR #3 integrada em `feat/brightbean-upstream-import`, commit `a9d397bf34c699b50b4237142cc50b905e3b105f`.
- CI [run 37728858063](https://github.com/OARANHA/CRISE/actions/runs/37728858063): cinco jobs aprovados; pytest 2.337 passed, 1 skipped, 808 warnings; Docker build sem publicação.
- PR #4 é proposta de hardening de Compose e Caddy com testes HTTP sintéticos. **Ainda não considerar a correção aprovada até a CI e revisão.**
- Próxima etapa: aguardar comunicação do operador (green/red), sem polling; depois revisar testes de isolamento entre clientes e confiança em `X-Forwarded-For`. Sem deploy.

## Atualização PR #4 e próxima verificação (2026-10-08)
- [PR #4](https://github.com/OARANHA/CRISE/pull/4) integrada na branch `feat/brightbean-upstream-import` com commit `4d5f9d400eab88ae80ca58b3087fc6537249c41b`.
- [Run #37729909304](https://github.com/OARANHA/CRISE/actions/runs/37729909304): cinco jobs verdes, incluindo Compose/Caddy e smoke tests 200 em mídia pública e 404 em mídia privada.
- PR #5, ainda não testada, unifica o cálculo do IP do login e API e adiciona regressões contra XFF falso.
- `main` não contém ainda o BrightBean; a PR #2 segue em rascunho, sem deploy.
- Aguardar green/red da PR #5, sem polling. Após isso, auditar isolamento dos nove clientes.

## PR #5 integrada e gate #6 de isolamento proposto (2026-10-08)
- [PR #5](https://github.com/OARANHA/CRISE/pull/5) integrada à branch de importação, commit `82bc2138999160edfd547cfcb1efbee7c8d187ac`.
- [CI #37730766539](https://github.com/OARANHA/CRISE/actions/runs/37730766539) aprovada: Ruff, Mypy, Pytest/PostgreSQL/migrations, Docker sem push e Gitleaks. Pytest: **2.348 passed, 1 skipped, 808 warnings**. Os 11 novos cenários do resolvedor IP passaram.
- PR #6 traz **testes adicionais de isolamento** entre workspaces/clientes no REST, MCP e HTMX, sem reescrever o código original. **Resultados ainda não validados**.
- Importação principal permanece em PR #2 draft, não incorporada à main. Sem deploy ou dados reais.
- Próxima ação: revisar green/red da PR #6 quando o operador comunicar, sem polling. Depois ampliar testes para mídia, posts, OAuth/MCP, workers, caches e evidências.
