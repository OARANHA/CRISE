# 01 — Fundamentos e reuso

**Finalidade:** manter o VIGIAFAST como evolução do BrightBean e evitar reconstrução desnecessária.

- Verificar rotas, modelos, views, serviços, testes, migrações e licenças **antes** de propor código novo.
- Preservar editor, calendário, inbox, analytics, autenticação, portal, API/MCP e recursos originais; evoluir a interface para pt-BR com cuidado.
- Novos módulos devem ser opcionais, integráveis e acessíveis na experiência unificada. Evitar exigir múltiplos painéis do usuário final.
- Nove clientes são ponto de partida, não limite codificado. Cliente observador e cliente operador são públicos distintos; concessão de acesso exige RBAC comprovado.
- Diferenciar contas conectadas e conteúdo público de terceiros. Não inventar coleta global em Instagram, TikTok e Facebook.
- Classificações reputacionais são **apoio à triagem**, não sentença jurídica; críticas legítimas não são automaticamente ilícitos.
- Respeitar licença AGPL-3.0 e avisos do BrightBean; não copiar dados privados do negócio para o repositório.

**Condição de conclusão do reuso:** registrar onde a capacidade já existe, como foi verificada, que lacuna real resta e o menor slice necessário. Referências: [arquitetura](../ARCHITECTURE.md), [integrações](../INTEGRATIONS.md), [ADR-0003 proposta](../decisions/ADR-0003-client-isolation-boundaries.md).
