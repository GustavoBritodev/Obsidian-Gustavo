---
tags:
  - tipo/geral
status: rascunho
---

Tags: #Prompt #Trabalho #Zurich

Boa tarde, ChatGPT! Você é um Analista de Negócios e Processos especialista em Suporte e ITSM na empresa Zurich, sua especialidade será na escrita de POPs que nada mais são do que documentos operacionais que descrevem a operação de uma frente de atuação da empresa Mosten dentro da Zurich.

O POP da vez será o POP de Problem Management, esse POP já iniciei o processo de elaboração porém não ficou dentro da realidade da operação realizada na Mosten, então recentemente entrevistei a responsável pela operação da torre de Problem Management da Mosten alocada na Zurich e anotei todo o passo a passo da operação e é a partir dessas anotações que você deve estruturar o POP de Configuration Management.

Para complementar e embasar alguns tópicos, enviarei em anexo um POP antigo da Zurich sobre a torre de Problem Management, porém lembre-se nosso foco será descrever a operação atual da torre de Problem Management da Mosten, logo você deve utilizar essas outras informações contidas no POP da Zurich apenas caso necessário para complementar ou explicar algum ponto.

Para auxiliar na estruturação e no modelo de documento, irei enviar em anexo um template de POP e também o POP antigo que eu havia feito, porém existem alguns pontos que não refletem a realidade atual da operação, utilize eles apenas como modelo de estrutura de escrita.

Como saída esperada peço que envie em formato de texto aqui no chat da nossa conversa o POP estruturado.

Caso identifique algum ponto com lacunas ou explicação frágil, peço que me sinalize antes de estruturar o POP para que eu explique e assim você consiga estruturar o POP que reflita a operação atual:

Torre de Problem 06/03:

Abre painéis do SN e vai em Problem Management Brasil e depois em Problem manager pra verificar as SLAs a Vencer

Pela SLA que vai vencer ela abre uma da lista de Problemas abertos e verifica o que que tem em aberto, o que tá estourado e verifica a aba Anotações do Problema

Em casos de problemas que não tem o nome do portfólio:

Vai em IC Afetado e pega o ID de correlação para ir na Base Change e poder saber o portfólio do problema 

A planilha Base Change deve ser Sempre aberta em modo área de trabalho

Na planilha de Base Change vai na aba de BASE_SEVERIDADE e procura pelo nome do gerente ou do incidente gerador contidos no Problema

Com isso ela vai na aba de Tarefas de Problema e entender quais as tarefas que estão em aberta (impeditivas)

Tarefas de Acompanhamento não tem problema estar em aberto (Em casos de data estourando ela mesmo pode alterar a data clicando na tarefa e indo no campo Target Date)

Casos de tarefa de acompanhamento também devem ser alterados no Azure DevOps aba Sprints pesquisando pelo ID da PTASK ou PRB (Caso PTASK não aparecer)

Ao localizar a User Story ela abre a US e localiza a PTASK dentro da Child no card

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

Próxima tarefa do dia é abrir a Base Change em modo Área de trabalho na aba BASE_PROBLEMA e limpa os filtros e então limpa os chamados encerrados filtrando pela coluna ESTADO

Com os chamados encerrados removidos, ela seleciona a coluna NÚMERO e visualiza a quantidade de chamados em andamento e depois vai no SN e verifica se a contagem bate com os do SN contidos no card de Problemas em andamento

Após isso vai no card do SN chamado em Tarefas Abertas - Geral, clica com o botão direito do mouse na coluna número e seleciona a opção de exportar em Excel e abre no modo área de trabalho

Com o Excel aberto seleciona o rótulo da planilha como público, com isso seleciona a planilha inteira e aplica a altura da linha como 15

Após isso aplica os filtros na planilha, seleciona a coluna Target Date e a coluna Número e seleciona geral na aba número do excel

Após isso volta na Base Change, seleciona a coluna da PTASK e insere uma coluna e limpa os filtros da planilha

Após isso na coluna inserida realiza um PROCX no primeiro registro de PTASK com a seguinte formula =PROCX([Primeiro registro de PTASK]; [Planilha baixada do SN, Coluna número e coluna Target Date])

Após isso copia a fórmula para todos os registros de PTASK e coloca Encerrado nos registros encerrados, altera o nome da coluna inserida para ATIVIDADE DO DIA e exclui a coluna antiga de ATIVIDADE DO DIA

Após isso aplica filtros, remove os encerrados e verifica os registros com N/D

Com isso retorna ao SN e vai no card de Tarefas que vencem essa semana, clica na coluna número e exporta um excel e abre em modo área de trabalho e aplica o rótulo de public

Para que com esses dados seja possível visualizar tudo de tarefa que tem para essa semana

