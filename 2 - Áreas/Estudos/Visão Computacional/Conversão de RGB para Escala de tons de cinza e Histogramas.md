O grayscale é uma técnica de design que utiliza apenas tons de cinza, variando do preto ao branco, para representar imagens.

O objetivo do Grayscale é reduzir o número de canais de cor usando apenas um valor por pixel. Isso reduz em quase 70% o processamento computacional.

A grayscale pode ser obtida por média ponderada dos canais RGB.

Ex:
![[Pasted image 20260701202423.png]]

A conversão do RGB para cinza é uma média ponderada dos canais levando em consdieração a sensibilidade do olho humano a cada cor:

$$
0,299 * Vermelho + o,587 * Verde + 0,114 * Azul = Pixel Cinza
$$

## Histograma (distribuição dos níveis de intensidade):
O histograma mostra quantos pixels têm cada valor de cor (intensidade). Pode ser aplicado para canais individuais (R, G, B ou cinza) ou totais.

*Utilidade:*
Análise de contraste e brilho e também a detecção de regiões escuras ou claras.

![[Pasted image 20260701203429.png]]

![[Pasted image 20260701203621.png]]

