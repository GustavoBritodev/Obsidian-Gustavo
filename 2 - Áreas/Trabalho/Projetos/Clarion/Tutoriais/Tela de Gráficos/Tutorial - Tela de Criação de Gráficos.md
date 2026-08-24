---
tags:
  - tipo/geral
status: rascunho
---

## 🎯 Objetivo
Antes de criar qualquer visualização, é necessário fornecer a matéria-prima: os dados. O objetivo desta etapa é permitir que o usuário conecte o sistema às suas fontes de informação, sejam elas arquivos locais, nuvem, APIs ou bancos de dados diretos.

## 🔍 Onde Acessar
A partir do [[Tutorial - Tela de Gráficos]], clique no botão **"+ Adicionar Gráfico"** e o sistema exibirá o modal de seleção de origem.

## 💻 Tipos de Conexões Disponíveis

> 📸 ![[Tela de Gráficos - Dropdown de Origem aberto.png]]

O sistema suporta múltiplas formas de ingestão de dados, divididas nas seguintes categorias:

### 1. Upload Local (Arquivos Estáticos)
> 📸![[Tela de Gráficos - Excel - CSV.png]]
Permite o envio direto de arquivos armazenados no computador do usuário.
* **Formatos Suportados:** Excel (`.xlsx`), CSV (`.csv`) e JSON (`.json`).
* **Limite de Tamanho:** Máximo de **300MB** por arquivo. Para bases maiores, recomenda-se o uso de Bancos de Dados ou APIs.
* 💡 **Dica de Ouro:** Ao importar planilhas, garanta que a primeira linha do arquivo contenha os cabeçalhos (nomes) das colunas para facilitar o mapeamento automático.

### 2. Conexões em Nuvem e Arquivos Salvos
> 📸 ![[Tela de Gráficos - Microsoft 365.png]]
* **Microsoft 365 (OneDrive/SharePoint):** Permite conectar à conta Microsoft do usuário para selecionar planilhas hospedadas na nuvem. Os gráficos conectados a essas fontes possuem sincronização inteligente: um botão "Sincronizar" busca a versão mais recente do arquivo automaticamente, sem necessidade de re-upload.
* **Módulo NetFactor:** Funcionalidade nativa para busca direta de extratos financeiros (analíticos e mensais). Automatiza a consolidação de performance, cálculos de CDI e rendimento bruto/líquido sem necessidade de upload manual.
* **Arquivos Salvos:** Repositório interno para reaproveitar bases de dados já conectadas.

### 3. Integrações Avançadas
> 📸 ![[Tela de Gráficos - Banco de Dados.png]]
* **API REST:** Permite consumir dados em tempo real de sistemas terceiros através de requisições HTTPS (suportando métodos GET e POST), com campos para inclusão de Headers e Body.
* **Banco de Dados:** Conexão direta via credenciais (Host, Porta, User, Password). O sistema possui suporte nativo para os bancos **PostgreSQL, MySQL e SQL Server**.