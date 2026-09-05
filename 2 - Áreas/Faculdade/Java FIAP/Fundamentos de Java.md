Na orientação a objetos não pensamos o problema em termos de tarefas e sim em entidades existentes dentro desse problema e em como essas entidades interagem entre si. A interação dessas entidades é o que resolve esses problemas

O paradigma da orientação a objetos visa trazer pra programação objetos reais.

Na orientação a objetos o código fica fragmentado em partes facilitando a leitura e manutenção do mesmo

## Java

Java é interpretado por "máquinas virtuais Java".
O Java foi feito pra programar praticamente de tudo.


## Portabilidade do Java

A portabilidade do Java se dá graças a suas máquinas virtuais, onde por exemplo um mesmo código pode ser usado em dispositivos diferentes.

A máquina virtual quando você compila seu código ela gera um código que somente aquela máquina virtual entende.

## Princípios da Orientação a Objetos (POO)

**1- Abstração**
**2- Encapsulamento**
**3- Modularização**
**4- Hierarquia**

**Abstração na POO**: É a capacidade de abstrair tudo aquilo que é irrelevante para meu negócio.

**Encapsulamento na POO**: É a ideia de proteção de alguns itens importantes dentro de um sistema. 
Exemplo: Número do RG, quando se olha para alguém você não vê, não sabe, não tem acesso ao RG da pessoa e para saber o número do RG de alguém só é possível usando um "método" que essa pessoa te forneça. O encapsulamento é sobre a informação e/ou o método não estar disponível diretamente, e sim através de um outro método ou alguma outra funcionalidade que seja implementada na entidade.

**Modularização na POO:** A modularização é a ideia de fazer módulos. É um exemplo quando você está fazendo um código que está ficando muito grande e complexo e quebrar esse código em códigos menores. e isso é feito através das classes que são unidades básicas de programação na POO. Também se entende como o processo de dividir um todo em partes bem definidas, que podem ser construídas e examinadas separadamente e que possam interagir entre si.

**Hierarquia de classes na POO**: As classes não possuem o mesmo "peso", é como se fosse uma árvore genealógica de classes. Isso se dá por conta da herança na POO. A herança é uma técnica e/ou capacidade de uma classe herdar os atributos e comportamentos de uma classe "pai", assim visando o reaproveitamento de código. Exemplo: O aluno é uma pessoa ou tem uma pessoa? Ele é uma pessoa então a classe ou objeto aluno ele herda atributos e características de quaisquer outras pessoas. Em contra partida, o aluno é uma disciplina ou tem uma disciplina? O aluno tem uma disciplina, então ele não é uma herança, o aluno não vai herdar de uma disciplina e sim dentro da classe do objeto aluno, terá uma referência à classe e ao objeto disciplina

Orientação a Objetos é abstrair do mundo real as informações e adequar para sistemas.

JVM = Java Virtual Machine

Java é portável porque a partir de um código Java que é entendível pelo olho humano ele é COMPILADO, fazendo a validação e gerando .class sendo esse .class composto por bytecodes e esses bytecodes que são interpretados pela JVM.

A linguagem Java é compilada e interpretada. Primeiro os arquivos de código fonte são compilados para bytecodes para depois serem interpretados pela JVM, assim iniciando a execução do software.

Herança é uma das formas de Hierarquia. 
