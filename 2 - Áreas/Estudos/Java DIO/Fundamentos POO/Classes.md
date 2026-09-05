Em Java, uma **classe** é a estrutura fundamental usada para definir os objetos e seu comportamento. Ela serve como um "molde" ou "projeto" para criar objetos, agrupando atributos (dados) e métodos (comportamentos) relacionados a um determinado conceito. A classe é um dos pilares da programação orientada a objetos (POO), permitindo a modularização e a reutilização de código.

### Estrutura de uma Classe

Uma classe em Java geralmente contém:

- **Atributos** (também chamados de variáveis de instância ou campos): que definem as características dos objetos criados pela classe.
- **Métodos**: que definem as ações ou comportamentos que os objetos dessa classe podem realizar.
- **Construtores**: usados para inicializar objetos.
- **Modificadores de acesso** (como `public`, `private`, `protected`), que controlam a visibilidade da classe, seus atributos e métodos.

#### Exemplo básico de uma classe:
```
public class Pessoa {
    // Atributos (variáveis de instância)
    private String nome;
    private int idade;

    // Construtor
    public Pessoa(String nome, int idade) {
        this.nome = nome;
        this.idade = idade;
    }

    // Método getter para obter o nome
    public String getNome() {
        return nome;
    }

    // Método setter para modificar o nome
    public void setNome(String nome) {
        this.nome = nome;
    }

    // Método para exibir uma saudação
    public void saudacao() {
        System.out.println("Olá, meu nome é " + nome + " e tenho " + idade + " anos.");
    }
}
```

Neste exemplo, temos uma classe `Pessoa` que define dois atributos (`nome` e `idade`), um construtor para inicializar esses valores, e métodos (getters e setters) para acessar e modificar os atributos. Além disso, há um método `saudacao()` que exibe uma mensagem usando esses atributos.

### Criando Objetos

Uma **classe** define a estrutura, mas os **objetos** são as instâncias dessa classe. Quando criamos um objeto, estamos criando uma instância de uma classe específica. Cada objeto possui sua própria cópia dos atributos definidos na classe, mas compartilha os métodos da classe.

#### Exemplo de criação de um objeto:
```
public class Main {
    public static void main(String[] args) {
        // Criando um objeto da classe Pessoa
        Pessoa pessoa1 = new Pessoa("Gustavo", 18);

        // Chamando um método no objeto
        pessoa1.saudacao();
        
        // Modificando o nome usando o setter
        pessoa1.setNome("Gustavo Brito");
        pessoa1.saudacao();
    }
}
```

Aqui, criamos um objeto `pessoa1` da classe `Pessoa` e usamos o método `saudacao()` para exibir uma mensagem. Em seguida, modificamos o nome usando o método `setNome()` e chamamos o método novamente.

### Modificadores de Acesso

Os modificadores de acesso determinam o nível de visibilidade de uma classe, seus atributos e métodos. Os principais modificadores são:

- **`public`**: Torna a classe, método ou atributo acessível de qualquer lugar.
- **`private`**: Torna o atributo ou método acessível apenas dentro da própria classe.
- **`protected`**: Permite que o método ou atributo seja acessado dentro da própria classe, classes do mesmo pacote e subclasses.
- **sem modificador** (padrão): Torna o elemento acessível apenas dentro do mesmo pacote.

#### Exemplo de visibilidade:
```
public class Carro {
    public String modelo;  // Visível de qualquer lugar
    private String placa;  // Visível apenas dentro desta classe
    protected int ano;     // Visível em classes do mesmo pacote ou subclasses
}
```

### Construtores

Os **construtores** são usados para inicializar os atributos de um objeto no momento da criação. Eles têm o mesmo nome da classe e não têm um tipo de retorno (nem `void`). Se nenhum construtor for explicitamente definido, o Java fornece um construtor padrão sem parâmetros.

#### Exemplo de um construtor com parâmetros:
```
public class Carro {
    private String modelo;
    private int ano;

    // Construtor
    public Carro(String modelo, int ano) {
        this.modelo = modelo;
        this.ano = ano;
    }

    public String getModelo() {
        return modelo;
    }

    public int getAno() {
        return ano;
    }
}
```

Aqui, o construtor recebe dois parâmetros (`modelo` e `ano`) e os utiliza para inicializar os atributos do objeto `Carro`.

### Métodos

Os métodos representam o comportamento de uma classe, ou seja, as ações que os objetos dessa classe podem realizar. Um método pode receber parâmetros, realizar cálculos ou ações, e retornar um resultado (ou não, se for `void`).

#### Exemplo de um método:
```
public class Calculadora {
    public int somar(int a, int b) {
        return a + b;
    }
}
```

Nesse exemplo, o método `somar()` recebe dois parâmetros inteiros e retorna a soma deles.

### Atributos (Variáveis de Instância)

Os **atributos** ou **variáveis de instância** são os dados que cada objeto da classe contém. Eles definem o estado do objeto. Normalmente, são declarados como `private` e acessados através de métodos getters e setters para garantir o **encapsulamento**.

#### Exemplo de atributos privados com getters e setters:
```
public class Produto {
    private String nome;
    private double preco;

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public double getPreco() {
        return preco;
    }

    public void setPreco(double preco) {
        if (preco > 0) {
            this.preco = preco;
        }
    }
}
```

### Herança

Em Java, uma classe pode **herdar** de outra classe usando a palavra-chave `extends`. A herança permite que uma classe reutilize métodos e atributos de outra classe, promovendo a reutilização de código e facilitando a criação de hierarquias.

#### Exemplo de Herança:
```
public class Animal {
    public void fazerSom() {
        System.out.println("O animal faz um som.");
    }
}

public class Cachorro extends Animal {
    public void fazerSom() {
        System.out.println("O cachorro late.");
    }
}
```

Aqui, a classe `Cachorro` herda de `Animal` e sobrescreve o método `fazerSom()` com seu próprio comportamento.

### Conclusão

Em Java, **classes** são blocos fundamentais da programação orientada a objetos, que agrupam atributos e métodos em uma estrutura organizada. Elas facilitam a criação de objetos que compartilham comportamento e estado, promovendo o encapsulamento, herança e reutilização de código. Utilizar classes de forma eficaz é essencial para a construção de aplicações modulares, escaláveis e fáceis de manter.