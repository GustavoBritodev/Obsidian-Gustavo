---
tags:
  - tipo/trabalho/projeto/mvp_de_proposta_comercial
---
#HNS/Anotações 
Objetivo: Definir MVP e estruturar um Backlog Evolutivo.

# Anotações entrevista com Luiz:
Atualmente as propostas são enviadas por pdf, Luiz quer que as propostas sejam enviadas através de um link para o cliente onde ele faz login e acessa o PDF lá no site em formato parecido com o de slides.

Hoje querem que as propostas entrem através de uma página do [mosten.com](http://mosten.com "http://mosten.com/")

Funcionalidades:

Querem que saia email para o comercial quando o cliente entrar na proposta

Quer que tenha um mapa de calor do site(onde ele mais acessou nos slides)

Funcionalidades de analytics

Tarefas:

Primeiro criar um documento de produto contendo as features (Backlog montado)

Criar MVP

Gerar backlog de tarefas pra desenvolvimento disso

Mosten | Consultoria em Tecnologia e Inovação para Empresas

A Mosten oferece consultoria em tecnologia e inovação, desenvolve soluções personalizadas que unem negócios e tecnologia para o sucesso de empresas.

# Anotações e-mail Richard:
Pessoal,

Tive uma ideia para otimizar nosso fluxo de propostas comerciais e, ao mesmo tempo, aumentar muito a percepção de valor para o cliente.

Hoje, normalmente enviamos uma proposta em PDF ou documento estático. A ideia é evoluir esse modelo para uma **proposta interativa em formato de landing page personalizada**, hospedada em um domínio nosso, por exemplo:

**mosten.com/nome-do-cliente**

A proposta deixa de ser apenas um arquivo e passa a ser uma experiência completa: com narrativa comercial, conteúdo técnico, modelo de contratação, protótipo navegável quando fizer sentido, chat com IA para dúvidas e botão de aceite direto pelo WhatsApp.

Fiz este exemplo (que deve ser melhorado em relação a design):  
[**https://dynamic-melba-4032b1.netlify.app/**](https://1e6c8b2f-81f1-4637-9323-2e7260982483.pipedrive.email/c/z48m0656ek/84leqwrozk/0wye6pp0k2/0?redirectUrl=https%3A%2F%2Fdynamic-melba-4032b1.netlify.app%2F&hash=Qu9DioqD8aJtxQ8uyQB0-imtsnvWiEgeu1CRD-twAug "https://1e6c8b2f-81f1-4637-9323-2e7260982483.pipedrive.email/c/z48m0656ek/84leqwrozk/0wye6pp0k2/0?redirectUrl=https%3A%2F%2Fdynamic-melba-4032b1.netlify.app%2F&hash=Qu9DioqD8aJtxQ8uyQB0-imtsnvWiEgeu1CRD-twAug")

O fluxo pensado seria assim:

**1. Comercial capta a demanda**  
O comercial conduz a reunião com o cliente, entende o cenário, dores, objetivos, escopo inicial e modelo de contratação mais adequado.

**2. Read.ai acompanha a reunião**  
A reunião é gravada/transcrita pelo Read.ai, gerando um resumo estruturado com os principais pontos discutidos, dores do cliente, oportunidades, próximos passos e informações relevantes para proposta.

**3. IA transforma o conteúdo em proposta técnica e comercial**  
A partir do conteúdo do Read.ai, uma IA via integração organiza as informações e gera a base da proposta: contexto, desafio, objetivo, solução proposta, módulos, roadmap, modelo comercial, diferenciais e próximos passos.

**4. Script gera a landing page e o protótipo**  
Com esse conteúdo estruturado, o script gera automaticamente uma LP personalizada para o cliente. Quando fizer sentido, também embarca um protótipo navegável dentro da própria proposta, para o cliente visualizar melhor a solução.

**5. Produtos valida e faz o deploy**  
O time de Produtos entra para validar se o conteúdo técnico está coerente, se o protótipo representa corretamente a solução e se a proposta está alinhada com o que conseguimos executar. Após validação, faz o deploy no ambiente da Mosten.

**6. Comercial envia o link ao cliente**  
O comercial deixa de enviar apenas um PDF e passa a enviar um link personalizado, com uma experiência mais profissional, interativa e rastreável.

**7. Acompanhamento pelo Pipedrive**  
Pelo Pipe, o comercial consegue acompanhar sinais de interesse, como abertura do link, cliques em CTAs e interação com a proposta. Isso ajuda a priorizar follow-ups com mais inteligência.

**8. Marketing acompanha via Analytics**  
O marketing consegue medir tempo médio de visualização, seções mais acessadas, páginas visualizadas, origem de tráfego e comportamento do cliente dentro da proposta.

**9. Cookies e remarketing**  
Conseguimos capturar cookies e criar públicos para remarketing, fortalecendo campanhas e comunicações futuras com quem já demonstrou interesse.

Na prática, isso envolve cada área da seguinte forma:

**Comercial**  
Responsável por captar a demanda, conduzir a reunião, validar o racional comercial, enviar o link ao cliente e acompanhar os sinais de interesse pelo Pipedrive.

**Produtos**  
Responsável por revisar o escopo técnico, validar se a proposta está aderente à solução, ajustar o protótipo quando necessário e garantir que aquilo que está sendo apresentado é executável.

**Marketing**  
Responsável por apoiar a identidade visual, acompanhar os dados de navegação, analisar comportamento dentro da LP e estruturar ações de remarketing.

**Tecnologia / Desenvolvimento**  
Responsável por manter o gerador das LPs, integrar Read.ai, IA, Pipedrive, Analytics e ambiente de deploy, além de garantir segurança, performance e escalabilidade.

**Gestão**  
Consegue ter mais visibilidade sobre quais propostas estão sendo abertas, quais clientes estão mais engajados, quais materiais performam melhor e onde o comercial deve focar energia.

O ganho principal é que deixamos de ter uma proposta estática e passamos a ter uma jornada comercial mensurável. O cliente recebe algo mais bonito, mais claro e mais impactante, enquanto internamente conseguimos acompanhar comportamento, intenção e timing de follow-up.

Acredito que isso pode virar um diferencial importante da Mosten, tanto na percepção do cliente quanto na nossa eficiência comercial.

Caso acreditem ser algo que realmente agregue valor, estruturamos esse fluxo e transformar em um modelo replicável para novas propostas.

Aguardo considerações.

# Anotações e-mail Luiz:
O foco é evoluir o modelo de envio de propostas, passando a disponibilizá-las em formato de site, acessadas por meio de links enviados aos clientes.

Mapeamos inicialmente algumas funcionalidades-chave:

- Autenticação de acesso
- Notificação ao time comercial quando a proposta for aberta (permitindo atuação no momento mais oportuno)
- Mapa de calor da navegação (identificando onde o cliente permaneceu por mais tempo)
- Integração completa com ferramentas de analytics para o Marketing
- ...entre outras evoluções previstas

O objetivo é trazer mais inteligência comercial, visibilidade sobre o comportamento do cliente e aumento da taxa de conversão.

Onde estamos? O Gustavo Martinho começou hoje a levantar os detalhes de todas as funcionalidades para definir um MVP e backlog evolutivo. Direcionarei seu e-mail para garantir que tudo que faz sentido esteja lá.

## Matriz de Moscow:

|                        **Funcionalidades**                         | **Must Have** | **Should Have** | **Could Have** | **Would Have** |
| :----------------------------------------------------------------: | :-----------: | :-------------: | :------------: | :------------: |
|                       Autenticação de Acesso                       |       X       |                 |                |                |
|        Notificação ao time comercial<br>por proposta aberta        |       X       |                 |                |                |
|                           Mapa de calor                            |               |        X        |                |                |
| Importação PDF de Proposta Técnica<br>para geração da Landing Page |       X       |                 |                |                |
|                          Painel de Admin                           |               |        X        |                |                |
|     Geração do conteúdo da proposta <br>através de transcrição     |               |                 |       X        |                |
|                        Captação de cookies                         |               |        X        |                |                |
|     Ferramentas de Analytics<br>(Comportamento dentro do site)     |               |        X        |                |                |
|                 Assistente Virtual (Chatbot) na LP                 |               |                 |       X        |                |
## Funcionalidades:
#### Must Have
Autenticação de Acesso:
* Validação e autenticação de acesso de usuário para identificação do usuário e facilitação na identificação para follow-up e contatos futuros.
Notificação ao time comercial por proposta aberta:
* Notificação via e-mail (Avaliar alternativas) para o time Comercial por proposta aberta, no e-mail deve conter o identificador da proposta e o nome do usuário que acessou.
Importação de PDF de Proposta Técnica para geração da Landing Page:
* Campo de exportação para o usuário anexar o PDF contendo a Proposta Técnica para o sistema processar e gerar a Landing Page através do PDF.

#### Should Have
Painel de Admin:
* Painel com visão de gestão sobre as informações de comportamento do usuário dentro da proposta técnica. Provavelmente vai consolidar as funcionalidades de Mapa de Calor, Captação de Cookies e Ferramentas de Analytics e outras possíveis evoluções.
Mapa de Calor:
* Dashboard/Mapa de Calor contendo as informações de clique na Landing Page, para ajudar a mensurar se CTAs estão sendo chamativos o suficiente e sendo clicados e também outros elementos da página.
Captação de Cookies:
* Capturar cookies para criar públicos para remarketing, fortalecendo campanhas e comunicações futuras com quem já demonstrou interesse.
Ferramentas de Analytics:
* Integração com ferramentas de Analytics ou painel de visualização próprio dentro do painel de Admin para medir tempo médio de visualização, seções mais acessadas, páginas visualizadas, origem de tráfego e comportamento do cliente dentro da proposta.

#### Could Have:
Assistente Virtual (ChatBot):
* Chatbot dentro da LP para resposta de possíveis dúvidas do cliente/usuário sobre a proposta.
Geração do conteúdo da proposta através da transcrição:
* Geração da LP através de transcrição de reuniões com os principais pontos discutidos, dores do cliente, oportunidades, próximos passos e informações relevantes para proposta.
## Escrita do Prompt para estruturação inicial:
Gemini, recebi uma demanda da minha gerência para elaboração de um backlog  priorizado de funcionalidades para uma ferramenta de geração/elaboração de propostas comerciais.

Com base nas informações que recebi consegui elaborar uma matriz de MoSCoW com as funcionalidades priorizadas, mas gostaria que você me ajudasse a descrever melhor as funcionalidades e avaliar se a priorização faz sentido, tendo em vista a dor trazida pelo comercial, onde atualmente enviam propostas técnicas através de PDFs, e visando demonstrar maturidade e percepção de valor para o cliente surgiu a demanda de elaborar essa ferramenta.

Como entregável preciso do backlog melhor estruturado, com base nas funcionalidades que enviarei abaixo, junto aos e-mails que recebi para contextualização e também com base nas instruções e contexto que enviei acima.

Abaixo segue os e-mails e a lista de funcionalidades que priorizei:

Prompt para ajuste do sistema:

Após acessar a proposta quando dou F5 o sistema não me redireciona novamente para adicionar o e-mail e também é possível ver um loading do HTML puro da página de login, arrume isso.

Após acessar a proposta senti falta de uma sidebar contendo o nome dos slides parecido com o material de apoio que enviei, onde nele contém a sidebar navegável.

No painel de Admin preciso que implemente a funcionalidade de drag and drop que lê o PDF da proposta e gera o site com a proposta e um link copiável para enviar ao cliente para que ele acesse a proposta.

Ainda no painel de Admin no trecho de acessos recentes, o IP e o Navegador não é interessante para visualização e sim dados de Analytics para remarketing, follow-up e etc.

Nos cards ao passar o mouse implemente a funcionalidade de tooltip para que mostre os e-mails e nomes dos usuários que acessaram.

Ainda no painel de Admin no engajamento por seção gostaria que as seções refletissem os mesmos nomes da sidebar a ser implementada com o nome dos slides.

Na sidebar do Painel de Admin também deve ser possível visualizar diferentes propostas para navegarmos e visualizar as informações delas e copiar o link de compartilhamento.


**Incluir funcionalidade de edição da proposta**
