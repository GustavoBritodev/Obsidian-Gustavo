Definição: Um objeto é recursivo se for definido em termos de si próprio
Na Programação: Uma função é recursiva quando chama a si mesma durante sua execução.
Recursão Direta: A função chama a si mesma diretamente (A chama A)
Recursão Indireta: A função chama outra que eventualmente a chama de volta (A chama B, que chama A)
* "Pense na Recursividade como um Jutsu de Clone das Sombas. A função principal invoca uma cópia exata de si mesma para resolver uma parte menor do problema"

### Condição de Parada
O Problema: Sem uma condição de parada, a recursão vira um loop infinito.
Caso Base: A parte do problema que pode ser resolvida DIRETAMENTE, sem mais chamadas recursivas.
Sua Função: Garantir que a recursão termine e retorne um valor válido.
Sem Caso Base: Stack Overflow!
* "Todo loop precisa de um 'break'. Na recursividade, esse é o Caso Base. É o nosso 'Dormammu, eu vim barganhar'. Se você esquecer, prepare-se para o temido Stack Overflow!"

### The Stack
Cada chamada: Cria um novo conjunto de variáveis locais na pilha.
LIFO (Last In, First Out): As chamadas são empilhadas e desempilhadas na ordem inversa.
Retorno: Quando a função retorna, seus dados são removidos da pilha.
Ordem Inversa: Os resultados são calculados de baixo para cima na pilha.
* "Pense na Stack como a mochila do seu personagem em um RPG. Cada vez que a função se chama, ela joga um novo 'estado de jogo' na mochila. Só quando o Caso Base é atingido, ela começa a tirar os itens, um por um!"

### Fatorial 
Definição: n! = n * (n -1)!
Caso Base: 0! = 1
Analogia: Calcular o Fatorial de 4 é como quebrar um grande desafio em sub-desafios menores até chegar no mais fácil (0!).
Processo: Cada chamada recursiva reduz o problema até atingir o caso base, então volta multiplicando os resultados.
* "O fatorial é o 'Hello Word!' da recursividade. Para calcular 4!, a função diz: 'Preciso de 4 vezes o fatorial de 3'. É uma corrente de dependências que só para no Caso Base. Depois, a corrente voltam multiplicando os resultados até o final. É o seu Combo Breaker de cálculo."

