# Estado canônico verificável — VIGIAFAST

**Data de referência:** 2026-10-08. Este snapshot deve ser reconciliado com Git e CI a cada nova sessão.

## REAL NOW — evidências
- GitHub: `OARANHA/CRISE` existente, público, inicialmente vazio; inicializado com `README.md` no commit `62744c16f5c94d4de0d40ac075423ea1382c2ac1`.
- Esta proposta documental está na branch `docs/canonical-foundation`; sua aprovação/merge ainda precisam ser observados no Git.
- BrightBean Studio identificado em `brightbeanxyz/brightbean-studio`, licença AGPL-3.0, base `main` observada em `96ccc1e88fefa171c4e5ca981dc9f289bdf60d39`.

## Atualização da branch de importação
- Snapshot original: `96ccc1e88fefa171c4e5ca981dc9f289bdf60d39`. Arquivos binários incluídos. README/CI originais preservados em docs/upstream.
- Importação em PR, não disponível em produção; validação CI da aplicação é etapa separada.

## O que NÃO está comprovado/implementado
- Snapshot integral do código do BrightBean importado na branch feat/brightbean-upstream-import e comparado byte a byte com o SHA fixado; **nenhum teste funcional executado ainda**.
- Nenhuma integração Obsei, Bellingcat, OpenMagpie, 4CAT ou conector de rede social foi implantada aqui.
- Nenhum teste da aplicação, teste real de API social, auditoria LGPD completa ou deploy foi executado neste repositório.
- Nenhum cliente, conta social, ocorrência, dado ou credencial real foi cadastrado aqui.

## Gaps
- Validação da importação por PR, teste do código original e estratégia de sincronização upstream (origem/SHA documentados).
- Validação funcional e segurança do código original, incluindo separação multiempresa.
- Mecanismo de descoberta de publicações de terceiros por nomes/variantes.
- Conectores testados com matriz explícita de capacidades e limitações.
- Fluxo de evidências e incidentes e classificação contextual brasileira.

## NEXT ACTION
1. Observar resultado/merge da PR documental.
2. Revisar a PR de importação de snapshot; ativar a CI upstream somente após revisão e executar testes originais.
3. Registrar achados, não iniciar deploy nem dados de clientes.

## Como atualizar
Registrar data, branch, SHA/PR, comando de teste e resultado, capacidades comprovadas e pendências. Nunca escrever 'funciona' somente porque o README de um fornecedor afirmou.
