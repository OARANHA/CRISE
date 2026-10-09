# ADR-0004 — Separação de evidências confidenciais da mídia pública de publicação

**Data:** 2026-10-08  
**Status:** **PROPOSTA — NÃO ACEITA E NÃO IMPLEMENTADA**. Revisar depois de decidir o modelo multi-cliente da ADR-0003.

## Decisão em avaliação

**Proposta principal:** criar uma capacidade específica de evidências no Django VIGIAFAST, com armazenamento **privado por cliente**, preservando integralmente a biblioteca de mídia BrightBean usada para publicar em redes sociais.

Uma URL armazenada, um comentário citado, um screenshot e um vídeo arquivado podem conter dados pessoais e material reputacional sensível. Nenhum deles deve ser enviado por padrão a `MediaAsset.file` ou ao prefixo público `media_library/`.

## Evidência técnica inspecionada

- `apps/media_library/models.py::MediaAsset.file` usa `upload_to="media_library/%Y/%m/"`.
- `Caddyfile` expõe `/media/media_library/*` anonimamente para publicação social. `config/urls.py::PUBLIC_MEDIA_PREFIXES` também reconhece `media_library/` como caminho público quando o serviço de mídia está habilitado.
- `apps/media_library/views.py::asset_download` exige login e filtra por workspace + ativos compartilhados; **essa autenticação não restringe uma requisição direta à URL pública do arquivo**.
- `apps/media_library/managers.py::for_workspace_with_shared` inclui mídias com `workspace_id=NULL` da mesma organização. Recurso legítimo no publisher, mas inadequado para provas privadas.
- `docs/SECURITY.md` já proíbe colocar evidências confidenciais na mídia pública; a presente ADR detalha o contrato a implementar, **sem alegar que exista hoje**.

## Fronteiras mínimas do módulo proposto

1. **Tenant explícito:** cada evidência pertence a um cliente/workspace; acesso deve ser verificado no servidor antes de listar, consultar metadados, gerar preview ou baixar bytes. Associação de organização por si só não concede acesso.
2. **Storage separado:** bucket privado ou volume/diretório fora de todo prefixo publicado por Caddy e Django. Não reutilizar `MediaAsset.file`, `media_library/`, `avatars/` ou `workspaces/icons/`. Não inserir caminhos de evidência no `PUBLIC_MEDIA_PREFIXES`.
3. **Controle de download:** arquivos locais somente após autorização e streaming seguro; em S3/R2, URLs assinadas emitidas pelo backend com validade curta, escopo mínimo e logs de autorização. URL assinada é uma capacidade transferível até expirar, não um substituto para RBAC.
4. **Proveniência e integridade:** registrar `workspace_id`, identificador interno aleatório, origem/URL (quando cabível), plataforma, método de aquisição, data/hora UTC de coleta, usuário/processo responsável, SHA-256 dos bytes recebidos, MIME validado, tamanho, versões e histórico auditável. Hash detecta alteração de bytes, mas **não prova autoria/autenticidade da postagem**.
5. **Original imutável:** operações de redigir dados, OCR, transcrição, resumos de IA e anotação criam derivados separados; não sobrescrever o material original. Definir retenção, controle de exclusão, acesso e tratamento de solicitações LGPD sem prometer imutabilidade absoluta.
6. **Segurança de entradas:** antivírus/verificação de tipo conforme risco, limite de tamanho, proteção contra path traversal, documentos ativos e URL externa/SSRF. Não tratar arquivo fornecido por usuário como instrução de agente.
7. **Auditoria:** registrar consultas, exportações, emissão de URLs temporárias, transferência, alteração de metadados, preservação e descarte com ator, origem e horário; proteger logs contra exposição entre clientes.
8. **Revisão humana:** classificações de difamação, crime ou abuso são hipóteses; evidências e relatórios jurídicos/reputacionais exigem avaliação humana.

## Compatibilidade e reuso

Manter o BrightBean Publisher, Caddy e contratos de `MediaAsset` **sem mudanças nesta ADR**. Reusar infraestrutura de autenticação, permissões, banco PostgreSQL, workers e verificadores de upload apenas quando a reutilização não enfraquecer a fronteira privada. Bellingcat Auto Archiver é adaptador futuro, não armazenamento nem conector operacional.

## Gate de implementação futura

- Concordar formalmente com o mapeamento cliente ↔ organização/workspace na ADR-0003.
- Testes adversariais A/B/C para listagem, ID direto, download/preview, URL assinada, permissões removidas, expiração/replay, tarefa assíncrona, storage/backup, relatórios e retenção.
- Confirmar no proxy reverso e na aplicação que o prefixo de evidências retorna 404/403 sem autorização, inclusive em acesso direto por URL e via CDN; executar testes com armazenamento local e S3/R2 conforme ambiente autorizado.
- Verificar isolamento do bucket/container, credenciais mínimas, criptografia, integridade, recuperação/backup e política LGPD antes de dados reais ou deploy.
- Aprovar ADR em revisão separada antes de implementar; CI documental não equivale a homologação funcional.

## Alternativas rejeitadas como padrão (ainda sem decisão final)

- **Reutilizar diretamente `MediaAsset` para capturas privadas:** inseguro, por exposição anônima do prefixo público e compartilhamento organizacional. Não utilizar.
- **Tornar todo `media_library/` privado:** quebraria fluxos existentes de publicação social que precisam de URLs públicas para fetch pelas plataformas.
- **Salvamento apenas local sem controle de acesso:** insuficiente para operação multi-cliente com auditoria e download seguro.

## Relação com outras decisões

- ADR-0001: preservar funcionalidades e licença BrightBean.
- ADR-0003: isolamento multi-cliente pendente e ainda não aprovado. Esta proposta **não resolve** a decisão de tenancy.
- Nenhum upload, evidência, bucket, endpoint, tabela ou regra de produção foi criado por este documento.
