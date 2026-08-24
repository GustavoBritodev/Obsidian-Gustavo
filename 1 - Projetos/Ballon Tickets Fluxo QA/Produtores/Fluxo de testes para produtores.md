---
tags:
- Plataforma_de_Ingressos
---


Fluxo de Criação de Contas: 

Está faltando Criar integração com o Google.

Além disso precisamos consertar o hover do botão de acessar com o google pois quando eu clicko ou passo o mouse em cima o nome desaparece

Além disso só é possível saber que eu posso logar ou criar conta com o google apenas na pagina de iniciar sessão é necessário também ter algo do tipo na parte de Registro de conta nova.

Tela de Verify-Email:
Precisando corrigir visual de input dos numeros 
![[Pasted image 20260409194041.png]]

Após a criação de uma conta que não é de produtora aparece para mim as seções de Meus Eventos e tudo que é possível de se fazer sendo um produtor mesmo eu não tendo completado o cadastro de produtor
![[Pasted image 20260409195331.png]]
![[Pasted image 20260409195356.png|717]]

Ao tentar concluir o processo de cadastro para eu virar um produtor deu erro:
![[Pasted image 20260409195632.png]]```

```
## Error Type
Console Error

## Error Message
Erro ao buscar perfil do organizador logado


    at getCurrentProducer (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0bu58e1._.js:1701:15)
    at async Dashboard.useEffect.fetchData (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0bu58e1._.js:3335:58)

Next.js version: 16.2.2 (Turbopack)

## Error Type
Console Error

## Error Message
Erro ao buscar resumo do produtor


    at getProducerSummary (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0bu58e1._.js:1710:15)
    at async Dashboard.useEffect.fetchData (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0bu58e1._.js:3335:58)

Next.js version: 16.2.2 (Turbopack)


## Error Type
Console Error

## Error Message
Erro ao buscar perfil do organizador logado


    at getCurrentProducer (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0bu58e1._.js:1701:15)
    at async ProducerEvents.useEffect.fetchData (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0hgxy5e._.js:3617:69)

Next.js version: 16.2.2 (Turbopack)
## Error Type
Console Error

## Error Message
Erro ao buscar perfil do organizador logado


    at getCurrentProducer (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0bu58e1._.js:1701:15)
    at async EventCreate.useEffect.fetchInitialData (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_088mexa._.js:2211:50)

Next.js version: 16.2.2 (Turbopack)
## Error Type
Console Error

## Error Message
[object Object],[object Object],[object Object],[object Object],[object Object],[object Object],[object Object],[object Object],[object Object],[object Object],[object Object]


    at registerProducer (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0~_7bh3._.js:1800:15)
    at async handleSubmit (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_03kxl0g._.js:2834:13)

Next.js version: 16.2.2 (Turbopack)


```

Além disso quando acesso a área de Produtor mesmo não tendo concluido o registro como produtor parece que ele está trazendo um produtor que ja esta cadastrado no banco

![[Pasted image 20260409200433.png]]
![[Pasted image 20260409200453.png]]


```
## Error Type
Console Error

## Error Message
Erro ao buscar perfil do organizador logado


    at getCurrentProducer (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0bu58e1._.js:1701:15)
    at async ProducerCustomize.useEffect.loadProducer (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0rkxygk._.js:2287:38)

Next.js version: 16.2.2 (Turbopack)

```