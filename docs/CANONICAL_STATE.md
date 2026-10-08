# VIGIAFAST — estado canônico verificável

**Snapshot de verificação:** 2026-10-08. Sempre reconciliar com GitHub antes de agir. Sem deploy ou homologação de clientes reais.

## REAL NOW

| Referência | Verificação pontual |
| --- | --- |
| `main` | `f6883b747ce1a6ae6a6968948da5225332ed4f2f` — BrightBean não integrado |
| `feat/brightbean-upstream-import` | `84139275e16efcd2201191275b24cc9ea3513fa6` — PR #25 integrada |
| [PR #2](https://github.com/OARANHA/CRISE/pull/2) | Aberta, Draft, base `main`; sem merge autorizado |
| [PR #25](https://github.com/OARANHA/CRISE/pull/25) | Integrada à branch de importação no SHA `84139275e16e...` |
| [CI pós-merge PR #25](https://github.com/OARANHA/CRISE/actions/runs/37848566089) | `completed/success` no SHA `84139275e16e...`; Pytest, Ruff, Mypy, Gitleaks e Docker: 5/5 |
| Slice atual M10 | [PR #26](https://github.com/OARANHA/CRISE/pull/26) aberta, branch isolada; CI inicial [#37856628216](https://github.com/OARANHA/CRISE/actions/runs/37856628216) **RED**, SHA `efe127c0ccf85db549a633fde5bfd14df941bfb5` — correção apenas da suíte de testes em nova revisão |

## PROVEN EVIDENCE

- BrightBean Studio Django/Python/PostgreSQL, AGPL-3.0, presente apenas na branch de importação; recursos de editor, calendário, aprovações, inbox, analytics, portal, mídias, API/MCP e RBAC preservados. Existência de código não equivale a homologação.
- PR #22: defesa pontual do diretório organizacional; PR #24: checagem de permissão atual nas quatro ações de aprovação; PR #25: bloqueio de comentário interno forjado pelo papel CLIENT, com oito regressões sintéticas e CI pós-merge aprovada. Não refazer.
- [M10](audits/2026-10-08-m10-editor-internal-visibility.md): código mostra filtros de comentários/replies e anexos INTERNAL somente para papel CLIENT. O papel EDITOR retém acesso, independentemente da afiliação de negócio pretendida. Dez testes de **caracterização** foram adicionados. Na primeira CI, oito passaram e dois falharam por conexão do banco fechada no teste com streaming; o desvio funcional M10 foi reproduzido. A correção do teste e a formatação aguardam nova CI, sem mudança das permissões da aplicação.
- Na tela do portal as raízes/replies são filtradas para EXTERNAL; isso não substitui os controles de dados das rotas de edição.

## GAPS → REUSE GATE → DECISION

1. ADR-0001 e ADR-0002: **aceitas**. ADR-0003 (isolamento multi-cliente/identidade) e ADR-0004 (storage de evidências): **propostas, não aceitas**.
2. Identidade interna VIGIAFAST × operador de cliente ainda não existe como controle persistido confiável. Dois EDITOR de origem distinta têm acesso interno idêntico nas rotas estudadas; esta divergência **não está corrigida**.
3. Mídia compartilhada pela organização, eventuais IDs sociais duplicados, REST/MCP, demais superfícies e storage de evidências privadas não estão homologados globalmente; evidências privadas não devem ir ao `media_library/`.
4. Próxima ação: operador informa `green` ou `red` para a nova execução da PR #26; verificar a CI **uma única vez** no novo SHA. O histórico do RED anterior permanece referenciado. Uma CI verde não aprova ADR nem autoriza merge. Após evidência, deliberar separadamente a afiliação e autorização por classe de dados na ADR-0003.
5. Sem merge na `main` ou PR #2; sem deploy, infraestrutura externa, dados reais de clientes ou coletas sociais.
