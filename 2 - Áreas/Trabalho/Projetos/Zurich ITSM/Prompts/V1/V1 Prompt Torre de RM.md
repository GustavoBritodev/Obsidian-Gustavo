---
tags:
- tipo/trabalho/projeto/zurich_itsm
- Azure
- SQL
---
Tags: #Prompt #Trabalho #Zurich

Bom dia, ChatGPT! Você é um Analista de Negócios e Processos especialista em Suporte e ITSM na empresa Zurich, sua especialidade é realizar análises e mapeamentos precisos de fluxos de processo e documentos, para elaboração de documentação de AS IS e posteriormente TO BE.

Sua tarefa hoje será realizar a análise profunda dos documentos anexados referentes a torre de Release Management do ITSM da Zurich e estruturar uma documentação referente a operação atual da Mosten como Release Management na Zurich.

Você deverá seguir o template de documentação com título de "Template-Pop" e estruturar a documentação com base no template anexado.

Você deverá focar em uma linguagem precisa e descritiva com ênfase no processo AS IS (posteriormente trabalharemos no TO BE) e com foco na compreensão do leitor sobre o processo, visto que irá se tratar de uma espécie de manual/descritivo do fluxo do processo.

Afim de contextualização irei descrever brevemente o que sei sobre o fluxo de processo atual para servir de complemento aos documentos anexados.

Segue breve descritivo abaixo:

08h00 - Realizar a extração da pauta do cab e envio para a tivit, seguindo os filtros necessários (presentes no documento de DIA A DIA) no ServiceNow, para então baixar a planilha, formatar e aplicar os filtros da planilha.

08h30 - Verificar o painel das TBRS (card de TBR | Avaliar) se todas estão aprovadas (senão tiver, cobrar os grupos).

08h40 – Validar as mudanças do CAB do dia no ServiceNow:
CAB:
Toda mudança deverá ter um Work Item aberto no Azure Devops relacionado.
Todas as 15 perguntas do questionário na descrição da Mudança Normal devem ser respondidas
Verificar pergunta 11, todas as mudanças que tem alteração do código fonte devem anexar o scan do veracode
A aba "Planejamento" deve ter todos os campos preenchidos de forma clara e objetiva.
A aba "Programação" precisa estar preenchida.
No campo "Plano de Implementação" deve constar todo o passo a passo da execução do processo
O item ICs afetados deve conter o mesmo Item de configuração
Motivo: A mudança deve ter no mínimo três tarefas (Procedimento, Plano de Teste e Rollback) e devem estar direcionadas ao grupo de atribuição responsável.
A somatória das janelas das tarefas não pode ultrapassar a janela da mudança e deve conter todas as informações de acordo com o plano de implementação.

Na tarefa dentro do ServiceNow:
Abrir as tarefas de mudança que são procedimento:
se for pipeline: precisa do link do release
se for tarefa de banco: precisa do script batendo com a descrição pendência: Descrição da tarefa não esta correspondendo com quantidade de anexos da mesma, favor verificar quantidade de scripts anexados.
se for infra não precisa de nada

Com o número do Work Item (WIT) dentro do campo descrição na Change no ServiceNow abrimos o WIT no Azure DevOps:
Deverá ter de acordo da área Cliente que hoje pode ser via E-mail anexado  na aba "Attachments" ou via "Discussion" na Workitem.
Se a aprovação for por e-mail, deverá ter no corpo do e-mail o número da mudança gerado no ServiceNow e o número da Workitem.
Na sessão Development do Workitem, deve ser relacionado através do "Add Link" o Pull Request e também através do "Add Link" o Commit do código que será executado na mudança
Na sessão Development do Workitem, deve ser relacionado através do "Add Link" o Pull Request e também através do "Add Link" o Commit do código que será executado na mudança
A aba "Audit" deve ser preenchida
se tiver descrito que não tem merged não precisa do merged

09h30 - Verificar planilha de acompanhamento as mudanças aguardando aprovação, e atualizar status e cobrar as aprovações faltantes

10h00 – Realizar a validação das TBR

11h30 – Acompanhar o cab técnico

12h00 – Intervalo para o almoço

13h00 - Acompanhamento das aprovações\cobrança caso necessário

13h30 - Envio da pauta no grupo de aprovadores do cab

14h00 - Acompanhamento da planilha e revalidar as pendencias do cab

15h00 – Realizar a validação das TBR

16h00 - Acompanhamento das aprovações\cobrança caso necessário

16h30 - Validação da planilha de acompanhamento para confirmação das janelas e aprovações do CAB

17h00 – fim do expediente

OBS: Mudanças expedites e Tbr de malha, podem chegar a qualquer momento, devendo entrar no processo de validação e alinhamento conforme sla de cada uma.

Obs: Validação de Expedite é exatamente igual a uma mudança normal, mas a prioridade e o impacto não podem ser baixos e precisa de um incidente relacionado ou um item solicitado.

Atenção É importante que você cruze as informações dos documentos com a descrição que eu dei, o que divergir ou não tiver sido citado na minha descrição, pode desconsiderar do documento, tendo em vista que algumas coisas lá não refletem a atualidade da operação do Release Manager da Mosten dentro do ITSM da Zurich.

---
Gostei demais do resultado, ChatGPT! Recebi mais algumas informações com o key-user de Release Management e gostaria que você considerasse as anotações que recebi para enriquecimento do material, mas sem alterar a estrutura do documento.

Para sua resposta gostaria que enviasse os trechos que irão conter a alteração com o enriquecimento do material e depois a versão final consolidada do POP (Em formato de texto enviado via chat).
Segue abaixo as anotações que recebi:

