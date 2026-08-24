---
tags:
  - tipo/trabalho/projeto/zurich_itsm
---
Boa tarde, ChatGPT! Você é um Analista de Negócios e Processos especialista em Suporte e ITSM na empresa Zurich, sua especialidade será na escrita de POPs que nada mais são do que documentos operacionais que descrevem a operação de uma frente de trabalho da empresa Mosten alocados na Zurich.

O POP da vez será o POP de Incident Management, esse POP eu já iniciei o processo de elaboração, porém não ficou alinhado com a proposta da documentação, que é documentar as atividades realizadas pela Torre (Frente de trabalho) do time da Mosten alocada na Zurich.

Sabendo da proposta do documento, recentemente conduzi algumas entrevistas com o responsável pela operação da torre de Incident Management da Mosten dentro da Zurich e anotei todo o passo a passo da operação e é a partir dessas anotações que você deve estruturar o POP de Incident Management.

Para complementar e embasar alguns tópicos, enviarei em anexo o POP que iniciei sobre Incident Management e também alguns POPs antigos da Zurich sobre a torre de Incident Management, porém lembre-se nosso foco será descrever a operação atual da torre de Incident Management, e a operação está descrita nas minhas anotações, logo você deve utilizar essas informações contidas nos POPs anexados apenas caso necessário para complementar ou explicar algum ponto.

Para auxiliar na estruturação e no modelo de documento, irei enviar em anexo um template de POP e também o POP antigo que eu havia elaborado, porém não reflete 100% a realidade da operação nesse momento, utilize eles como modelo de estrutura de escrita.

Como saída esperada peço que envie em formato de texto aqui no chat da nossa conversa o POP estruturado.

Caso identifique algum ponto com lacunas ou fragilidades na explicação, peço que me sinalize antes de estruturar o POP para que eu explique e assim você consiga estruturar o POP da maneira correta e sem precisar inventar informações.

Segue abaixo as anotações da entrevista com o responsável pela torre de Incident Management que mencionei anteriormente e que você deve utilizar para estruturar o POP que vai refletir a operação atual:

Torre de Incidentes:

Torre de Incidentes -> Delegação de demanda

Se alguém tem um problema vão falar com a torre de incidentes, e dentro do processo avaliam o impacto pra empresa pra avaliar se abre uma severidade (war room) ou apenas prioriza o incidente.

Ex: Contato costuma chegar via teams e pede pra ele priorizar uma demanda

Time de monitoramento é pra quem é demandado as demandas servidor, banco e SO

Demanda chega pra torre de incidentes e ela demanda pro time de monitoramento em casos de banco de dados, sistemas operacionais e servidores.

Time de monitoramento são da Tivit e fazem a ponte com os times internos responsáveis por Sistemas Operacionais, Middleware e Banco de dados.

---------------------

Severidade

Usuário e/ou identifica necessidade de severidade

Regras por severidade: não pode ser aberta por quem é do time de TI do portfólio responsável e o chamado não pode ter mais de 2 dias de abertura para poder abrir a severidade

Para abrir severidade/incidente o responsável pelo portfólio pode abrir se conter evidências no chamado

Com a severidade aberta o próximo passo do responsável da torre de incidentes é abrir a planilha chamada calculadora de severidade (Planilha Severity Sev) e preencher a aba Severity Details, onde ele pega o resumo e problema reportado no chamado e preenche os campos: Incidente Creation Date and Time, Incident Number, Issue Reported, Country and Service Line Impacted, Business Impacted, Main actions performed so far, Has a workaround or mitigation been implemented to reduce business impact? If not, why?, BU Major incident Manager, Teleconference Teams Room.

A calculadora de severidade (Aba Severity Calculator) trabalha com os fatores de cálculo na coluna factor sendo eles o número de usuários afetados (Number of user affecteds), Tempo de parada do sistema (Outage duration), Impact (Impacto), Business Sensitivity (Impacto no Negócio).

Com base nos pontos calculados se der 0-1 (Very Low), 2-3 (Low), 4-5 (Medium), 6-7 (Major), 8+ (Critical).

Em casos de Major (Confirm if 3 Watch List) cabe a torre de incidentes verificar o impacto a mais de uma unidade de negócio (País), caso afete mais de uma abre o Major e aciona Latam e comunica os responsáveis (Diretora de TI, Superintendente de TI) 

Até o nível médium, o Incident Manager salva a versão de cálculo da planilha e renomeia com o número de cálculo da severidade, o ID da severidade e uma breve descrição e envia por e-mail para o superintendente de TI (Marcos Schiavinatto) na caixa chamada Gerenciamento de Serviço solicitando o de acordo com o assunto do e-mail sendo o mesmo nome do arquivo e o mesmo nome da war room

O e-mail é enviado para o Marcos Schiavinatto em cópia para o Sidnei Andrade (Gerente de Governança de TI) e com cópia oculta para Gerenciamento de Serviço para manter a rastreabilidade.

Caso o Marcos demore a responder o e-mail com o de acordo, acionar ele via Teams para solicitar a formalização por e-mail.

Com o de acordo do Marcos o Incident Manager abre a war room no Teams com o nome sendo o mesmo do arquivo e adiciona como obrigatório quem abriu a severidade e como opcionais todos os plantonista e todos os outros operadores da torre de incidentes e também os operadores da torre de Problem, adiciona Luan e Jonatas (Parte administrativa do processo) e também a Raphaela (Analista de Governança de TI)

As ações decididas em war room só podem ser iniciadas após o de acordo do Marcos Schiavinatto 

O tempo máximo para resolução da severidade é 48 horas aceitável e 72 com explicações do porque a demora pois pode afetar ambiente produtivo.

