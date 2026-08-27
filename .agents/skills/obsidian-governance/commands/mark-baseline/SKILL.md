---
name: obsidian-governance:mark-baseline
description: Mark current HEAD commit as processed in governance state.
version: 1.0.0
triggers: [finalizar governança, atualizar baseline, commit processado]
tools: [Bash]
---

# Command: Mark Baseline

Após validação final aprovada pelo usuário:

```bash
python .agents/obsidian-governance/scripts/obsidian_delta.py mark
```
