---
tags:
  - tipo/trabalho/projeto/zurich_itsm
---
Tags: #Prompt #Trabalho #Zurich

Bom dia, ChatGPT! Você é um Analista de Negócios e Processos especialista em Suporte e ITSM na empresa Zurich, sua especialidade será na escrita de POPs que nada mais são do que documentos operacionais que descrevem a operação de uma frente de atuação da empresa Mosten dentro da Zurich.

O POP da vez será o POP de Configuration Management, esse POP eu já iniciei o processo de elaboração porém não ficou dentro da realizada da operação da Mosten, então recentemente entrevistei a responsável pela operação da torre de Configuration Management da Mosten dentro da Zurich e anotei todo o passo a passo da operação e é a partir dessas anotações que você deve estruturar o POP de Configuration Management.

Para complementar e embasar alguns tópicos, enviarei em anexo um POP antigo da Zurich sobre a torre de Configuration Management, porém lembre-se nosso foco será descrever a operação atual da torre de Config da Mosten, logo você deve utilizar essas outras informações contidas no POP da Zurich apenas caso necessário para complementar ou explicar algum ponto.

Para auxiliar na estruturação e no modelo do documento, irei enviar em anexo um template de POP e também o POP antigo que eu havia feito, porém não reflete a realidade da operação nesse momento, utilize eles apenas como modelo de estrutura de escrita.

Como saída esperada peço que envie em formato de texto aqui no chat da nossa conversa o POP estruturado.

Caso identifique algum ponto com lacunas ou explicação frágil, peço que me sinalize antes de estruturar o POP para que eu explique e assim você consiga estruturar o POP da maneira correta e sem precisar inventar informações.

Segue abaixo as anotações da entrevista com a responsável pela torre de Config que mencionei anteriormente e que você deve utilizar para estruturar o POP que reflita a operação atual:


Processo Config 05/03:

Começa pelo painel que mostra os chamados

olha os chamados abertos, quando pega um chamado ele vai pra chamado que estão sendo Tratados e quando ta aguardando os times terminarem as tasks ela move pra chamados pausados e o status fica como pendente

tem três tipos de chamados: cadastro de aplicação, atualização de aplicação e descomissionamento de aplicação

Pra identificar o tipo olhar o campo Tipo de Solicitação

pra atualização não precisa abrir tarefa para nenhum time (mais simples)

Todos os dias ela tem que entrar em todos os chamados que ainda estão em aberto, vai até tarefas de catalogo, verifica o campo Estado de cada grupo e atualiza no campo Atualização diária passando o status de cada grupo.

Dentro do POP ela consulta o que cada tipo de Task precisa de informação e cobra via Teams se tiver faltando alguma informação no chamado aberto.

Sempre em chamados de Descomissionamento ou Cadastro ela segue a cola do POP para saber quais as informações são necessárias para cada task e cada task tem um grupo responsável, em todos os chamados tem que ter as 7 checklist sendo uma pra cada grupo.

A atualização é um processo diário e para chamados em que todos os times finalizaram as respectivas tarefas ela vai em atualização diária e inclui que o chamado foi encerrado totalmente porque todos os times encerraram as devidas tasks.

Pra encerrar um chamado ela vai em tarefas de catálogo e vai na task de BRZ_IT_ITSM_Configuration_Management e vai em Estado e muda pra Encerrado totalmente e com isso o chamado é encerrado de vez. (Válido para os 3 tipos de chamados)

----------------------------------------------------------------------

Atualização de aplicação:

Dentro do chamado tem a descrição da solicitação que é onde vem o que tá sendo pedido para ser atualizado
pra atualizar ela vai em catalogo de serviços -> CSDM -> Business Application Onboarding Maintence -> Atualizar um aplicativo comercial ativo -> Pegar o nome da aplicação na descrição (dentro do chamado) -> Volta pro Business Application e cola o nome da aplicação no campo Número de contato

Então ela vê qual campo foi solicitado pra atualizar e dentro da tela de Business Application clica em Solicitar agora

Após isso a aplicação é atualizada e ela volta pro chamado e coloca uma mensagem pro solicitante confirmando a atualização e passa o número da requisição que foi gerada ao fazer a atualização

EX: Mandou mensagem pro solicitante e pega as anotações diárias coloca no campo Anotações de Trabalho e muda o status para encerrar totalmente e coloca que o motivo é que foi concluída a atualização da aplicação, com isso o chamado é finalizado e vai para chamados concluídos.

-------------------------------------------------------------------------

Chamados de descomissionamento:

Assim que cai um chamado de descomissionamento o primeiro item a ser verificado são os anexos de aprovação de Bussiness Owner e proprietário superintendente de TI, caso não tenha esses anexos ela chama o solicitante no Teams e cita que está faltando essas aprovações em anexo para que possa dar continuidade no processo. Caso ele não tenha essas aprovações no momento, ela informa que vai encerrar o chamado e que o solicitante abra outro quando possuir as aprovações.

Dentro da descrição vem o checklist de conformidade
Nesse checklist ela abre as tasks pros times
cada item do checklist é uma task 
Ela pega cada item do checklist e caso marcado sim ela pega o campo que ele preencheu,
scrolla a tela pra baixo e vai até tarefas de catálogo, clica em novo e então o SN vai abrir uma Task e coloca na descrição o que foi preenchido como sim do checklist e pega os dados da aplicação (Nome da aplicação e ID de correlação da aplicação), na descrição resumida e no Grupo de atribuição (time que vai realizar a tarefa) ela pega no POP de Config, após isso ela aperta em Salvar e então a task está criada e fica para responsabilidade do grupo atribuído.

