## 🎯 Objetivo
A tela de "Configurações" é o painel de controle global do sistema. O objetivo deste módulo é permitir a personalização da identidade visual da plataforma (White Label), a padronização da formatação de dados numéricos e o gerenciamento do acesso de usuários administrativos.

## 🔍 Onde Acessar
Acesse a tela através do menu superior do sistema, clicando em **"Configurações"**.
> 🔒 **Nota de Acesso:** Esta área é restrita e visível **apenas para usuários com perfil de Administrador**.

## 💻 Detalhamento da tela
A tela é dividida em três abas principais, cada uma responsável por um escopo específico da configuração do sistema: **Branding**, **Formato Numérico** e **Usuários**.

---

### Aba 1: Branding (White Label)
Nesta seção, o usuário personaliza as cores, logotipos e metadados, garantindo que o sistema tenha a identidade visual da sua própria empresa.

> 📸 ![[Tela de Configurações - Aba Branding.png]]

*   **Modo de Exibição:** Permite forçar o tema do sistema para Claro, Escuro, ou seguir automaticamente a preferência do sistema operacional do usuário.
*   **Título do Sistema:** Nome da empresa que será exibido na aba do navegador, em convites por e-mail e na identidade geral. 
    > ⚠️ **Atenção:** Caso este campo seja deixado em branco, o sistema utilizará o nome padrão "ChartGenius".
*   **Logos & Favicon:** Espaço para upload das variações de logotipo (Modo Claro, Modo Escuro, Ícone e Favicon). 
    *   *Regras de Arquivo:* O sistema aceita formatos PNG, JPG, WebP ou SVG, com limite de **5MB**. Recomenda-se o uso de imagens com fundo transparente.
*   **Metadados (SEO e Compartilhamento):** Configuração de `og:title` e `og:description`. Estas informações são cruciais, pois formam o "card" de pré-visualização gerado quando o link do dashboard é compartilhado em redes como WhatsApp ou LinkedIn. Se o título ficar vazio, o sistema herda o "Título do Sistema".
*   **Cores do Tema e da Empresa:** Personalização de cores hexadecimais para a interface (Primária, Secundária, Texto e Hover) em ambos os modos (Claro/Escuro). O sistema possui um atalho inteligente em "Cores da Empresa" que permite extrair a paleta automaticamente a partir da logo salva.

---

### Aba 2: Formato Numérico
Garante a consistência na exibição de moedas, decimais e milhares em toda a plataforma.

> 📸 ![[Tela de Configurações - Aba Formato Numérico.png]]

*   **Padrão Brasileiro vs. Americano:** O usuário pode alternar entre o sistema Brasileiro (ponto para milhar, vírgula para decimal) e o Americano (vírgula para milhar, ponto para decimal).
*   **Impacto Sistêmico:** A alteração neste painel é **global**. O formato selecionado será aplicado imediatamente em todos os dashboards, cards, tooltips, exportações de relatórios e notificações enviadas por e-mail.
*   **Pré-visualização:** Um painel lateral à direita exibe em tempo real como os números padrão, números grandes e percentuais ficarão visualmente após a escolha.

---

### Aba 3: Usuários
Área dedicada ao convite e gestão de membros da equipe administrativa.

> 📸 ![[Tela de Configurações - Aba Usuários.png]]

*   **Convidar Novo Usuário:** Exige o preenchimento de Nome Completo e E-mail. Ao enviar, o usuário recebe um e-mail com as instruções de acesso.
    > ⚠️ **Regra do Convite:** O link enviado por e-mail possui uma validade estrita de **7 dias**. Caso expire, o administrador precisará utilizar a seção de "Convites Pendentes" para reenviar o acesso.
*   **Convites Pendentes e Usuários Ativos:** Listagens separadas que permitem acompanhar quem ainda não aceitou o convite (com opção de revogar ou reenviar) e quem já está operando no sistema, exibindo a data exata de entrada e o perfil de permissão (ex: Administrador).

#### Exclusão de Usuários
A remoção de um usuário master da aplicação deve ser feita com cautela, devido à perda de dados atrelados à conta. Para acessar, clique no menu `...` ao lado de um usuário ativo e selecione a opção de exclusão.

> 📸 ![[Tela de Configurações - Aba Usuários - Excluir usuário.png]]

O sistema exibirá um modal de segurança listando exatamente o que será expurgado junto com o usuário.

> ⚠️ **Observação Importante sobre a Exclusão:**
> Ao excluir um usuário, clientes e dados compartilhados **não** são removidos. Os painéis vinculados a clientes ou definidos como públicos permanecem no sistema e continuam integralmente acessíveis a todos os demais Administradores. 
> 
> No entanto, a exclusão apagará permanentemente todos os ativos **privados** daquela conta, incluindo:
> * Gráficos privados (e suas predefinições pessoais).
> * Painéis (dashboards) estritamente privados.
> * Documentos globais enviados por ele (que não possuam vínculo com clientes).
> * Entradas de cache de integração (ex: Token Microsoft).