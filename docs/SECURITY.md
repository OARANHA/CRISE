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

## PR #14 — proposta de contrato para storage privado (2026-10-08)
A inspeção estática confirmou que `MediaAsset.file` ocupa `media_library/`, divulgado anonimamente em `Caddyfile` e `config/urls.py::PUBLIC_MEDIA_PREFIXES` para consumo das redes sociais. O controle de acesso em `asset_download` não revoga acesso direto ao endereço público. Mesmo contas privadas por workspace usam esse prefixo de publicação, portanto **não colocar evidências ou relatórios confidenciais ali**.

A ADR-0004 detalha proposta de armazenamento dedicado privado, autorização em cada ação, hashes, proveniência, auditoria e retenção. **Status: PROPOSTA, ainda sem implementação, testes operacionais ou escolha definitiva de tenancy**. Preservar a mídia pública original BrightBean e as regras de publicação. CI documental, se aprovada, não homologa segurança de evidências.

## Portal e acesso operacional de clientes — gate proposto na PR #15

O clone possui `apps/client_portal` com convites, link mágico, aprovações, posts publicados e histórico. O relatório nessa área ainda é um template sem relatório reputacional completo. Usuários externos que trabalharão como editor/contributor exigem **permissões explícitas para cada função** e manutenção das restrições de informação interna.

A emissão de link mágico exige `WorkspaceRole.CLIENT`, mas `portal_auth_required` confirma apenas associação ao workspace após a sessão de portal; além disso, `portal_approval_queue` filtra comentários externos quando o papel atual é literalmente `CLIENT`. O efeito de migrar um usuário externo para EDITOR ou custom role deve ser testado em cenário adversarial antes de habilitá-lo. Não assumir vazamento explorável sem testes; tratar como risco de autorização a avaliar.

Validar casos A/B/C, acesso direto, mudanças/revogação de permissão durante sessão ativa, preservação de comentários internos, relatórios, imagens públicas editoriais versus evidências privadas, e escopo de APIs/MCP. Um mesmo workspace contém pessoas com diferentes responsabilidades, mas **estar associado a ele não autoriza consultar todo dado**. ADR-0003/ADR-0004 pendentes, sem dados reais.

## PR #16 — Controle de visibilidade em comentários e anexos do portal (proposta)

O portal do cliente não deve revelar comentários internos quando uma associação `CLIENT` for promovida a outro papel mantendo uma sessão ativa. A filtragem EXTERNAL deve ser incondicional na superfície do portal e alcançar replies previamente carregadas. A view autenticada de download de anexo deve negar ao papel CLIENT a mídia marcada INTERNAL mesmo que tenha UUID e participação válida no workspace.

Essa defesa **não caracteriza isolamento completo dos usuários externos com papel de editor**, porque o BrightBean não diferencia ainda identidade "funcionário da agência" versus "funcionário do cliente" independentemente do papel. Sujeito a testes e definição da ADR-0003. Nunca armazenar evidências privadas no prefixo de mídia pública.

## PR #17 — tentativa de exclusão de comentário de outro cliente
Identificado por inspeção: `apps/approvals/comments.py::delete_comment` filtrava apenas UUID e estado; calculava a permissão do solicitante no workspace passado, sem validar que o objeto também pertencia a ele. A view ignorava a relação entre `post_id` da URL e o comentário antes da exclusão. A PR #17 propõe checagem dupla em serviço e view com testes adversariais A/B/C. **CI pendente**, sem homologação de toda a área de comentários.
