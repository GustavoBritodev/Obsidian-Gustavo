Branch que em tradução literal significa "ramo" é uma ramificação do seu projeto.

- Uma branch é um ponteiro móvel para um commit no histórico do repositório
- Quando você cria uma nova branch a partir de outra existente, a nova se inicia apontando para o mesmo commit da branch que estava quando foi criada. Ex: a branch main está no seu 4° commit e decido implementar uma nova funcionalidade que não tenho certeza se vai para o projeto final, então crio uma branch "teste" a partir da branch main, logo ela irá se iniciar a partir do 4° commit da branch main que é o commit mais recente da branch main.

As branchs atuam de maneira independente, mantendo o exemplo anterior, suponha que eu faça um novo commit na branch teste, logo a branch teste está apontada para o 5° commit, porém a branch main se mantém apontada para o 4°  commit uma vez que elas atuam de maneiras independentes