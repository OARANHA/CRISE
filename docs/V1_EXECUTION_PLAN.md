# Plano de execução VIGIAFAST V1 — produto operacional

**Data:** 2026-10-08. **Status:** plano de trabalho (não é ADR, implementação concluída nem autorização de deploy). **Sem etapa de demonstração.** Programa: [issue #32](https://github.com/OARANHA/CRISE/issues/32).

## Objetivo e critério real de entrega
Plataforma VIGIAFAST operacional, inteiramente em português brasileiro para fluxos principais, inicialmente nove clientes e preparada para inclusão de outros, reusando o BrightBean Studio Django/PostgreSQL sob AGPL-3.0. O produto é liberado somente depois de isolamento e controle de acesso comprovados, fluxo de trabalho end-to-end, conectores validados nas permissões efetivas, evidências privadas, revisão humana, LGPD e autorização para implantação.

**Não confundir:** código importado ≠ `main`; CI verde ≠ homologação; mock/fixture ≠ integração com rede social; decisão consultiva do JEV ≠ aprovação humana; documentação ≠ execução de agentes autônomos.

## REAL NOW verificado
- `main` @ `f6883b747ce1a6ae6a6968948da5225332ed4f2f`; PR [#2](https://github.com/OARANHA/CRISE/pull/2) aberta/Draft para `main` — sem autorização para merge.
- Base de desenvolvimento `feat/brightbean-upstream-import` @ `648050ab37525cd596e69b61a600ea09a1503886`, merge da PR [#31](https://github.com/OARANHA/CRISE/pull/31). CI do HEAD pós-merge **não verificada aqui**; CI pré-merge da PR #31 GREEN 5/5 no HEAD `7ce2acd...`.
- ADR-0003 (tenancy, afiliação) e ADR-0004 (storage privado) permanecem **propostas/não aceitas**. M11, M10, M09 ainda abertos. Nenhuma VPS escolhida/autorizada, nenhum deploy.
- Docker/Compose/Caddy/worker e testes de CI estão presentes. Branding pt-BR completo, monitoramento de terceiros, ocorrências, evidências privadas e sistema reputacional não estão prontos.

## Caminho crítico: nove marcos até V1

| Ordem | Marco / saída verificável | Dependência / gate |
| --- | --- | --- |
| 1 | **ADR-0003 + ADR-0004**: escolha tenant, afiliação, autoridade, legado, confidencialidade, storage privado | Aprovação humana específica, não inferida de um `green` |
| 2 | **Isolamento**: corrigir M11, depois M10 e M09; negativos cross-tenant A/B/C incluindo portal/REST/MCP/workers/UUID | Marco 1, testes e PRs distintos |
| 3 | **Fundação BrightBean**: preservar todos os módulos existentes/licença e revisar PR #2 | Segurança e revisão; merge `main` somente com autorização específica |
| 4 | **UX VIGIAFAST**: identidade visual, português brasileiro, fluxos claros para equipe e cliente | Pode iniciar agora sem mudar RBAC/tenant |
| 5 | **Operações reputacionais**: cliente, termos/variações, menção, triagem, ocorrência, responsável, alerta e histórico | Contrato tenant aprovado, reuso inventariado |
| 6 | **Fontes**: conectores permissíveis por rede; separar contas autorizadas vs terceiros, aferir cobertura, custos e lacunas | Matriz de viabilidade pode iniciar já; ingestão só após autorização |
| 7 | **Inteligência + provas**: pt-BR/Obsei com revisão humana; Auto Archiver validado; storage privado, hash/proveniência | Marco 1/2 e aceite ADR-0004 |
| 8 | **Relatórios + área cliente**: visões e notificações autorizadas, trilha de auditoria | Marco 2/5/7 |
| 9 | **GO/NO-GO de produção**: backups/restore, logs, segredos, HTTPS, testes multi-cliente, LGPD, licença, VPS e deploy autorizado | Todos os gates, domínio/VPS e autorização separados |

Esses são **macroetapas**, não nove PRs ou uma estimativa de tempo. Os marcos 4, descoberta do 6 e runbook do 9 são parcialmente paralelizáveis. Códigos de segurança, domínio e evidências possuem dependências rígidas.

## Quatro frentes de agentes (issues são as filas persistentes)

| Frente | Tarefa rastreável | Primeiro entregável isolado | Pode começar? |
| --- | --- | --- | --- |
| Segurança/arquitetura | [#33](https://github.com/OARANHA/CRISE/issues/33) | Matriz M11/M10/M09 e decisão ADR sem alteração runtime | **Sim**, só análise/testes caracterizadores; implementação após gate |
| UX/pt-BR | [#34](https://github.com/OARANHA/CRISE/issues/34) | Shell/login/navegação BrightBean → VIGIAFAST sem alterar auth/RBAC | **Sim**, PR funcional pequena |
| Monitoramento/inteligência | [#35](https://github.com/OARANHA/CRISE/issues/35) | Matriz fonte/permissões reais e contratos com fixtures sintéticas | **Sim**, sem ingestão real |
| Infra/QA | [#36](https://github.com/OARANHA/CRISE/issues/36) | Runbook Docker/VPS, matriz GO/NO-GO e testes não destrutivos | **Sim**, sem deploy |

**Coordenação central:** integrador revisa cada PR, conflitos, documentação e evidências; usuário autoriza merges e deploy. Ferramentas/skills existentes ajudam a gerar e revisar trabalho, mas **não há execução contínua automática de quatro agentes demonstrada** neste programa. Para rodá-los de fato, cada sessão/runner precisa ter acesso autorizado ao repositório e escopo delimitado.

## Protocolo de paralelismo obrigatório
1. Um agente/issue/branch/PR por slice. Branch sempre criada do SHA observado da importação; nunca editar `main` diretamente.
2. Reservar **propriedade de arquivos**: UX altera `templates/`, `theme/` e testes da experiência; segurança `apps/members/`/autorização e testes; fontes `apps/` de conectores apenas após autorização ou `docs/INTEGRATIONS.md`; infra Docker/Compose/Caddy/CI apenas em PR própria. Mudanças cruzadas requerem coordenador.
3. **Arquivos compartilhados** `docs/CANONICAL_STATE.md`, `MEMORY.md`, `AGENTS.md`, ADRs: integrador central concilia em um PR por vez; não permitir atualizações concorrentes às cegas.
4. Antes de implementar: provar por código que BrightBean não realiza a função; não duplicar auth, editor, calendário, inbox, portal ou mídia.
5. Cada PR: escopo, SHA base/head, contratos de acesso, migrações conservadoras, testes sintéticos negativos, CI do HEAD, licença e documentação atualizada, riscos e reversão. Sem polling contínuo da CI.
6. Não aceitar automaticamente status do JEV, CI ou agente como autorização. Não promover `EDITOR` a `internal` por role; não expor evidências por `MediaAsset`/Caddy público; não usar dados reais no Git.
7. Rebase/merge de uma frente em outra somente após decidir a ordem das PRs e resolver conflitos. O objetivo é reduzir **tempo calendário**, não contornar revisão ou permitir escrita concorrente na mesma branch.
8. `green` e `red` informados pelo operador são eventos para consulta **pontual** ao commit, não gatilhos de polling.

## Primeira onda autorizável já (antes da VPS)
- **UX #34:** começar pelo login, títulos e dashboard pt-BR com testes de renderização, sem alterar login, sessão ou autorização. Não afirmar branding integral ao concluir primeira PR.
- **Monitoramento #35:** auditar cobertura real e definir contrato de normalização e triagem sem coleta/credenciais.
- **Segurança #33:** preparar teste/contrato de M11 e parecer ADR-0003; nenhuma política nova antes do aceite.
- **Infra #36:** checklist e infraestrutura como código apenas em revisão, sem operação externa.
- Após a onda, consolidar evidências e obter deliberação explícita ADR-0003/0004; só então implementar M11/M10 e dados reputacionais privados.

## Evidências/referências
- [Roadmap de fases](ROADMAP.md), [estado canônico](CANONICAL_STATE.md), [segurança](SECURITY.md), [integrações](INTEGRATIONS.md).
- [Parecer ADR-0003](audits/2026-10-08-adr0003-tenancy-deliberation.md), [M11](audits/2026-10-08-m11-multi-org-context-characterization.md), [M10](audits/2026-10-08-m10-actor-affiliation-architecture-gate.md).
- JEV.1 `jev_route_task` consultivo em 2026-10-08: `split_task`, confiança `0.83` (`prob.split_task=0.87`); não determinístico e não vinculante.
