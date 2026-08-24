# Análise de Automação — Playbooks de TI Interna Mosten

> Entregável complementar aos Playbooks (nunca incorporado aos `.docx`), conforme a skill
> `/playbook-mosten`. Cobre os **15 Playbooks** de TI interna Mosten mapeados até o momento —
> os 12 já analisados anteriormente, revisados e reelaborados nesta rodada com detalhamento de
> **passo a passo técnico** por automação, e mais **3 Playbooks novos** incorporados nesta
> revisão: *Onboarding de Novos Colaboradores*, *Gestão de Ambiente de Infraestrutura de TI* e
> *Gestão de Wi-Fi*.
>
> Para cada processo: **(1)** mapeamento do trabalho manual automatizável, **(2)** proposta de
> automação por item — restrita a **script Python** ou **N8N** (Power Automate está fora de
> escopo e não é sugerido, nem como alternativa) — com **passo a passo técnico mínimo** (gatilho
> → extração/validação → chamada de API → confirmação/registro), e **(3)** uma marcação de
> **complexidade de implementação**, usada para montar a lista de priorização ao final do
> documento. Itens sem insumo técnico suficiente (sistema, API, gatilho ou permissão não
> confirmados) estão marcados como **⛔ SEM INSUMO SUFICIENTE** em vez de propostos de forma
> especulativa — todas essas lacunas estão consolidadas na seção final "Perguntas Pendentes".

## Legenda de Complexidade

A complexidade abaixo é uma estimativa de esforço/risco de implementação — não de valor de
negócio — e é o critério usado na seção final "Priorização de Implementação":

- 🟢 **Simples** — um único sistema, uma única chamada de API (ou um único gatilho de e-mail/
  webhook), sem espera por terceiros, sem encadeamento com outro Playbook. Normalmente
  implementável em poucas horas de desenvolvimento, uma vez o insumo técnico confirmado.
- 🟡 **Média** — envolve rotina agendada (cron/scheduled job) com lógica de comparação, ou
  encadeia 2 sistemas, ou depende de uma fonte de dados (planilha/wiki) cujo formato ainda
  precisa ser confirmado, mas cuja automação em si não é bloqueada por isso.
- 🔴 **Complexa** — encadeia 3 ou mais sistemas, envolve múltiplas aprovações humanas em série
  (espera por resposta de mais de uma pessoa), ou realiza reconciliação/auditoria entre uma
  fonte física e uma ou mais fontes digitais.
- ⛔ **Bloqueada** — sem insumo técnico suficiente (sistema, API, gatilho, permissão ou
  formato de dado não confirmado). Não entra na priorização até a lacuna ser respondida.

---

## 1. Playbook 0XX/26 — Onboarding de Novos Colaboradores *(novo)*

### Mapeamento de trabalho manual automatizável
- Validação de completude do e-mail de notificação de onboarding (todos os campos do template).
- Triagem do tipo de máquina (Empresa/Cliente/Pessoa) e roteamento ao fluxo correspondente.
- Criação de usuário e e-mail corporativo no Microsoft 365.
- Vinculação de máquina livre do estoque ao novo usuário no GLPI (melhoria já em implementação,
  segundo o próprio Playbook).
- Criação de acesso VPN no pfSense e cadastro de digital no InControl.
- Concessão de licenças conforme o perfil (Setor/Função) do colaborador.
- Cadastro do colaborador na plataforma OnFly pelo BackOffice/Administrativo.
- Cadastro do colaborador na plataforma dos Correios, quando residir fora da Baixada Santista.

### Proposta de automação por item

**1. Validação de completude do e-mail de notificação (Etapa 1)** — 🟢 **N8N**
- Gatilho: recebimento de e-mail em `suporte@mosten.com` com cópia a `entradaesaida@mosten.com`.
- Passo a passo:
  1. Trigger de e-mail (IMAP ou Microsoft Graph) filtrando remetente/assunto de onboarding.
  2. Parsing do corpo do e-mail extraindo os campos do template (Nome, E-mail Mosten, CPF,
     Data de Início, Setor, Função, Gestor, Cliente, Tipo de Contrato, Máquina, endereço etc.).
  3. Validação de presença de todos os campos obrigatórios; se algum estiver ausente, dispara
     resposta automática à Gente e Performance (GeP) solicitando complementação.
  4. Se completo, registra os dados extraídos (estrutura JSON) para uso pelas próximas
     automações desta lista (Itens 2–4, 7).
- Entrada: corpo do e-mail de onboarding. Saída: objeto estruturado com os dados do colaborador.

**2. Triagem e roteamento por tipo de máquina (Etapa 2)** — 🟡 **N8N**
- Gatilho: conclusão do Item 1 (e-mail validado).
- Passo a passo:
  1. Lê o campo "Máquina" (Empresa/Cliente/Pessoa) e o campo "Cliente" do objeto estruturado.
  2. Se "Empresa" ou "Pessoa": aciona o workflow de atribuição de equipamento do Playbook de
     Controle de Equipamentos e Máquinas (GLPI) — ver Playbook 6, Item 2.
  3. Se "Cliente" = Zurich: aciona o workflow do Playbook de Solicitação e Recebimento de
     Máquinas e Credenciais (Zurich) — ver Playbook 13, Item 1.
  4. Se "Cliente" ≠ Zurich: por ora, segue o mesmo ramo do passo 2 (Empresa), conforme definido
     no próprio Playbook enquanto não existir um Playbook específico para outros clientes.
- Entrada: campo Máquina/Cliente. Saída: chamada (trigger) ao sub-workflow correspondente.

**3. Criação de usuário e e-mail corporativo no Microsoft 365 (Etapa 4)** — 🟡 **Python** (ou N8N
com node HTTP), via Microsoft Graph API
- Gatilho: conclusão do Item 1.
- Passo a passo:
  1. Monta `nome.sobrenome@mosten.com` a partir do Nome/Sobrenome extraídos.
  2. `POST /users` (Microsoft Graph) criando o usuário com `passwordProfile.forceChangePasswordNextSignIn: true`
     e senha inicial gerada conforme a política interna.
  3. Consulta a lógica do Item 7 (licenças por perfil) e executa `POST /users/{id}/assignLicense`
     com o SKU identificado.
  4. Registra a confirmação de criação (e-mail/usuário) para uso do Item 4 (GLPI) e do fluxo de
     Termos de Uso (Playbook 10).
- Entrada: dados do colaborador (Item 1). Saída: usuário M365 criado + confirmação de licença.

**4. Vinculação automática de máquina livre no GLPI (Etapas 3a/3c)** — 🟢 **Python**
- Já em implementação, segundo a própria seção "Oportunidade de Melhoria de Processo" do
  Playbook: existe hoje um script que cria o usuário do novo colaborador no GLPI; a melhoria
  prevista é o mesmo script vincular automaticamente uma máquina livre do estoque.
- Passo a passo:
  1. Gatilho: confirmação do Item 3 (usuário M365 criado) ou do cadastro do usuário no GLPI.
  2. `GET /search/Computer` filtrando status = "Estoque" e localização em ["Armário de TI",
     "Arquibancada Cima", "Arquibancada Baixo"], em ordem de prioridade.
  3. `PUT /Computer/{id}` vinculando o campo "Nome" ao novo colaborador e mudando o status.
  4. Notifica a Infraestrutura TI para conferência física antes da entrega (a automação vincula
     o registro, não substitui a entrega física).
- Entrada: novo usuário GLPI. Saída: máquina vinculada, pronta para follow-up físico.

**5. Criação de acesso VPN no pfSense (Etapa 5)** — ⛔ **SEM INSUMO SUFICIENTE**
- Mesma lacuna já registrada no Playbook 030/25 (Offboarding) — não há confirmação de que a API
  REST do pfSense está habilitada, nem das credenciais/permissões disponíveis.

**6. Cadastro de digital no InControl (Etapa 6)** — ⛔ **SEM INSUMO SUFICIENTE**
- Mesma lacuna já registrada no Playbook 030/25 — não há confirmação de API/integração
  disponível no InControl (o cadastro de digital, em particular, provavelmente exige presença
  física do colaborador de qualquer forma, mas a criação do registro em si poderia ser
  automatizada caso a API exista).

**7. Concessão de licenças conforme o perfil (Etapa 7)** — 🟡 **Python**
- Passo a passo:
  1. Lê Setor/Função do objeto estruturado (Item 1).
  2. Consulta a Planilha de Controle de Licenças (aba "Referência Perfil x Sistema") — via
     Microsoft Graph API se hospedada em SharePoint/OneDrive, ou `openpyxl` se arquivo local.
  3. Retorna a lista de licenças/SKUs aplicáveis ao perfil.
  4. Aciona o `assignLicense` do Item 3 com o(s) SKU(s) identificado(s).
