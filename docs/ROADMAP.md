# Roadmap — VIGIAFAST

Roadmap é planejamento, **não comprovação de recursos entregues**. Manter status e PRs vinculados a cada fase.

## Fase 0 — Fundamentos documentais
- [x] Criar README público sem dados sensíveis.
- [ ] Integrar/mesclar documentação canônica e memória no main por PR.
- [ ] Estabelecer critérios objetivos de aceite e matriz de risco.

## Fase 1 — Importar e preservar BrightBean
- [x] Copiar snapshot integral para a branch de importação com upstream fixado e avisos de licença; **merge pendente**.
- [ ] Executar testes, lint, migrations e checks de segurança; registrar evidências.
- [ ] Validar comportamento real de RBAC, workspaces, inbox e API/MCP.
- [ ] Definir CI para evitar regressões antes da reformulação visual.

## Fase 2 — Operação simples para equipe
- [ ] Rebrand total da interface para VIGIAFAST em pt-BR, sem remover funcionalidade original.
- [ ] Cadastro multi-cliente, termos monitorados, prioridades e responsáveis.
- [ ] Módulo de ocorrências, notas, atribuições e histórico auditável.

## Fase 3 — Inteligência e evidências
- [ ] Prova de conceito Obsei com classificação contextual pt-BR e revisão humana.
- [ ] Prova de conceito Auto Archiver com hashes e storage protegido.
- [ ] Alertas e relatórios por cliente, sem vazamento inter-tenant.

## Fase 4 — Descoberta pública validada
- [ ] Pesquisa de menções por nome/variações em fontes públicas e APIs permitidas.
- [ ] Monitoramento de URLs conhecidas e coleta documentada de comentários disponíveis.
- [ ] Matriz por rede: cobertura, disponibilidade, limites, custo, LGPD e testes.

## Fase 5 — Homologação / produção
- [ ] Auditoria, backups/restauração, retenção, observabilidade e testes com dados sintéticos.
- [ ] Autorizações específicas para credenciais reais e deploy isolado.
- [ ] Treinamento da equipe e operação supervisionada.

**Regra:** nenhuma fase avança por descrição em chat; anexar PR/commit, testes e evidências em `docs/CANONICAL_STATE.md`.
