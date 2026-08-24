---
tags:
  - tipo/geral
status: rascunho
---

# Perguntas — EF Tela de Vínculo e Agendamento de Retirada (Portal Tecon)

> **Escopo:** RET-01 a RET-16 · GEN-02 · GEN-04  
> **Versão do documento de referência:** 01 — 30/01/2026

---

## 1. Acesso e Permissões

### Pergunta 1

O documento menciona "representante do cliente" como perfil autorizado para realizar o vínculo de carga. Como esse papel é cadastrado ou vinculado no sistema — é um perfil específico, um CNPJ autorizado manualmente ou uma outra forma de delegação?

> **Requisito de referência — RET-01 (Quem pode vincular e quem pode agendar)**
>
> - **Vínculo (dono da carga):** perfil com mesmo CNPJ do Consignee no N4 **ou representante do cliente.**
> - **Agendamento:** somente pessoas vinculadas ao CNPJ que fez o vínculo e/ou transportadora responsável pelo frete.

---

### Pergunta 2

A regra de agendamento diz que podem agendar "pessoas vinculadas ao CNPJ que fez o vínculo e/ou transportadora responsável pelo frete". Quando ambos estão habilitados ao mesmo tempo, a permissão é independente ou há alguma precedência entre eles?

> **Requisito de referência — RET-01 (Quem pode vincular e quem pode agendar)**
>
> - **Vínculo (dono da carga):** perfil com mesmo CNPJ do Consignee no N4 ou representante do cliente.
> - **Agendamento:** somente pessoas vinculadas ao CNPJ que fez o vínculo **e/ou** transportadora responsável pelo frete.

---

### Pergunta 3

Caso o CNPJ logado não corresponda ao Consignee do N4 (RET-04), qual mensagem de erro deve ser exibida? O portal simplesmente não retorna nenhuma carga, ou exibe um aviso explícito ao usuário?

> **Requisito de referência — RET-03 (Integração N4: retorno condicionado e validações)**
>
> - Validar se o número do documento existe no N4;
> - Validar CNPJ do portal corresponde ao CNPJ (consignee) na units do N4;
> - Retornar item, commodities, dimensões e tipo de carga: Bulk ou Breakbulk que não possuam impedimento (bloqueios para saída de gate).
>
> **Requisito de referência — RET-04 (Regra de elegibilidade do usuário)**
>
> Se o perfil logado não tiver vínculo com o dono da carga, não poderá realizar o vínculo e as cargas **não serão exibidas no portal.**

---

## 2. Pesquisa e Vínculo de Carga — Tela 1

### Pergunta 4

==Quais são todos os tipos de documentos de liberação aceitos na pesquisa da tela de vínculo? O documento cita ADM e leilão como exemplos — há uma lista completa e definitiva desses tipos?== Confirmar com o Rodrigo

> **Requisito de referência — RET-02 (Pesquisa por tipo e número de documento)**
>
> Dono da carga pesquisa pelo tipo e número do documento de liberação.

---

### Pergunta 5

==Um mesmo item pode ser vinculado a mais de uma transportadora em vínculos distintos (com saldos parciais), ou o vínculo de um item deve ser sempre para uma única transportadora por vez?==

> **Requisito de referência — RET-05 (Vínculo de itens à transportadora)**
>
> Dono/representante vincula itens retornados do N4 à transportadora para permitir agendamento.

---

### Pergunta 6

Campos do N4?

> **Requisito de referência — RET-06 (Criação de Delivery Order no N4)**
>
> Ao salvar, portal envia informações para o N4 criar **Delivery Order (ordem de saída)** com cargas e quantidades; N4 retorna número da ordem e portal salva o grupo.

---

### Pergunta 7

==O requisito RET-07 permite que um grupo de cargas possua mais de um BL. Há algum limite máximo de BLs por grupo, ou é ilimitado?==

> **Requisito de referência — RET-07 (Grupo com múltiplos BL)**
>
> Um grupo de cargas pode possuir mais de um BL.

---

### Pergunta 8

==Sobre a edição da Delivery Order (RET-09 — tela de vínculo): é possível adicionar novos itens/BLs a uma Delivery Order já criada, ou a edição se limita a ajustar quantidades de itens já existentes? Ao remover itens, o N4 deve ser atualizado em tempo real?==

> **Requisito de referência — RET-09 (Edição de Delivery Order no N4)**
>
> O dono da carga poderá editar as cargas disponíveis para retiradas que ainda possuem saldo para retirada e **não foram agendadas.**

---

