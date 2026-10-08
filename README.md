# VIGIAFAST — CRISEDIGITAL

Plataforma interna de monitoramento e gestão de crises reputacionais, inicialmente planejada para nove clientes.

**Estado:** base BrightBean importada em branch para revisão e testes, ainda não homologada nem implantada.

## Fonte oficial do projeto

Comece por [docs/PROJECT_SOURCE.md](docs/PROJECT_SOURCE.md). Para trabalho técnico, leia também [AGENTS.md](AGENTS.md), [MEMORY.md](MEMORY.md) e [docs/CANONICAL_STATE.md](docs/CANONICAL_STATE.md).

Este repositório é a fonte persistente da arquitetura, decisões, estado comprovado e próximos passos. Conversas com assistentes **não são fonte de verdade**.

## Direção técnica

- Reutilizar integralmente a base aberta do [BrightBean Studio](https://github.com/brightbeanxyz/brightbean-studio), sujeito à AGPL-3.0 e à validação técnica.
- Estudar Obsei para classificação e alertas; Bellingcat Auto Archiver para preservação.
- Avaliar OpenMagpie, 4CAT e Zeeschuimer como opcionais.
- Distinguir contas autorizadas/conectadas de descoberta de publicações de terceiros.
- Priorizar interface em português brasileiro e controles de segurança, LGPD e isolamento entre clientes.

**Importante:** não publicar neste repositório credenciais, tokens, dados pessoais ou conteúdo de ocorrências de clientes.

O projeto permanece independente de outros sistemas e serviços.

## Código original BrightBean

Origem e SHA fixado em [docs/upstream/BRIGHTBEAN_SOURCE.md](docs/upstream/BRIGHTBEAN_SOURCE.md). O aplicativo está em avaliação, não homologado; não implantar com dados reais antes dos testes.
