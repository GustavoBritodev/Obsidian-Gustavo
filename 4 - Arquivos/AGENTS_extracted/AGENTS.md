---
tags:
- AGENTS
- Obsidian
- API
- AWS
- BI
- DW
- PowerBI
- SQL
- API Recintos
---
# Vault Agent Policy

Este repositório usa governança obrigatória de Obsidian.

## Obrigatório em qualquer solicitação

1. Carregar `@.agents/skills/obsidian-governance/SKILL.md`.
2. Executar fluxo de delta governança:
   - `@.agents/skills/obsidian-governance/workflows/delta-governance/SKILL.md`
3. Quando necessário, usar comandos da suíte:
   - `@.agents/skills/obsidian-governance/commands/status/SKILL.md`
   - `@.agents/skills/obsidian-governance/commands/changed-files/SKILL.md`
   - `@.agents/skills/obsidian-governance/commands/apply-governance/SKILL.md`
   - `@.agents/skills/obsidian-governance/commands/mark-baseline/SKILL.md`

## Políticas de qualidade

- Tags só podem ser aplicadas em arquivos alterados desde o baseline (`obsidian_delta changed --markdown-only`), nunca varredura global por padrão.
- Não criar tags genéricas proibidas Exemplo:(`Geral`, `Trabalho`, `areas`).
- Não criar tags de ano (`19xx`, `20xx`) nem tags-palavra solta de título.
- Taxonomia obrigatória: preferir tags de domínio/tecnologia/cliente/projeto (ex.: `AWS`, `API`, `API Recintos`, `SQL`, `PowerBI`, `BI`, `DW`, `UNIMED`, `MOVECTA`, `ABA006`, `BRG067`).
- Novas tags fora da taxonomia devem ser explicitamente aprovadas antes de aplicar.
- Quando surgir contexto novo em notas/pastas, gerar sugestões de novas tags/ícones em relatório, sem aplicação automática de novas tags fora da taxonomia aprovada.
- Relatórios de sugestões:
  - `.obsidian-governance/reports/tag-suggestions-latest.json`
  - `.obsidian-governance/reports/icon-suggestions-latest.json`
- Toda execução deve entregar relatório explícito com `tags_adicionadas` e `tags_removidas` (lista única + por arquivo).
- As tags criadas devem estar de acordo com o contexto da anotação .md ou pastas
- Toda pasta/subpasta deve ter ícone contextual.
- Grafo deve permanecer legível e profissional.
- Mudanças estruturais grandes devem ser feitas com abordagem segura (dry-run, aplicação, verificação).
