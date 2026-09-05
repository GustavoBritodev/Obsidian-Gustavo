Documentação oficial sobre Generics -> https://docs.oracle.com/javase/tutorial/java/generics/why.html

Contexto do uso de Generics: 
- Evitar casting excessivo (olhar o que é casting)
- Evitar códigos redundantes
- Encontrar erros em tempo de compilação
- Introduzido desde o Java SE 5.0

Exemplo de código:
Lista<==String==> minhaLista = new Lista<>();

public class Lista<==T==> {
	private T t;
	.
	.
	.
	.
	.
}

Estudar: Unknown Wildcards (Unbounded) e Bounded Wildcard (Upper Bounded / Lower Bounded)
Link para documentação oficial sobre os Wildcards -> https://docs.oracle.com/javase/tutorial/extra/generics/wildcards.html
