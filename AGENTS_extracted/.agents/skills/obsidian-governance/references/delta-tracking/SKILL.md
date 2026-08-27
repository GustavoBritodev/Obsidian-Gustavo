---
name: obsidian-governance:reference:delta-tracking
description: Delta tracking model for vault governance using a persisted last processed commit.
version: 1.0.0
triggers: [delta, baseline, ultimo commit processado, rastreio]
tools: [Read, Bash]
---

# Delta Tracking

## Arquivos

- Estado: `.obsidian-governance/state.json`
- Script: `.agents/obsidian-governance/scripts/obsidian_delta.py`

## Comandos

Inicializar baseline:

```bash
python .agents/obsidian-governance/scripts/obsidian_delta.py init
```

Ver status:

```bash
python .agents/obsidian-governance/scripts/obsidian_delta.py status
```

Listar arquivos alterados:

```bash
python .agents/obsidian-governance/scripts/obsidian_delta.py changed --markdown-only
```

Marcar commit processado:

```bash
python .agents/obsidian-governance/scripts/obsidian_delta.py mark
```

## Regra de operação

Sempre analisar e aplicar governança por delta antes de marcar o novo baseline.
