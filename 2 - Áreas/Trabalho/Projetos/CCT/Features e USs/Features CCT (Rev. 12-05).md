---
tags:
  - tipo/geral
status: rascunho
---

#HNS/Features/CCT
### 2.2 Ajustar o fluxo de tracking no envio de propostas para o comercial
**Descrição:** Revisar e corrigir a lógica de gatilhos que inicia e encerra o rastreio de tempo (Lead Time) quando uma proposta é despachada do HNS para a equipe Comercial. O ajuste deve garantir que o indicador "HNS -> Comercial" reflita com precisão o momento em que a proposta fica disponível para o Comercial, evitando distorções nos gráficos de tempo de resposta.

---
### 2.3 Padronizar o fluxo e a nomenclatura dos status das propostas
**Descrição:** Unificar os nomes e a sequência lógica dos status das propostas em todos os componentes do sistema (filtros da tela de Propostas, gráficos do Dashboard e Linha do Tempo do modal de detalhes). O objetivo é eliminar discrepâncias (ex: termos diferentes para a mesma etapa) e garantir que o pipeline siga uma jornada linear e coerente para todos os perfis de usuário.

---
### 2.4 Alterar automaticamente o status da entrega para “Em Revisão” quando houver solicitação de ajuste no e-mail de entrega
**Descrição:** Implementar um gatilho de automação que detecta pedidos de alteração ou ajustes (via integração com o fluxo de e-mail de entrega). Ao disparar esse gatilho, o status da proposta deve transitar automaticamente para **"Em Revisão"**, atualizando instantaneamente o Dashboard e notificando os responsáveis de HNS.

---
### 2.6 Adicionar no card da proposta um checkbox de fechamento, indicando se foi fechado ou não
**Descrição:** Incluir um campo de seleção (checkbox) ou indicador visual na listagem principal de propostas e no modal de detalhes para marcar o "Fechamento" (Conversão/Ganho) da oportunidade. Essa funcionalidade servirá para separar propostas que chegaram ao fim do ciclo de vida da proposta daquelas que efetivamente se tornaram contratos fechados.

---
### 2.7 Implementar SLA de estimativas, permitindo visualizar o tempo gasto em cada etapa do processo
**Descrição:** Desenvolver um mecanismo de cronometragem para as etapas internas de pré-venda (como "Entendimento" e "Construção"). O sistema deve registrar quanto tempo a proposta permanece em cada fase e comparar com um tempo alvo (SLA) pré-definido, permitindo a visualização detalhada desses indicadores no modal de detalhes e na Linha do Tempo.

---
### 2.9 Ajustar o dashboard para os dados corretos de SLA
**Descrição:** Recalibrar a lógica de cálculo e a fonte de dados dos componentes de SLA no Dashboard Gerencial. Isso inclui garantir que o gráfico de "SLA de Entregas (Consolidado)" e os indicadores de "Lead Time" reflitam os novos ajustes de tracking e as métricas de tempo real, corrigindo possíveis erros de processamento de dados antigos.