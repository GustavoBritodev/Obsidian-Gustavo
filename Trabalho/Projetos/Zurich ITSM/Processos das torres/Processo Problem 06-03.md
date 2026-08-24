Tags: #Anotações #Trabalho #Zurich 

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


