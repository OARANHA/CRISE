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
