---
name: obsidian-governance:changed-files
description: List changed markdown files since baseline commit.
version: 1.0.0
triggers: [arquivos novos, arquivos alterados, delta markdown]
tools: [Bash]
---

# Command: Changed Files

Lista arquivos `.md` alterados desde o baseline:

```bash
python .agents/obsidian-governance/scripts/obsidian_delta.py changed --markdown-only
```
