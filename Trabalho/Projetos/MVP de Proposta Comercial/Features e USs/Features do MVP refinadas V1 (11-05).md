#HNS/Features/MVPPropostaComercial
## 1. Gestão de Acesso: Camada de Proteção por Senha

**O que é:** Um controle de segurança granular onde o emissor da proposta define a credencial de visualização.

- **Detalhamento Funcional:**
    
    - **Painel Admin:** No momento da finalização da proposta (Etapa 5), o Comercial deve ter um campo de input obrigatório para definir uma "Chave de Acesso" (string alfanumérica).
        
    - **Lógica de Validação:** Ao acessar a URL da proposta, o sistema deve interceptar a visualização com um _overlay_ de segurança (modal). O conteúdo da Proposta Técnica só deve ser renderizado após a validação da senha.

## 2. Geração de Proposta

**O que é:** O processo técnico onde o analista de HNS transforma os insumos comerciais em uma aplicação web funcional através do Lovable.

- **Detalhamento Funcional:**
    
    - **Interface de Orquestração (CCT/Lovable):** O analista de HNS aciona a geração da proposta através de um dos fluxos a serem definidos:
			- _Via API:_ Envio de prompts estruturados diretamente pelo chat do CCT via API do Lovable.
			- _Via Importação:_ Geração direta na plataforma desejada com posterior importação do código fonte ao CCT.
        
    - **Skill & Template Mapping:** O motor utiliza "Skills" específicas para a proposta dentro de um template pré-definido para cada tipo de proposta.
        
    - **Output:** A proposta é gerada como uma URL única que contém toda a estrutura navegável da proposta técnica.
        
    - **Hand-off:** Após a validação do HNS, a URL da proposta é vinculada à oportunidade e segue para a etapa de Configuração de Acesso (Feature 1), onde o Comercial assume o controle para definição de senha e envio.

## 3. Conversão Imediata: Botão de WhatsApp "Account Owner"

**O que é:** Um gatilho de contato direto que vincula o cliente ao responsável comercial daquela proposta específica.

- **Detalhamento Funcional:**
    
    - **Atribuição Dinâmica:** O link do WhatsApp não deve ser fixo. Ele deve ser gerado com base no perfil do "Dono da Conta" que solicitou a proposta.
        
    - **Mensagem Pré-configurada:** Ao clicar, o WhatsApp abre com uma mensagem automática: _"Olá, [Nome do Consultor], estou visualizando a proposta da [Empresa Cliente] e gostaria de tirar uma dúvida."_
        
    - **Rastreamento:** Cada clique no botão deve disparar um evento de "Conversão" para o dashboard de Analytics, permitindo medir a eficácia do CTA.

## 4. Monitoramento de Comportamento: Integração Microsoft Clarity

**O que é:** Implementação de telemetria visual para entender a "temperatura" do interesse do cliente.

- **Detalhamento Funcional:**
    
    - **Mapeamento de Heatmaps:** Identificar quais seções da proposta técnica retêm a atenção do cliente por mais tempo.
        
    - **Session Recording:** Gravação da jornada do usuário para detectar "Rage Clicks" ou confusão em partes específicas do texto técnico.

## 5. Alerta de Engajamento: Notificações em Tempo Real

**O que é:** Sistema de "early warning" para o time comercial agir no momento de maior interesse do cliente.

- **Detalhamento Funcional:**
    
    - **Gatilho (Trigger):** Notificação disparada no exato momento do primeiro acesso bem-sucedido (após digitar a senha correta).
        
    - **Canais:** Envio de mensagem para o Pipedrive ou e-mail, contendo: Nome da Empresa Cliente, Proposta Acessada e Link para o Dashboard de acompanhamento.
        
    - **Inteligência de Acesso:** Diferenciar "Primeiro Acesso" de "Acessos Recorrentes". Se o cliente abrir a proposta 5 vezes no mesmo dia, o alerta deve subir a prioridade para o comercial.

