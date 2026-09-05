
Atribuição e Referência
- ==As atribuições em Java são por cópia de valor sempre;==
- Com tipo primitivo, copiamos o valor em memória;
- Com objetos copiamos o valor da referência em memória, sem duplicar o objeto.

Anotação do entendimento:
Quando atribuimos (usamos o operador =) qualquer coisa no Java, no funcionamento a atribuição sempre será feita por cópia do valor. O que isso significa? Quando usamos tipos primitivos (int, String, float, double e etc) e atribuimos valor de um à outro essa atribuição será pelo valor em memória previamente atribuido a aquela primeira variável. Por exemplo intA = 1; intB = intA;
Nesse caso, mesmo que mudemos o valor do intA posteriormente dando a ele o valor de 2, por exemplo, o intB caso não o alteremos ele será sempre igual a 1 que era o valor de intA quando ele foi atribuido ao valor de intA, ou seja, com tipos primitivos a atribuição será sempre copiando o valor indexado a memória. Diferentemente de objetos, onde quando trabalhamos com dois objetos diferentes e atribuimos por exemplo, objA = 1; objB = objA, mesmo que alteremos o valor do objA o objB muda dinamicamente, porque ambos são a mesma coisa. Como assim a mesma coisa? Com objetos copiamos o valor da referência em memória, sem duplicar o objeto, ou seja, nos tipos primitivos ao atribuir a variavelA à variavelB o Java atribui o valor em memória previamente atribuido a variavelA, agora quando se trata de objetos, ao atribuir o objA ao objB você basicamente copia o endereço em memória onde o valor do objA está guardado, assim igualando o local onde eles acessam seu valor, logo objA e objB são a mesma coisa.

Exemplo de código:
```
package com.projeto.atribuicaoreferencia;  
  
public class Main {  
    public static void main(String[] args) {  
        int intA = 1;  
        int intB = intA;  
  
        System.out.println("Saída tipos primitivos: ");  
        System.out.println("intA=" + intA + " intB=" + intB);  
  
        intA = 2;  
  
        System.out.println("intA=" + intA + " intB=" + intB);  
  
        MeuObj objA = new MeuObj(1);  
  
        MeuObj objB = objA;  
  
        System.out.println("\nSaída objeto: ");  
        System.out.println("objA=" + objA + " objB=" + objB);  
  
        objA.setNum(2);  
  
        System.out.println("objA=" + objA + " objB=" + objB);  
    }  
}
```

Código do objeto:
```
package com.projeto.atribuicaoreferencia;  
  
public class MeuObj {  
    Integer num;  
  
    public MeuObj(Integer num) {  
        this.num = num;  
    }  
  
    public void setNum(Integer num) {  
        this.num = num;  
    }  
  
    @Override  
    public String toString() {  
        return this.num.toString();  
    }  
}
```

Exemplo de saída:
```
intA=1 intB=1
intA=2 intB=1
objA=1 objB=1
objA=2 objB=2
```

Post no LinkedIn:

🎯 Entenda Atribuição e Referência no Java

No Java, ao realizar atribuições (usando o operador =), sempre estamos copiando o valor. Mas isso funciona de maneiras diferentes para tipos primitivos e objetos. Vamos entender! 👇

🔹 Tipos Primitivos
Quando trabalhamos com tipos primitivos (ex.: int, float, double), ao atribuir o valor de uma variável a outra, ocorre a cópia do valor em memória.

Por exemplo:

int intA = 1;  
int intB = intA;  

A variável intB recebe uma cópia do valor de intA. Posteriores alterações no valor de intA não afetam intB, pois os dois armazenam valores independentes em áreas distintas da memória.

Essa característica é consistente para todos os tipos primitivos no Java (byte, short, int, long, float, double, char, boolean).

🔹 Objetos
Com objetos, o comportamento é diferente. Aqui, copiamos a referência em memória, e não o valor.

Exemplo:

MeuObj objA = new MeuObj(1);  
MeuObj objB = objA;  

Nesse caso, se alterarmos o valor em objA, objB refletirá a mesma mudança. Isso acontece porque ambos compartilham o mesmo endereço na memória, ou seja, apontam para o mesmo objeto.

💡 Resumo Prático

Tipos Primitivos: Copiam o valor armazenado em memória (independentes).
Objetos: Copiam o endereço de memória (compartilham o mesmo valor).

Compreender esse conceito, por mais básico que seja nos ajuda a entender o comportamento do seu código, assim ajudando a evitar possíveis bugs. 

Compreender essa diferença é essencial para evitar bugs e entender o comportamento do seu código. 🚀

Abaixo temos o exemplo ilustrado do código fonte principal e a saída: 👇
