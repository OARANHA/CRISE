#!/usr/bin/env bash
# Importa uma cópia verificável do código ABERTO BrightBean, sem executar código upstream.
# Destino: branch de revisão. NUNCA execute em servidores de produção.
set -Eeuo pipefail

readonly UPSTREAM_REPO="https://github.com/brightbeanxyz/brightbean-studio.git"
readonly UPSTREAM_SHA="96ccc1e88fefa171c4e5ca981dc9f289bdf60d39"
readonly ROOT="$(git rev-parse --show-toplevel)"
readonly TMPROOT="$(mktemp -d)"
trap 'rm -rf "$TMPROOT"' EXIT
readonly SRC="$TMPROOT/brightbean"

cd "$ROOT"
if [[ ! -f "docs/PROJECT_SOURCE.md" || ! -f "MEMORY.md" || ! -f "AGENTS.md" ]]; then
  echo "ERRO: documentação canônica ausente; abortando." >&2
  exit 1
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERRO: working tree não está limpa; abortando." >&2
  exit 1
fi
if [[ "$(git branch --show-current)" != "feat/brightbean-upstream-import" ]]; then
  echo "ERRO: branch inesperada; importação permitida só na branch de revisão." >&2
  exit 1
fi

git clone --quiet --filter=blob:none --no-checkout --depth=1 "$UPSTREAM_REPO" "$SRC"
git -C "$SRC" fetch --quiet --depth=1 origin "$UPSTREAM_SHA"
git -C "$SRC" checkout --quiet --detach "$UPSTREAM_SHA"
[[ "$(git -C "$SRC" rev-parse HEAD)" == "$UPSTREAM_SHA" ]] || { echo "ERRO: SHA inesperado."; exit 1; }

# Apenas transfere arquivos. Não instala dependências nem executa workflows upstream.
# Os dois arquivos com conflitos são preservados em docs/upstream/:
# - README upstream -> docs/upstream/BRIGHTBEAN_README.md
# - CI upstream -> docs/upstream/brightbean-ci.original.yml
# Todos os outros arquivos versionados são copiados para a raiz da aplicação.
rsync -a --exclude='/.git/' --exclude='/README.md' --exclude='/.github/workflows/' \
  --exclude='/AGENTS.md' --exclude='/MEMORY.md' --exclude='/docs/' \
  "$SRC/" "$ROOT/"
mkdir -p docs/upstream
cp "$SRC/README.md" docs/upstream/BRIGHTBEAN_README.md
cp "$SRC/.github/workflows/ci.yml" docs/upstream/brightbean-ci.original.yml

cat > docs/upstream/BRIGHTBEAN_SOURCE.md <<EOF
# Proveniência da base BrightBean Studio

