# Guia de Tageamento - Rede Neural (PARA + Zettelkasten)

Para o Obsidian funcionar como um "segundo cérebro" e desenhar uma Graph View (Rede Neural) rica e organizada, o uso adequado de tags e links é essencial. 

## 1. Tipos de Tags
Recomendamos o uso de tags aninhadas (com a barra `/`) para classificar a informação sem criar centenas de tags soltas.

- **Status da Nota:**
  - `#status/rascunho` - Notas não terminadas ou soltas
  - `#status/andamento` - Projetos ou áreas que estão em andamento
  - `#status/concluido` - Tarefas finalizadas ou notas completas e revisadas

- **Tipo da Nota:**
  - `#tipo/diario` - Notas de registro diário
  - `#tipo/reuniao` - Atas de reunião
  - `#tipo/projeto` - Um projeto do método PARA
  - `#tipo/conceito` - Uma nota zettelkasten, sobre um conceito atemporal
  - `#tipo/leitura` - Resumos de livros/artigos

- **Contexto / Tópico (O "neurônio" da rede):**
  - Use tags sobre os assuntos gerais para gerar clusters na Graph View.
  - Exemplos: `#programacao`, `#marketing`, `#saude`, `#financas`.

## 2. Como usar no dia a dia
- Toda nota que você cria deve ter, pelo menos, uma tag de **tipo** e uma de **contexto**.
- Na seção `properties` (Frontmatter) no topo da página, insira suas tags para manter a nota limpa.
- **Dica de Ouro:** Não use a tag no lugar de um link. Se uma entidade é importante (ex: uma pessoa, um cliente, um projeto grande), crie uma nota para ela e faça um *Link* `[[Nome do Cliente]]` em vez de usar `#cliente`. Links criam a rede neural muito mais forte!

## 3. Cores no Graph View
Abra o **Graph View** (Grafo) e clique na engrenagem. Vá em **Grupos (Groups)** e atribua cores para as tags que você criou:
- Ex: `#tipo/projeto` -> Vermelho
- Ex: `#tipo/diario` -> Cinza
- Ex: `#programacao` -> Azul

Isso fará o seu cofre florescer visualmente!