- **⛔ SEM INSUMO SUFICIENTE quanto à localização exata da planilha** (SharePoint/OneDrive ou
  arquivo local) — necessário para fechar o método de acesso programático (passo 2).

**8. Cadastro do colaborador na plataforma OnFly (Etapa 8)** — ⛔ **SEM INSUMO SUFICIENTE**
- Mesma lacuna já registrada no Playbook 030/25 — não há confirmação de que a OnFly expõe
  API/webhook de cadastro (hoje um passo manual do BackOffice/Administrativo).

**9. Cadastro do colaborador na plataforma dos Correios (Etapa 10)** — ⛔ **SEM INSUMO
SUFICIENTE**
- Mesma lacuna já registrada no Playbook de Logística TI — não há confirmação de qual sistema
  dos Correios é utilizado (API pública, SIGEP Web ou gateway de terceiro).

---

## 2. Playbook 030/25 — Bloqueio de Acessos e Devolução de Equipamentos (Offboarding)

### Mapeamento de trabalho manual automatizável
- Extração e validação dos dados do e-mail de desligamento (tag `[SAÍDA DE PESSOAS]`, CC do
  grupo, data/hora oficial de saída).
- Cálculo do instante exato de bloqueio (data/hora informadas − padrão 18h do último dia).
- Bloqueio de acesso no Microsoft 365, exclusão no pfSense (VPN), exclusão no InControl (acesso
  físico) e remoção do projeto Mosten Core no Azure DevOps.
- Localização do chamado de desligamento no GLPI e registro dos dados de encerramento (bloqueio
  confirmado, conta, máquina devolvida, data) + encerramento do chamado.
- Remoção do cadastro na plataforma OnFly.
- Monitoramento do atraso entre data de saída e execução efetiva do bloqueio (dor mapeada: caso
  de acesso físico residual por 5 dias).

### Proposta de automação por item

**1. Parsing do e-mail de desligamento e cálculo do gatilho de bloqueio** — 🟡 **N8N**
- Passo a passo:
  1. Trigger de e-mail (IMAP/Microsoft Graph) em `suporte@mosten.com` filtrando o assunto
     `[SAÍDA DE PESSOAS]`.
  2. Extrai nome, e-mail corporativo e data/hora de saída do corpo do e-mail.
  3. Calcula o instante de bloqueio (data informada + 18h, salvo instrução em contrário).
  4. Agenda (node de espera/cron) o disparo dos Itens 2, 3, 4 e 5 exatamente nesse instante —
     resolve diretamente a dor de atraso no bloqueio.
- Entrada: e-mail de desligamento. Saída: agendamento estruturado do bloqueio.

**2. Bloqueio no Microsoft 365** — 🟡 **N8N** (ou script Python com `msal` + Microsoft Graph API)
- Passo a passo:
  1. Gatilho: instante calculado no Item 1.
  2. `PATCH /users/{id}` alterando `accountEnabled: false`.
  3. Revoga sessões ativas: `POST /users/{id}/revokeSignInSessions`.
  4. Confirma o bloqueio e repassa o status ao Item 6 (registro no GLPI).
- Entrada: e-mail do colaborador (Item 1). Saída: confirmação de bloqueio.

**3. Exclusão no pfSense (VPN)** — ⛔ **SEM INSUMO SUFICIENTE**
- Não há confirmação de que a API REST do pfSense está habilitada neste ambiente, nem das
  credenciais/permissões disponíveis (bloqueio técnico já conhecido).

**4. Exclusão no InControl (acesso físico)** — ⛔ **SEM INSUMO SUFICIENTE**
- Mesma situação do pfSense — não há confirmação de API/integração disponível no InControl.

**5. Remoção do Azure DevOps** — 🟢 **Python**, via Azure DevOps REST API
- Passo a passo:
  1. Gatilho: conclusão do Item 2.
  2. Identifica o usuário no projeto Mosten Core: `GET /_apis/projects/{project}/teams/{team}/members`.
  3. Remove o membro: chamada de remoção via Graph API do Azure DevOps, autenticando com PAT
     (Personal Access Token) de conta de serviço.
  4. Confirma remoção e repassa status ao Item 6.
- Entrada: e-mail/usuário do colaborador. Saída: confirmação de remoção do Azure DevOps.

**6. Registro e encerramento do chamado no GLPI** — 🟡 **Python** ou **N8N**, via GLPI REST API
- Passo a passo:
  1. Gatilho: confirmação dos Itens 2 e 5, mais confirmação de devolução de equipamento pela
     GeP (e, quando disponíveis tecnicamente, dos Itens 3 e 4).
  2. Localiza o chamado de desligamento: `GET /search/Ticket` pelo nome do colaborador.
  3. `POST /Ticket/{id}/addfollowup` registrando bloqueio confirmado, conta, máquina devolvida
     e data.
  4. `PUT /Ticket/{id}` alterando status para "Solucionado/Fechado".
- Entrada: confirmações dos Itens 2, 3, 4, 5. Saída: chamado encerrado e documentado.

**7. Remoção do cadastro OnFly** — ⛔ **SEM INSUMO SUFICIENTE**
- Não há confirmação se a OnFly expõe API/webhook para remoção de cadastro, hoje um passo
  manual do Backoffice/Administrativo.

**8. Monitoramento de atraso no bloqueio físico** — 🟡 **N8N**
- Passo a passo:
  1. Gatilho: agendamento do Item 1.
  2. Scheduled job compara a data de saída com o status atual no InControl (assim que o Item 4
     estiver tecnicamente disponível).
  3. Se o acesso físico ainda estiver ativo além do instante calculado, dispara alerta à
     Infraestrutura TI.
- **Condicionado ao Item 4** — até o InControl ter API confirmada, este monitoramento fica na
  mesma fila de bloqueio.

---

## 3. Playbook 0XX/26 — Aquisição e Gestão de Periféricos

### Mapeamento de trabalho manual automatizável
- Registro do pedido pontual (já parcialmente automatizado: e-mail → chamado GLPI por
  integração existente).
- Avaliação do estoque existente (hoje sem controle formal — ver Dores do Processo Atual).
- Consolidação da lista mensal de compras dentro do teto de R$ 1.000,00.
- Geração e envio da planilha Excel à Backoffice/Administrativo.
- Acompanhamento dos prazos de orçamento/aprovação em duas etapas.

### Proposta de automação por item

**1. Consolidação de pedidos pontuais do mês via GLPI** — 🟢 **Python**
- Passo a passo:
  1. Gatilho: execução agendada próxima ao dia 20 de cada mês.
  2. `GET /search/Ticket` na GLPI REST API filtrando categoria = periféricos/materiais e
     período = mês corrente.
  3. Consolida os chamados em uma lista estruturada (`DataFrame`/dict), agrupando por item e
     quantidade.
  4. Repassa a lista consolidada para o Item 3 (geração da planilha).
- Entrada: chamados GLPI do mês. Saída: lista consolidada de pedidos pontuais.

**2. Avaliação de estoque** — ⛔ **SEM INSUMO SUFICIENTE**
- O próprio Playbook registra como dor a ausência total de controle de estoque/posse de
  teclado e mouse. Sem uma fonte de dados (planilha, tabela no GLPI ou outro sistema) que
  registre quantidade e posse atual, não há como automatizar esta etapa.

**3. Geração da planilha consolidada** — 🟢 **Python**, com `openpyxl`
- Passo a passo:
  1. Gatilho: conclusão do Item 1 (e do Item 2, quando existir fonte de estoque).
  2. Monta o `DataFrame` com as colunas do template (Categoria, Loja, Modelo, Quantidade, Valor
     Unitário, Frete, Total, Prazo, Link de Compra, Status).
  3. Calcula os totais/resumo por categoria.
  4. Exporta para `.xlsx` no formato já especificado na Etapa 4 do Fluxo do Processo.
- Entrada: lista consolidada (Item 1). Saída: arquivo `.xlsx`.

**4. Envio da planilha à Backoffice/Administrativo** — 🟢 **N8N**
- Passo a passo:
  1. Gatilho: geração do arquivo do Item 3, disparado automaticamente no dia 20 de cada mês.
  2. Node de e-mail (SMTP/Microsoft Graph) anexando o `.xlsx`.
  3. Envia para `administrativo@mosten.com` com corpo padrão indicando o período de referência.
- Entrada: arquivo do Item 3. Saída: e-mail enviado com anexo.

**5. Acompanhamento de prazos de orçamento e aprovação (Etapas 5–7)** — 🟡 **N8N**
- Passo a passo:
  1. Gatilho: envio da lista (Item 4).
  2. Scheduled job verifica o status da lista enviada (via retorno de e-mail, ou campo de
     status na planilha se centralizada em SharePoint/OneDrive).
  3. Ao se aproximar do vencimento do prazo, envia lembrete automático ao Gestor de Tecnologia.