- Origem: https://github.com/brightbeanxyz/brightbean-studio
- Commit de origem fixado: \`$UPSTREAM_SHA\`
- Licença do código original: AGPL-3.0; ver \`LICENSE\`.
- Importação: snapshot integral dos arquivos versionados, validada byte a byte.
- O README original está em \`docs/upstream/BRIGHTBEAN_README.md\`.
- Workflow original desativado por precaução e preservado em \`docs/upstream/brightbean-ci.original.yml\` até revisão.
- Preservar notices de copyright, licenças de terceiros e rastreabilidade.
- O histórico upstream é recuperável pelo SHA e pela URL acima. A cópia é snapshot, não um fork Git com todo o histórico.
- Nenhum teste de aplicação ou deploy é executado pelo bootstrap.
EOF

# Comprovar a importação exata de TODOS os arquivos versionados do upstream.
checked=0
while IFS= read -r -d '' relative; do
  mapped="$relative"
  case "$relative" in
    README.md) mapped="docs/upstream/BRIGHTBEAN_README.md" ;;
    .github/workflows/ci.yml) mapped="docs/upstream/brightbean-ci.original.yml" ;;
  esac
  if [[ ! -f "$ROOT/$mapped" ]] || ! cmp -s "$SRC/$relative" "$ROOT/$mapped"; then
    echo "ERRO: arquivo divergente ou ausente: $relative -> $mapped" >&2
    exit 1
  fi
  checked=$((checked + 1))
done < <(git -C "$SRC" ls-files -z)

[[ "$checked" -gt 800 ]] || { echo "ERRO: contagem de arquivos inesperadamente baixa: $checked"; exit 1; }
printf 'IMPORT_VALIDATED_FILES=%s\nIMPORT_SOURCE_SHA=%s\n' "$checked" "$UPSTREAM_SHA"

python3 - <<'PY'
from pathlib import Path
sha = "96ccc1e88fefa171c4e5ca981dc9f289bdf60d39"
p = Path("docs/CANONICAL_STATE.md")
s = p.read_text(encoding="utf-8")
s = s.replace(
    "- Nenhum código do BrightBean foi importado para OARANHA/CRISE até este marco.",
    "- Snapshot integral do código do BrightBean importado na branch feat/brightbean-upstream-import e comparado byte a byte com o SHA fixado; **nenhum teste funcional executado ainda**.",
)
s = s.replace(
    "## O que NÃO está comprovado/implementado",
    "## Atualização da branch de importação\n"
    f"- Snapshot original: `{sha}`. Arquivos binários incluídos. README/CI originais preservados em docs/upstream.\n"
    "- Importação em PR, não disponível em produção; validação CI da aplicação é etapa separada.\n\n"
    "## O que NÃO está comprovado/implementado",
)
s = s.replace(
    "- Importação integral e reproduzível do BrightBean com histórico de origem e licenciamento.",
    "- Validação da importação por PR, teste do código original e estratégia de sincronização upstream (origem/SHA documentados).",
)
s = s.replace(
    "2. Abrir PR específica para importar a base íntegra do BrightBean, fixar commit de origem, manter licença e executar a suíte de testes original.",
    "2. Revisar a PR de importação de snapshot; ativar a CI upstream somente após revisão e executar testes originais.",
)
p.write_text(s, encoding="utf-8")

p = Path("MEMORY.md")
s = p.read_text(encoding="utf-8")
s += "\n## Atualização após importação (branch em revisão)\n"
s += f"- Snapshot integral do BrightBean copiado na branch de importação, com SHA `{sha}` e verificação byte a byte de todos os arquivos versionados. Sem execução de testes da aplicação, sem deploy e sem aprovação de merge.\n"
p.write_text(s, encoding="utf-8")
p = Path("README.md")
s = p.read_text(encoding="utf-8")
s = s.replace("**Estado:** preparação arquitetural e documental. Não existe aplicação implementada neste repositório ainda.", "**Estado:** base BrightBean importada em branch para revisão e testes, ainda não homologada nem implantada.")
s += "\n## Código original BrightBean\n\nOrigem e SHA fixado em [docs/upstream/BRIGHTBEAN_SOURCE.md](docs/upstream/BRIGHTBEAN_SOURCE.md). O aplicativo está em avaliação, não homologado; não implantar com dados reais antes dos testes.\n"
p.write_text(s, encoding="utf-8")
p = Path("docs/PROJECT_SOURCE.md")
s = p.read_text(encoding="utf-8").replace(
    "Situação:** documentação/fundação; aplicação ainda não importada.",
    "Situação:** código-base em branch de importação; ainda não testado ou homologado.",
)
p.write_text(s, encoding="utf-8")
p = Path("docs/ARCHITECTURE.md")
s = p.read_text(encoding="utf-8").replace(
    "O código-fonte original ainda precisa ser importado e testado.",
    "O código-fonte original foi copiado na branch de importação; **ainda não foi testado**.",
)
p.write_text(s, encoding="utf-8")
p = Path("docs/ROADMAP.md")
s = p.read_text(encoding="utf-8").replace(
    "- [ ] Importar base integral com upstream fixado e avisos de licença.",
    "- [x] Copiar snapshot integral para a branch de importação com upstream fixado e avisos de licença; **merge pendente**.",
)
p.write_text(s, encoding="utf-8")
p = Path("docs/INTEGRATIONS.md")
s = p.read_text(encoding="utf-8").replace(
    "Nenhum componente abaixo está integrado ao repositório nesta data.",
    "Apenas o snapshot BrightBean foi copiado em branch para revisão. Nenhuma integração complementar foi ligada ou testada.",
).replace(
    "| Planejado | Importar e executar testes; AGPL-3.0;",
    "| Código em revisão | Executar testes; AGPL-3.0;",
)
p.write_text(s, encoding="utf-8")
PY

echo "IMPORT_PR_READY: snapshot no working tree; falta revisar, commitar e testar."
