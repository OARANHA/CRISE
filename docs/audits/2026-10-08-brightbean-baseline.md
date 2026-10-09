# Revisão estática inicial — BrightBean importado
**Data:** 2026-10-08
**Escopo:** apenas leitura de arquivos do snapshot BrightBean importado na PR #2. Não constitui pentest nem homologação.

## Procedência confirmada
- Upstream `brightbeanxyz/brightbean-studio` SHA `96ccc1e88fefa171c4e5ca981dc9f289bdf60d39`.
- GitHub Actions run `37728568048`: sucesso, `IMPORT_VALIDATED_FILES=874` com comparação byte a byte.
- Snapshot preserva arquivos binários, `LICENSE` AGPL-3.0, tests, configurações e código; README original em `docs/upstream/BRIGHTBEAN_README.md` e CI original em `docs/upstream/brightbean-ci.original.yml`.
- Ainda falta validar os testes originais e a integração à `main`; `green` do bootstrap **não significa testes funcionais aprovados**.

## Gates que impedem deploy
1. **Alto — exposição do PostgreSQL e credenciais demonstrativas:** `docker-compose.yml` publica a porta `5432:5432` e usa `POSTGRES_PASSWORD=postgres`; `docker-compose.prod.yml` herda serviços básicos e fixa `DATABASE_URL=postgres://postgres:postgres@postgres:5432/brightbean` no serviço de migração. Configurações demonstrativas não podem ser usadas com dados de clientes. Correção em PR de segurança separada, preservando cenários de desenvolvimento/teste.
2. **Alto — potencial exposição de anexos privados pela mídia:** `Caddyfile` usa `handle_path /media/*` + `file_server` diretamente para todo o volume `media_data`; `config/urls.py` publica apenas `media_library/`, `avatars/`, `workspaces/icons/` e exclui intencionalmente `comment_attachments/` por serem privados. Na configuração atual do proxy é possível haver diferença entre as garantias do Django e do Caddy. Exigir teste de acesso anônimo para `/media/comment_attachments/...` e restringir o proxy/armazenamento antes de exposição pública. Não afirmar exploração confirmada sem teste.
3. **Médio — origem de IP em rate limit:** `apps/accounts/middleware.py` usa diretamente o primeiro `HTTP_X_FORWARDED_FOR` quando presente. Validar cadeia de proxies confiáveis e impedir spoofing no ingresso. Testar comportamento sob proxy e acesso direto.
4. **GATE — isolamento entre os nove clientes:** os objetos e managers de workspace existem, mas não há validação exaustiva das rotas, API REST, MCP, workers, arquivos e relatórios neste ambiente. Exigir testes positivos e negativos inter-tenant.
5. **GATE — mídia/evidências:** não armazenar evidências em caminhos públicos de publicação. Armazenamento privado dedicado, hashes e trilhas de auditoria são requisitos ainda não implementados.
6. **GATE — linguagem e reputação:** `apps/inbox/sentiment.py` usa heurística por palavras em inglês. Não reutilizar classificação para decisões sensíveis sem análise contextual pt-BR e revisão humana.

## Plano de validação de código
A PR #3 adiciona `.github/workflows/ci.yml`, derivado de `docs/upstream/brightbean-ci.original.yml`: lint `ruff`, tipagem `mypy`, `makemigrations --check --dry-run`, `pytest --cov=apps`, build de imagem Docker **sem push**, e `gitleaks`. Todos usam permissões padrão `contents: read`; o banco de testes usa credenciais sintéticas em serviço efêmero.

## Não executado
Nenhum teste da aplicação, teste de autorização, análise dinâmica da Caddy, deploy, coleta Instagram/TikTok/Facebook ou auditoria LGPD completa foi comprovado até a criação desta PR.

## Próxima decisão
Após o operador informar o status da CI, revisar os logs uma única vez, registrar testes com resultados reais e então escolher se integraremos a PR #3 à branch de importação. Não unir a PR #2 à `main` enquanto os gates de segurança e testes críticos estiverem abertos.
