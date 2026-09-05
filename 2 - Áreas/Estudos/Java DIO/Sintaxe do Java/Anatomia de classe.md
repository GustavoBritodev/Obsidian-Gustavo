- Estrutura inicial
- Padrão de nomenclatura
- Declarando variáveis e métodos
- Identação
- Organizando arquivos
- Java Beans

As classes por padrão precisam estar dentro da pasta src.
### Padrão de nomenclatura

Por padrão a nomenclatura de classes começa com a primeira letra maiúscula e as demais palavras maiúsculas também, parecido com camel case.

Por padrão de nomenclatura todo arquivo .java deve começar com letra maiúscula.

Dentro do código o nome da classe deve ter o mesmo nome do arquivo. Exemplo:

```
// arquivo CalculadoraCientifica.java

public class CalculadoraCientifica {

}
```

Na declaração de variáveis ao adicionar a expressão final antes da declaração você torna imutável essa variável. Exemplo: 

```
final String BR = "Brasil";

BR = "Brazuca" // Nesse caso essa linha retornaria erro
```

Na declaração de variáveis os únicos símbolos permitidos são _ ou $, uma variável não pode começar com um número, uma variável não pode ter espaço no seu nome e uma variável não pode ter o nome de palavras reservadas da linguagem.