# Arquitetura-alvo — VIGIAFAST

> **Alvo proposto; não é um retrato de implementação.** O código-fonte original foi copiado na branch de importação; **ainda não foi testado**.

## Objetivo
Uma plataforma web interna, acessível em português brasileiro, para investigação, monitoramento e gestão de crise reputacional de múltiplos clientes com uma interface única.

## Núcleo
- **Aplicação principal:** BrightBean Studio completo (Python, Django, PostgreSQL, HTMX/Tailwind), com branding e módulos VIGIAFAST adicionais.
- **Multiempresa:** organização/workspace existentes são candidatos a isolamento; validar autorização em *todas* as rotas, tarefas, API e MCP antes de uso real.
- **Trabalhadores:** aproveitar agendamento e workers existentes antes de adicionar filas ou serviços.
- **API/MCP:** preservar as interfaces existentes e expor apenas ferramentas autenticadas com autorização e escopo adequados.
- **Experiência:** dashboard simples, Clientes, Monitoramento, Ocorrências, Evidências, Relatórios e Publicações (recursos BrightBean originais).

## Fluxo proposto
Cadastro de termos por cliente → descoberta em fontes permitidas → coleta normalizada → deduplicação → análise contextual pt-BR → triagem humana → ocorrência → preservação de evidência → alerta/relatório.

## Duas fontes de dados distintas
1. **Contas conectadas/autorizadas:** inbox, publicações, comentários, mensagens e dados permitidos nas APIs oficiais conforme escopos e tipo de conta.
2. **Publicações de terceiros:** conectores específicos de busca pública, indexadores, pesquisas documentadas e importações assistidas. Cobertura parcial por plataforma; nunca presumir acesso universal.

## Serviços opcionais
- Obsei: classificação, temas e alertas; usar API interna ou adaptador, sem precisar expor seu painel.
- Bellingcat Auto Archiver: preservação de URLs, metadados e arquivos; guardar material em armazenamento restrito e verificável.
- OpenMagpie: descoberta e filtros em fontes atualmente suportadas; validar qualidade, dependências e licença por componente.
- 4CAT e Zeeschuimer: investigação assistida por analistas, fora do fluxo obrigatório.

## Dados e segurança
- Identificar tenant/workspace em toda entidade; RBAC no backend, logs de auditoria, criptografia de segredos e limites de retenção.
- Separar evidência original da cópia redigida/normalizada para análise de IA.
- Arquivos com hashes, origem, timestamps, histórico de manuseio e status de captura.
- Dados de clientes e provas jamais no Git; configurar storage privado e acesso controlado no ambiente autorizado.

## Não objetivos do primeiro marco
Não recriar editor de publicações, calendário, autenticação ou inbox que o BrightBean já possua; não cobrir toda a internet; não automatizar juízo jurídico; não operar coletores de fontes restritas sem base legal e viabilidade.
