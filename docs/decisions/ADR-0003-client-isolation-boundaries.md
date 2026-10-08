# ADR-0003 — Limites de isolamento entre clientes

**Data:** 2026-10-08  
**Status:** **Proposta — NÃO ACEITA**. Exige validação de código, testes e decisão explícita antes de usar dados reais.

## Contexto
O VIGIAFAST prevê inicialmente nove clientes e funcionários que administram contas, menções, ocorrências e relatórios sem permitir acesso indevido de um cliente aos dados de outro. O BrightBean já tem `Organization`, `Workspace`, `OrgMembership`, `WorkspaceMembership`, chaves de API associadas a um único workspace e filtros na inbox.

A [PR #6](https://github.com/OARANHA/CRISE/pull/6) comprovou 16 cenários sintéticos em inbox REST/MCP/HTMX e emissão de chave: o cliente A não acessou mensagens dos clientes B (outro workspace na mesma organização) e C (outra organização).

**Mas:** `apps/media_library/managers.py::MediaAssetManager.for_workspace_with_shared` inclui mídias com `workspace_id IS NULL` e `organization_id` correspondente. A API `apps/api/routers/media.py` reutiliza esse filtro. Portanto, *workspaces diferentes de uma mesma organização não garantem isolamento absoluto de toda a mídia*: existe compartilhamento organizacional intencional no produto original. Não se pode assumir que um workspace == um tenant totalmente isolado.

O middleware original `apps/members/middleware.py` também descreve suporte a **uma organização por usuário na v1**. Colocar cada cliente em uma organização separada exigiria validação especial para funcionários que administram mais de um cliente.

## Opções a avaliar
1. **Uma organização da empresa + um workspace por cliente:** facilita operador centralizado, mas exige política explícita sobre ativos organizacionais compartilhados e testes de vazamento.
2. **Uma organização por cliente:** tende a reforçar fronteira dos ativos org-shared, mas exige evolução comprovada de acesso multi-organização para equipe interna; maior impacto sobre o BrightBean.
3. **Operador central + tenants de domínio separados:** possível no futuro, porém só com arquitetura, segurança e migrações aprovadas; não reconstruir RBAC antes de avaliar a base.

## Proposta de trabalho, não decisão de implantação
- Manter, **para fins de teste**, clientes sintéticos A/B na mesma organização e C em outra.
- Testar ativos privados por workspace versus ativos org-shared. Reproduzir o compartilhamento existente, quantificar seu impacto e definir se deve ser negado por padrão na experiência VIGIAFAST.
- Manter **evidências, capturas e dados reputacionais privados** em storage segregado por cliente, nunca na mídia pública de publicação, nem compartilhados por organização por padrão.
- Operadores acessam dados de clientes distintos **somente quando** possuem escopo/permissão explícitos.
- Decisões jurídicas/reputacionais sempre com revisão humana. Não incluir dados reais em testes.
- Estabelecer gate de regressão REST, MCP, HTMX, workers, armazenamento e relatórios antes de aceitar ADR.

## Gate para aceitar
Exigir teste negativo demonstrando que usuário sem permissão de B não acessa listagem, UUID, download, anotação ou relatórios de B, mesmo conhecendo identificadores. Se houver compartilhamento intencional, defini-lo como uma concessão específica, auditável e **nunca aplicável a evidências privadas**.

## Consequências e riscos
- Reutilização da base reduz custo mas exige compatibilização com modelo de compartilhamento atual.
- Até completar os testes e decisão, **proibido tratar a aplicação como homologada para nove clientes reais**.

## Referências
- [Matriz de isolamento](../audits/2026-10-08-client-isolation-matrix.md)
- `apps/media_library/managers.py`
- `apps/api/routers/media.py`
- `apps/members/middleware.py`
- [PR #6](https://github.com/OARANHA/CRISE/pull/6)

## Experimento previsto — PR #8 (sem decisão de produto)
- Testes adversariais de leitura/edição de posts e mídia em REST e MCP, com clientes A/B/C fictícios.
- Teste explícito confirma que o BrightBean **já compartilha** `MediaAsset.workspace_id=NULL` dentro de uma organização; isso **não valida** compartilhar evidências do VIGIAFAST.
- Aguardar CI. Não aceitar ADR nem modificar política de mídia compartilhada automaticamente.

## Nova evidência de risco — webhooks Meta, PR #11 proposta
- Unicidade de `SocialAccount` é `(workspace, platform, account_platform_id)`, permitindo a mesma página de Facebook registrada em mais de um workspace.
- `_process_meta_events` busca todos os registros correspondentes ao identificador nativo e valida o segredo de app da organização. Isso pode produzir **fanout do mesmo evento** para clientes diferentes da mesma organização que tenham conectado a mesma página.
- Os testes propostos apenas documentam esse roteamento e o filtro entre organizações; **não estabelecem nem autorizam a política do VIGIAFAST**. Precisamos decidir se links duplicados à mesma conta são permitidos e, em caso positivo, como evitar exposição indevida de mensagens privadas.
- Aguardar CI da PR #11 e análise de consequências para contas Meta já conectadas antes de qualquer restrição, migração ou bloqueio de duplicidade.

## Controle defensivo proposto — destinatários de alertas em tarefas assíncronas (PR #13)
- As views BrightBean verificam `WorkspaceMembership` quando atribuem uma mensagem; a associação FK pode permanecer depois de revogação ou ser alterada por importação/manutenção.
- A validação **no momento do envio** deve confirmar a associação do destinatário ao `message.workspace_id`. Caso não exista, retornar ao comportamento já existente de notificar os owners/managers atuais desse workspace, **sem** alcançar o usuário desligado.
- Regressões propostas cobrem mesmo workspace, outro workspace da mesma organização e outro de organização distinta, para alertas de nova mensagem e SLA. A **CI da PR #13 ainda está pendente**.
- Isso é endurecimento localizado do limite de autorização, não a aceitação do modelo multi-cliente da ADR-0003.

## Interface com ADR-0004 (proposta de evidências)
A definição de um workspace por cliente permanece **pendente**. Qualquer módulo de evidências deverá ter vínculo por cliente, não compartilhar por organização e usar storage dedicado **fora** de `media_library/`. A ADR-0004 detalha o contrato proposto; sua existência não aceita esta ADR nem autoriza ingestão real.

## Escopo confirmado pelo produto — portal do cliente e operação pelo próprio cliente (PR #15 proposta)

**Necessidade de produto confirmada:** o VIGIAFAST precisa preservar **todas as funcionalidades do clone BrightBean** e atender, em uma interface integrada, (a) funcionários internos que operam vários clientes; (b) clientes que consultam conteúdo, acompanham monitoramento e aprovam materiais; e (c) funcionários autorizados do próprio cliente que **trabalham** em edição, calendário, inbox e recursos habilitados. Nove clientes são apenas o início; cadastros de novos clientes e usuários não devem ter limite fixo na aplicação.

**Direção a avaliar — NÃO ACEITA:** usar provisoriamente uma organização operacional VIGIAFAST com workspace específico por cliente, compartilhando as implementações originais do BrightBean. Essa organização única **não é uma fronteira de isolamento comprovada**; mídias organizacionais compartilhadas e contas Meta nativas duplicadas continuam riscos abertos. Avaliar novamente alternativa de organizações separadas antes da aceitação.

### Reutilização comprovada por inspeção do código (não equivale a homologação)

- `apps/client_portal/urls.py` e `apps/client_portal/views.py`: dashboard, fila de aprovação, ações de aprovar/solicitar ajustes/rejeitar/suspender, postagens publicadas, histórico e rota de relatórios. `portal_reports` **apenas renderiza template**: não há relatório reputacional completo nessa view.
- `apps/client_portal/views_admin.py`: convite de clientes, geração/envio de link e remoção de participação. `apps/client_portal/services.py::generate_magic_link` exige papel `CLIENT` no workspace para emitir o link.
- `apps/members/models.py`: `OrgMembership`, `WorkspaceMembership` e `CustomRole.permissions` já dão base a permissões por workspace. Papéis incluem owner, manager, editor, contributor, client e viewer; **papel "cliente" não implica autorização para editor ou todas as funções**.
- `apps/client_portal/decorators.py::portal_auth_required` exige autenticação, sessão de portal e **alguma** `WorkspaceMembership`, mas não verifica diretamente `workspace_role=CLIENT`. A rota de aprovação consulta workspace; controles detalhados por ação/permissão, papel e visibilidade devem ser testados, não presumidos.
- `apps/client_portal/views.py::portal_approval_queue` aplica filtro `visibility=EXTERNAL` aos comentários quando `workspace_role=CLIENT`; o comportamento após transformar cliente em editor ou papel customizado precisa de revisão para impedir exposição de comentários internos.
- `apps/members/middleware.py::RBACMiddleware` resolve `OrgMembership` com `.first()` e documenta **uma organização por usuário na v1**; não pressupor operação multi-organização já suportada.

### Experiências desejadas (sem implementações novas nesta PR)

| Público | Experiência | Acesso de referência | Restrição obrigatória |
| --- | --- | --- | --- |
| Administrador interno VIGIAFAST | Gestão de clientes, funcionários, permissões e configurações | Org owner/admin conforme autorização | Registrar ações e restringir dados privados por cliente; papel global não libera evidências automaticamente |
| Analista/gestor interno | Trabalhar nos workspaces explicitamente atribuídos | `WorkspaceMembership` | Sem acesso implícito a outros clientes, mesmo na mesma organização |
| Cliente observador | Painel do próprio cliente, aprovações, publicações, atividade e futuros relatórios autorizados | Portal BrightBean com papel `CLIENT` e sessão válida | Não exibir notas internas, evidências não liberadas ou dados de terceiros |
| Cliente operador | Trabalhar nas ferramentas BrightBean expressamente habilitadas no seu workspace | Papéis editor/contributor ou `CustomRole` **após validação de fluxo** | Permissões por ação e por dado; não assumir que link mágico de `CLIENT` fornece acesso de editor |
| Consultor externo | Acesso temporário a ações específicas | Associação e permissões explícitas | Revogação e validade verificadas, sem privilégios organizacionais gerais |

**Separar identidade do ator (funcionário interno versus usuário de cliente) de sua função em um workspace.** Um cliente pode precisar editar conteúdo e também ver o portal, mas o modelo atual tem um `workspace_role` por par usuário/workspace. Antes de atribuir editor a usuários de cliente, decidir como manter restrições de informação interna, aprovações, autenticação e visualização do portal sem confiar somente na aparência da interface. Não conceder permissões ao trocar de tela; validar sempre no backend.

### Gate obrigatório antes de aceitar ADR-0003 e liberar o portal para clientes reais

1. Criar matriz formal de **quem pode ver/fazer o quê** nos módulos herdados: publicações, calendário, inbox, analytics, aprovações, relatórios, mídias, gestão de contas sociais, configurações, API, MCP, downloads e futuros casos/evidências.
2. Simular usuários internos e clientes observador/operador A/B (mesma organização) e C (outra organização). Testar navegação direta por UUID, troca de workspace, sessão de portal, papéis editor/client/custom, identidade de cliente e fontes de dados compartilhadas.
3. Garantir que comentários/notas internas, mensagem privada, relatórios, arquivos e evidências não sejam mostrados a clientes só porque têm permissão de editar publicações. Não reutilizar `MediaAsset` público para evidências (ver ADR-0004).
4. Testar convite, login, link mágico expirado/usado, revogação de associação, downgrade de papel, offboarding, sessão já iniciada e API-key/OAuth associados ao workspace. Certificar que a área de trabalho do cliente não se torne uma forma de acessar outros clientes.
5. Preservar integralmente as funcionalidades editoriais originais e os avisos/licença BrightBean; interface em pt-BR de acordo com papéis e sem publicar dados reais de clientes.
6. Não declarar o portal de relatórios de crise como implementado; planejar a camada própria de monitoramento de terceiros e relatórios com dados permitidos, respeitando limitações de Instagram, TikTok e Facebook.

**Estado:** apenas definição de requisitos e investigação de reuso. ADR-0003 e ADR-0004 permanecem **PROPOSTAS/NÃO ACEITAS**. Não houve alteração de autenticação, portal, dados, infraestrutura ou deploy.

## PR #16 — Proteção pontual do portal, proposta com CI pendente

Revisão estática encontrou diferença entre sessão de portal e papel atual: no portal de aprovações, o filtro EXTERNAL dependia literalmente de `WorkspaceRole.CLIENT`. Ao tornar-se EDITOR, um usuário poderia manter a sessão anterior, que passaria a consultar comentários internos. O prefetch de replies não filtrava visibilidade. A rota de anexos `approvals.views.comment_attachment` não negava ao cliente básico um anexo interno por UUID conhecido, embora exija login e participação no workspace.

O patch proposto filtra sempre comentários/replies externos na experiência de portal, e nega anexos internos ao papel CLIENT mesmo por URL direta, preservando as funções de edição internas. **Não cria identidade permanente de "usuário externo" separada do papel**: usuários do cliente com EDITOR/CONTRIBUTOR continuam precisando de autorização formal, testes abrangentes e políticas de dados internos em todas as rotas. ADR-0003 permanece NÃO ACEITA; não há implantação.

## PR #17 — isolamento da exclusão de comentários (proposta)
`PostComment` guarda o vínculo ao workspace por `post__workspace`. O serviço de exclusão original usava somente `id=comment_id` e verificava autorização do usuário em um `workspace` informado externamente; isso não garante que o objeto pertence ao mesmo workspace. A view também recebia `post_id` sem validar associação do comentário à postagem da URL.
A PR #17 propõe exigir `post__workspace` no serviço e `post=post` na view antes de excluir. Regressões com clientes sintéticos A/B na mesma organização e C em outra, mais casos permitidos para autor/gestor. **CI ainda não verificada**, não considerar implementado em staging. Não decide o modelo completo de tenants.
