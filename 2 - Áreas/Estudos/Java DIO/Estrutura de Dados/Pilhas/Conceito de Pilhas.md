O último a ser colocado é sempre o primeiro a sair

**Regras de uma pilha:**
- LIFO (Last in First Out)
- O último elemento que entra é o primeiro a sair

**Anotações:** 
Ao trabalhar com pilhas não é possível acessar um elemento no meio da pilha por exemplo, trabalharemos sempre com o último elemento inserido na pilha. Esse fato ocorre em via de regra para manter a estrutura de dados como uma pilha

- O de cima aponta para o debaixo 

No topo da pilha temos uma referencia de nó que aponta para o último nó que foi adicionado e na base da pilha a referencia de nó do ultimo nó aponta para nulo

O método top identifica o valor do topo da pilha, ou seja o ultimo valor a ser adicionado e retorna o valor do mesmo mas sem manipula-lo ou altera-lo.

Exemplo de código do método Top:
`No meuNo = pilha.top();`

`No meuNo = (referencia do nó do topo da pilha, retornando o nó mas sem alterar a estrutura da pilha);`

`int numero = meuNo.getInt();`

`int numero = (dado armazenado no Nó);`

-------------------------------------------------------------------------

Exemplo de código do método Pop:
`No meuNo = pilha.pop();

`No meuNo = (referencia do nó no topo da pilha, retornando o conteúdo do nó e o excluindo do topo da pilha);`

`int numero = meuNo.getInt();`

`int numero = (dado armazenado no nó`

A principal diferença do método top e pop é que o pop exclui o elemento do topo da pilha, fazendo assim com que a referência do nó do topo passe para o debaixo do que foi manipulado pelo método pop.

--------------------------------------------------------------------------

O método Push basicamente cria um novo nó e o adiciona pro topo da pilha e altera a referência de topo para apontar para si e pega o antigo valor da referencia de topo para apontar para o nó que ficará abaixo.

--------------------------------------------------------------------------

O método isEmpty verifica se a referência de topo aponta para algum nó, verificando assim se a estrutura de dados existe. Exemplo de código abaixo:

`public boolean isEmpty(){`
	`if(refNo == null){`
		`return true;`
	`} else{`
		`return false;`
	`}`
	
`}`