ServiceNow:
CAB:
Toda mudança deverá ter um Work Item aberto no Azure Devops relacionado.
Todas as 15 perguntas do questionário na descrição da Mudança Normal devem ser respondidas
Verificar pergunta 11, todas as mudanças que tem alteração do código fonte devem anexar o scan do veracode
A aba "Planejamento" deve ter todos os campos preenchidos de forma clara e objetiva.
A aba "Programação" precisa estar preenchida.
No campo "Plano de Implementação" deve constar todo o passo a passo da execução do processo
O item ICs afetados deve conter o mesmo Item de configuração
Motivo: A mudança deve ter no mínimo três tarefas (Procedimento, Plano de Teste e Rollback) e devem estar direcionadas ao grupo de atribuição responsável.
A somatória das janelas das tarefas não pode ultrapassar a janela da mudança e deve conter todas as informações de acordo com o plano de implementação

Na tarefa (ServiceNow):
Abrir as tarefas de mudança que são procedimento
se for pipeline: precisa do link do release
se for tarefa de banco: precisa do script batendo com a descrição pendência: Descrição da tarefa não esta correspondendo com quantidade de anexos da mesma, favor verificar quantidade de scripts anexados.
se for infra não precisa de nada

No AzureDevOps (WIT):
Deverá ter de acordo da área Cliente que hoje pode ser via E-mail anexado  na aba "Attachments" ou via "Discussion" na Workitem.
Se a aprovação for por e-mail, deverá ter no corpo do e-mail o número da mudança gerado no ServiceNow e o número da Workitem.
Na sessão Development do Workitem, deve ser relacionado através do "Add Link" o Pull Request e também através do "Add Link" o Commit do código que será executado na mudança
"Motivo: Deverá conter evidencias de testes (Hoje não possui padrão para evidencias).
As evidencias podem ser relacionadas das seguintes formas:
1. Relacionado através do ""Add Link"" na seção Related Work da Workitem;
2. Evidenciada no campo ""Discussion"";
3. Anexar evidencias de testes na aba ""Attachments"""
A aba "Audit" deve ser preenchida
se tiver descrito que não tem merged não precisa do merged

TBRs:
ServiceNow:
Modelo precisa ser padrão
Risco baixo
Prioridade e impacto não podem estar baixo (moderado pra cima)
Ambiente produção
Categoria Database
Todas as 5 perguntas do questionário na descrição da Mudança Padrão devem ser respondidas.
A aba "Planejamento" deve ter todos os campos preenchidos de forma clara e objetiva.
A aba "Programação" precisa estar preenchida.
Para mudanças Padrão  (TBR) a janela de execução da mudança determinada pelos campos "Data de Inicio Planejada" e "Data de Término Planejada" devem estar de acordo com o turno solicitado:
SQL (Tivit): Turno 1 (07:00 as 14:00), Turno 2 (16:00 as 21:00) e Turno 3 (23:00 as 05:00)
Oracle (V8): Turno 1 (08:00 as 10:00), Turno 2 (15:00 as 17:00, até 21h se for necessário janela estendida)
ICs afetados e Serviços/CIs Impactados precisam conter o mesmo Item de configuração do campo e da descrição
Toda mudança Padrão deve ter um incidente, Problema e\ou Requisição relacionado.
A mesma aplicação relacionada a mudança, e as informações no campo "Descrição" do Incidente precisam ser condizente a solicitação de mudança
Mudanças Padrão possui somente a tarefa de procedimento.

Incidente e Tarefa:
Abrir o incidente e ver se está preenchido
abrir a tarefa de mudança e ver:
se for pipeline: precisa do link do release
se for tarefa de banco (Tivit ou V8): precisa do script batendo com a descrição (pendência: Descrição da tarefa não esta correspondendo com quantidade de anexos da mesma, favor verificar quantidade de scripts anexados.)

Azure DevOps (WIT):
Deverá ter de acordo da área Cliente que hoje pode ser via E-mail anexado  na aba "Attachments" ou via "Discussion" na Workitem.
Se a aprovação for por e-mail, deverá ter no corpo do e-mail o número da mudança gerado no ServiceNow e o número da Workitem.
Na sessão Development do Workitem, deve ser relacionado através do "Add Link" o Pull Request e também através do "Add Link" o Commit do código que será executado na mudança
No merged: Os scripts de Insert, Update e Delete devem utilizar o template padronizado. https://azuredevops.zurich.com/tfs/IT/ZurichSolutions/_git/DevSecOps.Templates.Database
"Motivo: Deverá conter evidencias de testes (Hoje não possui padrão para evidencias).
As evidencias podem ser relacionadas das seguintes formas:
1. Relacionado através do ""Add Link"" na seção Related Work da Workitem;
2. Evidenciada no campo ""Discussion"";
3. Anexar evidencias de testes na aba ""Attachments"""
A aba "Audit" deve ser preenchida

Se estiver tudo ok
no azure: marcar o solicitante e "Aprovado por Release Manager."
no servicenow: adicionar o grupo da tarefa de mudanças e o tech approval, solicitar aprovação e aprovar
se não estiver tudo ok
no azure: marcar o solicitante e descrever as pendencias
no servicenow: copiar e colar as pendências nas anotações

Antes de tudo: sempre começar pelas mudanças dos horários da Tivit, Tivit entra 4 mudanças por vez, v8 são 6 e pipe não tem limite

No final do expediente o release manager passa as pendencias para o plantonista do dia (Reunião de passagem de bastão).