Caso o item do checklist estiver marcado como não, ela vai em tarefa de catalogo, clica em novo e na tela da task ela coloca na descrição os dados da aplicação e o que o solicitante colocou no checklist (Motivo de ter marcado como não)

No grupo de atribuição ela coloca o grupo de Config = BRZ_IT_ITSM_Configuration_Management (nosso) e vai atribuir a quem está atendendo o chamado (no caso ela)

após isso ela inclui uma atualização diária passando o status Encerrado e colocando o motivo do solicitante ter marcado como não
após isso ela muda o campo Estado para Encerrado totalmente e clica em Salvar, com isso o chamado de Descomissionamento é encerrado.

Ela segue o mesmo processo para todos os checklists da descrição (Sempre tem que ter 7 tasks no chamado)

--------------------------------------------------------------------------------------------

Cadastro de aplicação:

Para cadastro de aplicação o chamado deve ter em anexo a ata do comitê de arquitetura (caso não tenha, seguir mesmo processo de descomissionamento, cobrar solicitante...)

Identifica o tipo de chamado no campo Tipo de Solicitação e verifica os checklists, para abrir as tasks de cada checklist ela deve verificar as Características Técnicas para poder criar a aplicação
Com isso ela vai em Catálogos de Serviço -> CSDM Management Requests -> Business Application Onboarding and Maintenance -> Selecionar o tipo de solicitação -> Criar um novo aplicativo comercial -> Selecionar o tipo de aplicação empresarial -> Aplicação ou Application Component (Para saber qual deles é ela vai na wiki de config e verifica se na descrição do chamado ela se encaixa em Aplicação ou Application Component)
Após isso ela preenche os demais campos com base no que foi incluído na descrição do chamado no trecho de Características Técnicas, com todos os campos preenchidos ela clica em Solicita agora e após o clique o SN gera um número, com esse número ela volta no chamado e adiciona um comentário informando ao solicitante que foi concluído o cadastro da aplicação e informa o número gerado
Após isso ela pega o checklist e vai abrindo as tasks pros times (a partir daqui, segue o mesmo processo de descomissionamento)

------------------------------------

Outra responsabilidade é realizar monitoramento contínuo e em todos os cards apresentados no PowerBI devem estar zerados (Total Apps, Certified, Completeness, Quality, Failed KRI 01 e Existing KRI 01), caso não esteja zerado ela verifica ao aplicação está gerando não conformidade e verifica o porque, o porque fica em uma das colunas marcada em vermelho, Exemplo no caso de Assess Bussiness Owner Email é porque o responsável pela aplicação foi desligado da empresa, cada coluna tem um motivo e a problemática fica marcada em vermelho.

Em casos como esse ela abre um incidente para essa aplicação indo em Incidente -> Criar novo -> Pra abrir incidentes já possuímos um modelo pré-definido indo nos três pontinhos no canto inferior direito -> Filtrar modelos -> Digitar config -> Na última opção tem Apresentou Inconformidade -> Selecionar essa e então o SN abre um modelo pré-definido e ela preenche os campos.

Nos campos de Solicitante e Usuário Impactado ela preenche com o nome dela, em IC afetado ela pega o Name da aplicação em uma das colunas no PowerBI, vai no SN clica em Aplicações de Negócios na sidebar, e pesquisa o nome no Campo Nome, copia o nome e cola em IC afetado e então ele vai aparecer para seleção, na descrição ela cola o nome da aplicação, o ID de correlação (apresentado na tela de Aplicações de Negócios com o nome pesquisado), e digita o motivo da inconformidade e no caso do exemplo ela solicita pra informarem o nome do novo Business Owner, com isso ela volta em Aplicações de Negócios, copia o Grupo de Suporte e cola em Grupo de Atribuição na tela de Novo Incidente, com isso ela clica em salvar e cria um incidente para o grupo atribuído.
quando eles tiverem o nome do novo business owner eles tem que abrir um chamado de volta pra Config solicitando atualização da aplicação e na descrição ele menciona o nome do novo Business Owner

Em alguns tipos de Inconformidade não há como prever, exemplo do Business Owner, mas em outros casos ela verifica o POP e procura o passo a passo para iniciar a correção de inconformidade

De 15 em 15 dias ela vai no POP e clica no Link da seção de Passos para iniciar a correção de inconformidade, com o Link aberto ela clica na coluna de ID de correlação, Exportar -> Excel
Com isso a máquina realiza o download do excel, ela adiciona o rótulo de Public, vai na coluna Data de término de contrato, aplica um filtro e filtra pelo ano de 2026, caso tenha uma para uma data próxima então ela abriria um incidente pra alterar essa data pra que não vire inconformidade

Caso não tenha aplicações com a data de término de contrato próxima ela vai aplica o filtro na coluna de Data de início e filtra pelo ano de 2026 e seleciona o mês atual, caso possua aplicações ela deve verificar quando tiver próximo e abrir um incidente pra cada aplicação solicitando uma nova data, passo a passo de incidente é o mesmo do template...