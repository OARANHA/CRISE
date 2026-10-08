---
name: vigiafast-seguranca
description: "Use em qualquer mudança de clientes, permissões, inbox, mídias, webhooks, API, relatórios ou evidências para exigir testes adversariais de isolamento."
---

# Gate de segurança entre clientes

1. Verifique ADR-0003 e ADR-0004 e seus status. **Propostas não são autorização** para dados reais ou deploy.
2. Identifique ator, papel, workspace, organização, fonte, ação e classificação do dado. Não confunda funcionário de cliente com funcionário interno, mesmo se ambos tiverem EDITOR.
3. Avalie IDOR por UUID, listagem, download, HTMX, REST, MCP, filas, cache, webhooks, revogação, comentários internos, mídia `org-shared` e links mágicos.
4. Crie testes sintéticos A/B (workspaces na mesma organização) e C (outra organização); cubra casos permitidos e proibidos sem dados reais.
5. Evidências e relatórios confidenciais exigem storage separado do `media_library/` editorial público, com trilha de acesso e retenção LGPD.
6. Verifique que a correção não rompe funções BrightBean e que avaliações reputacionais sensíveis permanecem sob revisão humana.

**Saída:** vetor de risco, comportamento real, teste reprodutível, resultado obtido/não obtido e limites ainda abertos. Não declarar isolamento global com base em teste pontual.
