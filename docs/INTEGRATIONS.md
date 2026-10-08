# Matriz de integrações e capacidades — VIGIAFAST

**Estados válidos:** referência avaliada; planejado; em desenvolvimento; testado; operacional; suspenso. Apenas o snapshot BrightBean foi copiado em branch para revisão. Nenhuma integração complementar foi ligada ou testada.

| Componente | Papel | Estado | Restrições e próximos testes |
| --- | --- | --- | --- |
| [BrightBean Studio](https://github.com/brightbeanxyz/brightbean-studio) | Base integral multiempresa, inbox, publicação, API/MCP | Código em revisão | Executar testes; AGPL-3.0; conexão social exige OAuth/autorização |
| [Obsei](https://github.com/obsei/obsei) | Classificação e alertas; modelos locais/externos | Referência avaliada | 1.0 em release candidate; validar contrato API e pt-BR; Apache-2.0 |
| [Bellingcat Auto Archiver](https://github.com/bellingcat/auto-archiver) | Arquivamento de URLs de evidências | Referência avaliada | Testar por plataforma, proveniência, armazenamento e taxa de falhas; MIT |
| [OpenMagpie](https://github.com/obris-dev/openmagpie) | Descoberta e alerta semântico em feeds sociais | Referência avaliada | Instagram/Facebook/TikTok não cobertos agora; examinar `ee/` e licença aplicável |
| [4CAT](https://github.com/digitalmethodsinitiative/4cat) | Análise de datasets sociais | Opcional | MPL-2.0 em LICENSE; uso assistido e suporte variável de coleta |
| [Zeeschuimer](https://github.com/digitalmethodsinitiative/zeeschuimer) | Captura assistida do que o navegador vê | Opcional | Requer operação consciente de extensão; não é descoberta universal |
| [ScrapeCreators Skills](https://github.com/ScrapeCreators/social-media-research-skills) | Referência de fluxos de pesquisa e contratos de API | Referência avaliada | Skills abertas ≠ motor proprietário; serviço API opcional pago |

## Matriz social inicial: não inventar capacidade
| Plataforma | BrightBean em contas conectadas | Descoberta de terceiros | Comentários de terceiros |
| --- | --- | --- | --- |
| Instagram | API oficial: inbox, comentários e menções conforme autorização | Ainda sem conector testado | Ainda sem garantia/cobertura comprovada |
| Facebook | API oficial: páginas conectadas, comentários, menções e mensagens conforme permissões | Ainda sem conector testado | Ainda sem garantia/cobertura comprovada |
| TikTok | Publicação/analytics na matriz original; **não** leitura de comentários no inbox | Ainda sem conector testado | Ainda sem garantia/cobertura comprovada |
| Web/RSS/YouTube/Reddit/Bluesky | Avaliar APIs e feeds caso a caso | Possíveis fontes complementares | Variável por fonte/permissões |

## Protocolo de validação
Para cada conector documentar: tipo de fonte, autorização, termos permitidos, período, paginação, comentários/respostas, custos, limites, cobertura verificada, erros observados, data do teste, amostras sintéticas e fallback. Nunca inserir URLs ou nomes dos clientes em repositório público.
