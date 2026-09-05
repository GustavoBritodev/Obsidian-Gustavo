### Condição Ternária

```
int nota = 7;

String resultado = nota >= 7 ? "Aprovado" : "Reprovado"; //Após o ? é o if (true) atribuindo o valor "Aprovado" para a variável resultado e após o : o else (false) atribuindo o valor "Reprovado" para a variável resultado

System.out.println(resultado);
```

- Após o ? é o if (true) atribuindo o valor "Aprovado" para a variável resultado e após o : o else (false) atribuindo o valor "Reprovado" para a variável resultado

#### Ternário mais complexo com else if (condições encadeadas)

```
int nota = 5;

String resultado = nota >= 7 ? "Aprovado" : nota>=5 && nota < 7 ? "Recuperação" : "Reprovado";

System.out.println(resultado);
```

- Após o ? é o if (true) atribuindo o valor "Aprovado" para a variável resultado, após o : que atua como else vem a condição nota>=5 && nota < 7 e em seguida ? que atua como if da mesma, logo após vem o : que atua como else sendo ele o resultado de falso de todas as condições anteriores para chegar no else.

## Switch case

```
	String plano = "T";

    switch(plano){
        case "T":{
            System.out.println("5 GB de Youtube");
        }
        case "M":{
            System.out.println("Whatsapp e Instagram ilimitado");
        }
        case "B":{
            System.out.println("100 minutos de ligação");
        }
```
 - Nesse caso por não ter o break após a instrução correspondente, o código lê todos os cases abaixo. Tendo a saída de dados como:

```
 5 GB de Youtube
Whatsapp e Instagram ilimitado
100 minutos de ligação
```

Para mostrar apenas a única condição verdadeira correspondente e encerrar a leitura do código nela seria necessário usar o break. Assim o código ficaria assim:

```
String plano = "T";

    switch(plano){
        case "T":{
            System.out.println("5 GB de Youtube");
        break;
        }
        case "M":{
            System.out.println("Whatsapp e Instagram ilimitado");
        break;    
        }
        case "B":{
            System.out.println("100 minutos de ligação");
        break;    
        }
```

- Nesse caso a saída de dados seria apenas o "5 GB de Youtube". Outra forma de fazer assim mas sem usar o break seria utilizando o rule switch, que funciona igual o break porém tem a sintaxe mais simples fazendo o uso da seta -> após a verificação, nesse caso ficaria assim o código:

```
String plano = "T";

    switch(plano){
        case "T" -> {
            System.out.println("5 GB de Youtube");
        }
        case "M" -> {
            System.out.println("Whatsapp e Instagram ilimitado");
        }
        case "B" -> {
            System.out.println("100 minutos de ligação");
        }
```
