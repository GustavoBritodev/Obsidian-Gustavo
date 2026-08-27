---
tags:
  - tipo/trabalho/projeto/clarion
---
## 🎯 Objetivo
A tela de "Dashboard" é o ambiente principal de consumo de dados da plataforma. Enquanto o módulo de "Painéis" foca na construção e layout (arrastar e soltar), o "Dashboard" é projetado para a exploração analítica. É aqui que os gestores e usuários finais aplicam filtros dinâmicos, cruzam períodos, exportam relatórios e extraem inteligência do que foi construído.

## 🔍 Onde Acessar
Acesse a tela através do menu lateral esquerdo do sistema, clicando na primeira opção: **"Dashboard"** (ícone de casa).

## 💻 Detalhamento da tela
Ao acessar o módulo, o sistema carregará o painel principal. A interface é dividida entre uma barra superior de ações, um painel lateral de filtros (que pode ser recolhido) e a área de exibição dos gráficos.

> 📸 ![[Tela de Dashboard - Com Painel Cadastrado.png]]

*   **Estado Vazio:** > 📸 ![[Tela de Dashboard - Sem Painel Cadastrado (Sem Gráficos).png]]
    Se não houver nenhum painel criado ou liberado para o usuário, a tela exibirá a mensagem "Nenhum painel cadastrado", orientando o usuário a acessar o menu de Painéis para criar o primeiro.
*   **Seleção de Painel:** > 📸 ![[Tela de Dashboard - Dropdown de Painel Expandido.png]]
    No canto superior esquerdo da área de exibição, há um menu suspenso (`Painel:`) que permite alternar rapidamente entre os diferentes dashboards aos quais o usuário tem acesso (ex: Dashboard Financeiro, Dashboard Portuário), sem precisar voltar à tela de listagem.

---
## ⚙️ Ações e Ferramentas (Barra Superior)

No cabeçalho do Dashboard, o usuário possui ferramentas vitais para a manipulação da visualização e extração dos dados:

*   **Editar:** Atalho rápido que redireciona o usuário para o modo de construção/layout daquele painel específico.
*   **Refresh:** Força a atualização dos gráficos, buscando os dados mais recentes nas fontes conectadas.
*   **Data Base (Sincronização Temporal):** Recurso avançado para painéis que utilizam múltiplas fontes de dados (ex: planilhas diferentes). Ao clicar, abre-se um modal onde o usuário deve selecionar qual é a **coluna de data de referência** para cada fonte. Isso garante que, ao aplicar um filtro de período global (ex: "Ano de 2026"), todos os gráficos obedeçam à regra, mesmo vindo de tabelas distintas.
*   **Tela Cheia:** Oculta os menus laterais e superiores para visualização em monitores ou apresentações.

---
## 📥 Gerador de Relatórios (Exportação)

A função de "Exportar", localizada no topo superior direito, não apenas baixa dados brutos, mas atua como um assistente de montagem de *Status Reports*.

### 1. Exportação em Excel
> 📸 ![[Tela de Dashboard - Exportar Excel - Painel Completo.png]]

Ideal para manipulação de dados brutos. O sistema oferece duas modalidades:
*   **Painel Completo:** O sistema gera um **único arquivo Excel**. Cada gráfico (widget) presente no dashboard será convertido automaticamente em uma **aba (planilha) separada** dentro deste mesmo arquivo.
*   **Por Seção:** Permite que o usuário selecione manualmente apenas os gráficos específicos que deseja exportar para o arquivo.

### 2. Exportação em PDF (Status Report)
> 📸 ![[Tela de Dashboard - Exportar PDF - Seleção de Seção Expandido.png]]

Esta opção abre um assistente de 3 passos para criar apresentações formatadas:
*   **Passo 1 (Painéis):** Selecione um ou múltiplos painéis que farão parte do relatório.
*   **Passo 2 (Seções):** Personalize a estrutura. O usuário pode criar "Seções" nomeadas, selecionar os gráficos que compõem cada seção, definir a orientação da página (Retrato ou Paisagem) e adicionar **Comentários** (textos analíticos que acompanharão os gráficos).
*   **Passo 3 (Exportação):** Finalização e distribuição.
    *   **Ajustar à Página Única:** Opção para comprimir o visual em uma só folha.
    *   **Pré-visualizar:** Abre o PDF gerado em tela cheia para conferência final.
    *   **Distribuição Inteligente:** Além de baixar o arquivo, o sistema permite enviá-lo diretamente pela plataforma.
        *   **E-mail:** Permite digitar destinatários, assunto e corpo do e-mail.
        *   **WhatsApp:** Permite inserir um número com DDD. O PDF será hospedado na nuvem e um link de acesso será incluído automaticamente na mensagem do WhatsApp.

---
## 🗂️ Painel de Filtros (Lateral Esquerda)

O grande diferencial do ambiente de consumo é a barra lateral de filtros, que permite fatiar os dados em tempo real sem alterar a estrutura original do painel.

> 📸 ![[Tela de Dashboard - Com Painel Cadastrado (Filtros Inativos).png]]

### 1. Filtros Personalizados
Permite criar lógicas condicionais dinâmicas na hora da análise. O usuário seleciona a Coluna desejada, a Operação (ex: "Igual a", "Contém", "Maior que") e digita o valor. Ao clicar em **"Aplicar Filtro"**, todos os gráficos da tela que compartilharem essa estrutura de dados serão recalculados.

### 2. Agrupamento de Dados
Permite agrupar informações na visualização temporariamente, escolhendo uma coluna específica de agrupamento.

### 3. Predefinições de Filtros (Filtros Salvos)
> 📸 ![[Tela de Dashboard - Com Painel Cadastrado ( Predefinições de Filtros).png]]
Para evitar que o usuário precise recriar os mesmos filtros complexos todos os dias (ex: "Vendas do Mês Atual + Estado de SP + Categoria A"), é possível salvar o conjunto de regras.
*   O usuário seleciona quais fontes de dados farão parte da predefinição, dá um nome a ela e clica em **"+ Salvar Nova"**.
*   **Visibilidade e Permissões:** 
	* **Restrita:** Apenas o criador vê e pode usar a predefinição. 
	* **Pública:** O filtro fica disponível para todos os usuários do cliente. No entanto, para proteger a estrutura original, **outros usuários poderão apenas aplicar** a predefinição em suas visões, não tendo permissão para editá-la ou excluí-la.