# MEMORY.md — memória técnica persistente

> Este arquivo contém **somente contexto técnico publicável** e deve ser atualizado em PRs. Não armazene nomes, dados, publicações, incidentes, evidências ou credenciais de clientes.

## Identidade e propósito
- Projeto: **CRISEDIGITAL**; produto: **VIGIAFAST**.
- Repositório canônico: https://github.com/OARANHA/CRISE (público nesta fase).
- Operação pretendida: uso interno por equipe não técnica, inicialmente para **9 clientes**, com isolamento por cliente.
- Redes prioritárias: Instagram, TikTok e Facebook; ampliar com fontes públicas viáveis.
- Interface 100% em português brasileiro; uma aplicação única para o usuário.

## Decisões vigentes
- Base pretendida: importar e evoluir **integralmente** BrightBean Studio (Django/Python/PostgreSQL); preservar os recursos existentes e a AGPL-3.0. Veja ADR-0001.
- Documentação canônica reside no Git; chat não é memória de projeto. Veja ADR-0002.
- Candidatos para complementar: Obsei (inteligência), Bellingcat Auto Archiver (preservação); avaliar OpenMagpie e 4CAT/Zeeschuimer de forma opcional.
- Não implantar serviços nem importar coletores desconhecidos antes de revisar código, licenças, segurança e adequação real.

## Lacunas conhecidas
- BrightBean atende principalmente contas sociais autorizadas; não existe evidência de descoberta universal de publicações de terceiros.
- Não prometer comentários de terceiros em toda a rede, em especial Instagram/TikTok/Facebook.
- Análise atual do BrightBean é baseada em palavras-chave em inglês; demanda análise contextual em pt-BR.
- Evidências exigem origem, horário, integridade verificável e armazenamento restrito; arquivamento simples não é certificação jurídica.

## Registro de continuidade
- **2026-10-08** — Repositório OARANHA/CRISE verificado inicialmente público e vazio; iniciada fundação documental. Ainda sem importação de software, testes executados ou deploy do VIGIAFAST.
- Próximo marco: executar e revisar a CI de base do BrightBean em branch independente, corrigir bloqueios críticos de segurança e validar isolamento dos nove clientes antes de quaisquer dados reais.

## Regras de manutenção
Alterar este arquivo quando uma decisão, marco, resultado ou bloqueio relevante mudar; manter curto, datado e com links de commits/PRs. Registrar fatos comprovados; questões abertas em `docs/CANONICAL_STATE.md`.

## Atualização após importação (branch em revisão)
- Snapshot integral do BrightBean copiado na branch de importação, com SHA `96ccc1e88fefa171c4e5ca981dc9f289bdf60d39` e verificação byte a byte de todos os arquivos versionados. Sem execução de testes da aplicação, sem deploy e sem aprovação de merge.

## Validação de importação e revisão estática (2026-10-08)
- Importação integral confirmada em [Actions #37728568048](https://github.com/OARANHA/CRISE/actions/runs/37728568048): 874 arquivos versionados idênticos ao upstream (`96ccc1e88fefa171c4e5ca981dc9f289bdf60d39`); snapshot no commit `b80322fd0d1386b0c13ef7891f98817b6d38d5d3` da PR #2.
- A importação por snapshot não incorporou o histórico Git completo do upstream; a origem e SHA estão documentados.
- Validação Django, CI e build sem resultados ainda; PR separada para habilitar checks originais.
- Revisão estática detectou Compose com porta/senha PostgreSQL demonstrativas e Caddy com possível exposição de mídia privada; bloqueiam qualquer deploy até correção.

## Baseline validada (2026-10-08)
- PR #3 merged em branch de importação, commit `a9d397bf34c699b50b4237142cc50b905e3b105f`.
- [CI baseline](https://github.com/OARANHA/CRISE/actions/runs/37728858063): 2.337 testes aprovados, 1 ignorado; lint, mypy, PostgreSQL, build sem publicação e Gitleaks verdes.
- PR #4 em preparação: Caddy allowlist da mídia pública, Compose com segredo explícito e testes sintéticos. Sem CI confirmada, sem deploy.

## Segurança validada / próximo slice (2026-10-08)
- PR #4 merge na branch de importação: `4d5f9d400eab88ae80ca58b3087fc6537249c41b`. CI #37729909304 verde (5 jobs, smoke tests Caddy).
- PR #5 em desenvolvimento: reaproveitar resolvedor `_client_ip` da Agent API no login; validar cadeia `X-Forwarded-For` direita→esquerda. Testes pendentes da CI.
- Ainda sem deploy, sem dados de clientes e sem avaliação abrangente de isolamento entre tenants.
