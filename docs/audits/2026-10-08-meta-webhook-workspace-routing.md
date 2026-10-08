# VIGIAFAST — Roteamento de webhooks Meta por identidade de conta

**Data:** 2026-10-08  
**Status:** inspeção estática do código BrightBean e testes propostos na PR #11. **CI da PR #11 pendente.**

## Código observado
- `apps/social_accounts/models.py`: chave única `(workspace, platform, account_platform_id)`, permitindo o mesmo ID externo em workspaces diferentes.
- `apps/inbox/webhooks.py::_meta_receive`: exige assinatura HMAC de um segredo de app configurado.
- `apps/inbox/webhooks.py::_process_meta_events`: seleciona TODAS as `SocialAccount` conectadas cujo `account_platform_id` corresponde à entrada; valida que o segredo da organização é um dos segredos assinantes.
- `apps/inbox/webhooks.py::_create_if_new`: cria `InboxMessage` associado à conta e workspace da conta. Unicidade da mensagem é por `(social_account, platform_message_id)`.

## Hipóteses a verificar com dados sintéticos
1. Duas páginas Meta **distintas** na mesma organização: evento de A somente em A.
2. A **mesma página** Meta vinculada a dois workspaces da mesma organização: evento é entregue a **ambos** os workspaces. Comportamento upstream documentado, **não** uma política de privacidade aprovada.
3. A mesma ID de página em organizações com **segredos diferentes**: evento assinado apenas por A não pode registrar mensagem em B.

## Impacto sobre o produto
O modelo de nove clientes do VIGIAFAST não pode presumir que um workspace por cliente impede replicação de DMs e comentários quando uma conta social nativa é vinculada a múltiplos workspaces.

Antes de conectar contas reais, decidir: proibir duplicidade de identidade social por cliente, exigir vínculo de propriedade único, ou implementar compartilhamento explícito autorizado e auditável. Nenhuma das opções está aceita.

**Limites:** sem chamadas externas à Meta, sem credenciais reais, sem migração, sem alteração de roteamento ou deploy. Os testes da PR #11 ainda precisam passar em CI e não abrangem todas as modalidades de comentários, tasks e Instagram.
