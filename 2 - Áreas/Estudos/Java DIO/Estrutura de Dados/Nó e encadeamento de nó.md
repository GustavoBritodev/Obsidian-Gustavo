- O nó é um espaço em memória que armazena não somente o dado que você quer armazenar mas também uma referência para um próximo nó

Para entender o conceito de nó imagine que você tem um nó e dentro dele tem um dado que você quer armazenar, esse dado pode ser int, string ou qualquer outro tipo primitivo e ainda dentro do nó você tem a referência para um próximo nó. Ao criar o segundo nó você atribui o segundo nó para a referência do primeiro nó e assim fazendo o encadeamento de nós, ou seja você vai no primeiro nó pega a referência dele e aponta para o segundo nó. O mesmo serve para um terceiro nó, onde a referência do segundo nó irá apontar para o terceiro nó, e caso este seja seu último nó você pega a referência dele e aponta para nulo.

Exemplo de código da classe No com getters, setters e construtor:
```
public class No {  
    private String conteudo;  
    private No proximoNo;  
  
    public No(String conteudo) {  
        this.proximoNo = null;  
        this.conteudo = conteudo;  
    }  
    
    public No getProximoNo() { return proximoNo; }  
  
    public void setProximoNo(No proximoNo) { this.proximoNo = proximoNo; }  
  
    @Override  
    public String toString() {  
        return "No{" +  
                "conteudo='" + conteudo + '\'' +  
                '}';  
    }  
}
```

Classe Main com a saída dos nós:
```
public class Main {  
    public static void main(String[] args) {  
  
        No no1 = new No("Conteúdo no1");  
  
        No no2 = new No("Conteúdo no2");  
        no1.setProximoNo(no2);  
  
        No no3 = new No("Conteúdo no3");  
        no2.setProximoNo(no3);  
  
        No no4 = new No("Conteúdo no4");  
        no3.setProximoNo(no4);  
  
        //no1->no2->no3->no4->null  
  
        System.out.println(no1);  
        System.out.println(no1.getProximoNo());  
  
        System.out.println("-------------------");  
  
        //Encadeamento por referência  
        System.out.println(no1);  
        System.out.println(no1.getProximoNo());  
        System.out.println(no1.getProximoNo().getProximoNo());  
        System.out.println(no1.getProximoNo().getProximoNo().getProximoNo());  
        System.out.println(no1.getProximoNo().getProximoNo().getProximoNo().getProximoNo());  
    }  
}
```