Após isso volta pra Base Change na aba BASE_PROBLEMA e aplica o filtro pras N/Ds 

E copia a PTASK no Azure DevOps para verificar se foi criada ou não dentro do Azure

Com as US de ND abertas ela pega o numero da PRB e joga no SN e verifica no SN na aba de Tarefas de Problemas qual a PTASK que deve ser aberta no Azure DevOps

No Azure DevOps ela verifica quais as childs de PTASKS abertas e verifica qual que ainda não está aberta no Azure DevOps

Cria uma nova Child da PTASK que não foi aberta da PRB

Copia a descrição resumida da PRB no SN e cola na descrição da Child

Copia a descrição da PRB no SN e cola no card do Azure DevOps e atribui o card a si mesma

Copia a target date da PTASK no SN e cola no Due Date do Azure DevOps

E em Original Estimate de Effort Hours no Azure DevOps inclui 1 hora e então salva

Após salvar altera o status para active

----------------------------------------------------------------------------------------------------------------------------------------------------

Fechamento de portfólio


após isso volta na PTASK, faz download do arquivo anexado na PTASK e então anexa no card correspondente do Azure DevOps na seção de Attachments

Na descrição do card cola o número do incidente aberto na PTASK dentro do SN e verifica a quem deve ser direcionado (Responsável pelo portfólio)

Ao iniciar o dia primeiro ver as SLAS o que tem para estourar, após isso abrir a base change, conferir o que tem de ND e pedir pra abrir US para a RAphaela e a Estela, elas abrindo você abre no Azure as Ptasks mas preenche a base change com as informações do Service Now e coloca a mensagem de script que já tem pronta referente a descrição de pedido que está lá no service now para direcionar ao responsável do portfólio
 
 
 
RESPONSAVEIS POR CADA PORTIFOLIO
Personal Lines - LETÍCIA LANNES
Partnerships e CAP - Rafaela Zschaber
CLAIMS - Mateus Ananias
Corporate Services - Elisangela Guimaraes
LIFE e PREV - Adriana Bianchine
Channels - Lígia Pessoa
CI - Felipe Sampaio
Oper e infra (interno) - Alex Pezata
Oper e infra (externo) Ana é da Tivit 

Azul - todas tasks sem atrasos
PRIMEIRO DE TUDO OLHAR INVESTIGAÇÃO NA BASE CHANGE DEPOIS VERIFICA AS SLA´S E PARTE PARA AS IMPLEMENTAÇÕES
 
 
Amarelo - quando há alteração de target date
Vermelho - Estouro de SLA

INVESTIGAÇAO LAUDO RCA Azure Devops

@,por gentileza, deem andamento à elaboração do laudo de Análise de Causa Raiz (RCA) referente à severidade INC22509482, conforme o arquivo anexo.
Caso necessário o complementação no laudo RCA por outro portfólio, por favor, preencher as informações abaixo.
         - Motivo:
         - Portifólio:
         - Responsável:
O prazo para  entrega do material é 10/10/2025.
Se precisarem de mais tempo ou algum apoio, por favor, não hesitem em nos contatar.
Estamos à disposição para ajudar no que for preciso!
 
 
 
Após essa mensagem interagir novamente perguntando se tem algum retorno da atividade.
 
 
Exemplo: Boa tarde, @Elisangela Guimaraes (Contractor) @Evelyn Marques e @Simone Soares, por gentileza, temos algum retorno referente a atividade?
 
Cc: @Ana Lima (Contractor) @Raphaela Marques @Luan Santos (Contractor) @Jônatas Silva (Contractor) @Pedro Ueno (Contractor)
 
 

Analise de Reincidência Azure Devops

@, por gentileza, deem andamento à Atualização de laudo RCA por Reincidência referente à severidade INC22859039, conforme o arquivo anexo.
Caso necessário o complementação no laudo RCA por outro portfólio, por favor, preencher as informações abaixo.
         - Motivo:
         - Portifólio:
         - Responsável:
