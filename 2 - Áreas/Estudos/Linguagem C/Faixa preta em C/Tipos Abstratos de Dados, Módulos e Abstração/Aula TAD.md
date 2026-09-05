Módulos:
* cabecalho.h: Define a interface -  A vitrine dos módulos
* implementacao.c: o segredo de como faz - escondido do resto do código
* prototipos: o que o módulo promete fazer - sem revelar segredos
O cabeçalho é uma "vitrine" que permite que outros módulos usem suas funções sem conhecer os detalhes internos.

Conceito de TAD
TAD = Tipo + Operações
* Um TAD define um Tipo de Dado e o conjunto de operações que podem ser realizadas com ele
Abstração
* Foco no **O Quê** (Comportamento)  -Não no Como (Implementação)
Encapsulamento
* Esconder os detalhes internos - Expor apenas a Interace Pública
Quando você escolhe a classe 'Mago' em um RPG, você sabe o que ele faz (lançar feitiços, pouca defesa). Você não precisa saber como o código do feitiço funciona internamente. Isso é TAD!