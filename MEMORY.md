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
- Próximo marco: revisar a base e licença do BrightBean; importá-la com histórico verificável em branch separada, executar testes originais e registrar diagnóstico.

## Regras de manutenção
Alterar este arquivo quando uma decisão, marco, resultado ou bloqueio relevante mudar; manter curto, datado e com links de commits/PRs. Registrar fatos comprovados; questões abertas em `docs/CANONICAL_STATE.md`.
