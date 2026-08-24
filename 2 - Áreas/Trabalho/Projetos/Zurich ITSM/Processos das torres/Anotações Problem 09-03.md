---
tags:
  - tipo/trabalho/projeto/zurich_itsm
---
#Suporte/Zurich/ProcessoProblem
Problem 

Adicionar depois PTASKs para análise de laudo

A partir de agora quando for fechar um laudo RCA ela deve abrir uma PTASK para análise de Laudo

Ela deve inserir Análise de Laudo no campo de descrição resumida

Quando receber um Laudo de RCA ela deve ler o laudo e entender pra quem está sendo direcionado

Essas informações costuma vir nos primeiros campos, 

Deve se atentar com o INC que vem no laudo e se ele está batendo com o que vem na PRB no ServiceNow

Descrição, Grupo de atribuição, Responsável, Prazo de entrega, complexidade e critério de aceite também tem que estar batendo com a PRB no ServiceNow


Para a liberação do acesso para incluir a análise do laudo ela deve abrir a PTASK, ir em Mais opções (três pontinhos) clica em Mostrar/ocultar barra de modelos e então escolhe o modelo correspondente de acordo com o que viu na PRB (Para análise de laudo enviar para Luan ou Jonatas de acordo com o portfólio e para tarefa de acompanhamento no nome da Estela)  clica os três pontinhos, ela deve buscar o Análise de Investigação de Laudo em Filtras Modelos e seleciona a análise de laudo e o template já vai aparecer e após isso ela pega a PRB abre o Problem Manager e espelha o que tem na PRB na PTASK, espelha dados como prioridade e se atentar na causa raiz, se for baixa avaliar a severidade e preencher a o campo target date (5 dias pra frente da PRB para alta, etc....)

No campo Task Purpose é Strategic quando for investigação e quando mitigação é Mitigate RC e após isso pegar o Laudo que estava na Task anterior de investigação de versão

sempre verificar o último laudo anexado na seção de Atividades

Após isso pega Id da PRB, abre base change e verifica as informações e então busca a PRB no Azure DevOps e cria uma PTASK na child da PRB com os dados da PTASK de análise de laudo

Após isso voltar na Base Change, busca pela PRB correspondente e altera a coluna Status Atual para Análise de Laudo RCA e na coluna Atualização linha do tempo muda para [Problem Manager] Análise de laudo RCA, e na coluna da Atividade do dia adicionar a data que está no ServiceNow e no Azure DevOps e também adiciona o número da PTASK na coluna da PTASK

Após isso copia o link da PTASK no Azure DevOps e cola na coluna Azure e também altera a coluna portfólio para o portfólio novo (Problem management) e também a coluna responsável para o responsável de Análise de laudo RCA.

----------------------------------------------------------------

tarefas com segunda versão de laudo em aberto não é possível marcar a apresentação do RCA caso estejam com pendência de entrega do responsável do portfólio, verifica  no azure se enviaram o laudo e se enviaram fechar (documentar no azure que está fechando (campo de discussion) e adicionar no service now print e interação do porque que ta fechando) a tarefa e caso não enviaram cobrar os responsáveis (abertura da tarefa para investigação de laudo)

-----------------------------------
Pontos a adicionar na documentação de Problem:

Em uma PRB que não aparece a PTASK pois está na sprint anterior, ao alterar a due date, alterar também o campo iteration para a sprint correta

-------------------------------------------------------------------------------

Em casos de desligamento de funcionário que ainda possuem PTASKs atribuídas a si, executar o processo abaixo:

2 vezes no dia ela tem que verificar se as PTASKS que são tarefa de acompanhamento e alterar o nome do responsável atribuído para Estela Figaro (Sub Coordenação de ITSM)

O processo consiste em abrir a tela de Problem Manager do ServiceNow, ir em tarefas em pendência, exportar um excel com as tarefas em pendência e filtras pelo nome de funcionários atribuídos que foram desligados

Em casos de tarefa de acompanhamento quando chegar próximo do fim da data da causa raiz, prorrogar a data para dois meses adiante.

-----------------------

