#### Quartis (Quartil)
Quartil é basicamente pegar um conjunto de dados ordenado e dividir em 4 partes (Q1, Q2, Q3).

#### Quartil para dados agrupados com intervalo
fi = Frequência do Intervalo
Fac = Frequência acumulada
Σfi = Somatório de todas as frequências (Frequência acumulada)
Li = Limite inferior
K = É utilizado para definir o quartil de interesse, utilizado através da representação em fração de cada quartil.  Representações em fração de cada quartil (Q1, Q2, Q3):$$ Q1 = \frac{1}{4}⠀⠀⠀Q2 = \frac{1}{2}⠀⠀⠀Q3 = \frac{3}{4}$$* = O trecho do quartil que desejamos descobrir (Q1, Q2 ou Q3).
h = Amplitude. Diferença entre um dois pontos de um intervalo.

Fórmula: $$ * = Li + \frac{K⠀ .⠀Σfi - Fac⠀anterior}{f⠀intervalo} $$
Ex:

| Estatura  | fi  |    Fac     |
| :-------: | :-: | :--------: |
| 160 - 164 |  7  | ==**7**==  |
| 164 - 168 |  4  | ==**11**== |
| 168 - 172 |  5  | ==**16**== |
| 172 - 176 |  8  | ==**24**== |
| 176 - 180 | 16  | ==**40**== |
#### Resolução do Exemplo para encontrar o Q1:
$$ Q1 = Li + \frac{ K⠀ .⠀Σfi - Fac⠀anterior}{f⠀intervalo} $$
$$PosicaoQ1 = K.Σfi⠀=⠀\frac{1}{4} . 40$$
$$PosicaoQ1 = 10$$
$$Q1 = 164 + \frac{10 - 7}{4} . 4$$
$$Q1 = 167$$
#### Resolução do Exemplo para encontrar o Q2:
$$ Q2 = Li + \frac{ K⠀ .⠀Σfi - Fac⠀anterior}{f⠀intervalo} $$
$$PosicaoQ2 = K.Σfi⠀=⠀\frac{1}{2} . 40$$
$$PosicaoQ2 = 20$$
$$Q2 = 172 + \frac{20 - 16}{8} . 4$$
$$Q1 = 174$$
Resolução do Exemplo para encontrar o Q3:
$$ Q3 = Li + \frac{ K⠀ .⠀Σfi - Fac⠀anterior}{f⠀intervalo} $$
$$PosicaoQ3 = K.Σfi⠀=⠀\frac{3}{4} . 40$$
$$PosicaoQ3 = 30$$
$$Q3 = 176 + \frac{30 - 24}{16} . 4$$
$$Q3 = 177,5$$