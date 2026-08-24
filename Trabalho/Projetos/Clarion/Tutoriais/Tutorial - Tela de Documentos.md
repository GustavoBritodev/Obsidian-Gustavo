## 🎯 Objetivo
A tela de "Documentos Globais" funciona como um repositório centralizado do sistema. O objetivo deste espaço é armazenar e disponibilizar arquivos de caráter **informativo** (como manuais de uso, termos de serviço, políticas ou cartilhas) que precisam estar acessíveis para **todos os clientes** cadastrados na plataforma. Os arquivos aqui depositados não são consumidos como base de dados para os dashboards, servindo exclusivamente para download e consulta.

## 🔍 Onde Acessar
Acesse a tela através do menu superior do sistema, clicando em **"Documentos"**.

## 💻 Detalhamento da tela
Ao acessar a página, o usuário visualiza a lista completa de arquivos globais disponíveis no sistema. Caso seja o primeiro acesso e não existam arquivos, a tela exibirá o estado vazio com um atalho central para "Adicionar Documento".

> 📸 ![[Tela de Documentos - Com Upload.png]]

Na tela principal de documentos, as seguintes informações e recursos são apresentados:

*   **Barra de Busca:** Permite localizar documentos específicos digitando partes do nome do arquivo.
*   **Tabela de Arquivos:** Exibe os metadados fundamentais de cada documento, incluindo o Nome do Arquivo, uma breve Descrição, o Tamanho (em KB/MB), quem foi o usuário responsável pelo envio (Enviado por) e a Data exata do upload.
*   **Tag "Global":** Localizada ao lado do nome do arquivo, esta etiqueta serve para reforçar visualmente que a visibilidade daquele documento é exclusivamente global, ou seja, todos os ambientes de clientes têm acesso a ele.
*   **Ação de Download:** Representada pelo ícone de seta para baixo. Qualquer usuário com acesso ao painel pode baixar os arquivos informativos para sua máquina local.

### Adicionando um Novo Documento (Upload)
Para enviar um novo arquivo para o repositório, clique no botão **"Upload"** (localizado no canto superior direito) ou no botão central **"Adicionar Documento"** (caso a lista esteja vazia).

> 📸 ![[Tela de Documentos - Modal de Upload.png]]

O modal de upload apresentará os seguintes campos:

*   **Arquivo:** Área para seleção do documento na sua máquina. O sistema aceita exclusivamente arquivos nas extensões **.pdf, .xlsx, .docx e .csv**, respeitando o limite máximo de **50MB** por upload.
*   **Descrição (opcional):** Campo de texto livre para adicionar um breve contexto sobre o conteúdo do arquivo, facilitando o entendimento dos clientes antes de realizarem o download.

> ⚠️ **Atenção:** 
> O impacto do upload é imediato. Assim que o botão **"Enviar"** é clicado, o documento passa a ficar visível e disponível para download na seção de documentos de **todos** os clientes do sistema.

### Removendo um Documento
A ação de deletar um documento global remove o arquivo do repositório de todos os clientes simultaneamente. Por se tratar de uma ação com impacto sistêmico, **somente usuários com perfil de Administrador** possuem permissão para visualizar o ícone de lixeira e executar a exclusão.

> 📸 ![[Tela de Documentos - Exclusão de documento.png]]

Para excluir, o administrador deve clicar no ícone de **lixeira** (na coluna de Ações) e confirmar a intenção no modal de segurança.

> ⚠️ **Observação Importante**
> A ação de exclusão não pode ser desfeita. Ao confirmar, o documento será permanentemente apagado da base de dados do Clarion e o link de download deixará de funcionar imediatamente para todos os usuários e clientes.