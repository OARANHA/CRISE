# Arquitetura-alvo — VIGIAFAST

> **Arquitetura-alvo proposta; não é homologação.** O BrightBean foi importado para a branch de revisão e recebeu testes sintéticos por PR, mas o produto completo ainda não está integrado à `main` nem validado para dados reais.

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

## Fronteira pública/privada de arquivos — proposta ADR-0004
A biblioteca BrightBean `MediaAsset` tem missão **editorial**: arquivos destinados à publicação podem ser buscados anonimamente no prefixo `/media/media_library/*`. A tela autenticada de download não torna esses bytes confidenciais. A mídia org-shared também pode ser visível em múltiplos workspaces da mesma organização.

**Proposta, não implementada:** o futuro módulo `Evidências` utiliza entidade e storage próprios, privados por cliente, jamais o prefixo de publicação. O backend autoriza consulta, preview, download e emissão de URL temporária; guarda original, derivados, hash, origem, UTC, histórico de custódia, retenção e trilha de auditoria. Integrações de arquivamento só entram após validação de fonte/termos. Exige ADR-0003 (tenancy) e ADR-0004 aprovadas antes de desenvolver com dados reais.

## Duas experiências para o mesmo produto — proposta (PR #15)

**Painel interno:** a equipe VIGIAFAST administra vários clientes e acessa somente os workspaces autorizados; supervisor pode acompanhar diferentes equipes. **Área do cliente:** usuários externos podem acompanhar aprovações, publicações e atividades já fornecidas pelo BrightBean; numa modalidade de trabalho, colaboram em edição, calendário, inbox e analytics apenas conforme permissões verificadas.

Reaproveitar `apps/client_portal`, `WorkspaceMembership`, `CustomRole`, os módulos existentes de publicação/analytics e `apps/approvals`, evitando reconstrução. O relatório do portal existente é apenas estrutura de página. Monitoramento reputacional, ocorrências e evidências privadas são funções adicionais e ainda não implementadas.

**Atenção de segurança:** link mágico no portal atual requer papel CLIENT para emissão; usuário com papel editor não ganha automaticamente o mesmo acesso ao portal, e mudar o papel pode alterar a visibilidade de comentários internos. Exigir testes antes de unificar os papéis/experiências. O modelo um-org/vários-workspaces é hipótese de implementação, não garantia de isolamento; ver ADR-0003 e ADR-0004.
