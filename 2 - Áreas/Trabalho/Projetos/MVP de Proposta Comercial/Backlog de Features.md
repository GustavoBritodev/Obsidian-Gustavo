---
tags:
  - tipo/geral
status: rascunho
---

#HNS/Backlog/MVPPropostaComercial
# Lista de Features:
Autenticação de Acesso:
* Validação e autenticação de acesso de usuário para identificação do usuário e facilitação na identificação para follow-up e contatos futuros.
Notificação ao time comercial por proposta aberta:
* Notificação via e-mail para o time Comercial por proposta aberta, no e-mail deve conter o identificador da proposta e o nome do usuário que acessou.
Importação de PDF de Proposta Técnica para geração da Landing Page:
* Campo de exportação para o usuário anexar o PDF contendo a Proposta Técnica para o sistema processar e gerar a Landing Page através do PDF.
Painel de Admin:
* Painel com visão de gestão sobre as informações de comportamento do usuário dentro da proposta técnica. Provavelmente vai consolidar as funcionalidades de Mapa de Calor, Captação de Cookies e Ferramentas de Analytics e outras possíveis evoluções.
Mapa de Calor:
* Dashboard/Mapa de Calor contendo as informações de clique na Landing Page, para ajudar a mensurar se CTAs estão sendo chamativos o suficiente e sendo clicados e também outros elementos da página.
Captação de Cookies:
* Capturar cookies para criar públicos para remarketing, fortalecendo campanhas e comunicações futuras com quem já demonstrou interesse.
Ferramentas de Analytics:
* Integração com ferramentas de Analytics e/ou painel de visualização próprio dentro do painel de Admin para medir tempo médio de visualização, seções mais acessadas, páginas visualizadas, origem de tráfego e comportamento do cliente dentro da proposta.
Assistente Virtual (ChatBot):
* Chatbot dentro da proposta gerada para resposta de possíveis dúvidas do cliente/usuário sobre a proposta.
Geração do conteúdo da proposta através da transcrição:
* Geração da LP através de transcrição de reuniões com os principais pontos discutidos, dores do cliente, oportunidades, próximos passos e informações relevantes para proposta.

# Lista de Features (Refinadas e Incrementadas) V1

#### **Geração e Inteligência Artificial (Core)**
- **Integração com Read.ai:** Coleta de transcrições e resumos estruturados das reuniões comerciais para servir de insumo inicial.
- **Motor de Proposta com IA (RAG):** Processamento do conteúdo das reuniões para gerar automaticamente seções de contexto, desafios, objetivos, módulos técnicos e roadmap.
#### **Experiência do Cliente (Landing Page)**
- **Landing Page Interativa Personalizada:** Substituição do PDF por um site dinâmico sob o domínio `[mosten.com/nome-do-cliente](https://mosten.com/nome-do-cliente)`.
- **==Embed de Protótipos Navegáveis:** Integração direta de ferramentas de design para que o cliente visualize a solução proposta dentro da própria LP.==
- **Botão de Conversão "Aceite via WhatsApp":** CTA direto para facilitar o fechamento comercial imediato com o responsável pela conta.
- **Assistente Virtual (Chatbot com RAG):** Chatbot alimentado especificamente com os dados daquela proposta para sanar dúvidas pontuais do cliente em tempo real.
#### **Gestão e Rastreabilidade (Comercial & Marketing)**
- **Integração de Sinais de Interesse com Pipedrive:** Atualização automática do status do negócio (deal) quando o link é aberto ou CTAs são clicados.
- **Notificações em Tempo Real:** Alertas via e-mail ou canais internos quando um tomador de decisão acessa a proposta, identificando o usuário via autenticação.
- **Painel de Admin & Analytics:** Centralização de métricas de tempo de visualização por seção, origem de tráfego e comportamento detalhado.
- **Mapa de Calor e Comportamento:** Visualização de zonas de maior interesse (cliques e scroll) para entender quais partes da proposta técnica geram mais dúvidas ou engajamento.
- **Captura de Cookies para Remarketing:** Estruturação de audiências para campanhas de marketing direcionadas a clientes que visualizaram propostas específicas.
# Lista de Features Incrementada V2

#### **Geração e Inteligência Artificial (Core)**
- **Prompt-to-Proposal (Interface de Criação):** Uma interface de prompt (estilo chat ou "Gama") onde o Comercial descreve necessidades específicas e a IA gera a estrutura visual e textual da Landing Page.
- **Integração Figma via MCP (Model Context Protocol):** Uso de IA para ler designs elaborados no Figma e transformá-los automaticamente em código para a Landing Page, acelerando o deploy de propostas personalizadas.
- **Edição Assistida por IA:** Funcionalidade que permite ao usuário solicitar ajustes específicos (ex: "troque esta imagem" ou "mude o tom deste texto") via comandos de linguagem natural após a geração inicial.
- **Integração com Read.ai:** Coleta de transcrições e resumos estruturados das reuniões comerciais para servir de insumo inicial.
- **Motor de Proposta com IA (RAG):** Processamento do conteúdo das reuniões para gerar automaticamente seções de contexto, desafios, objetivos, módulos técnicos e roadmap.
#### **Experiência do Cliente (Landing Page)**
- **Acesso Seguro por Senha:** Camada de proteção que exige uma senha (enviada pelo comercial) para visualizar a proposta, garantindo a confidencialidade do projeto.
- **Landing Page Interativa Personalizada:** Substituição do PDF por um site dinâmico sob o domínio [mosten.com/nome-do-cliente/titulo-da-proposta](https://mosten.com/nome-do-cliente/titulo-da-proposta).
- **Embed de Protótipos Navegáveis:** Integração direta de ferramentas de design para que o cliente visualize a solução proposta dentro da própria LP.
- **Botão de Conversão "Aceite via WhatsApp":** CTA direto para facilitar o fechamento comercial imediato com o responsável pela conta.
- **Assistente Virtual (Chatbot com RAG):** Chatbot alimentado especificamente com os dados daquela proposta para sanar dúvidas pontuais do cliente em tempo real.
#### **Gestão e Rastreabilidade (Comercial & Marketing)**
- **Hospedagem via Portal Mosten:** Integração da ferramenta dentro do portal interno da consultoria para centralizar a gestão de propostas e acessos dos líderes.
- **Integração com Microsoft Clarity:** Uso da ferramenta específica para visualização de mapas de calor e gravações de sessão para entender o comportamento real de navegação do cliente.
- **Painel de Visitas via Google Analytics API:** Visualização direta no Admin da quantidade de acessos e tempo de permanência, filtrados por proposta técnica.
- **Integração de Sinais de Interesse com Pipedrive:** Atualização automática do status do negócio (deal) quando o link é aberto ou CTAs são clicados.
- **Notificações em Tempo Real:** Alertas via e-mail ou canais internos quando um tomador de decisão acessa a proposta, identificando o usuário via autenticação.
- **Painel de Admin & Analytics:** Centralização de métricas de tempo de visualização por seção, origem de tráfego e comportamento detalhado.
- **Captura de Cookies para Remarketing:** Estruturação de audiências para campanhas de marketing direcionadas a clientes que visualizaram propostas específicas.

Para amanhã:

Alinhar Features mapeadas com o processo atual de proposta técnica e validar o que faz sentido (Muda processo ou adapta features)

![[Backlog de Features 2026-05-07 09.53.56.excalidraw]]