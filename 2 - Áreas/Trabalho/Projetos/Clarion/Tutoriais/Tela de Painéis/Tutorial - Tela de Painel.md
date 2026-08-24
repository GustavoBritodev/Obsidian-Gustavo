---
tags:
  - tipo/geral
status: rascunho
---

## 🎯 Objetivo
O módulo de "Painéis" é a vitrine final do sistema. Enquanto o módulo de Gráficos atua como a fábrica de componentes, os Painéis são o produto finalizado. O objetivo desta tela é permitir que o usuário consolide diferentes gráficos em uma única página interativa (Dashboard), criando uma visão gerencial ampla que facilita a análise de métricas e a tomada de decisões.

## 🔍 Onde Acessar
Acesse a tela através do menu superior do sistema, clicando em **"Painéis"**.

## 💻 Detalhamento da tela
Ao acessar o módulo, o usuário visualiza a listagem de todos os dashboards construídos e disponíveis no seu ambiente de trabalho.

> 📸 ![[Tela de Painel - Com Painéis.png]]

* **Estado Vazio:** Caso seja o primeiro acesso (ou não haja painéis permitidos para o usuário), a tela exibirá uma mensagem amigável de estado vazio com um atalho central para "Criar Painel".
* **Barra de Busca:** Permite filtrar e localizar dashboards específicos pelo nome.
* **Listagem (Cards):** Cada painel é representado por um card contendo seu Título, Nível de Visibilidade (Público ou Restrito), Data da última modificação e o Nome do Autor.
* **Ações:** O botão de opções (`...`) no canto superior do card permite gerenciar o painel (Editar ou Excluir).

---

## ⚙️ Fluxos de Uso

### 1. Construindo um Painel (Drag & Drop)
Para montar um novo dashboard, clique no botão **"+ Criar Painel"** localizado no canto superior direito.

> 📸 ![[Tela de Painel - Criação de Painéis - Com Gráficos.png]]

A interface de criação atua como uma prancheta de desenho, dividida em duas áreas fundamentais:
* **Barra Lateral (Biblioteca):** Lista todos os gráficos previamente construídos no módulo "Gráficos". 
* **Área de Trabalho (Canvas):** Um grid (grade) maleável onde o dashboard ganha forma.
* **Como montar:** O construtor utiliza a tecnologia *Drag and Drop* (Arraste e Solte). Basta clicar no gráfico desejado na barra lateral, arrastá-lo para a área de trabalho e soltar. **Não há limite máximo de gráficos** que podem ser inseridos em um único painel.
* **Customização do Layout:** Uma vez no canvas, o usuário tem total liberdade espacial. É possível arrastar os gráficos pelas bordas para redimensioná-los (esticar ou encolher) e reposicioná-los para dar destaque às métricas mais importantes.
* **Sincronização em Tempo Real:** O painel funciona como um organizador e visualizador. Isso significa que, se o usuário editar a aparência, os filtros ou os dados de um gráfico lá no módulo original de "Gráficos", **essa alteração refletirá automaticamente** e em tempo real no painel.

### 2. Salvando e Permissões
Após organizar o layout ideal, o usuário deve consolidar o trabalho clicando no botão **"Salvar"**.

> 📸 ![[Tela de Painel - Salvar Painel.png]]

O modal de salvamento exige a definição de duas propriedades:
* **Título do Painel:** Nome amigável que identificará o dashboard.
* **Visibilidade:** Define as regras de acesso à visualização.
    * **Público:** O dashboard fica disponível para todos os usuários com acesso àquele cliente/ambiente.
    * **Restrito:** O dashboard é privado e visível apenas para o seu criador.

### 3. Visualização e Modo Apresentação
A tela de visualização é o modo de consumo do dashboard. Nela, a barra lateral de edição some, entregando uma interface limpa e focada exclusivamente na leitura dos dados.

> 📸 ![[Tela de Painel - Visualizar Painel.png]]

No cabeçalho deste modo de leitura, o usuário possui atalhos de interação:
* **Botão "Atualizar":** Força o sistema a buscar os dados mais recentes das fontes (Bancos, APIs, Planilhas) e atualizar todos os gráficos do painel simultaneamente.
* **Botão "Tela Cheia":** > 📸 ![[Tela de Painel - Tela Cheia.png]]
    Expande o dashboard para ocupar 100% da resolução do monitor, ocultando a barra de navegação do navegador e os menus superiores do sistema. É a opção ideal para apresentações de resultados em reuniões ou para exibição contínua em monitores de operação/TVs. Para sair deste modo, basta clicar no botão de restaurar ou pressionar a tecla `ESC`.