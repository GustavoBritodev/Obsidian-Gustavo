## 🎯 Objetivo
Detalhar o funcionamento do painel de construção visual. Após conectar os dados (veja [[Tutorial - Tela de Criação de Gráficos]]), o usuário acessa o motor de edição, padronizado em 5 abas principais para modelar a informação.

## 💻 O Painel de Controle Superior
> 📸 ![[Tela de Gráficos - Editar Gráfico Barras - Aba Dados.png]]

No cabeçalho do construtor, além de nomear o gráfico, o usuário tem acesso a duas funções vitais:
* **Visibilidade (Público/Restrito):** Define as permissões de acesso ao visual.
* **Botão "Atualizar Dados":** Força a releitura da fonte original (útil para dados via API, Banco ou Microsoft 365).

## 🗂️ As 5 Abas de Edição

Independentemente da maioria dos gráficos escolhidos (Barras, Linhas, Área), a lógica de construção segue o fluxo destas 5 abas:

### 1. Dados (A Estrutura)
Onde ocorre o mapeamento primário. O usuário seleciona os campos da sua base para compor o **Eixo X** (Geralmente dimensões, datas, categorias) e o **Eixo Y** (Métricas, valores a serem quantificados). É possível adicionar múltiplas séries no Eixo Y para gráficos comparativos.

### 2. Filtros (O Refinamento)
> 📸 ![[Tela de Gráficos - Editar Gráfico Barras - Aba Filtros.png]]
Permite criar condicionais de exibição. Ex: "Mostrar apenas Vendas onde Status = Concluído". 
💡 **Dica de Data:** O filtro flexível para datas aceita formatos diretos como `DD/MM/YYYY` ou `YYYY-MM-DD`, sem necessidade de inputar horários.

### 3. Ajustes (A Matemática)
> 📸 ![[Tela de Gráficos - Editar Gráfico Barras - Aba Ajustes.png]]
Área para operações lógicas.
* **Agrupar dados repetidos:** Opção essencial para consolidar linhas com a mesma categoria no Eixo X (Ex: somar todas as 10 vendas do "Produto A" em uma única barra).
* **Agregação:** Como os dados do Eixo Y devem ser tratados (Soma, Média, Contagem, Mínimo, Máximo).
* **Periodicidade Temporal:** Se o Eixo X utilizar datas, o sistema permite agrupar a granularidade automaticamente por Dia, Mês/Ano, Trimestre ou Ano.
* **Ordenação e Limites:** Permite ordenar pelo nome (X) ou valor (Y). 💡 **Dica para Rankings:** Para exibir um Top 10, escolha "Ordenar por Valor (Y)", Direção "Decrescente (Z-A)" e defina o Limite de Itens para 10.

### 4. Aparência (O Visual)
> 📸 ![[Tela de Gráficos - Editar Gráfico Barras - Aba Aparência.png]]

- **Estilo de Cores:** Utilize esquemas pré-definidos de paletas profissionais (Colorido, Monocromático, Pastel) ou defina cores específicas por série. Em gráficos de pizza, há um botão "Gerar Cores" para colorir fatias automaticamente.
- **Formatação Numérica:** Inclusão de máscaras de valor (Sufixos como `%` e Prefixos como `R$`), além da escala de exibição para abreviar grandes números (Ex: "1M").

### 5. Visualização (A Interatividade)
Controla o comportamento e a legibilidade do gráfico.
* Muitos Itens (Top N + Outros): Para gráficos poluídos, ative a opção "Top N + Agrupar Outros" para focar nos itens principais e consolidar o resto em uma fatia "Outros".
* Nomes Longos no Eixo X: Se os rótulos estiverem apertados ou cortados, você pode:
	1. Aumentar a "Largura Mínima da Barra" (habilitando scroll horizontal).
	2. Ativar a "Barra de Navegação (Brush)" no rodapé do gráfico.
	3. Ajustar o "Ângulo do Texto" para 45º ou 90º.