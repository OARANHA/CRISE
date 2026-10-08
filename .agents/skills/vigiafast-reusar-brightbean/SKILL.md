---
name: vigiafast-reusar-brightbean
description: "Use antes de criar ou substituir funcionalidades do VIGIAFAST para reaproveitar módulos, rotas, testes e permissões existentes no BrightBean."
---

# Reuso obrigatório do BrightBean

1. Nomeie a capacidade desejada e distinga **conta social conectada** de **descoberta de terceiros**.
2. Localize implementação real nos apps Django, URLs, managers, tarefas, modelos, templates, API/MCP e testes da branch atual.
3. Documente `já existe`, `existe parcialmente` ou `não existe`, citando arquivos, comportamento e limitações, sem confiar só no README.
4. Preserve autenticação, editor, calendário, inbox, analytics, portal do cliente e mecanismos de aprovação. Respeite AGPL-3.0 e avisos.
5. Proponha o menor adaptador/módulo incremental; preferir extensões e organização visual a refazer componentes.
6. Para social media, confira scopes e condições das APIs; não prometer leitura indiscriminada de Instagram, Facebook ou TikTok.

**Saída:** mapa `requisito → código reaproveitado → lacuna → teste → decisão`, com referência a `docs/ARCHITECTURE.md`, `docs/INTEGRATIONS.md` e `docs/ROADMAP.md`.
