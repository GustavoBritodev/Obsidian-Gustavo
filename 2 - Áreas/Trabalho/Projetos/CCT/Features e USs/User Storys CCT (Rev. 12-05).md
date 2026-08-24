---
tags:
  - tipo/geral
status: rascunho
---

#HNS/UserStorys/CCT
### User Story: 2.2 Ajustar o fluxo de tracking no envio de propostas para o comercial

**Como** Gestor de Operações, 
**Quero** que o rastreio de tempo entre o HNS e o Comercial seja preciso, 
**Para** que os indicadores de Lead Time reflitam o desempenho real da equipe técnica.

**Regras de Negócio:**

* **RN01:** O cronômetro da etapa "HNS -> Comercial" deve ser disparado no exato momento em que o analista de HNS altera o status para a fase que sinaliza o fim da construção técnica.

* **RN02:** O encerramento deste tracking específico deve ocorrer quando o Consultor Comercial realiza a primeira interação documentada ou o envio formal ao cliente.

**Critérios de Aceite:**

* **AC01:** Os indicadores de "Lead Time" no modal de detalhes devem exibir o tempo decorrido sem atrasos de processamento.

* **AC02:** O componente "Tempos de Resposta" no Dashboard deve refletir os dados ajustados para a transição "Envio da Proposta até Aguardando Assinatura de Contato".

---
### User Story: 2.3 Padronizar o fluxo e a nomenclatura dos status das propostas

**Como** Usuário do Sistema, 
**Quero** que os nomes e a ordem dos status sejam uniformes em todas as telas, 
**Para** evitar confusão sobre o estágio atual de uma oportunidade.

**Regras de Negócio:**

* **RN01:** A nomenclatura deve seguir estritamente a ordem: Novo, Entendimento, Construção, Em Revisão, Entregue e Cancelado.

* **RN02:** Esta padronização deve ser aplicada de forma global, substituindo qualquer termo divergente em gráficos, filtros e tabelas.

**Critérios de Aceite:**

* **AC01:** O filtro "Todos os Status" na tela de Propostas deve exibir a lista padronizada.

* **AC02:** O gráfico de "Pipeline Ativo" no Dashboard deve utilizar as mesmas legendas e cores definidas na padronização.

* **AC03:** A "Linha do Tempo" no modal de detalhes deve refletir a sequência lógica acordada.

---
### User Story: 2.4 Alterar automaticamente o status da entrega para “Em Revisão” quando houver solicitação de ajuste no e-mail de entrega

**Como** Analista de HNS, 
**Quero** que o status da proposta mude automaticamente para "Em Revisão" ao receber um pedido de ajuste, 
**Para** que eu possa agir rapidamente sem necessidade de atualização manual pelo comercial.

**Regras de Negócio:**

* **RN01:** O gatilho deve ser ativado por uma integração que identifique solicitações de ajuste originadas do fluxo de e-mail de entrega.

* **RN02:** Ao transitar para "Em Revisão", o sistema deve registrar uma entrada automática na "Linha do Tempo" da proposta.

**Critérios de Aceite:**

* **AC01:** O status da proposta na listagem principal deve mudar visualmente para "Em Revisão" imediatamente após o gatilho.

* **AC02:** O volume de propostas no Dashboard deve ser atualizado para refletir o incremento na categoria "Em Revisão".

---
### User Story: 2.6 Adicionar no card da proposta um checkbox de fechamento, indicando se foi fechado ou não

**Como** Usuário do CCT, 
**Quero** marcar propostas como "Fechadas" através de um checkbox, 
**Para** distinguir projetos convertidos em contrato assinado de propostas apenas finalizadas.

**Regras de Negócio:**

* **RN01:** O checkbox de fechamento deve estar disponível apenas para propostas que já atingiram estágios avançados do pipeline (ex: Aguardando Assinatura).

* **RN02:** Marcar este campo não deve alterar o status da proposta, mas sim adicionar uma tag de "Conversão" para fins de visualização e relatório.

**Critérios de Aceite:**

* **AC01:** Incluir o checkbox na linha da proposta dentro da tabela de visualização geral de propostas.

* **AC02:** O indicador de contrato assinado deve ser visível dentro do modal de detalhes da proposta.

---
### User Story: 2.7 Implementar SLA de estimativas, permitindo visualizar o tempo gasto em cada etapa do processo

**Como** membro do time de HNS, 
**Quero** visualizar o tempo gasto em cada etapa interna (Entendimento e Construção), 
**Para** identificar gargalos produtivos e garantir o cumprimento dos prazos acordados.

**Regras de Negócio:**

* **RN01:** O sistema deve cronometrar o tempo de permanência nos status "Entendimento" e "Construção".

* **RN02:** Deve haver uma comparação visual entre o tempo gasto e o "Tempo Alvo" (SLA) definido para cada tipo de solicitação.

**Critérios de Aceite:**

* **AC01:** Exibir o tempo acumulado por fase no componente "Indicadores de Lead Time".

* **AC02:** A "Linha do Tempo" deve mostrar o tempo de duração de cada estágio já concluído.

---
### User Story: 2.9 Ajustar o dashboard para os dados corretos de SLA

**Como** Gestor, 
**Quero** que os gráficos de SLA apresentem dados auditados e corretos, 
**Para** que as decisões estratégicas sejam baseadas em métricas reais.

**Regras de Negócio:**

* **RN01:** A lógica do gráfico "SLA de Entregas (Consolidado)" deve considerar os novos parâmetros de tracking ajustados na US 2.2.

* **RN02:** Os dados devem ser agrupados corretamente nas categorias: "Até 1 dia útil", "Até 5 dias úteis" e "Fora do Prazo".

**Critérios de Aceite:**

* **AC01:** O gráfico de barras deve exibir a distribuição mensal correta conforme os novos cálculos de SLA.

* **AC02:** O widget de "Start Operacional" deve listar as propostas e seus tempos de SLA de acordo com a nova fonte de dados.