# Importação integral BrightBean — plano e limites

**Estado:** fluxo de importação preparado; execução depende da aprovação e do resultado do workflow. Não pressupor sucesso antes de verificar o commit remoto e os arquivos.

## Por que um workflow isolado?
O conector GitHub acessa arquivos de texto, mas não consegue transferir os binários originais. Uma cópia parcial perderia logos, imagens e ícones e não poderia ser declarada íntegra. O workflow executa **somente no GitHub Actions** para baixar um snapshot da fonte pública, copiar arquivos e conferir todos por comparação byte a byte.

## Origem fixada
- Repositório: https://github.com/brightbeanxyz/brightbean-studio
- SHA: `96ccc1e88fefa171c4e5ca981dc9f289bdf60d39`
- Licença: AGPL-3.0 (e avisos legais das dependências).

## Escopo do workflow
- Gatilho: push do script/workflow na branch `feat/brightbean-upstream-import`.
- Permissão: escrita limitada ao conteúdo do repositório para registrar a importação na branch.
- Preserva na raiz a documentação canônica do VIGIAFAST; copia todo o restante do BrightBean.
- Conserva README e CI originais em `docs/upstream/` para evitar sobrepor documentação e executar workflows sem revisão.
- Não faz builds, testes da aplicação, deploy, uso de tokens sociais, nem acessa dados de clientes.
- Ao finalizar, registra resultado real em Git e atualiza documentação para "código copiado, não testado".
- Não faz merge; a PR continua aguardando revisão.

## Próxima fase obrigatória
1. Confirmar o resultado do workflow **uma vez**, sem polling.
2. Verificar quantidade e conteúdo dos arquivos transferidos e revisar `LICENSE`, `docs/upstream`, `Dockerfile`, `docker-compose.yml`, `.env.example` e permissões de APIs.
3. Em PR separada, ativar CI upstream revisada (lint, mypy, pytest, migrações, build sem push) e registrar resultados.
4. Testar isolamento por cliente e autenticação antes de qualquer uso de dados reais.

## Plano alternativo
Se GitHub Actions estiver desativado ou sem permissão de escrita, executar `scripts/bootstrap_brightbean.sh` em ambiente de desenvolvimento **controlado**, na mesma branch, e publicar o commit com revisão humana. Não copiar somente os arquivos de texto.
