---
tags:
  - tipo/trabalho/projeto/clarion
---
Você deve atuar como um especialista em User Experience com expertise em elaboração de documentações que detalham o funcionamento de telas (Ex: Tutoriais).

Seu objetivo é me auxiliar na seguinte demanda: 
Recebi a tarefa de elaborar tutoriais a partir de telas de um sistema que eu não tenho amplo domínio acerca das regras.

Esses tutoriais serão implementados no sistema através de tooltips em trechos específicos da tela, a ideia é que ao vendermos esse sistema como um produto, esses tutoriais abarquem todo o funcionamento e possíveis dúvidas do usuário, de modo que não seja necessário prestarmos suporte.

De uma forma extremamente resumida, o sistema se trata de um gerador de Dashboards a partir de bases de dados determinadas pelo usuário, com a experiência totalmente customizável.

Eu pensei em um plano de trabalho para que atuemos em conjunto que consiste nas seguintes etapas:
1. Definimos o plano de implementação
2. Eu te passo o contexto que sei do sistema, junto ao print de todas as telas do sistema.
3. Elaboramos um padrão de escrita desses tutoriais (podendo ser usado como exemplo ou referência um template de tutorial em documento que possuo).
4. Decidimos se vai ser por seção da tela ou por tela inteira.
5. Elaboramos os tutoriais (por seção ou tela).
6. Implementamos na tela.

Avalie se essas etapas fazem sentido e sugira melhorias caso as identifique.

Avalie também a possibilidade de elaborarmos uma skill para leitura da tela, identificação das funcionalidades e geração desses tutoriais de uso, pensando no uso em outras IAs que possam ter mais facilidade na compreensão e leitura de telas, isso caso você esbarre em limitações técnicas.

É de extrema importância que quando falarmos das telas e das regras, você não assuma ou imagine regras, sempre faça perguntas caso alguma funcionalidade não seja auto explicativa com a tela.

---
Excelente! Gostei do plano de trabalho otimizado, então vamos iniciar pelo primeiro passo:

1. A granularidade deve ser a Mista, pensando por exemplo em um tooltip ou botão que dê um contexto geral sobre a tela e também tooltipos específicos e contextuais. O usuário final não consigo prever, pois o sistema será vendido como um produto para diferentes empresas, logo é importante que a forma de escrita atenda a diferentes públicos.

2. O template de referência enviarei logo abaixo, mas não se apegue ao modelo de escrita dele, tome ele apenas como um ponto de partida de onde podemos evoluir para adaptar a escrita a nossa necessidade de negócio:

1.	Introdução	
• Nome da tela: [Insira o nome da tela]
• Objetivo da tela: [Descreva brevemente o que o usuário pode fazer nesta tela.]

2.	Elementos da Tela
2.1 Visão Geral
[Insira um print da tela destacando suas principais seções]

3.	Fluxo de Uso
3.1 [Nome da Funcionalidade]
[Insira um print da tela destacando suas principais seções]
1.	[Descreva o passo a passo para realizar as principais ações na tela.]

Com as informações acima definidas, como por exemplo o padrão de escrita, no próximo prompt enviarei os prints do sistema separados por tela, então a cada prompt enviarei os prints de uma tela em específico.

Na elaboração do padrão de escrita, tenha ciência de que algumas coisas que estão explícitas no funcionamento da tela não é necessário entrar no máximo de detalhe de tutorial ou até mesmo não é necessário escrever, faça essa análise crítica a cada tela, pois é importante tomarmos cuidado para que a tela não fique poluída com tooltips em demasia ou um tutorial enorme, mas é tão importante quanto que abarquemos todas as possíveis dúvidas dos usuários

---
Os dashboards gerados pelos clientes consomem dados desses documentos globais (ex: uma base de dados macro em .xlsx) ou eles são apenas para download informativo (ex: Manuais, Termos de Uso em .pdf)?
R: Não, são apenas para download informativo. 

O modal informa o limite de 50MB, mas não restringe o tipo de arquivo visualmente. O sistema aceita qualquer extensão ou temos uma "whitelist" (lista de permitidos) específica? .pdf, .xlsx, .docx, .csv

Qualquer usuário com acesso a essa tela pode excluir o documento que você enviou, ou existe uma trava de permissão (ex: apenas o autor ou um Administrador pode apagar)? Somente admin

A existência da tag "Global" na tabela sugere que, no futuro ou em outras telas, teremos documentos com tags específicas de clientes (ex: Tag "Mosten", Tag "Corporação Acme")? Se sim, essa tela mistura arquivos globais e específicos, ou é exclusivamente global? Exclusivamente global

Enviar oportunidade de melhoria pro Lucas, sobre as tags de global na tela de Documentos

---
Gostei demais dos resultados! Porém, o stakeholder/gerente da demanda solicitou que ela seja implementada de uma maneira mais específica.

A ideia é que o tutorial seja feito em formato de texto, semelhante ao tutorial do PSOffice encontrado no link: https://produtopsoffice.atlassian.net/wiki/spaces/psoffice/overview?homepageId=819410

Espelhe-se no modelo de tutorial do PSOffice, que aborda o fluxo das telas, especificidades de campo e funcionamento geral, faça uma varredura completa na documentação do Tutorial do PSOffice (Caso não consiga, me sinalize que envio os demais links).

O fluxo será parecido com o que estávamos fazendo, onde eu irei enviar o print das telas e você gerar o material da documentação, reservando espaço para prints das telas (me sinalizando sempre onde incluir) e enviando sempre o tutorial em padrão de escrita markdown com # e etc para que eu possa apenas copiar e colar no Obsidian e deixar o tutorial registrado.

Continue não assumindo regras ou informações e focando no que está implícito, campos explícitos ou telas simples você pode focar na introdução e contexto da tela, a ideia segue sendo de que devemos dar ênfase no que está implícito e abarcar todas as potenciais dúvidas do usuário acerca de funcionamento de campos, contexto e etc.
