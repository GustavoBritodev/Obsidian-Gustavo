---
tags:
  - tipo/trabalho/projeto/clarion
---
# 📄 Gerenciamento de Clientes (Tela Inicial)

## 📌 Objetivo
Esta é a tela principal de aterrissagem (Home) do sistema Clarion. O objetivo deste painel é atuar como um hub central de organização, permitindo que o usuário separe seus ambientes de trabalho, painéis e bases de dados por clientes, setores ou projetos distintos. Cada "Card" atua como um espaço de trabalho (Workspace) isolado.

## 🖼️ Visão Geral
> 📸 ![[Tela Inicial.png]]

Ao acessar o sistema, o usuário visualiza todos os ambientes de clientes aos quais possui permissão de acesso. A navegação prioriza uma busca rápida e uma visão macro do nível de atividade em cada um desses espaços.

---
## ⚙️ Fluxos de Uso

### 1. Criando um Novo Ambiente de Cliente
> 📸 ![[Tela Inicial - Modal Adicionar Novo Cliente.png]]

Para iniciar um novo projeto ou isolar dados de um novo parceiro, é necessário criar um Cliente. Este fluxo cria uma nova "pasta raiz" no sistema onde os futuros gráficos e dashboards habitam de forma exclusiva.

*   **Acesso:** Botão `+ Adicionar Novo Cliente` no canto superior direito.
*   **Ação:** Preenchimento de dados de identificação e identidade visual do cliente.
*   **Resultado:** Um novo card é gerado na Tela Inicial e o ambiente fica pronto para receber conexões de dados.

### 2. Editando um Cliente
> 📸 ![[Tela Inicial - Edição de Cliente.png]]

Permite a atualização rápida das informações cadastrais ou da identidade visual de um ambiente já existente.

*   **Acesso:** Clicar no menu `...` do card desejado e selecionar "Editar".
*   **Ação:** Modificação dos dados preexistentes (Nome, Categoria ou Logotipo).
*   **Resultado:** O card e as propriedades internas do ambiente são atualizados imediatamente.

### 3. Excluindo um Cliente
> 📸 ![[Tela Inicial - Exclusão.png]]

A exclusão de um ambiente é tratada como uma ação de alto risco. Para evitar exclusões acidentais que resultariam em grande perda de trabalho, o sistema exige uma confirmação explícita.

*   **Acesso:** Clicar no menu `...` do card desejado e selecionar "Remover".
*   **Ação:** O usuário deve obrigatoriamente digitar o nome exato da empresa no campo de texto para habilitar o botão de remoção.
*   **Resultado:** O ambiente inteiro é purgado do sistema de forma irreversível.

---
## 📋 Detalhamento de Campos e Regras

### Tabela 1: Elementos da Tela Principal (Cards e Busca)

| Elemento / Campo | Comportamento Implícito & Regras de Negócio |
| :--- | :--- |
| **Barra de Busca** | Permite filtrar rapidamente os clientes exibidos no painel principal através de termos contidos em seus nomes ou categorias. |
| **Card: Última Atividade** | Exibe a data da última interação no ambiente deste cliente. **Gatilho de atualização:** A data é alterada exclusivamente quando há alguma **edição** no ambiente do cliente. Apenas acessar ou visualizar o ambiente não engatilha a atualização desta data. |
| **Card: Gráficos** | Indicador numérico do volume de dados visuais do cliente. **Regra de contagem:** Representa a soma total de componentes de gráficos individuais criados dentro daquele ambiente, e não o número de painéis (dashboards) inteiros. |
| **Card: Menu de Ações (`...`)** | Menu de atalho rápido que disponibiliza as opções de **Editar** as informações cadastrais do cliente ou **Remover** o ambiente. |

### Tabela 2: Modais de "Adicionar" e "Editar" Cliente

| Elemento / Campo                       | Comportamento Implícito & Regras de Negócio                                                                                                                                                                                                                                           |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Nome do cliente**                    | Identificação principal do card. No modo de edição, alterar este nome refletirá imediatamente na exibição do card na tela inicial.                                                                                                                                                    |
| **Categoria**                          | Campo de classificação do cliente (Ex: Tecnologia, Marketing). Funciona estritamente como uma tag visual para facilitar a organização e a busca na tela inicial, não possuindo impacto sistêmico em regras de permissão ou cruzamento de dados.                                       |
| **Logotipo Atual (Apenas Edição)**     | Exibe uma prévia visual da imagem que está atualmente vinculada ao cliente. O usuário pode utilizar o ícone de "**X**" no canto superior da imagem para desvincular o logotipo atual antes de carregar um novo arquivo ou inserir uma nova URL.                                       |
| **Upload de Logotipo (Arquivo local)** | Permite o carregamento de uma nova imagem. **Limitações:** O sistema aceita estritamente os formatos PNG, JPG, WebP e SVG, com tamanho máximo delimitado a 5MB por arquivo. Qualquer formato fora dessa lista resultará em erro no envio.                                             |
| **URL do logotipo (Link Externo)**     | Alternativa ao upload local. **Regra de Estabilidade:** É obrigatório o uso de um link direto para a imagem hospedada em um servidor público. <br><br>⚠️ *Atenção:* Caso o servidor de origem de um link externo caia ou a URL seja alterada, a imagem "quebrará" no sistema Clarion. |
| **Conflito de Imagem (Upload vs URL)** | **Comportamento:** Caso o usuário preencha um link de URL e também faça o upload de um arquivo simultaneamente, o sistema priorizará a imagem oriunda do arquivo local (Upload).                                                                                                      |

---
## ⚠️ Atenção e Impactos Sistêmicos

> **Nota de Impacto - Exclusão de Clientes:** 
> A ação de remover um cliente **não pode ser desfeita**. Conforme alertado pelo sistema, ao confirmar a remoção, ocorre a exclusão permanente de:
> * Todos os usuários vinculados à empresa.
> * Todos os painéis (dashboards) da empresa.
> * Todos os gráficos e seus arquivos de dados em anexo.
> * Todas as permissões de acesso aos relatórios.