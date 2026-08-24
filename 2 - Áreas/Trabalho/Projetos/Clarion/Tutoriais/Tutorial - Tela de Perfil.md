---
tags:
  - tipo/geral
status: rascunho
---

## 🎯 Objetivo
A tela "Meu Perfil" é o espaço individual e restrito de cada usuário dentro da plataforma. O objetivo deste módulo é centralizar a gestão de credenciais de segurança, identidade visual da conta (avatar) e dados cadastrais básicos, oferecendo autonomia para que o próprio usuário gerencie sua presença e acesso no sistema.

## 🔍 Onde Acessar
Acesse a tela através do cabeçalho (header) no canto superior direito, clicando no botão circular com as iniciais do usuário e selecionando a opção correspondente ao perfil.

## 💻 Detalhamento da tela
A página é organizada em blocos focados em diferentes aspectos da gestão da conta: identidade, dados básicos, segurança e encerramento.

> 📸 ![[Tela de Perfil.png]]

### Foto de Perfil e Informações Pessoais
No lado esquerdo, o usuário pode personalizar seu avatar no sistema. No painel central, gerencia seus dados de contato.

*   **Upload de Imagem (Avatar):** O usuário pode carregar uma foto que substituirá as iniciais no cabeçalho.
    *   *Regras de Arquivo:* O sistema aceita formatos PNG, JPG, WebP, SVG e **GIF**, com tamanho máximo de **5MB**.
*   **Nome Completo:** Campo livre para atualização de como o usuário é identificado nas listagens e cards da plataforma.
*   **E-mail:** Exibe o endereço vinculado à conta. 
    > 🔒 **Regra Sistêmica:** O e-mail funciona como a chave de acesso do usuário e **não pode ser alterado** através desta tela. 

### Segurança (Alteração de Senha)
Área dedicada à atualização da credencial de acesso. Para realizar a troca, o usuário precisa obrigatoriamente validar sua identidade fornecendo a senha atual.

*   **Processo de Troca:** O usuário deve informar a `Senha atual`, criar uma `Nova senha` e repeti-la no campo `Confirmar nova senha`. Os ícones de olho (👁️) permitem visualizar os caracteres digitados para evitar erros de digitação.

> 📸 ![[Tela Perfil - Regras de redefinição de senha 1.png]]

*   **Requisitos de Senha:** O sistema possui um medidor de força de senha em tempo real. Para que a nova senha seja aceita e o botão de salvar seja liberado, ela deve cumprir rigorosamente todas as seguintes exigências de complexidade:
    *   Pelo menos 8 caracteres.
    *   Pelo menos uma letra maiúscula.
    *   Pelo menos uma letra minúscula.
    *   Pelo menos um número.
    *   Pelo menos um caractere especial.
    *   As senhas inseridas nos campos "Nova senha" e "Confirmar nova senha" devem coincidir.

### Zona de Perigo (Exclusão da Conta)
No final da página, o sistema oferece a opção do próprio usuário encerrar sua jornada e remover seu acesso à plataforma de forma autônoma.

*   **Excluir minha conta:** Ação extrema que desativa o login atual. Ao clicar no botão, o sistema exige uma confirmação final.

> 📸 ![[Tela de Perfil - Modal de exclusão de Perfil.png]]

*   **Confirmação:** Um modal simples de alerta ("Tem certeza absoluta?") será exibido. O usuário deve clicar em "Sim, excluir minha conta" para finalizar o processo.

> ⚠️ **Observação Importante sobre a Exclusão:**
> Uma vez que o usuário exclua a própria conta, a ação é **irreversível**. Todos os dados do usuário serão permanentemente removidos dos servidores da plataforma, não havendo possibilidade de recuperação do acesso ou dos dados vinculados à conta original.