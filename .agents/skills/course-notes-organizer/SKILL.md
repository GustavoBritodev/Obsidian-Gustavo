---
name: course-notes-organizer
description: Create and organize course notebooks in Obsidian. Automatically structure directories, modules, and lesson markdown files. Populates notes with proper frontmatter, structured summaries, tools/commands, references, and complete transcripts. Use this skill when the user wants to organize a course syllabus, import course HTML/text, or structure lesson materials and video transcriptions.
---

# Course Notes Organizer

Esta skill orienta e automatiza o processo de estruturação de cadernos de cursos e pós-graduações dentro do Obsidian, gerando pastas e notas de aulas padronizadas com base em ementas, ementas em HTML ou transcrições brutas.

---

## 📂 1. Estrutura de Pastas do Curso

Ao organizar um curso ou disciplina, siga rigidamente a seguinte hierarquia de pastas:

```
[Pasta do Curso]/
└── Fase [N] - [Nome da Fase]/
    ├── 00 - [Módulo de Boas-Vindas]/
    │   └── 01 - [Nome da Introdução].md
    ├── 01 - [Nome do Primeiro Módulo]/
    │   ├── Aula 1 - [Nome da Aula].md
    │   └── Aula 2 - [Nome da Aula].md
    ├── 02 - [Nome do Segundo Módulo]/
    │   └── ...
    └── [Utils ou Anexos]/
```

### Regras de Ouro de Nomenclatura:
1. **Fase/Etapa**: Nomeie a pasta raiz com o padrão `Fase [N] - [Nome]`. (Atenção para preservar espaços no final se já existentes no padrão do usuário).
2. **Módulos (Pastas)**: Identifique o que representa um módulo ou divisor de seção (por exemplo, classes `is-marcador` em HTML de portais de ensino) e crie uma subpasta correspondente numerada sequencialmente a partir de `00 - ...`, ex: `00 - Welcome`, `01 - Red Team Operations`, `02 - Malware Analysis`.
3. **Aulas (Arquivos MD)**: Identifique o que representa uma aula (por exemplo, classes `conteudo-digital-item`) e crie um arquivo `.md` correspondente dentro da pasta do módulo, ex: `Aula 1 - Pós-exploração Linux - parte 1.md`.

---

## 📝 2. Template de Nota de Aula

Todo arquivo de aula (`.md`) deve obrigatoriamente seguir a estrutura padrão abaixo. Um arquivo de exemplo também está salvo em `assets/aula-template.md`.

```markdown
---
title: "Aula [N] - [Nome da Aula]"
date: [YYYY-MM-DD]
tags:
  - FIAP
  - RedTeam
  - Fase5
  - [Tags Específicas]
---

# Aula [N] - [Nome da Aula]

## 📌 Introdução
> [!info] 
> [Resumo sucinto de 1 a 2 parágrafos apresentando a visão geral e os objetivos de aprendizado da aula.]

## 📝 Notas de Aula
### Conteúdo Principal
- [Ponto importante 1]
- [Ponto importante 2]

### 🛠️ Ferramentas & Comandos
- [Nome da Ferramenta] -> [Descrição rápida de uso]
  ```bash
  [Comando exato utilizado na aula]
  ```

## 🔗 Referências & Links Úteis
- [Nome do Link/Artigo](URL)

## Transcrição
[Transcrição completa e literal da aula/vídeo]
```

---

## 🗣️ 3. Como Processar Transcrições e Popular o Template

Quando fornecido uma transcrição bruta ou arquivos de áudio/vídeo transcritos, siga este passo a passo para extrair inteligência e popular a nota:

### Passo 1: Análise e Separação da Transcrição
* Identifique a qual aula a transcrição pertence.
* Cole a transcrição literal na seção final `## Transcrição` da nota correspondente.

### Passo 2: Extração de Conceitos (Notas de Aula)
* Leia a transcrição e extraia os conceitos principais abordados.
* Adicione no item `### Conteúdo Principal` as teorias, metodologias e explicações conceituais passadas pelo instrutor.

### Passo 3: Mapeamento de Ferramentas & Comandos
* Localize **todas** as menções a comandos e ferramentas no texto da transcrição.
* Formate-as sob a seção `### 🛠️ Ferramentas & Comandos` com explicações do porquê foram usadas e blocos de código markdown (` ```bash `) contendo os comandos exatos.

### Passo 4: Extração de Materiais de Apoio
* Busque na transcrição ou em abas adjacentes do portal de ensino (ex: aba de "materiais de apoio" ou links contidos na página original) todos os links úteis e adicione na seção `🔗 Referências & Links Úteis`.

### Passo 5: Geração de Metadados e Introdução
* Escreva um resumo executivo inteligente no callout `📌 Introdução`.
* Preencha as propriedades frontmatter (`title`, `date`, `tags` personalizadas ao tema da aula).
