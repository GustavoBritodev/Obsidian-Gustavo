---
name: obsidian-governance:reference:policies
description: Governance policies for tags, icons, graph style, and folder semantics.
version: 1.0.0
triggers: [policy, padrão, convenções do vault]
tools: [Read]
---

# Governance Policies

## Tags

- Sempre semânticas (tema, cliente, tecnologia, domínio).
- Não usar tags genéricas proibidas: `Geral`, `Trabalho`, `areas`.
- Não usar tags de ano (`19xx`, `20xx`) nem palavras soltas de título.
- Aplicar tags por delta: processar somente arquivos retornados por `obsidian_delta.py changed --markdown-only`.
- Em Trabalho/Clientes, priorizar taxonomia controlada (tecnologia + cliente + código de projeto).
- Qualquer tag nova fora da taxonomia deve ser aprovada explicitamente pelo usuário antes da aplicação.
- Quando surgir contexto novo, sugerir tags candidatas em relatório separado sem aplicar automaticamente.
- Em diário, ignorar widgets de tarefas (` ```tasks ... ``` `) para inferência.
- Toda execução deve gerar relatório com:
  - `tags_adicionadas_unicas`
  - `tags_removidas_unicas`
  - detalhamento por arquivo

## Ícones de pasta

- Toda pasta/subpasta deve ter ícone contextual.
- Clientes críticos têm override explícito (ex.: UNIMED, Bridgestone, MOVECTA, ABA).
- Evitar fallback genérico quando possível.
- Para pastas novas sem regra específica, gerar sugestões de novos ícones/overrides em relatório.

## Grafo

- Clusters por domínio (Diário, Projetos, Áreas, Trabalho/Clientes, Recursos, Arquivo, Assets).
- Paleta consistente e legível.
- Priorizar visual profissional: baixa poluição, bom contraste.

## Estrutura

- Seguir estrutura raiz pactuada com o usuário.
- Migrações estruturais sempre em lote seguro (dry-run + aplicação + verificação).