- **⛔ Parcialmente bloqueado**: o prazo exato desta etapa está marcado como `[A CONFIRMAR]` no
  próprio Playbook — sem esse SLA definido, o gatilho temporal do lembrete não pode ser fechado.

---

## 4. Playbook 0XX/26 — Chamados (Recebimento, Gestão e Classificação de Chamado)

### Mapeamento de trabalho manual automatizável
- Validação de completude das informações obrigatórias na abertura do chamado.
- Contagem e alerta de SLA por prioridade (Primeira Resposta e Resolução).
- Verificação/confirmação da inclusão do gestor em cópia para chamados que exigem aprovação.
- Registro estruturado de atividades e confirmação de encerramento.

### Proposta de automação por item

**1. Checklist automático de completude na abertura** — 🟢 **N8N**
- Passo a passo:
  1. Gatilho: webhook de novo chamado no GLPI.
  2. `GET` na GLPI REST API consultando os campos obrigatórios preenchidos (nome do
     solicitante, descrição, mensagens de erro, prints, impacto).
  3. Se algum campo estiver vazio, dispara resposta automática ao solicitante pedindo
     complementação — antes da triagem humana (Etapa 2).
- Entrada: chamado recém-aberto. Saída: chamado validado ou solicitação de complementação.

**2. Monitoramento de SLA por prioridade (Alta/Média/Baixa)** — 🟡 **N8N**
- Passo a passo:
  1. Scheduled job a cada 15–30 min.
  2. `GET /search/Ticket` filtrando chamados abertos e não resolvidos.
  3. Calcula o tempo decorrido desde a abertura e compara com os limites do Catálogo de SLA
     por Prioridade (1h/4h/1 dia útil para primeira resposta).
  4. Ao ultrapassar o limite, envia alerta (e-mail/Slack/Teams via N8N) à Infraestrutura TI.
- Entrada: chamados abertos + timestamps. Saída: alerta de estouro de SLA.

**3. Confirmação de gestor em cópia para chamados com aprovação (Etapa 4)** — 🟡 **Python**
- Passo a passo:
  1. Gatilho: abertura de chamado marcado como "requer aprovação".
  2. `GET` na GLPI REST API pelo campo de e-mails em cópia do chamado.
  3. Cruza com uma tabela colaborador→gestor.
  4. Se o e-mail do gestor não estiver presente, dispara alerta para a Infraestrutura TI
     solicitar a inclusão.
- **⛔ SEM INSUMO SUFICIENTE quanto à fonte colaborador→gestor** (Convenia via API? planilha?)
  — necessário para fechar o passo 3.

**4. Lembrete de pendência de registro de atividades** — 🟡 **N8N**
- Passo a passo:
  1. Scheduled job identifica chamados "em atendimento" há mais de X horas.
  2. Verifica ausência de novo followup registrado no GLPI.
  3. Notifica o analista responsável.
- Não recomendado automatizar o conteúdo do registro em si (depende de julgamento técnico).

**5. Reabertura de chamado (Exceção Tratada)** — 🟢 **N8N**
- Passo a passo:
  1. Trigger de e-mail de resposta do solicitante após o encerramento (já integrado ao GLPI).
  2. Detecta resposta pós-fechamento pelo assunto/thread do e-mail.
  3. `PUT /Ticket/{id}` via GLPI REST API alterando status para "Em atendimento (atribuído)".
- Entrada: e-mail de resposta pós-fechamento. Saída: chamado reaberto.

---

## 5. Playbook 0XX/26 — Compra de Máquinas

### Mapeamento de trabalho manual automatizável
- Verificação periódica do estoque mínimo de máquinas Zurich (5 a 7 unidades).
- Envio dos dados técnicos da máquina retirada à Gestão de Contas.
- Acompanhamento do prazo de configuração pela Zurich (~5 dias) e alerta de atraso.
- Monitoramento de retorno da Controladoria sobre orçamentos (>5 dias úteis).

### Proposta de automação por item

**1. Verificação automática do estoque mínimo** — 🟡 **N8N**
- Passo a passo:
  1. Scheduled job diário.
  2. `GET /search/Computer` na GLPI REST API filtrando especificação "Zurich" e status
     "Estoque".
  3. Se a contagem cair abaixo de 5 unidades, dispara alerta à Infraestrutura TI.
  4. Monta automaticamente o rascunho do e-mail de solicitação de compra (Etapa 1.2) para
     revisão humana antes do envio.
- Resolve diretamente a dor "checagem depende de iniciativa manual".

**2. Envio dos dados técnicos da máquina retirada** — 🟢 **Python**
- Passo a passo:
  1. Gatilho: atualização de status da máquina no GLPI para "Retirada"/vinculada a novo
     processo.
  2. `GET /Computer/{id}` pelo número de patrimônio, retornando Service Tag, RAM, Processador,
     SSD.
  3. Monta automaticamente o e-mail/registro para a Gestão de Contas.
- Entrada: patrimônio da máquina. Saída: e-mail/registro com dados técnicos.

**3. Acompanhamento do prazo de configuração pela Zurich (~5 dias)** — 🟡 **N8N**
- Passo a passo:
  1. Gatilho: data de envio da máquina (Etapa 2.4).
  2. Scheduled job conta os dias decorridos.
  3. Decorridos 5 dias sem confirmação de disponibilidade, dispara lembrete automático à
     Infraestrutura TI para reforçar o contato com a Gestão de Contas.
- Implementa diretamente o item de Monitoramento já previsto no próprio Playbook.

**4. Monitoramento do retorno da Controladoria sobre orçamentos (>5 dias úteis)** — 🟡 **N8N**
- Passo a passo: análogo ao Item 3, contando a partir da data de envio da solicitação de
  compra e alertando quando ultrapassar 5 dias úteis sem retorno.

**5. Acionamento do motoboy (Etapas 2.4 e 2.7)** — ⛔ **SEM INSUMO SUFICIENTE**
- Não há confirmação de qual sistema o Backoffice/Administrativo usa para acionar o motoboy
  (app de terceiro com API, WhatsApp manual, telefone).

---

## 6. Playbook 0XX/26 — Controle de Equipamentos e Máquinas (GLPI)

### Mapeamento de trabalho manual automatizável
- Verificação de cadastro no GLPI por número de patrimônio antes da atribuição.
- Atribuição/desvinculação do campo "Nome" (colaborador) na máquina.
- Devolução ao estoque (remoção do nome, mudança de status, registro de data).
- Auditoria trimestral de conciliação estoque físico × GLPI.
- Atualização de status/inventário na entrega e devolução de celular corporativo.

### Proposta de automação por item