### Pergunta 9

==O documento menciona que o dono da carga "informa à transportadora o número da ordem de saída" (RET-08). Esse comunicado acontece fora do portal (por outros meios) ou o próprio portal deve oferecer algum mecanismo de notificação ou compartilhamento desse número?==

> **Requisito de referência — RET-08 (Comunicação para agendamento)**
>
> Dono da carga informa à transportadora o número da ordem de saída para realização do agendamento.

---

## 3. Agendamento de Retirada Break Bulk — Tela 2

### Pergunta 10

O requisito RET-09 (tela de agendamento) usa o mesmo identificador do RET-09 (edição de DO na tela de vínculo). Isso é intencional ou trata-se de um erro de numeração no documento? Qual a numeração correta para a tela de agendamento de retirada break bulk? Erro

> **Requisito de referência — RET-09 (Pesquisa por documento ou ordem de saída — Tela 2)**
>
> Ao pesquisar por tipo/número do documento ou número da Delivery Order, portal apresenta a(s) delivery order vinculadas à transportadora.

---

### Pergunta 11

==Na seleção de itens para agendamento (RET-10), a transportadora pode agendar uma quantidade parcial dos itens vinculados na DO, ou deve agendar todos de uma vez? Se parcial, o saldo remanescente fica disponível para novos agendamentos?==

> **Requisito de referência — RET-10 (Seleção de itens e quantidades — não bulk)**
>
> Se item **não bulk**, transportadora seleciona **itens** a serem retirados.

---

### Pergunta 12

Para itens em estado "inbound" (descarga direta), há alguma validação ou regra adicional além da elegibilidade de T-state? Por exemplo: confirmação de atracação do navio ou janela de tempo mínima?

> **Requisito de referência — RET-11 (Itens elegíveis por estado)**
>
> Exibir cargas com T-state **yard** ou **inbound** (inclui inbound em caso de descarga direta).

---

### Pergunta 13

O campo "motorista" no agendamento de retirada (RET-12) deve ser sempre selecionado de uma lista pré-cadastrada da transportadora, ou é possível digitá-lo livremente? Caso seja lista pré-cadastrada, quem realiza esse cadastro e por qual tela? Consultar EF de Agendamento de Entrega de Carga

> **Requisito de referência — RET-12 (Campos — retirada)**
>
> Campos a informar:
> - Motorista (cadastrados para transportadora)
> - Placa da carreta (obrigatório)
> - Placa do cavalo 1 (obrigatório)
> - Placa do cavalo 2 (se bitrem)
> - Data e hora da janela (obrigatório)
> - Itens

---

### Pergunta 14

Quando não há nenhuma janela/calendário disponível para o tipo de carga da retirada (RET-13), qual mensagem ou orientação deve ser exibida ao transportador?

> **Requisito de referência — RET-13 (Calendário e vagas — equivalente contêiner)**
>
> Sistema escolhe automaticamente calendário conforme filtros e disponibiliza vagas conforme janelas disponíveis para seleção do transportador.
>
> Caso o registro tenha mais de um calendário que seja apto para o agendamento, utilizar o que possuí maior detalhes com a carga a ser agendada.

---

### Pergunta 15

=="Agendamentos efetivados não podem ser editados" (RET-16) — qual status define que um agendamento foi efetivado? É o status "Utilizado" definido no GEN-05, ou existe um critério diferente (ex.: gate in registrado no N4)?==

> **Requisito de referência — RET-16 (Edição/Exclusão)**
>
> Usuário deve poder editar/excluir conforme tolerância do calendário e status; **agendamentos efetivados não podem ser editados**; sincronizar com N4.
>
> **Requisito de referência — GEN-05 (Status do agendamento)**
>
> Os agendamentos deverão possuir os seguintes status:
> - **Pendente** – Aguardando agendamento
> - **Agendado** – Agendamento aguardando utilização
> - **Utilizado** – Usado
> - **No Show** – Atrasado

---

### Pergunta 16

Quando o usuário exclui um agendamento de retirada dentro da tolerância permitida, o saldo dos itens retorna automaticamente para a DO e fica disponível para novo agendamento? O N4 deve ser notificado simultaneamente?

> **Requisito de referência — RET-16 (Edição/Exclusão)**
>
> Usuário deve poder editar/excluir conforme tolerância do calendário e status; agendamentos efetivados não podem ser editados; **sincronizar com N4.**
>
> **Requisito de referência — GEN-01 (Sincronização com N4)**
>
> Em qualquer edição/exclusão permitida, sempre sincronizar com N4 para manter equivalência entre sistemas.