a torre de incidentes é responsável por conduzir a war room, entender o que está sendo feito

Como boa prática é importante anotar a data e horário das ações que foram tomadas e o uma breve descrição do que foi feito

Outro ponto é o prazo de 48  para reabertura de war room (Ex.: Severidade foi encerrada mas voltou a dar problema, então tem o prazo de 48 horas para reabertura a partir do fechamento)

Ações paralelas:

Ao chegar o email com o de acordo, a torre de incidentes deve adicionar ao chamado no ServiceNow o e-mail com o de acordo e a calculadora

Com os valores preenchidos na calculadora, marcar o campo Alto Impacto (checkbox) que vai abrir os campos para preenchimento (mesmos campos da calculadora) após isso clica em salvar

Com o encerramento da severidade cabe a torre de incidentes preencher o documento chamado Incidente Report, com os campos de descrição (Anotações com data e horário das decisões tomadas em war room), o ambiente, a solução de contorno e os próximos passos 

No cabeçalho tem os seguintes campos para serem preenchidos: Portfólio, Data, Incidente ID, Problem ID, Owner Problem, Times técnicos, Incidente Manger, Impacto, Status Atual, Duração Total, Início e Fim.

Em algumas severidades marcam um checkpoint, isto é, com a resolução da severidade agendam um checkpoint para verificar se tudo correu bem para poder encerrar de fato a severidade.

Dentro do ServiceNow tem o campo IC Afetado que dentro do ícone de informações apresenta o App ID no campo ID de correlação

Com o encerramento ou em paralelo da abertura da severidade cabe a torre de incidentes preencher a base change com os dados que vem na abertura do incidente no service now

No campo DT_ABERTURA dentro da Base change na aba BASE_SEVERIDADE é importante colocar a data e hora da abertura, coluna NIVEL_SEVERIDADE vem do cálculo da planilha de cálculo, DT_FECHAMENTO mesma lógica de DT_ABERTURA, para contar a data do fechamento deve considerar a data no service now com o campo estado Resolvido na área de atividades

No preenchimento dos campos da Base Change e Service Now para preenchimento a coluna IT_OWNER deve ser puxado do campo Responsável de TI (Service Now) e GERENTE do campo Gerenciado por (Service Now)

Para preenchimento do campo portfólio verificar quem é o superintendente de TI no organograma no Teams olhando pela pessoa que abriu a severidade

Antes de fechar a severidade é uma boa prática definir quem é o responsável pela severidade (ofensor) que então o responsável pela severidade vai interagir com a torre de Problem

Em casos de severidade que o IT Owner for Hurbem Pinto antes da abertura deve conter o de acordo da Raphaela Marques (Horário Comercial) e nos demais horários Sidnei Andrade, com o de acordo seguir o fluxo do processo (De acordo do marcos e etc...)

-----------------------------------------------------------------------------------------

Sanitização 

É uma rotina de apoio com o time de Release, onde a sanitização basicamente é um fechamento de mudanças

No ServiceNow o operador de incidentes abre a tela do grupo de Release Manager na aba Pos Implementation e abre o card de sanitização.

Ao abrir o card o sistema vai abrir uma tabela e para exportação da tabela clicar na coluna numero e extrair o excel

Com o excel extraído colocar como Public, colocar padrão de altura de linha 15, criar coluna Classificação e Observações

A coluna classificação vem com base no campo Descrição Resumida onde o operador identifica se é uma TBR ou uma RFC

Após isso ele pega o ID da mudança na coluna número, pesquisa no service now 

Com a mudança aberta, seja ela TBR ou RFC, o operador analisa e identifica o status da mudança, caso esteja em um status anterior a agendado e a data atual for maior do que 15 dias da data de abertura, cabe ao incident manager cancelar a mudança indo no menu burger do canto superior esquerdo chamado Ações adicionais e ir na opção Cancelar mudança e adicionar o Motivo (Ex.: Esperado prazo de 15 dias).

Em casos de mudanças com a data dentro do prazo, o Incident Manager verifica as tarefas de mudança, se todas as tarefas estiverem encerradas e/ou canceladas, ele pode dar sequência com o encerramento da mudança

Tendo tarefas de mudança em aberto, cabe ao operador solicitar ao responsável pela tarefa o encerramento da mesma, nesses casos é uma boa prática adicionar na planilha na coluna de observações o nome do responsável pela mudança que foi cobrado

Outra boa prática é deixar em amarelo na planilha mudanças que faltam ser cobradas e em vermelho as que já foram cobradas

Em casos em que as tarefas de mudanças estão todas encerradas, o Incident Manager pode atribuir a mudança a si mesmo para dar sequência com o encerramento

Após isso ele  inclui no campo Data de início real o mesmo valor contido no campo Data de início planejado e então seleciona o botão Salvar


Após isso o ServiceNow libera o botão implementar que ao ser selecionado a mudança passa para o próximo estágio chamado Implementar

Quando ele entra em estado de implementação ele cria duas tarefas que podem ser ignoradas e libera para preenchimento o campo Data de término real que deve ser preenchido com o mesmo valor do campo data de término planejada

E na aba de informações de Fechamento selecionar no campo Código de fechamento a opção Sucessfull e nas anotações de encerramento digita Bem-sucedido

Após isso seleciona o botão Revisão para a mudança ir para o status Revisão

Então o Incidente Manager revisa a mudança para verificar se não houve nenhum erro nos processos anteriores

Estando tudo certo ele clica no botão Fechar e a mudança vai para o status Encerrado

Com isso a boa prática é deixar a mudança encerrada em verde na planilha de sanitização e altera a coluna estado para encerrado

