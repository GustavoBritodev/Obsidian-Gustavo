---
tags:
- Excalidraw
- Obsidian
---
# 🤖 Regras de Orquestração para IA (Obsidian Vault)

Você (a Inteligência Artificial) está operando e auxiliando no gerenciamento do cofre Obsidian do Gustavo. Siga estas diretrizes de arquitetura rigorosamente.

## 1. Organização do Cofre (Método PARA)
- **1 - Projetos:** Projetos ativos, limitados no tempo e com objetivo claro.
- **2 - Áreas:** Responsabilidades contínuas e perenes (ex: Trabalho, Faculdade, Estudos).
- **3 - Recursos:** Assuntos de interesse contínuo (artigos, links, Excalidraw, etc).
- **4 - Arquivos:** Itens inativos de Projetos ou Áreas descontinuadas.
- **Diário:** Apenas para Daily Notes.
- **Não crie pastas soltas** na raiz sem explícita autorização do usuário. Se precisar gerar notas, aloque-as na pasta estrutural correta. Não utilize "Inbox", as notas entram direto na estrutura.
- **Anexos:** Salve anexos por padrão na pasta `assets`.

## 2. Taxonomia de Tags e YAML (Frontmatter)
Este cofre não utiliza tags de "status" no conteúdo (como rascunho/andamento) e evita tags genéricas dispersas (ex: `#frontend` solto). 
Toda nova anotação criada **deve obrigatoriamente** conter um bloco Frontmatter (YAML) com a chave `tags` seguindo o formato em cascata: `tipo/macro/tema`.

- Se for de **Estudo**: `#tipo/estudo/visao_computacional`, `#tipo/estudo/ia`.
- Se for de **Trabalho**: `#tipo/trabalho/projeto/nome_do_projeto` ou `#tipo/trabalho/reuniao`.
- Se for da **Faculdade**: `#tipo/faculdade/materia`.
- Geral / Raiz: `#tipo/geral`.

## 3. Gestão da Rede Neural (Links Duplos)
- A principal fonte de conexão não é a tag, é o link: `[[Link Bidirecional]]`.
- Ao invés de inserir uma tag `#João`, sempre use a entidade estruturada `[[João]]`.
- Dê prioridade a conexões orgânicas e Mapas de Conteúdo (MOC).

## 4. Notas Diárias (Daily Notes e Templater)
- As notas diárias usam o **Templater**. O formato da data baseia-se em `YYYY-MM-DD`.
- Toda nova nota criada na pasta `Diário/` receberá o template automaticamente.
- Evite sobrescrever as anotações passadas, trabalhe injetando afazeres no dia corrente (hoje).

## 5. Linguagem
- Todas as interações diretas (explicações, commits) e nomes/títulos de anotações devem ser, obrigatoriamente, em **Português do Brasil (pt-BR)**. Nomes de variáveis em blocos de código podem permanecer em inglês se necessário.

## 6. Sincronização via Git (Obsidian Git)
- O cofre é ativamente rastreado pelo plugin "Obsidian Git" e versionado.
- Sempre que você executar rotinas que reescrevam muitos arquivos ou alterem arquitetura em lote, invoque um comando de Git para commitar e salvar as mudanças na branch `main`.

## 7. Auto-Atualização do AGENTS.md
- A qualquer iteração nossa e eventual atualização nas regras do Obsidian, você (a IA) deverá garantir que este documento (AGENTS.md) também seja atualizado com os novos padrões combinados.
- Este arquivo deve sempre ser espelhado nos caminhos `AGENTS.md` (raiz) e `.agents/AGENTS.md`.
