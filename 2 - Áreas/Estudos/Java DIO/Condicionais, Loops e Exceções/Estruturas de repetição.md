### For com array

- Exemplo de código:
```
String alunos [] = {"Gustavo", "Felipe", "Gabriel", "Camila"};
   
   for(int i = 0; i<alunos.length; i++){
       System.out.println("O aluno no índice " + i + " é " + alunos[i]);
   }
```

Exemplo de saída do código acima:
```
O aluno no índice 0 é Gustavo
O aluno no índice 1 é Felipe
O aluno no índice 2 é Gabriel
O aluno no índice 3 é Camila
```

- Outra forma de trabalhar com for e arrays seria assim:
```
for(String aluno : alunos){
    System.out.println("O nome do aluno é: " + aluno);
}
```

Nesse caso acima a variável aluno recebe o valor da posição do array alunos a cada iteração. Sendo a saída de dados assim:
```
O nome do aluno é: Gustavo
O nome do aluno é: Felipe
O nome do aluno é: Gabriel
O nome do aluno é: Camila
```

### Break e continue

O continue continua o laço e o break interrompe o laço de repetição. No exemplo abaixo se o valor for igual a 3 ele continua o laço pulando a instrução de saída que é o System.out.println(numero). Assim não mostrando o 3 na saída de dados.

```
for(int numero = 1; numero <=5; numero++){
	if(numero == 3)
		continue;

	System.out.println(numero);
}
```

Exemplo de saída de dados do exemplo do continue:
```
1
2
4
5
```

No exemplo do break quando o número for igual a 3 ele encerra o laço:
```
for(int numero = 1; numero <=5; numero++){
	if(numero == 3)
		break;

	System.out.println(numero);
}
```

Exemplo de saída de dados do exemplo do break:

```
1
2
```