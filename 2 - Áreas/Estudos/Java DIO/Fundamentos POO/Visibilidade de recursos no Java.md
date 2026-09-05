No Java, a visibilidade de recursos (ou modificadores de acesso) é uma maneira de controlar o acesso a classes, métodos, construtores e variáveis em um programa. Ela desempenha um papel essencial na definição de como os diferentes componentes de um sistema interagem entre si e é crucial para a criação de código mais seguro e modular.

Os modificadores de visibilidade mais comuns em Java são:

1. **public**: O recurso é acessível de qualquer lugar.
2. **private**: O recurso é acessível apenas dentro da própria classe.
3. **protected**: O recurso é acessível dentro da própria classe, classes do mesmo pacote e subclasses.
4. **default (sem modificador)**: O recurso é acessível dentro do mesmo pacote.

### Exemplos:

#### **public**:
```
public class Pessoa {
    private String nome;

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return nome;
    }
}

```

Aqui, a variável `nome` e o método `falar()` são públicos, ou seja, qualquer classe pode acessar esses membros, tanto dentro quanto fora do pacote.

#### **private**:
```
public class Pessoa {
    private String nome;

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return nome;
    }
}

```

Neste caso, a variável `nome` é privada, o que significa que ela só pode ser acessada dentro da própria classe `Pessoa`. Para acessá-la, são usados métodos públicos (`setNome` e `getNome`), fornecendo um mecanismo de controle.

#### **protected**:
```
public class Funcionario extends Pessoa {
    protected double salario;
    
    protected void aumentarSalario(double valor) {
        this.salario += valor;
    }
}

```

O modificador `protected` permite que a variável `salario` e o método `aumentarSalario()` sejam acessíveis dentro da própria classe, suas subclasses (como `Funcionario`) e classes do mesmo pacote.

#### **default (pacote)**:
```
class Cliente {
    String nome;

    void comprar() {
        System.out.println(nome + " está comprando.");
    }
}

```

Quando nenhum modificador é especificado, o recurso é acessível apenas dentro do mesmo pacote.

### Por que usar visibilidade?

- **Encapsulamento**: Um dos princípios fundamentais da Programação Orientada a Objetos. Ao definir certos membros como `private`, por exemplo, você pode proteger os dados internos da classe de modificações externas indesejadas, garantindo que as alterações ocorram apenas através de métodos controlados.
    
- **Modularidade**: Controlar a visibilidade ajuda a criar uma separação clara entre a interface pública de uma classe (o que outras classes podem usar) e sua implementação interna (o que é mantido privado).
    
- **Manutenção**: Ao restringir o acesso a certos membros da classe, fica mais fácil manter e modificar o código, pois sabe-se exatamente onde essas variáveis ou métodos estão sendo usados.
    
- **Reutilização**: Modificadores como `protected` permitem criar classes que podem ser estendidas (herança), dando flexibilidade sem comprometer a integridade dos dados.
    

### Exemplo final de uso:

Imagine uma classe `Banco`, onde é crucial manter as informações de saldo privadas:
```
public class Banco {
    private double saldo;

    public Banco(double saldoInicial) {
        this.saldo = saldoInicial;
    }

    public void depositar(double valor) {
        if (valor > 0) {
            saldo += valor;
        }
    }

    public double getSaldo() {
        return saldo;
    }
}

```

Aqui, `saldo` é privado para garantir que ele não possa ser alterado diretamente, mas há métodos públicos para depósito e consulta, permitindo controle sobre como o saldo é manipulado.

Esses níveis de visibilidade ajudam a proteger os dados, manter o código organizado e facilitar a manutenção e a evolução de sistemas complexos.