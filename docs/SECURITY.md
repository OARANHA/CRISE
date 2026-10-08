# Segurança, LGPD e dados — VIGIAFAST

## Política para repositório público
Permitido: código, documentação, configurações de exemplo sem valores reais, testes sintéticos, matrizes de capacidades, ADRs e diagnósticos anonimizados.
Proibido: credenciais reais, `.env`, chaves, cookies/sessões, dados pessoais dos nove clientes, termos de monitoramento identificáveis, posts/comentários reais, capturas, evidências, planilhas ou relatórios confidenciais.

## Requisitos de implantação futura
- Autenticação robusta, RBAC, logs de auditoria, limitação de taxa e controle de acesso por organização/workspace.
- Verificar isolamento de dados nos modelos, APIs, MCP, tarefas assíncronas, caches, webhooks, uploads, relatórios e índices de busca.
- Criptografar credenciais em repouso; segredos fornecidos por gerenciador seguro, nunca Git.
- Evidências e relatórios privados com hash, horários e rastreabilidade de origem e alterações.
- Avaliar retenção, necessidade, finalidade, direitos dos titulares e base legal conforme LGPD.
- Usar somente coleta compatível com permissões, condições das fontes e enquadramento jurídico aplicável.
- Toda suspeita de ilícito requer revisão humana e, quando necessário, orientação jurídica qualificada.

## Nota sobre a base BrightBean
O README original menciona mídia de publicação servida em caminhos acessíveis publicamente em certas configurações (`SERVE_MEDIA`). Isso **não** é aceitável para evidências ou arquivos de clientes. Antes de uso real, separar storage público destinado a publicações do armazenamento protegido de evidências.

## Licenças
- BrightBean: AGPL-3.0 — preservar avisos e cumprir disponibilização de código correspondente nas condições da licença quando aplicável; uso interno não é isenção automática de obrigações ligadas à interação em rede.
- Obsei: Apache-2.0; Bellingcat Auto Archiver: MIT; 4CAT e Zeeschuimer: MPL-2.0; revisar termos do componente/versão efetivamente importados.
- Identidade visual própria é permitida nos limites aplicáveis; não apagar avisos legais obrigatórios nem assumir que marcas de terceiros são licenciadas.

## Gatilhos de parada
Não fazer deploy nem ingerir dados reais enquanto não houver configuração segura, validação de isolamento, política de retenção e autorização específica.

## Correções propostas na PR #4
- PostgreSQL sem porta publicada e com senha obrigatória via `VIGIAFAST_DB_PASSWORD`; URL de conexão definida em `.env` protegido, usando mesma senha.
- Django acessível apenas na loopback do host para o cenário Compose; proxy Caddy continuacomo entrada na produção.
- Caddy publica só `media_library/`, `avatars/`, `workspaces/icons/`; anexos internos e outras rotas de mídia retornam 404 na borda.
- CI fará validação sintática de Compose/Caddy e teste HTTP sintético de mídia pública/privada. Não considerar aprovado antes do workflow.
- Continuam abertos gates de isolamento entre clientes, cabeçalho IP e storage privado de evidências.

## PR #5 — resolução de IP com proxies confiáveis (proposta sob teste)
- Login e Agent API usam o mesmo `_client_ip`; só se considera `X-Forwarded-For` quando `REMOTE_ADDR` corresponde a um proxy presente em `BB_TRUSTED_PROXIES`.
- A cadeia XFF é analisada da direita para a esquerda, para não confiar em IP arbitrário inserido à esquerda pelo cliente. Hop inválido retorna `REMOTE_ADDR`.
- Configurar somente IPs de proxies reais e estáveis, sem curingas. CIDR não é suportado.
- Em instalações com múltiplas instâncias, usar cache compartilhado para rate limiting; o contador atual não é atômico sob alta concorrência.
- PR #5 precisa passar na CI antes de integração. Validação inter-tenant permanece pendente.

## Estado comprovado após a PR #6 — 2026-10-08
- A CI de [PR #6](https://github.com/OARANHA/CRISE/pull/6) passou: [run #37763047990](https://github.com/OARANHA/CRISE/actions/runs/37763047990), 16/16 novos casos da inbox REST/MCP/HTMX/API-key; o teste de isolamento de todos os módulos **não está concluído**.
- **Risco de isolamento:** `MediaAssetManager.for_workspace_with_shared` torna assets de organização (`workspace_id = NULL`) visíveis a workspaces da mesma organização. O recurso é intencional na base BrightBean; para VIGIAFAST, essa capacidade precisa de política explícita e testes, jamais aplicá-la a dados de crise ou evidências privadas.
- [ADR-0003](decisions/ADR-0003-client-isolation-boundaries.md) é apenas proposta, sem autorização para ativar clientes reais.
- Configurações de Caddy/DB/proxy foram validadas por CI em PRs #4 e #5; isso não substitui revisão de infraestrutura instalada, segredos únicos e cache de rate limit compartilhado.