O prazo inicial para essa entrega é 21/11/2025.
Se precisarem de mais tempo ou algum apoio, por favor, não hesitem em nos contatar.
Estamos à disposição para ajudar no que for preciso!
Cc: @r.marques, @estela.figaro e @ana.lima3
_____________________________________________________________________________________________
INVESTIGAÇAO  PORTIFOLIO - SERVICE NOW
Direcionado ao portifólio a solicitação de entrega da versão do RCA, conforme imagem abaixo.
_____________________________________________________________________________________________
PRENCHIMENTO RCA
Por gentileza, seguir com o preenchimento completo do RCA, com informações detalhadas.
Cc: @r.marques, @estela.figaro e @ana.lima3
_____________________________________________________________________________________________
FINALIZAÇAO DE TAREFA RCA
Obrigada pela atualização.
Em breve informaremos a data de apresentação do laudo.
Cc: @r.marques, @estela.figaro e @ana.lima3
_________________________________________________________________________________________________
MENSAGEM A SER COLOCADA NO SERVICE NOW - SOLICITAÇAO DE AUXILIO.
Direcionado ao portifólio a solicitação de auxilio, conforme imagem abaixo.
Cc: @r.marques, @estela.figaro e @ana.lima3
_____________________________________________________________________________________________
MENSAGEM A SER COLOCADA NO AZURE DEVOPS - POSTERGAÇAO DE DADA
O prazo foi estendido para 03/10/2025. Agora, estamos aguardando o retorno do portifólio.
Cc: @r.marques, @estela.figaro e @ana.lima3
_____________________________________________________________________________________________
MENSAGEM A SER COLOCADA NO SERVICENOW - POSTERGAÇAO DE DADA
Estamos alterado a data da entrega da tarefa para 16/01/2026, conforme solicitado pelo portifólio., segue evidencia em anexo.
Cc: @r.marques, @estela.figaro e @ana.lima3
___________________________________________________________________________________________
MENSAGEM A SER COLOCADA NO SERVICENOW - ATIVIDADE EM ATRASO OU REAGENDADA
Direcionado ao portifólio a solicitação de entrega da atividade devido a mesma se encontrar em atraso.
Cc: @r.marques, @estela.figaro e @ana.lima3
___________________________________________________________________________________________
MENSAGEM A SER COLOCADA NO SERVICENOW - ATIVIDADE EM DIA
Direcionado ao portifólio a solicitação de entrega da atividade. segue evidencia em anexo.
Cc: @r.marques, @estela.figaro e @ana.lima3
___________________________________________________________________________________________
MENSAGEM A SER COLOCADA NO SERVICENOW  E AZUREDEVOPS - PARA AVALIAÇAO DE LAUDO RCA
@Ana Lima (Contractor), por gentileza seguir com analise do laudo e se possível seguir com o agendamento para apresentação do laudo RCA.
Cc: @r.marques, @estela.figaro
___________________________________________________________________________________________
MENSAGEM A SER COLOCADA NO AZURE DEVOPS - POSTERGAÇAO DE DADA
@.......por gentileza precisamos de um retorno referente a tarefa, vocês poderiam estar nos auxiliando?
Cc: @r.marques, @estela.figaro e @ana.lima3
___________________________________________________________________________________________
LAUDO RCA INCOMPLETO
V8,Primeiramente, gostaríamos de agradecer pelo envio do laudo e pelo empenho dedicado à elaboração do material.
Notamos algumas oportunidades para tornar o laudo ainda mais claro e acessível, facilitando a compreensão dos fatos por qualquer pessoa, independentemente da área de atuação. Orientamos incluir mais detalhes sobre a causa raiz, as tratativas realizadas e eventuais ações futuras. Além disso, evidências como prints de conversas e logs de ferramentas enriquecem o documento e trazem mais transparência ao processo.
Estamos à disposição para apoiar em caso de dúvidas.
Cc: @r.marques, @estela.figaro e @ana.lima3
__________________________________________________________________________________________
***MITIGAÇAO

@,por gentileza, precisamos da sua ajuda para dar andamento na tarefa de mitigação
A data de entrega está se aproximando, e a conclusão dessa ação é essencial para resolvermos a questão.
A entrega é 11/08/2025
Se precisarem de mais tempo ou algum apoio, por favor, não hesitem em nos contatar. Estamos à disposição para ajudar no que for preciso!
Cc: @r.marques, @estela.figaro e @ana.lima3
______________________________________________________________________________________
Falta de informação no plano de mitigação.
por gentileza qual a implementação feita? Precisamos que a mesma seja descrita, facilitando a compreensão dos fatos por qualquer pessoa, independentemente da área de atuação. Orientamos incluir mais detalhes sobre as tratativas realizadas e eventuais ações futuras. Além disso, evidências como prints de conversas e logs de ferramentas enriquecem o documento e trazem mais transparência ao processo.
Estamos à disposição para apoiar em caso de dúvidas.
Cc: @r.marques, @estela.figaro e @ana.lima3
_________________________________________________________________________________________
PORTIFOLIO MITIGAÇAO
Direcionado ao portifólio a solicitação de entrega da tarefa de mitigação, conforme imagem abaixo.
Cc: @r.marques, @estela.figaro e @ana.lima3
_________________________________________________________________________________________
FECHAR TAREFA SERVICE NOW
Conforme alinhamento com a equipe de PROBLEM MANAGEMENT, tarefa finalizada.
_________________________________________________________________________________________
FECHAR US SIDNEI, PRINCIPAL
@sidnei, por gentileza, poderia seguir com o encerramento da US? Os critérios de aceite mapeados já foram concluídos
Cc: @r.marques, @estela.figaro e @ana.lima3
__________________________________________________________________________________________
VALIDAÇAO DE LAUDO POR EMAIL
Laudo encaminhado por e-mail para validação do BSM, retorno do mesmo em 29/01/2026, conforme e-mail anexo.
Cc: @r.marques, @estela.figaro e @ana.lima3
 
 
 
