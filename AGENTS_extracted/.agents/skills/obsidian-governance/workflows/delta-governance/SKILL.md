---
name: obsidian-governance:workflow:delta-governance
description: End-to-end workflow for processing vault changes using last processed commit baseline.
version: 1.0.0
triggers: [workflow governança, rastrear alterações, aplicar padrões por delta]
tools: [Bash, Read, Write]
---

# Workflow: Delta Governance

## Execução one-click (preferencial)

```bash
python .agents/obsidian-governance/scripts/obsidian_governance_run.py
```

Com atualização de baseline ao final:

```bash
python .agents/obsidian-governance/scripts/obsidian_governance_run.py --mark
```

Saída obrigatória: resumo em terminal + relatório JSON em `.obsidian-governance/reports/`.

## Fases

1. **Status**
   - `python .agents/obsidian-governance/scripts/obsidian_delta.py status`
2. **Delta**
   - `python .agents/obsidian-governance/scripts/obsidian_delta.py changed --markdown-only`
3. **Aplicação**
   - `python .agents/obsidian-governance/scripts/tag_vault_notes.py`
   - `python .agents/obsidian-governance/scripts/populate_folder_icons.py`
4. **Verificação**
   - validar ausência de tags proibidas no frontmatter
   - validar JSON de `.obsidian/*`
5. **Checkpoint**
   - com aprovação do usuário: `python .agents/obsidian-governance/scripts/obsidian_delta.py mark`

## Critério de sucesso

Arquivos alterados desde baseline foram processados, regras aplicadas, e baseline atualizado quando aprovado.
