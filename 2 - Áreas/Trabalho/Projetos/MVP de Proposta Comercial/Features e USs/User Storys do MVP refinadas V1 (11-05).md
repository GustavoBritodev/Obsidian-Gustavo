---
tags:
  - tipo/geral
status: rascunho
---

#HNS/UserStorys/MVPPropostaComercial
## User Story: 1. Feature: Gestão de Acesso (Proteção por Senha)

**Como** Consultor Comercial, 
**Quero** definir uma senha para a proposta técnica, 
**Para** que a visualização do conteúdo seja restrita apenas a stakeholders autorizados pelo cliente.

**Regras de Negócio:**

* **RN01:** A definição da senha é obrigatória para que o link seja gerado.
  
* **RN02:** A senha deve ser uma string alfanumérica (letras e números).
  
* **RN03:** O sistema não deve carregar/renderizar o conteúdo da proposta no DOM antes da validação da senha para evitar inspeção de código.

**Critérios de Aceite:**

* **AC01:** Ao acessar a URL da proposta, o sistema deve exibir um _overlay_ (modal) de segurança bloqueando todo o conteúdo.

* **AC02:** Deve existir um campo de input obrigatório no overlay (modal) de segurança para inserção da senha.

* **AC03:** O botão "Acessar" deve validar a senha via requisição; se correta, o modal é removido e a proposta é exibida; se incorreta, exibe a mensagem de erro: "Senha incorreta. Tente novamente".

---
## User Story: 2. Feature: Geração de Proposta

**Como** Analista do HNS, 
**Quero** orquestrar a geração de uma proposta web funcional, 
**Para** que o cliente receba uma proposta técnica interativa e baseada nos insumos coletados.

**Regras de Negócio:**

* **RN01:** O sistema deve suportar dois fluxos de entrada: via API Lovable (Envio de prompts estruturados via CCT) ou via importação manual do arquivo .ZIP contendo o código fonte. 
  
* **RN02:** A proposta deve ser gerada obrigatoriamente a partir de um template e um tipo de proposta enviados junto ao prompt/skill para garantir a padronização visual.

* **RN03:** A URL gerada deve ser única por oportunidade e persistente (não expirar durante o ciclo de follow-up).

**Critérios de Aceite:**

* **AC01:** Interface de orquestração deve permitir selecionar o template e enviar a de geração da proposta.

* **AC02:** Após a conclusão do processamento e a validação técnica da proposta pelo analista de HNS, o sistema deve disparar automaticamente uma notificação via e-mail ao Consultor Comercial responsável (Dono da Conta), informando que o material está pronto para a etapa de configuração de acesso e envio ao cliente.

* **AC03:** O sistema deve fornecer uma funcionalidade de visualização prévia (Preview) que permita ao analista de HNS validar a integridade técnica e a aderência ao template da proposta gerada, antes de confirmar a conclusão da etapa e liberar o acesso para o time Comercial.      

---
## User Story: 3. Feature: Conversão Imediata (Botão de WhatsApp)

**Como** Cliente, 
**Quero** ter um canal direto de contato com o responsável pela conta dentro da proposta, 
**Para** que eu possa sanar dúvidas técnicas ou comerciais sem sair da página.

**Regras de Negócio:**

* **RN01:** O número do WhatsApp deve ser populado dinamicamente com base no `Account_Owner` da oportunidade no CRM/CCT.

* **RN02:** A mensagem pré-configurada deve utilizar variáveis dinâmicas (Nome do Consultor e Nome da Empresa Cliente).

**Critérios de Aceite:**

* **AC01:** Exibir um botão flutuante (CTA) de WhatsApp visível em todas as seções da proposta gerada.

* **AC02:** Ao clicar, deve abrir o WhatsApp Web/App com a mensagem: _"Olá, [Nome do Consultor], estou visualizando a proposta da [Empresa Cliente] e gostaria de tirar uma dúvida."

* **AC03:** O sistema deve disparar um evento `onClick` para o dashboard de Analytics sempre que o botão for acionado.

---
## User Story: 4. Feature: Monitoramento de Comportamento (Clarity)

**Como** Consultor Comercial, 
**Quero** monitorar a interação do cliente com a proposta, 
**Para** identificar quais seções geram mais interesse ou possíveis pontos de confusão (atrito).

**Regras de Negócio:**

* **RN01:** O snippet de rastreio do Clarity deve ser carregado de forma assíncrona em todas as propostas para evitar impactos na performance de carregamento da página.

* **RN02:** O monitoramento comportamental e a gravação de sessão só devem ser iniciados após a validação bem-sucedida da senha de acesso.

* **RN03:** Deve-se configurar o mascaramento automático de dados sensíveis (Masking), garantindo que apenas o comportamento de navegação e a interação com a estrutura da página sejam capturados.

* **RN04:** O sistema deve associar cada sessão do Clarity ao **ID único da proposta**.   

**Critérios de Aceite:**   

* **AC01:** O sistema deve disponibilizar mapas de calor (Heatmaps) que demonstrem cliques, movimentos e profundidade de rolagem por seção da proposta.

* **AC02:** O dashboard deve identificar automaticamente eventos de **Rage Clicks** e **Dead Clicks** para sinalizar problemas de usabilidade.

* **AC03**: Deve ser possível reproduzir a jornada visual do usuário, simulando sua interação com os elementos da aplicação.

* **AC04:** A gravação da sessão no Clarity deve possuir um vínculo rastreável dentro dos relatórios de eventos do Google Analytics 4.       

---
## User Story: 5. Feature: Alerta de Engajamento (Notificações)

**Como** Consultor Comercial, 
**Quero** ser alertado em tempo real sobre o acesso do cliente, 
**Para** que eu possa realizar o follow-up no momento de maior engajamento.

**Regras de Negócio:**

* **RN01:** O gatilho de notificação só deve ser disparado após o sucesso na autenticação da senha.

* **RN02:** O sistema deve classificar acessos recorrentes: se houver mais de 5 acessos no mesmo dia, a notificação deve conter o prefixo "[HOT LEAD]".

**Critérios de Aceite:** 

* **AC01:** Envio de notificação imediata via Pipedrive (Atividade) ou E-mail após o primeiro acesso.

* **AC02:** O corpo da notificação deve conter: Nome da Empresa, Nome da Proposta e o link direto para o dashboard de acompanhamento de métricas.

* **AC03:** Visualizar no Painel de Analytics a data e hora exata de cada acesso bem-sucedido.