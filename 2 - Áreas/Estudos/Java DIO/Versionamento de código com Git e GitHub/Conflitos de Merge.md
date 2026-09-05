Um conflito de Merge acontece quando temos alterações concorrentes

git pull é a junção dos comandos git fetch que baixa as alterações + o comando git merge que mescla as alterações.

O git fetch se faz útil na situação em que supomos que alguém tenha feiot uma alteração no repositório remoto e você ainda não possui ela localmente porém ainda não quer mesclar as alterações do repositório local e remoto, nessa situação você usa o **git fetch origin main** sendo o repositório local entitulado como origin e a branch selecionada para trazer as alterações do commit mais recente sendo a main.

git diff main origin/main mostra as diferenças das branchs locais e remotas sendo no exemplo a main a branch do repositório remoto e a origin/main a do repositório local.

Para trazer as alterações desse repositório remoto para o repositório local é possível utilizar o comando git merge origin/main sendo o origin/main seu repositório local.

Para clonar o repositório de uma branch especifica é possível utilizar o comando git clone URLDOREPOSITORIO --branch teste --single-branch. Sendo teste a branch especifica

ESTUDAR MELHOR O COMANDO GIT STASH