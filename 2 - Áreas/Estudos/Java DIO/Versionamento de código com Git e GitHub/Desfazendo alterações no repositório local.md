Ex: Caso tenha dado git init na pasta errada só utilizar o comando rm -rf .git para remover recursivamente e a força o diretório .git

**git restore** para restaurar um arquivo especifico para a versão que ele estava no último commit (cuidado ao utilizar esse comando pois ele remove todas as alterações caso feitas localmente e sem dar o commit). 
Ex: git restore README.md

**git commit --amend -m "texto novo do commit anterior"** para alterar mensagem do último commit (usar caso escrever errado a mensagem do commit).

**git reset (--soft, --mixed, --hard)** para desfazer um commit localmente, após dizer o tipo do reset vc passa a hash do commit para qual vc quer retornar

**git log** mostra o histórico de commits no repositório, já o git status mostra se há arquivos para serem commitados, ou seja, sofreram alterações e ainda não receberam commit dessas novas alterações feitas. **git reflog**  passa essas informações de maneira mais detalhadas.

Após adicionar novos arquivos e usar o comando git add . e quiser remover algum arquivo especifico da area de preparação e para que o mesmo não seja commitado utilizar o comando git reset <"caminho do arquivo">. Outra alternativa é o comando git restore --staged <"caminho do arquivo">.

**Área de preparação** é quando adicionamos arquivos do nosso diretório ou repositório local 
para serem commitados, exemplo disso é quando usamos o comando git add . que adiciona todos os arquivos do seu repositório para a área de preparação para poder fazer o commit.