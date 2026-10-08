# AGENTS.md — instruções permanentes a assistentes e desenvolvedores

Você trabalha no produto VIGIAFAST, do projeto CRISEDIGITAL. Responda e implemente a interface em português brasileiro.

## Ao começar
- Leia `docs/PROJECT_SOURCE.md` na ordem definida; não assuma que um chat anterior descreve o estado atual.
- Confira estado real de `main`, PRs, branch, SHA e testes; identifique exatamente o que está implementado e o que é planejamento.
- Antes de criar código, abra o código existente do BrightBean e verifique capacidade e testes que podem ser reutilizados.
- Dê preferência à evolução incremental da base Django/Python/PostgreSQL; não reescreva o projeto em outra stack por conveniência.

## Princípios
- Preservar integralmente os recursos funcionais do BrightBean, salvo decisão formal em ADR.
- Trabalhar em módulos opcionais e integráveis; painel VIGIAFAST único para funcionários não técnicos.
- Isolar os dados dos clientes, aplicar menor privilégio, autenticação, LGPD e revisão humana de decisões sensíveis.
- Diferenciar contas autorizadas/conectadas de descoberta de publicações de terceiros; não prometer acesso irrestrito a Instagram, TikTok ou Facebook.
- Para riscos reputacionais, separar crítica legítima, ironia, alegação e hipótese de ilícito. Nunca classificar automaticamente como crime.
- Preservar direitos autorais, marcas e avisos de licença. Interface VIGIAFAST própria não autoriza suprimir avisos legais.

## Fluxo de entrega
- Uma tarefa/slice por PR, com critérios de aceitação e testes adequados.
- Cada PR que alterar comportamento deve atualizar `docs/CANONICAL_STATE.md`, `MEMORY.md` e, se necessário, ADRs/arquitetura/integrações.
- Explicitar resultados de testes executados e os não executados, sem inventar sucessos.
- Não fazer polling contínuo do CI; esperar comunicação do operador.
- Não aplicar mudanças destrutivas, deploys, rotação de segredos ou operações em outros sistemas sem autorização explícita.
- Não incluir `.env` real, tokens, perfis pessoais, posts, comentários, capturas ou relatórios reais de clientes no Git público.

## Documentação viva e skills
- O índice em `docs/README.md` e a doutrina em `docs/doutrina/` complementam as regras existentes, **sem substituir ADRs aceitas ou evidências reais**.
- Skills em `.agents/skills/` são guias opcionais para agentes compatíveis; a presença dos arquivos não prova carregamento automático.
- `docs/CANONICAL_STATE.md` deve permanecer como snapshot atual e conciso; `MEMORY.md` como memória curta. Registro antigo vai para Git/PRs ou `docs/historico/`, nunca como status atual.

## Saída ao encerrar
Registrar: branch e SHA, arquivos alterados, PR, testes executados, riscos conhecidos e próxima ação concreta. Atualizar os arquivos do repositório; não depender do chat para continuidade.
