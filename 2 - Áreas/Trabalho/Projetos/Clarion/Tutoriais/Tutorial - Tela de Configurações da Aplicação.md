---
tags:
  - tipo/trabalho/projeto/clarion
---
## 🎯 Objetivo
O módulo de "Configurações da Aplicação" centraliza a administração do ambiente (tenant) do cliente. É o local onde administradores gerenciam os dados institucionais, a identidade visual (temas), as chaves de integração de Inteligência Artificial e o controle de acesso de usuários (permissões e convites).

## 🔍 Onde Acessar
Acesse a tela através do menu inferior esquerdo do sistema, clicando em **"Configurações da Aplicação"** (ícone de engrenagem).

## 🗂️ Estrutura das Abas
A tela é dividida em 4 guias principais, permitindo uma navegação focada em cada área administrativa:

### 1. Informações (Dados Cadastrais)
> 📸 ![[Tela de Configurações da Aplicação - Aba Informações.png]]

Nesta aba, ficam armazenados os dados institucionais da conta:
* **Informações Básicas:** Nome da empresa, Categoria e CPF/CNPJ.
* **Logotipo:** Área para upload da identidade visual da empresa. 
    * *Regra de Upload:* Tamanho máximo de **5MB**. Formatos aceitos: PNG, JPG, WebP, SVG e GIF. (Recomendado imagem quadrada 200x200px).
* **Contato e Endereço:** Dados corporativos (E-mail, Telefone) e localização completa integrada (CEP, Logradouro, etc).

### 2. Temas (Identidade Visual)
> 📸 ![[Tela de Configurações da Aplicação - Aba Temas.png]]

Permite a customização (whitelabel) das cores do ambiente do cliente, garantindo aderência ao seu *Brandbook*.
* **Cores Customizáveis:** É possível definir via código Hexadecimal (ou color picker) a **Cor Primária, Cor Secundária e Cor Terciária**.
* **Aplicação das Cores:** Estas configurações afetam o ecossistema do cliente como um todo. Além de alterarem a interface da plataforma, elas passam a compor a **paleta de cores padrão dos gráficos**. Caso um gráfico não tenha cores específicas selecionadas manualmente durante sua criação, o sistema utilizará a paleta definida nesta tela.
* Há também uma função rápida de **"Restaurar Padrão"** para reverter a plataforma às cores originais do Clarion.

### 3. IA (Inteligência Artificial)
> 📸 ![[Tela de Configurações da Aplicação - Aba IA.png]]

O centro de controle do motor cognitivo da plataforma. Subdivide-se em duas configurações vitais:
* **Assistente de IA (Interno):** Campo seguro para inserir a chave da API (API Key) da OpenAI. Esta chave é o que dá "vida" e permite o funcionamento do módulo nativo `[[Assistente de IA]]` dentro do Clarion.
* **Assistente de IA Externo (Integração MCP):** Permite que ferramentas de IA externas do usuário (como Cursor, Claude Desktop, Notebooks) consumam e analisem os dados gráficos do Clarion de forma segura via protocolo MCP. O administrador pode gerar chaves de acesso com validade pré-definida (Ex: 30 dias) e revogá-las a qualquer momento.

### 4. Utilizadores (Gerenciamento de Acesso)
> 📸 ![[Tela de Configurações da Aplicação - Aba Utilizadores - Aba Usuários Ativos.png]]

Painel de controle para gerenciar quem tem acesso ao ambiente e o que podem fazer.
* **Métricas de Topo:** Exibe de forma rápida o total de Usuários Ativos, Administradores, Visualizadores e Convites Pendentes.
* **Aba Usuários Ativos:** Lista todos os membros atuais, exibindo nome, e-mail, data de entrada e nível de acesso. O botão de Ações (`...`) permite editar as permissões ou remover o usuário.
* **Aba Convites Pendentes:** > 📸 ![[Tela de Configurações da Aplicação - Aba Utilizadores - Aba Convites Pendentes.png]]
    Lista e-mails aguardando cadastro. Para adicionar membros, o administrador clica em **"+ Convidar Usuário"**, insere o e-mail e define o papel. O sistema enviará um link seguro para que o próprio convidado configure sua senha e complete o perfil.

#### 🛡️ Matriz de Permissões
O sistema trabalha com dois níveis hierárquicos claros:
* 👑 **Administrador:** Acesso total. Pode gerenciar outros usuários, alterar configurações globais, e criar/editar painéis e gráficos livremente.
* 👁️ **Visualizador:** Acesso restrito apenas para leitura. Não edita gráficos nem acessa configurações.