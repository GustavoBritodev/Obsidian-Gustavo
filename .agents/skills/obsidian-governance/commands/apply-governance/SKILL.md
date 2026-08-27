---
name: obsidian-governance:apply-governance
description: Apply governance scripts for tags and folder icons across the vault.
version: 1.0.0
triggers: [aplicar padrões, padronizar vault, corrigir tags, corrigir ícones]
tools: [Bash]
---

# Command: Apply Governance

Executa padronização por delta (modo one-click recomendado):

```bash
python .agents/obsidian-governance/scripts/obsidian_governance_run.py
```

Para também atualizar o baseline no final:

```bash
python .agents/obsidian-governance/scripts/obsidian_governance_run.py --mark
```

Execução manual equivalente (recomendado por delta):

```bash
python .agents/obsidian-governance/scripts/obsidian_delta.py changed --markdown-only > .obsidian-governance/reports/last-changed-markdown.json
python .agents/obsidian-governance/scripts/tag_vault_notes.py --only-files-json .obsidian-governance/reports/last-changed-markdown.json
python .agents/obsidian-governance/scripts/populate_folder_icons.py
```

Depois valide:

```bash
python .agents/obsidian-governance/scripts/obsidian_delta.py changed --markdown-only
```

Regras obrigatórias de tags nesta execução:

- Não criar `Geral`, `Trabalho`, `areas`.
- Não criar tags de ano (`19xx`, `20xx`).
- Não criar tags-palavra solta fora da taxonomia.
- Reportar `tags_adicionadas` e `tags_removidas` no resumo final.
