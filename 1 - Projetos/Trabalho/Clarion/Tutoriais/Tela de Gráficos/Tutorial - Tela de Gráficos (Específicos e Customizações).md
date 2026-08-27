---
tags:
  - tipo/trabalho/projeto/clarion
---
## 🎯 Objetivo
Enquanto a maioria dos gráficos segue o padrão documentado em [[Tutorial - Tela de Configuração e Edição de Gráficos]], alguns tipos visuais possuem abas e regras exclusivas para atender propósitos analíticos avançados. Este documento cataloga essas exceções e regras específicas.

## 💻 Particularidades por Gráfico

### 1. Gráfico de Número Grande (KPI)
> 📸 ![[Tela de Gráficos - Editar Gráfico Número Grande - Aba Dados.png]]
Focado em simplicidade para exibir um indicador único.
* **Regra de Abas:** Perde as abas "Ajustes" e "Visualização". 
* **Funcionamento:** Exige apenas uma coluna e sua agregação. Além da "Soma", utilize a agregação "Contagem Distinta" para descobrir, por exemplo, o número exato de clientes únicos em um período.

### 2. Gráfico Mapa de Calor (Geográfico)
> 📸 ![[Tela de Gráficos - Editar Gráfico Mapa de Calor - Aba Dados.png]]
Utilizado para densidade territorial.
* **Regra de Eixos:** Exige uma "Coluna de Localização" e o respectivo "Tipo de Localização". É possível usar **UF** (para visões macro estaduais) ou **CEP** (para identificar demanda granular em bairros/ruas).
* **Ação Obrigatória:** Clique em **"Montar Mapa"** para renderizar as localizações.
* **Customização Visual:** Na aba Aparência, ajuste o controle de **Raio e Intensidade** para controlar o tamanho da "mancha" de calor e limpar ruídos visuais.

### 3. Análise ABC (Curva de Pareto)
> 📸 ![[Tela de Gráficos - Editar Gráfico Curva ABC - Aba Dados.png]]
Focado em classificar itens por relevância (Regra 80/20).
* **Aba Exclusiva:** A aba "Dados" torna-se "Análise ABC". O modo percentual tradicional distribui os itens nos clássicos limites 80/15/5 (Categorias A, B e C, respectivamente).
* **Linha de Pareto:** Na aba Visualização, ative esta linha sobreposta para visualizar a curva de valor acumulado e identificar o exato ponto de inflexão da operação.

### 4. Gráfico de Pizza (e Rosca/Donut)
> 📸 ![[Tela de Gráficos - Editar Gráfico Pizza - Aba Aparência.png]]
* **Dica Oculta de UX:** O sistema não possui um gráfico de "Rosca" separado. Para transformar a sua Pizza em uma Rosca, basta acessar a aba **Aparência** e aumentar o controle deslizante **"Tamanho do centro (%)"**.

### 5. Tabelas e Tabelas Dinâmicas (Pivot)
> 📸 ![[Tela de Gráficos - Editar Gráfico Tabela Dinâmica - Aba Dados.png]]
* **Tabela Simples:** Seleção direta (e restrição) das colunas essenciais para exibição tabular sem poluir o painel.
* **Tabela Dinâmica:** Opera sob lógica de _Pivot Table_. Arraste campos entre Linhas, Colunas e Métricas. Utilize a opção "Tabela Hierárquica" para agrupar registros automaticamente por mês/ano, gerando subtotais organizados.