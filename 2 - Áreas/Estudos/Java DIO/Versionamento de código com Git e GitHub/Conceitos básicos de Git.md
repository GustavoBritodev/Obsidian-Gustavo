#### git config
- --global (é referente as informações no usuário)
- --system (é referente as configurações do sistema como um todo)
- --local (é referente a localização de um repositório especifico que você se encontra)

Para mudar branch padrão: git config --global init.defaultBranch main

No terminal do git e na pasta que eu abrir o terminal se eu der o git clone + url do repositório, o repositório, irá aparecer na pasta onde abri o terminal.

Caso seja um repositório privado ele vai pedir o uso de token

para salvar o token e não pedir mais para clonar o repositório e não ter que ficar pegando o token toda hora é possível usar o comando git config credential.helper store