Comando para clonar repositório de uma branch especifica:
git clone (URL) --branch (nome-da-branch) --single-branch

comando git pull para trazer a versão mais recente do repositório remoto  para um repositório local que já esteja conectado com o repositório remoto.

comando **git checkout -b teste**. Nesse caso o comando irá trocar da branch que você está para essa nova branch que você está criando que no caso do exemplo recebe o nome de teste.

Supondo que exista uma branch chamada main o comando git checkout main irá posiciona-lo na branch main caso você esteja na teste por exemplo.

**git merge teste** mescla uma branch para a branch principal, no caso do exemplo ele une a branch teste junto à branch main.

**git branch -v** lista o último commit de cada branch.

**git branch** lista as branchs que você tem no seu repositório.

Para deletar uma branch que não está mais em uso é possível usar o comando git branch -d teste. Sendo o teste o nome da branch que deseja excluir.