---

## 4. Integração SILOG

### Pergunta 17

Na falha técnica do SILOG (GEN-02), o agendamento é impedido completamente. Existe algum mecanismo de retentativa automática, ou o usuário deve tentar novamente manualmente? Há um prazo ou número máximo de tentativas?

> **Requisito de referência — RET-14 (Integração SILOG — mesma regra)**
>
> Ao clicar "Finalizar/Agendar":
> - **Falha técnica:** erro de comunicação (impede agendamento).
> - **Não cadastrado:** "Motorista/Placas/Transportadora não cadastrado no Silog" (bloqueante).
> - **Sucesso:** prossegue.
>
> **Requisito de referência — GEN-02 (Erros SILOG)**
>
> - **Falha técnica:** impede agendamento, exibe erro de comunicação.
> - **Não cadastrado:** bloqueante.

---

### Pergunta 18

O requisito RET-14 menciona que "Motorista/Placas/Transportadora não cadastrado no Silog" é bloqueante. A validação ocorre para os três juntos ou individualmente? Caso um deles falhe, o erro aponta qual elemento específico não está cadastrado?

> **Requisito de referência — RET-14 (Integração SILOG — mesma regra)**
>
> Ao clicar "Finalizar/Agendar":
> - **Falha técnica:** erro de comunicação (impede agendamento).
> - **Não cadastrado:** "Motorista/Placas/Transportadora não cadastrado no Silog" **(bloqueante).**
> - **Sucesso:** prossegue.

---

## 5. Agendamentos Simultâneos

### Pergunta 19

O GEN-04 determina que o sistema deve impedir conflitos de agendamento simultâneo para o mesmo veículo/motorista/janela. A verificação de conflito considera apenas a placa frontal, ou inclui também a combinação placa frontal + placa traseira + motorista?

> **Requisito de referência — GEN-04 (Agendamento simultâneo)**
>
> Sistema deverá impedir conflitos de agendamento de entrega de carga, entrega de contêiner, retirada de contêiner, retirada de bulk e autorização de janela dentro do mesmo período. **Sempre exibir para o usuário qual o conflito.**

---

### Pergunta 20

Quando um conflito de agendamento é detectado (GEN-04), o portal exibe qual o tipo de conflito existente. Esse detalhe é exibido antes de o usuário tentar confirmar, ou somente no momento da tentativa de salvar?

> **Requisito de referência — GEN-04 (Agendamento simultâneo)**
>
> Sistema deverá impedir conflitos de agendamento de entrega de carga, entrega de contêiner, retirada de contêiner, retirada de bulk e autorização de janela dentro do mesmo período. **Sempre exibir para o usuário qual o conflito.**

---

## 6. Pontos em Aberto

### Pergunta 21

O documento indica a necessidade de "conversar com a operação" sobre o processo de bulk/granel e há trechos riscados sobre exceções de tickets bulk. Qual é a regra final definida para o fluxo de retirada bulk? Isso impacta diretamente os requisitos BULK-01 a BULK-04, que estão no mesmo escopo desta tela.

> **Nota do documento (seção "Pontos em Aberto")**
>
> O documento aponta necessidade de alinhamento com operação para o processo de granel/bulk ("conversar com a operação"), e há trechos riscados relativos a exceções/tickets bulk. Recomenda-se fechar decisão e registrar regra final.
>
> **Requisito de referência — BULK-01 (Tela de autorização/carrossel)**
>
> Criar tela de "autorização de janela" para transportador criar carrossel de motoristas e carretas autorizadas para retirada de carga bulk vinculada a ela (delivery order de bulk).

---

### Pergunta 22

As seções 6 (Manutenção de Dados) e 7 (Segurança Lógica) estão em branco no documento. Há perfis de acesso a definir para a tela de retirada (ex.: quem pode consultar, quem pode cancelar vínculo)? Há alguma regra de expiração ou arquivamento de DOs e agendamentos?

> **Requisito de referência — RET-01 (Acesso/Permissões)**
>
> - **Vínculo (dono da carga):** perfil com mesmo CNPJ do Consignee no N4 ou representante do cliente.
> - **Agendamento:** somente pessoas vinculadas ao CNPJ que fez o vínculo e/ou transportadora responsável pelo frete.
>
> ⚠️ *As seções 6 (Manutenção de Dados) e 7 (Segurança Lógica) estão sem conteúdo na versão atual do documento — solicitar preenchimento ao cliente.*

---