Mensagem Portfólio
 
 
Boa tarde, time!
Espero que todos estejam bem.
Me chamo Thatiana e estarei apoiando vocês na Torre de Problemas.
 
 
Mensagem para responsável
 
Oi, mais uma outra dúvida eu vou puxar o do Alex posso mandar esse texto como mensagem pra ele?: Boa tarde, Alex!
Espero que esteja bem.
Me chamo Thatiana e estarei apoiando seu portfólio na Torre de Problemas.
Identificamos que há algumas PTASKs em aberto vinculadas ao seu portfólio. Para darmos continuidade adequada ao tratamento dessas demandas, preciso do seu posicionamento sobre o andamento de cada uma delas.
Peço, por gentileza, que os retornos sejam realizados via Azure, marcando todo o time de Problemas. Assim conseguimos garantir maior agilidade e qualidade no atendimento.
Fico à disposição caso precise de qualquer apoio.
Identificamos que temos algumas PTASKs em aberto vinculadas ao portfólio. Para darmos continuidade adequada ao tratamento das tarefas, precisamos de um posicionamento sobre o andamento de cada uma delas. Peço que os retornos sejam realizados via Azure, marcando todo o time de Problemas. Dessa forma, conseguimos garantir um atendimento mais ágil e com maior qualidade.
 
 
Tudo DÚVIDAS fazer no PRB MELHORES NÃO ESQUECER QUE É LÁ
 
LETICIA LANES é LATAM RESOLVERS de PORTFOLIO PERSONAL LINES DENTRO DA BASE CHANGE
 
 
Claims: Carlos Eduardo / Eliene Viana	
Life, Prev & Cap: Thiago Fernandes / Marcos Sanches	
Partnerships: José Pereira da Silva Filho / Gustavo Inacio	
Personal Lines & CI: César Henrique da Silva / Vinicius Vist / Diogo Chiconi
Por gentileza, verificar aprovações da pauta CAB de hoje
 
 
Para cobrar os portfólios filtrar por portfólios, antes de fazer isso arruma tudo para aparecer todos os portfólios, clica na coluna atividade do dia e classifica de A a Z, após isso vai na coluna filtra por porftolio e seleciona as 3 colunas de ATIVIDADE DO DIA, PTASK E AZURE VOU NO TEAMS entro no portfólios destinado e coloco a mensagem para pedir para verificarem as ptasks já tenho o seguinte texto pronto:
 
 
Boa tarde, time!
Espero que todos estejam bem.
Me chamo Thatiana e estarei apoiando vocês na Torre de Problemas.
 
 
Mensagem para responsável
 
Oi, mais uma outra dúvida eu vou puxar o do Alex posso mandar esse texto como mensagem pra ele?: Boa tarde, Alex!
Espero que esteja bem.
Me chamo Thatiana e estarei apoiando seu portfólio na Torre de Problemas.
Identificamos que há algumas PTASKs em aberto vinculadas ao seu portfólio. Para darmos continuidade adequada ao tratamento dessas demandas, preciso do seu posicionamento sobre o andamento de cada uma delas.
Peço, por gentileza, que os retornos sejam realizados via Azure, marcando todo o time de Problemas. Assim conseguimos garantir maior agilidade e qualidade no atendimento.
Fico à disposição caso precise de qualquer apoio.
Identificamos que temos algumas PTASKs em aberto vinculadas ao portfólio. Para darmos continuidade adequada ao tratamento das tarefas, precisamos de um posicionamento sobre o andamento de cada uma delas. Peço que os retornos sejam realizados via Azure, marcando todo o time de Problemas. Dessa forma, conseguimos garantir um atendimento mais ágil e com maior qualidade.
 
 
e após colar o que pegou na base change com essa mensagem pegar o nome do responsável do portfólio e colocar @ responsável Exemplo:
 
Boa tarde a todos!
Por gentileza temos algum retorno referente as atividades? @nome do responsável do portfólio
 
e isso é durante 3 dias e dentro do azure e dentro do servisse now que estamos aguardando dentro do portfólio
 
para documentar e provar que foi cobrado no azure devemos printar a tela do azure onde está a nossa interação porém renomear o print com o nome da ptask referida antes de anexar no servisse now pois tem que identificar certo quem está sendo mencionado
