# Skills de desenvolvimento do VIGIAFAST

Diretório de procedimentos modulares no formato `<slug>/SKILL.md`, com metadados `name` e `description`. Servem para agentes que suportam e reconhecem esse padrão; outros assistentes podem lê-las manualmente.

| Skill | Usar para |
| --- | --- |
| [vigiafast-retomar](vigiafast-retomar/SKILL.md) | Reconciliar GitHub e contexto ao iniciar um trabalho |
| [vigiafast-reusar-brightbean](vigiafast-reusar-brightbean/SKILL.md) | Inventariar código existente e minimizar retrabalho |
| [vigiafast-seguranca](vigiafast-seguranca/SKILL.md) | Modelar riscos e testes negativos entre clientes |
| [vigiafast-documentar](vigiafast-documentar/SKILL.md) | Manter estado, memória e histórico sem contradições |
| [vigiafast-entregar](vigiafast-entregar/SKILL.md) | Validar PR/CI no SHA e encerrar um slice |

**Regra:** uma skill não é ferramenta executável, não realiza deploy nem autoriza ações. `AGENTS.md` e `docs/PROJECT_SOURCE.md` continuam prevalecendo; verificar se o agente em uso realmente descobre skills locais. Se não houver descoberta automática, carregar o arquivo apropriado explicitamente.
