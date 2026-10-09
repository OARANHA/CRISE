# VIGIAFAST — Reuso do portal BrightBean para clientes observadores e operadores

**Data:** 2026-10-08  
**Status:** inspeção estática da branch de importação, sem testes executados neste slice e sem aprovação do modelo multi-cliente. Complementa a ADR-0003.

## Capacidades identificadas no clone

| Origem | Comportamento observado no código | Limitação |
| --- | --- | --- |
| `apps/client_portal/urls.py` e `views.py` | Dashboard, aprovação/ajustes/rejeição/suspensão, publicados e histórico | Monitoramento reputacional e relatórios de crise ainda não implementados |
| `apps/client_portal/views.py::portal_reports` | Renderiza `client_portal/reports.html` | **Placeholder**, não é relatório real de crise |
| `apps/client_portal/views_admin.py` | Convites de clientes, envio de link e remoção de acesso | A gestão usa papel `CLIENT`; operação cliente-editor requer desenho adicional |
| `apps/client_portal/services.py::generate_magic_link` | Exige `workspace_role=CLIENT` para emitir link | Editor/custom role não pode ser presumido elegível ao mesmo link |
| `apps/client_portal/decorators.py::portal_auth_required` | Verifica autenticação, sessão de portal, `portal_workspace_id` e associação ao workspace | Não exige explicitamente papel `CLIENT`; autorizações por ação dependem de outros controles |
| `apps/client_portal/views.py::portal_approval_queue` | Restringe comentários a `visibility=EXTERNAL` quando `workspace_role=CLIENT` | Mudar o cliente para EDITOR/custom exige teste de visibilidade de notas internas |
| `apps/members/models.py` | OrgMembership, WorkspaceMembership e CustomRole | Um papel base por usuário/workspace; modelagem de "cliente-operador" precisa compatibilizar acesso ao portal e editor |
| `apps/members/middleware.py` | Resolve primeira associação organizacional do usuário | v1 assume uma organização por usuário |
| BrightBean editor, calendário, inbox, analytics | Recursos existentes para usuários autorizados | Não atribuir automaticamente todos ao papel CLIENT; validar permissão e API por módulo |

## Hipóteses de produto, não decisões aprovadas

- **Pessoas internas:** trabalham em múltiplos clientes apenas conforme permissões explícitas.
- **Cliente observador:** acompanha aprovações/publicações/atividade; futuros relatórios de crise e alertas somente quando implementados.
- **Cliente operador:** pode produzir conteúdo e trabalhar em recursos BrightBean autorizados no próprio workspace. Deve manter barreiras contra dados internos da agência e outros clientes mesmo com papel editor.
- **Capacidade de crescimento:** nove clientes inicialmente, novos clientes e pessoas adicionados por cadastro, sem limite fixo no código. Escalabilidade real depende de carga, quotas de fontes, custos e infraestrutura.
- **Opção operacional provisória:** uma organização para a operação e workspaces por cliente, condicionada a controles para mídia compartilhada, IDs sociais duplicados e relatórios/evidências privadas.

## Testes que faltam antes de uso real

1. Criar usuários sintéticos A/B/C observadores e operadores, internos e desligados.
2. Cobrir portal com sessão válida, link consumido/expirado, downgrade/remoção de papel, troca de workspace e acesso por UUID direto.
3. Validar que edição de publicação não expõe comentário interno, DM, evidência privada, relatórios de outro cliente ou settings organizacionais; testar HTMX/REST/MCP.
4. Validar permissões de postagem, inbox, analytics, aprovação e relatórios conforme role (CLIENT/EDITOR/CONTRIBUTOR/custom).
5. Homologar modelo tenancy da ADR-0003 e storage privado da ADR-0004 antes de clientes reais, uploads de evidências e deploy.

**Sem novos endpoints, componentes de UI, alterações de RBAC, publicação em redes sociais, dados reais ou deploy nesta inspeção.**
