---
name: obsidian-governance
description: Obsidian governance framework for this vault. Enforces structure, semantic tags, graph styling, icon consistency, and commit-delta tracking. Use on every maintenance or content request in this repository.
version: 1.0.0
author: Jonathan + Assistant
tags: [obsidian, governance, tags, graph, icons, workflow, delta]
triggers: [organizar vault, padronizar notas, revisar tags, ajustar grafo, limpar estrutura, novo arquivo]
tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Obsidian Governance Framework

Framework base para manter o vault limpo e consistente ao longo do tempo.

## Objetivos

1. Evitar despadronização de estrutura e metadados.
2. Garantir tags semânticas (sem tags genéricas proibidas).
3. Manter ícones por contexto em todas as pastas.
4. Manter o grafo legível, profissional e segmentado por domínio.
5. Processar sempre por delta desde o último commit governado.
6. Sugerir extensões de taxonomia (tags/ícones) quando houver contexto novo, sem aplicação automática de novas tags fora da taxonomia aprovada.

## Comandos do framework

- `@.agents/obsidian-governance/commands/status`
- `@.agents/obsidian-governance/commands/changed-files`
- `@.agents/obsidian-governance/commands/apply-governance`
- `@.agents/obsidian-governance/commands/mark-baseline`

## Workflows

- `@.agents/obsidian-governance/workflows/delta-governance`

## Agentes especializados

- `@.agents/obsidian-governance/agents/governor`

## Referências

- `@.agents/obsidian-governance/references/policies`
- `@.agents/obsidian-governance/references/delta-tracking`

## Execução one-click

```bash
python .agents/obsidian-governance/scripts/obsidian_governance_run.py
python .agents/obsidian-governance/scripts/obsidian_governance_run.py --mark
```

## Relatório obrigatório

Toda execução deve retornar um relatório resumido no terminal e salvar relatório em:

- `.obsidian-governance/reports/governance-report-*.json`
- `.obsidian-governance/reports/tag-suggestions-latest.json`
- `.obsidian-governance/reports/icon-suggestions-latest.json`