**1. Verificação de cadastro por patrimônio e alerta de divergência** — 🟢 **Python**
- Passo a passo:
  1. Gatilho: retirada de máquina do estoque para atribuição.
  2. `GET /search/Computer` na GLPI REST API filtrando por número de inventário.
  3. Se não encontrada, sinaliza a divergência (mesma que motiva a dor "Divergência recorrente
     entre estoque físico e GLPI") em vez de depender da checagem manual na tela Computadores.
- Entrada: número de patrimônio. Saída: confirmação de cadastro ou alerta de divergência.

**2. Atribuição automática ao colaborador (campo "Nome")** — 🟢 **N8N**
- O Playbook já registra esta melhoria em fase de implementação ("Vinculação de usuário a cada
  máquina no GLPI"), na seção "Oportunidade de Melhoria de Processo" — o detalhamento abaixo
  formaliza o fluxo técnico dessa automação já em andamento.
- Passo a passo:
  1. Gatilho: e-mail de onboarding processado (Playbook 1, Item 1) ou chamado de troca de
     equipamento aprovado no GLPI.
  2. Confirma o número de patrimônio da máquina a ser atribuída.
  3. `PUT /Computer/{id}` via GLPI REST API preenchendo o campo "Nome".
- Elimina o passo manual de digitação repetida em toda atribuição.

**3. Devolução ao estoque** — 🟡 **N8N**
- Passo a passo:
  1. Gatilho: e-mail de desligamento da GeP (mesmo gatilho do Playbook 030/25) ou chamado de
     troca de equipamento.
  2. `PUT /Computer/{id}` limpando o campo "Nome".
  3. Ajusta `states_id` para "Estoque".
  4. Adiciona a data no campo de comentário via GLPI REST API.
- Entrada: confirmação de devolução. Saída: máquina reclassificada como disponível.

**4. Auditoria trimestral de conciliação** — 🔴 **Python**
- Passo a passo:
  1. Gatilho: cadência trimestral (a cada 3 meses), conforme Etapa 7 do Fluxo do Processo.
  2. `GET /search/Computer` exportando todos os ativos com status "Estoque"/"Em uso" via GLPI
     REST API.
  3. Compara com uma lista de contagem física (ex.: planilha alimentada por leitura de código
     de patrimônio).
  4. Gera relatório de divergências (itens no físico sem registro e vice-versa) para a
     Infraestrutura TI revisar e corrigir no GLPI.
- **⛔ SEM INSUMO SUFICIENTE quanto ao formato/ferramenta da contagem física** (planilha manual?
  leitor de código de barras integrado?) — necessário para fechar o formato de entrada (passo
  3). Classificada como Complexa por envolver reconciliação entre fonte física e sistema.

**5. Entrega/devolução de celular corporativo** — 🟢 **Python**
- Passo a passo:
  1. Gatilho: confirmação da Infraestrutura TI de que o checklist físico de testes de hardware
     foi concluído (checklist em si permanece manual, exige inspeção física).
  2. `PUT` no ativo correspondente atualizando status no GLPI.
  3. Dispara notificação ao Backoffice/Administrativo (e-mail via N8N).
- Entrada: confirmação do checklist. Saída: status atualizado + notificação.

### Alternativa fora do escopo (opcional)
A **formatação e preparação do equipamento (Etapa 3)** — instalação limpa do Windows, drivers e
softwares padrão — é hoje manual via Rufus e Boot Menu, mas tem uma categoria de ferramenta mais
adequada do que script Python ou N8N: soluções de deployment como **Windows Autopilot** ou um
servidor **MDT (Microsoft Deployment Toolkit)**, que automatizam imagem, drivers e instalação de
softwares corporativos (OpenVPN, GLPI Agent) de ponta a ponta.

---

## 7. Playbook 0XX/26 — Manutenção Corretiva e Preventiva

### Mapeamento de trabalho manual automatizável
- Cálculo da decisão reparo vs. substituição (limite de custo de 50% e vida útil de referência
  por modelo).
- Registro do reparo associado ao patrimônio.
- Atualização semestral da Tabela de Referência de Depreciação por Modelo.
- Execução e registro do checklist de manutenção preventiva do estoque.
- Abertura da solicitação de compra de substituição.

### Proposta de automação por item

**1. Cálculo automático de reparo vs. substituição** — 🟡 **Python**
- Passo a passo:
  1. Recebe como entrada o custo estimado de reparo, o valor de um equipamento novo equivalente
     e o modelo do ativo.
  2. Consulta a Tabela de Referência de Depreciação por Modelo (Wiki do Mosten Core) via Azure
     DevOps Wiki REST API.
  3. Aplica a regra dos 50% e a vida útil de referência.
  4. Retorna a recomendação (reparar/substituir) com a justificativa — a decisão final
     permanece com a Infraestrutura TI, mas o cálculo deixa de ser manual.
- Entrada: custo, valor de novo, modelo. Saída: recomendação + justificativa.

**2. Registro do reparo associado ao patrimônio** — 🟢 **Python**
- Passo a passo:
  1. Gatilho: conclusão da Etapa 1.4.
  2. `POST /Computer/{id}/addfollowup` (ou campo de comentário dedicado) via GLPI REST API.
  3. Grava data e causa do defeito.
- Entrada: dados do reparo. Saída: registro no GLPI.

**3. Atualização semestral da Tabela de Depreciação** — 🟡 **Python**
- Passo a passo:
  1. Gatilho: execução agendada semestral.
  2. Recalcula a depreciação linear por modelo (fórmula de 20% ao ano).
  3. `PUT /wiki/wikis/{wikiIdentifier}/pages` via Azure DevOps Wiki REST API, atualizando a
     página correspondente.
- Entrada: tabela vigente + fórmula. Saída: página da Wiki atualizada.

**4. Checklist de manutenção preventiva semestral do estoque** — 🟡 **N8N**
- Passo a passo:
  1. Scheduled job semestral.
  2. `GET /search/Computer` via GLPI REST API listando todas as máquinas com status "Estoque".
  3. Abre automaticamente um chamado/checklist por ativo para a Infraestrutura TI executar
     (limpeza, SMART, bateria, drivers etc.).
- Os resultados de cada item do checklist continuam exigindo inspeção manual; a geração e o
  rastreio dos checklists deixam de depender de iniciativa manual.

**5. Pesquisa de mercado semestral (Etapa 2.1)** — ⛔ **SEM INSUMO SUFICIENTE**
- O Playbook não define fontes específicas (sites de fornecedores, marketplaces) a serem
  consultadas nem um formato de saída padronizado.

**6. Abertura da solicitação de compra de substituição (Etapa 2.4)** — 🟢 **N8N**
- Passo a passo:
  1. Gatilho: qualquer uma das Etapas 1.3, 2.1, 2.2 ou 2.3 identifica necessidade de
     substituição.
  2. Dispara automaticamente o e-mail/registro para o Playbook de Compra de Máquinas.
- Evita a dependência de lembrete manual entre os dois Playbooks.

---

## 8. Playbook 0XX/26 — Controle de Incidentes de TI

### Mapeamento de trabalho manual automatizável
- Identificação de chamados encerrados classificados como "Incidente" no GLPI.
- Criação da página de post-mortem na Wiki com a estrutura fixa de campos.
- Notificação ao Gestor de Tecnologia para aprovação.
- Registro do pré-post-mortem (simulação anual) na Wiki.
- Verificação do checklist de conformidade do processo.

### Proposta de automação por item

**1. Identificação automática do gatilho (chamado "Incidente" encerrado)** — 🟢 **N8N**
- Passo a passo:
  1. Webhook ou scheduled job consultando a GLPI REST API.
  2. Filtra chamados com status "Fechado" e tipo = "Incidente".
  3. Verifica ausência de post-mortem vinculado.
- Entrada: chamados fechados. Saída: disparo do Item 2.

**2. Criação da página de post-mortem pré-preenchida** — 🟡 **Python** (ou N8N com HTTP Request)
- Passo a passo:
  1. Gatilho: Item 1.
  2. `PUT /wiki/wikis/{wikiIdentifier}/pages` via Azure DevOps Wiki REST API.
  3. Cria a página com título padrão (data + número do chamado) e campos obrigatórios
     estruturados (Resumo, Linha do tempo, Impacto, Causa raiz, Responsável, Prioridade, Ações
     corretivas, Status de aprovação).
- Reduz o trabalho manual de montar a estrutura a cada incidente; o conteúdo analítico
  continua humano.

**3. Notificação ao Gestor de Tecnologia para aprovação (Etapa 3)** — 🟢 **N8N**
- Passo a passo:
  1. Gatilho: página do post-mortem marcada como concluída pela Infraestrutura TI.
  2. Alerta automático (e-mail/Teams) cobrando a aprovação dentro do prazo de 1 dia útil.

**4. Registro do pré-post-mortem (simulação anual)** — 🟡 **Python**
- Passo a passo:
  1. Gatilho: execução agendada anual.
  2. Gera a página na Wiki a partir de um template com os cenários do Catálogo.
  3. Permite que a Infraestrutura TI preencha diretamente o resultado da discussão de cada
     cenário durante a sessão.

**5. Verificação automatizada do checklist de conformidade** — 🟡 **Python**
- Passo a passo:
  1. Gatilho: execução agendada mensal.
  2. Cruza os chamados "Incidente" fechados no GLPI com as páginas existentes na Wiki.
  3. Sinaliza incidentes sem post-mortem registrado dentro do prazo de 1 dia útil.
- Apoia o Checklist de Verificação do Processo já descrito no Playbook.

---

## 9. Playbook 0XX/26 — Controle de Licenças

### Mapeamento de trabalho manual automatizável
- Notificação da abertura do chamado de alteração de licença (hoje sem mecanismo automático).
- Consulta à Planilha de Controle de Licenças para identificar licenças a conceder/remover.
- Submissão e coleta das três aprovações (GeP, Controladoria, Gestor da Área).
- Execução da concessão/remoção nos sistemas aplicáveis.
- Atualização da planilha de controle.

### Proposta de automação por item

**1. Notificação automática de abertura de chamado de alteração de licença** — 🟢 **N8N**
- Passo a passo:
  1. Trigger via GLPI REST API (webhook ou polling) filtrando chamados na categoria "alteração
     de licença".
  2. Notifica a Infraestrutura TI imediatamente por e-mail/Teams.
- Resolve diretamente a dor de ausência de notificação automática.

**2. Identificação das licenças aplicáveis ao novo perfil** — 🟡 **Python**
- Passo a passo:
  1. Gatilho: chamado validado (Item 1).
  2. Lê a Planilha de Controle de Licenças (aba "Referência Perfil x Sistema") — via Microsoft
     Graph API se em SharePoint/OneDrive, ou `openpyxl` se local.
  3. Retorna a lista de licenças a conceder/remover para o novo perfil informado no chamado.
- Mesma dependência de localização da planilha já sinalizada no Playbook de Onboarding (Item 7).

**3. Submissão para as três aprovações (GeP, Controladoria, Gestor da Área)** — 🔴 **N8N**
- Passo a passo:
  1. Gatilho: lista de licenças identificada (Item 2).
  2. Workflow de aprovação por e-mail (nodes de e-mail + espera por resposta, ou integração com
     Microsoft Teams via N8N).
  3. Envia a proposta de alteração aos três aprovadores em paralelo.
  4. Libera o próximo passo (Item 4) somente quando todas as respostas positivas forem
     recebidas.
- Classificada como Complexa por envolver espera serializada de três aprovadores distintos.

**4. Execução da alteração em Microsoft 365** — 🟢 **Python**, via Microsoft Graph API
- Passo a passo:
  1. Gatilho: três aprovações confirmadas (Item 3).
  2. `POST /users/{id}/assignLicense` para concessão/remoção, usando e-mail do colaborador e
     SKU identificados no Item 2.
  3. Confirma sucesso, repassando para o Item 6 (atualização de planilha).

**5. Execução da alteração em cursor e Azure DevOps** — ⛔ **SEM INSUMO SUFICIENTE**
- O próprio Playbook registra que o provisionamento de cursor está restrito a uma única pessoa,
  sem definição de tipo de licença/plano por perfil, e que o Azure DevOps não tem perfis
  elegíveis definidos (tratado caso a caso). Sem essas definições e sem confirmação de que
  cursor expõe API de provisionamento (SSO/SCIM) ou de permissão de administração de
  organização no Azure DevOps, não é possível propor a automação concreta.

**6. Atualização da planilha de controle de licenças** — 🟡 **Python** (ou N8N com o mesmo
conector do Item 2)
- Passo a passo:
  1. Gatilho: confirmação de execução (Item 4, e Item 5 quando desbloqueado).
  2. Grava o novo vínculo perfil-colaborador-licença na planilha.

---

## 10. Playbook 0XX/26 — Gestão de Contrato de Termos de Uso de Máquinas e Celulares

### Mapeamento de trabalho manual automatizável
- Levantamento dos dados da máquina vinculada ao colaborador (GLPI).
- Geração e envio do Termo de Uso via ClickSign.
- Atualização do campo de controle de assinatura no GLPI após a assinatura.
- Monitoramento de pendências de assinatura (já previsto como "Oportunidade de Melhoria" no
  próprio Playbook, ainda não implementado).

### Proposta de automação por item

**1. Levantamento dos dados da máquina vinculada (Etapa 2)** — 🟢 **Python**
- Passo a passo:
  1. Gatilho: conclusão do onboarding (Playbook 1) ou troca de máquina no GLPI (Playbook 6).
  2. `GET /Computer/{id}` via GLPI REST API pelo colaborador.
  3. Retorna modelo e número de patrimônio da máquina atribuída.
- Elimina a consulta manual da Infraestrutura TI ao GLPI antes de repassar os dados à GeP.

**2. Geração e envio do Termo de Uso via ClickSign (Etapa 3)** — 🟡 **N8N** (ou script Python
com a API REST do ClickSign)
- Passo a passo:
  1. Gatilho: conclusão do Item 1.
  2. Cria o documento a partir de um template pré-cadastrado no ClickSign.
  3. Preenche os dados do colaborador e da máquina (Item 1).
  4. Envia automaticamente para assinatura eletrônica.

**3. Atualização automática do campo de controle de assinatura no GLPI (Etapa 4)** — 🟢 **N8N**
- O próprio Playbook já descreve esta automação na seção "Oportunidade de Melhoria de
  Processo": "a automação prevista consulta o GLPI para identificar quem já está assinado e
  atualiza o campo automaticamente para assinado assim que a assinatura é confirmada" — o
  detalhamento abaixo formaliza essa automação já prevista.
- Passo a passo:
  1. Gatilho: **webhook de conclusão de assinatura do ClickSign**.
  2. Ao receber a notificação de que o documento foi assinado, executa `PUT /Computer/{id}`
     (ou o campo dedicado a ser criado no GLPI, já referenciado como pendência transversal).
  3. Marca o status como "Assinado".
- Elimina a necessidade de consulta periódica manual ao GLPI.

**4. Monitoramento de pendências e bloqueio por falta de assinatura** — ⛔ **SEM INSUMO
SUFICIENTE**
- O próprio Playbook marca como `[A CONFIRMAR]` o prazo máximo para assinatura antes do
  bloqueio do equipamento. Sem esse prazo definido, não é possível configurar o gatilho
  temporal do lembrete/bloqueio automatizado.

---

## 11. Playbook 0XX/26 — Gestão de Telecom

### Mapeamento de trabalho manual automatizável
- Verificação de elegibilidade e disponibilidade de chip na planilha de controle.
- Solicitação de nova linha/aparelho à Vivo (sem SLA formalizado).
- Notificação entre Infraestrutura TI, BackOffice e GeP a cada etapa de entrega.
- Atualização da planilha de controle (responsável, patrimônio, status do Termo de Uso).
- Revisão periódica de linhas sem uso ("limpa" a cada 2 anos) — hoje totalmente manual.

### Proposta de automação por item

**1. Verificação de elegibilidade e disponibilidade de chip** — 🟡 **Python**
- Passo a passo:
  1. Gatilho: recebimento da solicitação (Etapa 1).
  2. Cruza colaborador/departamento/nível hierárquico com os critérios de elegibilidade
     (departamento com direito automático, nível hierárquico, exceções mapeadas).
  3. Retorna "elegível" ou "não elegível".
  4. Consulta a planilha de controle para disponibilidade de chip.
- **⛔ SEM INSUMO SUFICIENTE quanto ao formato/localização exata da "planilha de controle"**
  (Excel local? SharePoint/OneDrive? Google Sheets?) — necessário para fechar o passo 4.

**2. Solicitação de nova linha/aparelho à Vivo** — ⛔ **SEM INSUMO SUFICIENTE** (disparo em si)
- Não há confirmação de que a Vivo disponibiliza API de autoatendimento corporativo.
- **O que pode ser automatizado desde já — 🟢 N8N**: monitoramento do prazo de retorno.
  1. Scheduled job contando os dias corridos desde a solicitação.
  2. Alerta o BackOffice quando ultrapassar a média de 10 dias úteis (aparelho) ou quando não
     houver SLA definido para linha.
- Resolve parcialmente a dor "sem prazo definido para retorno da Vivo", dando visibilidade.

**3. Notificação de entrega entre Infraestrutura TI → BackOffice → GeP (Etapas 7 e 8)** — 🟡
**N8N**
- Passo a passo:
  1. Gatilho: Infraestrutura TI marca a entrega como concluída (atualização de status no GLPI).
  2. N8N notifica automaticamente o BackOffice.
  3. BackOffice, por sua vez, aciona a notificação à GeP para o Termo de Uso.
- Elimina o risco de atraso na cadeia de comunicação manual.

**4. Atualização da planilha de controle (Etapa 9)** — 🟡 **Python** ou **N8N**
- Mesmo conector do Item 1 (uma vez definido o formato), atualizando automaticamente
  responsável, patrimônio e status do termo a partir da confirmação dos Itens 2/3.

**5. Revisão periódica de linhas sem uso ("limpa", a cada 2 anos)** — 🟢 **N8N**
- Passo a passo:
  1. Scheduled job mensal.
  2. Lê a planilha de controle e calcula, por linha, a data de término do período de
     fidelização (2 anos após a contratação).
  3. Sinaliza automaticamente ao BackOffice as linhas que já passaram desse prazo para
     avaliação de cancelamento.
- Resolve diretamente a dor "depende hoje de verificação manual, linha a linha".

---

## 12. Playbook 0XX/26 — Solicitação de Códigos de Envio para Logística TI

### Mapeamento de trabalho manual automatizável
- Envio do e-mail de solicitação de código reverso com todos os campos obrigatórios.
- Geração do código de rastreio junto aos Correios.
- Envio do código de rastreio ao colaborador/prestador via WhatsApp.
- Monitoramento do prazo de validade do código (risco de vencimento sem postagem).
- Cadastro do colaborador como destinatário na plataforma dos Correios (onboarding remoto) e
  geração da pré-postagem direta.

### Proposta de automação por item

**1. Padronização e validação do e-mail de solicitação (Etapa 2)** — 🟢 **N8N**
- Passo a passo:
  1. Formulário estruturado (webhook/form trigger).
  2. Garante o preenchimento de todos os campos exigidos (item, dados do colaborador/
     prestador, endereço completo, Setor).
  3. Só permite o envio a `administrativo@mosten.com` com todos os campos completos.
- Reduz idas e vindas por campo faltante.

**2. Geração do código de rastreio (Etapa 3) e pré-postagem direta (Etapas 7–8)** — ⛔ **SEM
INSUMO SUFICIENTE**
- O Playbook cita apenas "a plataforma dos Correios", sem especificar se é a API pública dos
  Correios, o sistema SIGEP Web, ou um gateway de terceiro contratado pelo BackOffice.

**3. Envio do código de rastreio via WhatsApp (Etapa 4)** — ⛔ **SEM INSUMO SUFICIENTE**
- Não há confirmação de integração de WhatsApp Business API configurada (necessária para envio
  automatizado via N8N), ou se o envio é feito manualmente pelo WhatsApp pessoal da GeP.

**4. Monitoramento do prazo de validade do código (Exceção Tratada)** — 🟢 **N8N**
- Passo a passo:
  1. Registra a data de envio do código (Etapa 4) e a data de validade informada pelos
     Correios.
  2. Scheduled job compara com a data atual.
  3. Ao se aproximar do vencimento sem confirmação de postagem, alerta automaticamente a GeP
     para solicitar um novo código.
- Implementável de forma independente dos Itens 2 e 3, pois depende apenas de datas já
  registradas manualmente hoje.

---

## 13. Playbook 0XX/26 — Solicitação e Recebimento de Máquinas e Credenciais (Zurich)

### Mapeamento de trabalho manual automatizável
- Envio dos dados do profissional ao Gestor de Projeto (Zurich).
- Separação da máquina em estoque respeitando a lista de equipamentos homologados vigente.
- Formalização da solicitação de envio (e-mail) e envio dos dados completos ao cliente.
- Acompanhamento do prazo de devolução da máquina enviada à Zurich.
- Verificação de que o profissional não possui outra máquina ativa simultânea (dor mapeada).

### Proposta de automação por item

**1. Envio estruturado dos dados do profissional ao Gestor de Projeto** — 🟢 **N8N**
- Passo a passo:
  1. Gatilho: dados coletados pela Gestão de Contas/GeP (formulário ou e-mail estruturado).
  2. Repassa automaticamente ao Gestor de Projeto em formato padronizado.
- Reduz erro de transcrição manual.

**2. Validação do modelo contra a lista de equipamentos homologados vigente** — 🟡 **Python**
- Passo a passo:
  1. Consulta a lista de homologados (Anexo do Playbook).
  2. Valida automaticamente se o modelo separado do estoque consta como vigente antes de
     prosseguir.
- **⛔ SEM INSUMO SUFICIENTE quanto a onde essa lista é mantida** de forma estruturada e
  consultável (Wiki? Planilha compartilhada com a Gestão de Contas?).

**3. Envio dos dados completos da máquina ao cliente** — 🟢 **Python**
- Passo a passo:
  1. `GET /Computer/{id}` na GLPI REST API pelo patrimônio da máquina separada (mesma lógica do
     Item 2 do Playbook de Compra de Máquinas).
  2. Monta automaticamente o e-mail/registro (Service Tag, RAM, processador, SSD, tela) para a
     Gestão de Contas repassar ao cliente.

**4. Acionamento do motoboy (Etapas 9 e 12)** — ⛔ **SEM INSUMO SUFICIENTE**
- Mesma lacuna já registrada no Playbook de Compra de Máquinas.

**5. Acompanhamento do prazo de devolução da máquina enviada à Zurich (Etapa 13)** — 🟡 **N8N**
- Passo a passo:
  1. Registra a data prevista de devolução (informada pela Zurich).
  2. Scheduled job dispara alerta automático à Gestão de Contas próximo ao vencimento.
  3. Sugere combinar a retirada com um novo envio (já recomendado no próprio Playbook).

**6. Verificação de máquina duplicada por profissional (dor mapeada)** — 🟢 **Python**
- Passo a passo:
  1. `GET /search/Computer` na GLPI REST API por profissional.
  2. Sinaliza caso existam duas ou mais máquinas ativas simultaneamente vinculadas ao mesmo
     nome, antes de autorizar um novo envio.
- Resolve diretamente o caso concreto já registrado nas Dores do Processo Atual.

**7. Abertura dos chamados no Portal da Zurich (Etapas 4 e 10)** — ⛔ **SEM INSUMO SUFICIENTE**
- O Portal da Zurich é um sistema do cliente, externo à Mosten; não há confirmação de API
  disponível nem de credenciais/permissão de integração.

---

## 14. Playbook 0XX/26 — Gestão de Ambiente de Infraestrutura de TI *(novo)*

### Mapeamento de trabalho manual automatizável
- Validação de completude da solicitação de subscription/recurso Azure.
- Centralização do histórico de solicitações e aprovações (hoje só em e-mail — dor mapeada).
- Monitoramento semanal de custos das subscriptions ativas.
- Alerta de proximidade ao limite de 10 subscriptions ativas simultâneas (dor mapeada).
- Repasse de custo ao cliente por billing profile com controle por tag (etapa não detalhada).
- Solicitação e aprovação de novo template de pipeline de CI/CD.

### Proposta de automação por item

**1. Validação estruturada do e-mail de solicitação (Etapa 1)** — 🟢 **N8N**
- Passo a passo:
  1. Trigger de e-mail dirigido ao Gestor de Tecnologia com `devops@mosten.com` em cópia.
  2. Valida presença dos campos mínimos (tipo de recurso, billing profile de destino,
     justificativa).
  3. Confirma que a resposta de aprovação do Gestor de Tecnologia ficou registrada no mesmo
     thread antes de sinalizar a Esteira de DevOps para execução.

**2. Centralização do histórico de solicitações/aprovações** — ⛔ **SEM INSUMO SUFICIENTE**
- O Playbook registra como dor que o histórico está "concentrado inteiramente em e-mails, sem
  uma aplicação de histórico centralizada". Não há confirmação de onde esse histórico deve
  passar a ser centralizado (SharePoint List? planilha dedicada? ferramenta de service desk?)
  — necessário antes de propor o script/workflow de registro automático.

**3. Monitoramento semanal de custos por subscription (Etapa 2)** — 🟡 **N8N/Python**, via
Azure Cost Management API
- Passo a passo:
  1. Scheduled job semanal.
  2. `GET /providers/Microsoft.CostManagement/query` (Azure Cost Management API) por
     subscription ativa.
  3. Compara recursos identificados com a lista de solicitações/aprovações registradas (uma vez
     o Item 2 resolvido).
  4. Sinaliza recursos sem uso aparente, órfãos ou sem aprovação correspondente à Esteira de
     DevOps.

**4. Alerta de proximidade ao limite de 10 subscriptions ativas (dor mapeada)** — 🟢 **N8N**
- Passo a passo:
  1. Scheduled job (semanal, junto ao Item 3).
  2. Lista subscriptions ativas via Azure Resource Manager API.
  3. Se a contagem se aproximar de 10, alerta a Esteira de DevOps para avaliar consolidação ou
     encerramento antes de atingir o limite.

**5. Repasse de custo ao cliente por billing profile com tag (Etapa 3)** — ⛔ **SEM INSUMO
SUFICIENTE**
- O próprio Playbook marca esta etapa inteira como `[A CONFIRMAR]` (gatilho, solicitante,
  aprovador, responsável e critérios de aceitação) — sistema de extração, campos de tag,
  periodicidade e papel responsável ainda não definidos.

**6. Solicitação e aprovação de novo template de pipeline (Etapa 4)** — 🟢 **N8N**
- Passo a passo:
  1. Formulário/e-mail estruturado à Esteira de DevOps informando linguagem, solicitante e
     versão.
  2. Notifica o Tech Lead do solicitante para aprovação (pulando esta etapa quando o próprio
     solicitante for o Tech Lead).
  3. Ao aprovar, sinaliza a Esteira de DevOps para criação do template.
- A Etapa 5 (criação de pipeline a partir de template existente) já é self-service por design
  do próprio Playbook — não há trabalho manual a automatizar nela.

---

## 15. Playbook 0XX/26 — Gestão de Wi-Fi *(novo)*

### Mapeamento de trabalho manual automatizável
- Manutenção do Mapa de Redes e Conectividade a cada mudança técnica.
- Solicitação de troca de senha de rede Wi-Fi.
- Reporte e tratamento de problema de conectividade.
- Liberação de acesso Wi-Fi para visitante.
- Liberação de MAC para equipamento fora da segmentação padrão.
- Acompanhamento de contratos e SLA dos provedores de internet.

### Proposta de automação por item

Este é o Playbook com a maior proporção de etapas ainda `[A CONFIRMAR]` no próprio documento —
das 7 etapas do Fluxo do Processo, 5 têm gatilho, solicitante e/ou responsável integralmente em
aberto. Por isso, a maior parte da análise abaixo está bloqueada por definição, não por excesso
de cautela.

**1. Manutenção do Mapa de Redes e Conectividade (Etapa 1)** — ⛔ **SEM INSUMO SUFICIENTE**
- A atualização do próprio Playbook (documento Word) não é o tipo de rotina que se automatiza
  via script/N8N. O que poderia ser automatizado é um **monitoramento de divergência** entre o
  Mapa documentado e o estado real da rede — mas isso depende de confirmar se a **Controladora
  UniFi (WCSRV01)** expõe API de consulta de inventário (Access Points, status, firmware) e se
  o **pfSense** expõe API para consulta de configuração de rede. Sem essa confirmação, não é
  possível propor o script concreto. A mesma lacuna bloqueia a automação do alerta de firmware
  pendente (AP-01 e AP-02, já registrado como dor).

**2. Solicitação de troca de senha de rede Wi-Fi (Etapa 2)** — ⛔ **SEM INSUMO SUFICIENTE**
- O próprio Playbook marca a etapa inteira como `[A CONFIRMAR]` — não há hoje definição de
  canal de solicitação, solicitante nem aprovador.

**3. Reporte e tratamento de problema de conectividade (Etapa 3)** — ⛔ **SEM INSUMO
SUFICIENTE**
- Mesma situação — etapa inteira `[A CONFIRMAR]` no Playbook.

**4. Liberação de acesso Wi-Fi para visitante (Etapa 4)** — ⛔ **SEM INSUMO SUFICIENTE**
- Não há confirmação de como o acesso à rede Mosten_Inovation é liberado hoje.

**5. Liberação de MAC para equipamento específico (Etapa 5)** — ⛔ **SEM INSUMO SUFICIENTE**
- O procedimento de liberação de MAC é citado, mas não está detalhado no próprio Playbook.

**6. Regras de uso da VPN individual (Etapa 6)** — sem automação nova a propor nesta etapa
- A criação técnica do usuário/certificado VPN no pfSense já está mapeada como automação
  pendente no Playbook de Onboarding (Item 5) e no Playbook 030/25 (Itens 3/4) — mesma lacuna
  de API do pfSense. Este Playbook trata apenas da regra de uso, não da execução técnica.

**7. Acompanhamento de contratos e SLA dos provedores de internet (Etapa 7)** — ⛔ **SEM
INSUMO SUFICIENTE**
- Gatilho, responsável (Infraestrutura TI sozinha ou com o Backoffice/Administrativo?),
  periodicidade e critérios de aceitação estão todos `[A CONFIRMAR]` no próprio Playbook.

---

## Priorização de Implementação

Lista consolidada de todas as automações propostas nas 15 análises acima, ordenada da mais
simples para a mais complexa (critério de complexidade na Legenda, no início do documento). O
objetivo é dar ao time um roteiro prático de "por onde começar" — dentro de cada nível, a ordem
também considera dependências (ex.: automações já em fase de implementação, segundo os próprios
Playbooks, aparecem primeiro).

### 🟢 Tier 1 — Simples (implementar primeiro)

| # | Playbook | Automação | Ferramenta |
|---|----------|-----------|------------|
| 1 | GLPI | Atribuição automática ao colaborador — campo "Nome" (Item 2) — *já em implementação* | N8N |
| 2 | Onboarding | Vinculação automática de máquina livre no GLPI (Item 4) — *já em implementação* | Python |
| 3 | Termos de Uso | Atualização automática do campo de assinatura no GLPI via webhook ClickSign (Item 3) — *já prevista no próprio Playbook* | N8N |
| 4 | Onboarding | Validação de completude do e-mail de notificação (Item 1) | N8N |
| 5 | Chamados | Checklist automático de completude na abertura (Item 1) | N8N |
| 6 | Ambiente de Infraestrutura | Validação estruturada do e-mail de solicitação (Item 1) | N8N |
| 7 | Logística TI | Padronização e validação do e-mail de solicitação (Item 1) | N8N |
| 8 | Zurich | Envio estruturado dos dados do profissional ao Gestor de Projeto (Item 1) | N8N |
| 9 | GLPI | Verificação de cadastro por patrimônio e alerta de divergência (Item 1) | Python |
| 10 | Compra de Máquinas | Envio dos dados técnicos da máquina retirada (Item 2) | Python |
| 11 | Zurich | Envio dos dados completos da máquina ao cliente (Item 3) | Python |
| 12 | Termos de Uso | Levantamento dos dados da máquina vinculada (Item 1) | Python |
| 13 | Manutenção | Registro do reparo associado ao patrimônio (Item 2) | Python |
| 14 | Licenças | Execução da alteração em Microsoft 365 (Item 4) | Python |
| 15 | GLPI | Entrega/devolução de celular corporativo (Item 5) | Python |
| 16 | Zurich | Verificação de máquina duplicada por profissional (Item 6) | Python |
| 17 | Periféricos | Consolidação de pedidos pontuais do mês via GLPI (Item 1) | Python |
| 18 | Periféricos | Geração da planilha consolidada (Item 3) | Python |
| 19 | Periféricos | Envio da planilha à Backoffice/Administrativo (Item 4) | N8N |
| 20 | Licenças | Notificação automática de abertura de chamado de alteração de licença (Item 1) | N8N |
| 21 | Incidentes | Identificação automática do gatilho — chamado "Incidente" encerrado (Item 1) | N8N |
| 22 | Incidentes | Notificação ao Gestor de Tecnologia para aprovação (Item 3) | N8N |
| 23 | Manutenção | Abertura da solicitação de compra de substituição (Item 6) | N8N |
| 24 | Chamados | Reabertura de chamado (Item 5) | N8N |
| 25 | Offboarding 030/25 | Remoção do Azure DevOps (Item 5) | Python |
| 26 | Logística TI | Monitoramento do prazo de validade do código (Item 4) | N8N |
| 27 | Telecom | Revisão periódica de linhas sem uso — "limpa" (Item 5) | N8N |
| 28 | Telecom | Monitoramento do prazo de retorno da Vivo (dentro do Item 2) | N8N |
| 29 | Ambiente de Infraestrutura | Alerta de proximidade ao limite de 10 subscriptions ativas (Item 4) | N8N |
| 30 | Ambiente de Infraestrutura | Solicitação e aprovação de novo template de pipeline (Item 6) | N8N |

### 🟡 Tier 2 — Média complexidade

| # | Playbook | Automação | Ferramenta |
|---|----------|-----------|------------|
| 1 | Onboarding | Triagem e roteamento por tipo de máquina (Item 2) | N8N |
| 2 | Onboarding | Criação de usuário e e-mail corporativo no M365 (Item 3) | Python/N8N |
| 3 | Onboarding | Concessão de licenças conforme perfil (Item 7) — pendente local da planilha | Python |
| 4 | Offboarding 030/25 | Parsing do e-mail de desligamento e cálculo do gatilho de bloqueio (Item 1) | N8N |
| 5 | Offboarding 030/25 | Bloqueio no Microsoft 365 (Item 2) | N8N |
| 6 | Offboarding 030/25 | Registro e encerramento do chamado no GLPI (Item 6) | Python/N8N |
| 7 | Offboarding 030/25 | Monitoramento de atraso no bloqueio físico (Item 8) — condicionado ao InControl | N8N |
| 8 | Periféricos | Acompanhamento de prazos de orçamento e aprovação (Item 5) — prazo pendente | N8N |
| 9 | Chamados | Monitoramento de SLA por prioridade (Item 2) | N8N |
| 10 | Chamados | Confirmação de gestor em cópia em chamados com aprovação (Item 3) — fonte pendente | Python |
| 11 | Chamados | Lembrete de pendência de registro de atividades (Item 4) | N8N |
| 12 | Compra de Máquinas | Verificação automática do estoque mínimo (Item 1) | N8N |
| 13 | Compra de Máquinas | Acompanhamento do prazo de configuração pela Zurich (Item 3) | N8N |
| 14 | Compra de Máquinas | Monitoramento do retorno da Controladoria sobre orçamentos (Item 4) | N8N |
| 15 | GLPI | Devolução ao estoque (Item 3) | N8N |
| 16 | Manutenção | Cálculo automático de reparo vs. substituição (Item 1) | Python |
| 17 | Manutenção | Atualização semestral da Tabela de Depreciação (Item 3) | Python |
| 18 | Manutenção | Checklist de manutenção preventiva semestral do estoque (Item 4) | N8N |
| 19 | Incidentes | Criação da página de post-mortem pré-preenchida (Item 2) | Python/N8N |
| 20 | Incidentes | Registro do pré-post-mortem — simulação anual (Item 4) | Python |
| 21 | Incidentes | Verificação automatizada do checklist de conformidade (Item 5) | Python |
| 22 | Licenças | Identificação das licenças aplicáveis ao novo perfil (Item 2) — pendente local da planilha | Python |
| 23 | Licenças | Atualização da planilha de controle de licenças (Item 6) | Python/N8N |
| 24 | Termos de Uso | Geração e envio do Termo de Uso via ClickSign (Item 2) | N8N |
| 25 | Telecom | Verificação de elegibilidade e disponibilidade de chip (Item 1) — pendente local da planilha | Python |
| 26 | Telecom | Notificação de entrega em cadeia TI → BackOffice → GeP (Item 3) | N8N |
| 27 | Telecom | Atualização da planilha de controle (Item 4) | Python/N8N |
| 28 | Zurich | Validação do modelo contra a lista de equipamentos homologados (Item 2) — local pendente | Python |
| 29 | Zurich | Acompanhamento do prazo de devolução da máquina (Item 5) | N8N |
| 30 | Ambiente de Infraestrutura | Monitoramento semanal de custos por subscription (Item 3) | N8N/Python |

### 🔴 Tier 3 — Complexa (múltiplos sistemas ou aprovações em série)

| # | Playbook | Automação | Ferramenta |
|---|----------|-----------|------------|
| 1 | GLPI | Auditoria trimestral de conciliação estoque físico × GLPI (Item 4) | Python |
| 2 | Licenças | Submissão para as três aprovações — GeP, Controladoria, Gestor da Área (Item 3) | N8N |

### ⛔ Bloqueadas — aguardando confirmação (fora da priorização até resposta)

Estas automações não entram nos tiers acima porque dependem de uma confirmação técnica listada
na seção "Perguntas Pendentes" a seguir. Assim que cada lacuna for respondida, o item volta a
ser classificado (Simples/Média/Complexa) e reavaliado na priorização:

- Onboarding — Itens 5, 6, 8, 9 · Offboarding 030/25 — Itens 3, 4, 7 · Periféricos — Item 2 ·
  Chamados — Item 3 (fonte de dados) · Manutenção — Item 5 · Licenças — Item 5 · Termos de Uso
  — Item 4 · Telecom — Itens 1, 2, 4 (parcial) · Logística TI — Itens 2, 3 · Zurich — Itens 2,
  4, 7 · Ambiente de Infraestrutura — Itens 2, 5 · Wi-Fi — Itens 1, 2, 3, 4, 5, 7.

---

## Perguntas Pendentes para Habilitar Automação Completa

As lacunas abaixo bloqueiam o detalhamento técnico de itens específicos das análises acima.
Estão organizadas por sistema/tema para facilitar a resposta em conjunto:

1. **pfSense** — a API REST está habilitada e há credenciais/permissões disponíveis para
   automação de criação/exclusão de usuário (VPN)? *(Afeta: Offboarding 030/25 — item 3;
   Onboarding — item 5; Wi-Fi — item 6)*
2. **InControl** — existe alguma integração/API disponível para automação de cadastro/exclusão
   de credencial de acesso físico? *(Afeta: Offboarding 030/25 — item 4; Onboarding — item 6)*
3. **OnFly** — a plataforma expõe API/webhook para cadastro e remoção de cadastro? *(Afeta:
   Offboarding 030/25 — item 7; Onboarding — item 8)*
4. **Estoque de periféricos/materiais de manutenção** — onde esse estoque passará a ser
   registrado (planilha dedicada, campo no GLPI, outro sistema)? *(Afeta: Periféricos — item 2)*
5. **Fonte colaborador → gestor** — qual sistema deve ser consultado para validar
   automaticamente se o gestor certo foi incluído em cópia num chamado com aprovação (Convenia
   via API? outra fonte)? *(Afeta: Chamados — item 3)*
6. **Sistema de acionamento de motoboy** — o Backoffice/Administrativo usa algum
   aplicativo/plataforma com API para chamar o motoboy, ou o acionamento é manual (telefone/
   WhatsApp)? *(Afeta: Compra de Máquinas — item 5; Zurich — item 4)*
7. **Formato de registro da contagem física de estoque (auditoria trimestral)** — como a
   contagem física é hoje registrada para viabilizar a comparação automatizada com o GLPI?
   *(Afeta: GLPI — item 4)*
8. **Fontes da pesquisa de mercado semestral** — quais sites/fornecedores devem ser consultados
   e em que formato o resultado deve ser registrado? *(Afeta: Manutenção — item 5)*
9. **cursor e Azure DevOps (licenciamento)** — cursor expõe alguma API de provisionamento
   (SSO/SCIM)? Existe permissão de administração de organização no Azure DevOps disponível para
   automação? *(Afeta: Licenças — item 5)*
10. **Prazo de assinatura do Termo de Uso antes do bloqueio do equipamento** — já marcado como
    `[A CONFIRMAR]` no próprio Playbook; sem esse prazo não é possível configurar o gatilho
    temporal do lembrete/bloqueio automatizado. *(Afeta: Termos de Uso — item 4)*
11. **Formato/localização da planilha de controle de Telecom** — Excel local, SharePoint/
    OneDrive ou Google Sheets? *(Afeta: Telecom — itens 1 e 4)*
12. **API de autoatendimento da Vivo** — existe algum canal de integração corporativa para
    solicitação de linhas/aparelhos, ou o processo é inteiramente manual via portal/atendente?
    *(Afeta: Telecom — item 2)*
13. **Sistema de geração de código de rastreio dos Correios** — API pública dos Correios,
    SIGEP Web, ou gateway de terceiro contratado? *(Afeta: Logística TI — item 2; Onboarding —
    item 9)*
14. **Integração de WhatsApp** — existe WhatsApp Business API configurada, ou o envio do código
    de rastreio é feito manualmente pelo WhatsApp pessoal da GeP? *(Afeta: Logística TI — item 3)*
15. **Local de manutenção da lista de equipamentos homologados vigente (Zurich)** — Wiki,
    planilha compartilhada com a Gestão de Contas, ou outro repositório? *(Afeta: Zurich — item 2)*
16. **API do Portal da Zurich** — existe alguma integração disponível para abertura automática
    de chamados no portal do cliente? *(Afeta: Zurich — item 7)*
17. **Localização da Planilha de Controle de Licenças (aba "Referência Perfil x Sistema")** —
    SharePoint/OneDrive ou arquivo local? *(Afeta: Onboarding — item 7; Licenças — item 2)*
18. **Local de centralização do histórico de solicitações/aprovações de subscription/recurso
    Azure** — SharePoint List, planilha dedicada, ou ferramenta de service desk? Hoje o único
    registro é o e-mail de aprovação, o que dificulta auditoria. *(Afeta: Ambiente de
    Infraestrutura — item 2)*
19. **Repasse de custo por billing profile (Azure)** — já marcado como `[A CONFIRMAR]` no
    próprio Playbook: sistema de extração, campos de tag, periodicidade e papel responsável
    ainda não definidos. *(Afeta: Ambiente de Infraestrutura — item 5)*
20. **UniFi Controller (WCSRV01)** — expõe API para consulta de inventário de rede (Access
    Points, firmware, status)? O pfSense expõe API para consulta de configuração de rede?
    *(Afeta: Wi-Fi — item 1 e a dor de atualização de firmware pendente nos APs)*
21. **Processo de troca de senha de rede Wi-Fi** — qual é o canal de solicitação, quem solicita
    e quem aprova hoje? *(Afeta: Wi-Fi — item 2)*
22. **Processo de reporte e tratamento de problema de conectividade Wi-Fi** — qual é o canal e
    quem é o responsável pelo atendimento? *(Afeta: Wi-Fi — item 3)*
23. **Processo de liberação de Wi-Fi para visitante (rede Mosten_Inovation)** — existe hoje um
    fluxo definido, e quem aprova? *(Afeta: Wi-Fi — item 4)*
24. **Procedimento de liberação de MAC** — qual é o detalhamento do fluxo (gatilho, solicitante,
    aprovador)? *(Afeta: Wi-Fi — item 5)*
25. **Contratos/SLA dos provedores de internet** — qual é o gatilho e a periodicidade de
    acompanhamento, e o Backoffice/Administrativo participa da negociação/contratação de um
    novo provedor, ou isso é conduzido inteiramente pela Infraestrutura TI? *(Afeta: Wi-Fi —
    item 7)*
