---
tags:
- tipo/trabalho/projeto/playbooks
- AWS
- Azure
---
# Pontos a Confirmar e Lacunas — Playbooks de TI Mosten (034/26 a 047/26)

**Escopo analisado:** 14 Playbooks (034, 035, 036, 037, 038, 039, 040, 041, 042, 043, 044, 045, 046 e 047/26).
**Metodologia:** leitura integral dos 14 documentos, extração de todos os marcadores `[A CONFIRMAR]` explícitos, e cruzamento de conteúdo entre Playbooks (e, quando relevante, com a Ata MO003-TI-25 e com o Playbook 030/25) em busca de ambiguidades, tratamentos divergentes do mesmo tema e lacunas estruturais.
**Como usar:** cada item traz o **Ponto a Confirmar** e uma **Pergunta Objetiva** que, respondida, resolve o ponto. A Parte 1 reúne questões que atravessam mais de um Playbook; a Parte 2 organiza pendências específicas de cada documento (incluindo as transversais que se originam nele).

---
## Resumo Executivo — Achados mais críticos

1. **PLAYBOOK 036/26 ("Compra de Máquinas") é inteiramente sobre a conta Zurich, mas não leva "(Zurich)" no título** — inconsistente com o Playbook 047 e com o próprio rascunho anterior do documento, que já usava "(Zurich)" no nome. *(ver T1)*
2. **Não existe, em nenhum dos 14 Playbooks, um processo de compra/reposição para o estoque GERAL da empresa** (notebooks Lenovo ThinkPad / Dell Latitude, fora do escopo Zurich) — a Ata MO003-TI-25 registra que esse tema (item 1) foi deliberadamente absorvido pelo processo de Manutenção Corretiva e Preventiva, mas o Playbook 044 aponta de volta para o 036 (que é 100% Zurich). *(ver T2)*
3. **Cinco Playbooks (036, 037, 041, 046, 047) não têm a seção obrigatória "Periodicidade de Revisão"**, presente em todos os demais 9 documentos. *(ver T3)*
4. **Dois e-mails diferentes para "compras"** — `compras@mosten.com` (só no 036) vs. `administrativo@mosten.com` (034, 042, 046, 047) — sem explicação da relação entre eles. *(ver T4)*
5. **Critério de elegibilidade a celular corporativo divergente** entre o Playbook 037 (referência técnica) e o Playbook 042 (dono do processo). *(ver T5)*

---
## Parte 1 — Questões Transversais (envolvem mais de um Playbook)

### T1. Nome do Playbook 036 não reflete que é um processo exclusivo da conta Zurich
**Ponto a Confirmar:** O PLAYBOOK 036/26 trata exclusivamente da reposição de estoque de máquinas com especificações *Zurich*, alocação para novos colaboradores nessa conta, aprovação pela Gestão de Contas (papel que "só existe em Playbooks Zurich") e envio de/para a *Zurich* como cliente. Não há nenhum trecho do documento que trate de máquinas de uso geral da empresa. O título atual, no entanto, é apenas "PLAYBOOK 036/26 – Compra de Máquinas", sem o sufixo "(Zurich)" usado no Playbook 047 ("Solicitação e Recebimento de Máquinas e Credenciais (Zurich)"). O próprio rascunho anterior deste documento já referenciava esse processo como "PLAYBOOK de Compra de Máquinas **(Zurich)**" a partir do Playbook 047 — o sufixo parece ter se perdido nesta versão final, inclusive na referência feita a este Playbook dentro do próprio 047/26 atual (que hoje diz apenas "PLAYBOOK de Compra de Máquinas", sem "(Zurich)").
**Pergunta Objetiva:** O título oficial deve ser corrigido para **"PLAYBOOK 036/26 – Compra de Máquinas (Zurich)"**, e todas as referências cruzadas a ele nos demais Playbooks (044, 047) devem ser atualizadas para incluir "(Zurich)"? R: O papel de Gestão de Contas não é exclusivo da Zurich. Outro ponto, é que o processo de Compra de Máquinas sem ser da conta Zurich está sim descrito no Playbook.

### T2. Não há Playbook para reposição do estoque GERAL de máquinas (não-Zurich)
**Ponto a Confirmar:** A Ata MO003-TI-25 registra explicitamente, no item 1 ("Processo de Compra de Máquinas"), que esse tema **não foi tratado como processo distinto** na reunião de mapeamento — o assunto mais próximo discutido (periodicidade de pesquisa de mercado e substituição de equipamentos) foi classificado, por orientação do responsável, como parte do **Processo de Manutenção Corretiva e Preventiva** (item 14, hoje Playbook 044). Coerente com isso, o Playbook 044 (Etapa 2.4) diz que, ao identificar necessidade de substituição/renovação de **qualquer** equipamento, a Infraestrutura TI "abre diretamente a solicitação de compra... seguindo o fluxo e os prazos do Playbook de Compra de Máquinas" — sem distinguir se a máquina é de estoque geral (Lenovo ThinkPad / Dell Latitude, conforme referência técnica do Playbook 037) ou de estoque Zurich (Dell Pro). Porém, o único "Playbook de Compra de Máquinas" que existe (036) é **exclusivamente Zurich** (aprovação pela Gestão de Contas, cliente Zurich configurando a máquina etc.) — um fluxo que não faz sentido para renovar, por exemplo, o notebook de um colaborador interno sem vínculo com a Zurich.
**Pergunta Objetiva:** Existe hoje um processo (ainda que informal) de compra para reposição do estoque **geral** da empresa — com aprovador próprio (ex.: Gestor de Tecnologia, em vez de Gestão de Contas) e fluxo próprio de fornecedor —, que deveria virar um Playbook específico (ex.: "Compra de Máquinas — Estoque Geral")? Ou toda compra de máquina, seja para estoque geral ou Zurich, deveria mesmo seguir o mesmo fluxo do Playbook 036, com a Gestão de Contas aprovando também compras de uso interno? Enquanto isso não for definido, a referência do Playbook 044 (Etapa 2.4) ao "Playbook de Compra de Máquinas" deve ser ajustada para deixar claro que hoje ela só cobre o cenário Zurich? Compra de Máquinas de uso interno segue o mesmo processo, com exceção da aprovação do Gestor de Contas.

### T3. Seção obrigatória "Periodicidade de Revisão" ausente em 5 Playbooks
**Ponto a Confirmar:** O padrão de estrutura fixa do projeto inclui a seção "Periodicidade de Revisão" em todo Playbook. Ela está presente em 9 dos 14 documentos (034, 035, 038, 039, 040 — como A CONFIRMAR —, 042, 043, 044, 045), mas está **totalmente ausente** em **036, 037, 041, 046 e 047** (o texto salta direto de "Dores"/"Exceções Tratadas" para "Histórico de Alterações").
**Pergunta Objetiva:** Qual periodicidade de revisão deve ser adotada para cada um destes 5 Playbooks?
- PLAYBOOK 036/26 (Compra de Máquinas – Zurich):
- PLAYBOOK 037/26 (Controle de Equipamentos e Máquinas – GLPI):
- PLAYBOOK 041/26 (Gestão de Contrato de Termos de Uso):
- PLAYBOOK 046/26 (Solicitação de Códigos de Envio para Logística TI):
- PLAYBOOK 047/26 (Solicitação e Recebimento de Máquinas e Credenciais – Zurich):

*(Como referência, processos de natureza semelhante hoje adotam: Onboarding e Manutenção — semestral; Chamados, Periféricos e Telecom — anual; Wi-Fi — trimestral; Offboarding/030/25 — semestral.)* R: Aplique a revisão que julgar melhor para cada um deles, com limite máximo de revisão anual.

### T4. Dois e-mails distintos para o mesmo tipo de atividade de compras
**Ponto a Confirmar:** O Playbook 036 (Compra de Máquinas) usa `compras@mosten.com` e o termo "time de Compras" como responsável por processar a compra em si. Todos os demais Playbooks que envolvem compras/logística (034 – Periféricos, 042 – Telecom, 046 – Logística, 047 – Zurich) usam `administrativo@mosten.com` e o papel "BackOffice/Administrativo (Compras)".
**Pergunta Objetiva:** `compras@mosten.com` é a mesma caixa/equipe do `administrativo@mosten.com` (BackOffice/Administrativo), apenas com um alias diferente usado especificamente para compra de máquinas Zurich? Ou são times/e-mails realmente distintos? Se distintos, qual a fronteira entre eles? Um vai direto pra Controladoria e um vai direto pra BackOffice, esse ponto não é necessário alterar e está descrito corretamente nos Playbooks.

### T5. Critério de elegibilidade a celular corporativo descrito de forma diferente em dois Playbooks
**Ponto a Confirmar:** O Playbook 037 (Referência Técnica de Equipamentos) resume a regra como: *"apenas colaboradores em nível de líder técnico ou acima podem receber celular corporativo."* Já o Playbook 042 (Gestão de Telecom — dono do processo) define **três** caminhos de elegibilidade: (a) departamento com direito automático, (b) nível hierárquico de líder técnico ou acima, ou (c) decisão da gestão de Operações. A frase do 037 restringe a regra a apenas um dos três critérios, podendo induzir leitura equivocada de quem está apto a receber o aparelho.
**Pergunta Objetiva:** A frase de elegibilidade no Playbook 037 deve ser corrigida para citar os três critérios completos definidos no Playbook 042 (ou substituída por uma remissão direta ao Playbook 042, sem reproduzir a regra)? A elegibilidade correta é a de Telecom, ajuste isso no 037.

### T6. "Departamento com direito automático" a linha/aparelho nunca é nomeado
**Ponto a Confirmar:** O Playbook 042 usa repetidamente a expressão "departamento com direito automático" como um dos três critérios de elegibilidade a linha/aparelho corporativo, mas em nenhum lugar do documento esse departamento é nomeado. A única pista indireta está em "Exceções Tratadas": *"Analistas de Marketing dentro do BackOffice/Administrativo: mesmo fazendo parte de uma área com direito automático a linha/aparelho, não recebem esses itens"* — o que sugere que BackOffice/Administrativo é (ou inclui) esse departamento, mas isso nunca é afirmado diretamente na definição de elegibilidade.
**Pergunta Objetiva:** Qual(is) é(são) o(s) departamento(s) com direito automático a linha e/ou aparelho corporativo? A frase de elegibilidade (Escopo e Etapa 1) deve nomear explicitamente esse(s) departamento(s), em vez de deixar a informação implícita apenas na seção de Exceções? Controladoria e BackOffice.

### T7. Playbook 042 referencia o Playbook 041 como "a ser atualizado" — mas essa atualização já foi feita
**Ponto a Confirmar:** No "Não inclui" do Playbook 042 (Telecom, criado em 29/07/2026) consta: *"tratados no PLAYBOOK de Gestão de Contrato de Termos de Uso... (Playbook a ser atualizado para incluir o gatilho de telecom, como próxima entrega)."* Porém, o Playbook 041 (criado em 24/07/2026, portanto **antes** do 042) já contempla esse gatilho integralmente como "cenário (c)" em toda a sua seção 3.1 a 3.3.
**Pergunta Objetiva:** Posso corrigir o trecho do Playbook 042 para remover a menção de que o Playbook 041 "ainda precisa ser atualizado", já que essa integração já existe desde a criação do 041? Pode corrigir.

### T8. Possível sobreposição entre a auditoria trimestral de estoque (037) e a manutenção preventiva semestral do estoque (044)
**Ponto a Confirmar:** O Playbook 037 (GLPI) prevê uma "Auditoria periódica de estoque" **trimestral**, focada em conciliar a quantidade/identificação física das máquinas em estoque com o cadastro no GLPI. O Playbook 044 (Manutenção Corretiva e Preventiva) prevê, separadamente, uma "Execução da manutenção preventiva do estoque" **semestral** (item 2.3), focada em testes funcionais (limpeza, boot, bateria, atualização de sistema/antivírus etc.) das máquinas em estoque. O próprio Playbook 044 sinaliza que essa sobreposição foi identificada durante o mapeamento e ficaria registrada como "ponto de atenção transversal", mas nenhum dos dois documentos define a relação entre as duas atividades.
**Pergunta Objetiva:** A auditoria trimestral (conferência de registro no GLPI) e a manutenção preventiva semestral (checklist técnico funcional) são atividades complementares e independentes — cada uma com seu propósito e periodicidade próprios —, ou deveriam ser unificadas/sequenciadas em uma rotina única? Caso permaneçam separadas, isso deve ser explicitado em "Não inclui" de cada um dos dois Playbooks, para deixar claro que não há duplicidade? R: São processos separados.

### T9. Campo de assinatura do Termo de Uso no GLPI (criado pelo Playbook 041) ainda não está refletido no Playbook 037
**Ponto a Confirmar:** O Playbook 041 (Termos de Uso) descreve, em "Oportunidade de Melhoria de Processo", a criação de um campo específico no GLPI para controle de assinatura do Termo de Uso. O Playbook 037 (Controle de Equipamentos e Máquinas – GLPI), que documenta os campos e o funcionamento do GLPI em detalhe, não menciona esse campo em nenhum momento.
**Pergunta Objetiva:** Esse campo de controle de assinatura já existe hoje no GLPI (mesmo que a automação de atualização ainda não esteja pronta)? Se sim, o Playbook 037 deve ser atualizado nesta rodada para documentá-lo (nos Critérios de Aceitação da Etapa de atribuição/verificação de cadastro), ou isso fica para uma revisão futura, quando a melhoria estiver implementada? R: Inclua essa oportunidade de melhoria no 037, igual no 041.

### T10. Liberação do vínculo com o tenant da Zurich no desligamento — referenciada no 047, mas ausente do Playbook 030/25
**Ponto a Confirmar:** O Playbook 047 (Zurich) declara, em "Não inclui": *"Devolução da máquina no desligamento do profissional, incluindo o recebimento pela Gente e Performance (GeP), a liberação do vínculo com o tenant da Zurich e a solicitação de código reverso --- tratado no PLAYBOOK de Bloqueio de Acessos e Devolução de Equipamentos [030/25]."* Porém, a lista de sistemas sob responsabilidade da Infraestrutura TI no Playbook 030/25 (conforme project knowledge: Microsoft 365, pfSense, InControl e Azure DevOps) não menciona o tenant Zurich em nenhum momento.
**Pergunta Objetiva:** A liberação do vínculo com o tenant da Zurich no desligamento de um profissional alocado nessa conta é, de fato, uma etapa hoje executada dentro do fluxo do Playbook 030/25 (por algum papel/sistema não listado explicitamente), ou é uma lacuna real que precisa ser adicionada a esse Playbook (fora do escopo desta rodada de edição, mas a ser sinalizada a quem for revisar o 030/25)? Pode remover esse tópico do não inclui do 047.

### T11. "Gestor de Tecnologia" e "Gestor da Área (Tecnologia ou Negócios)" — mesmo papel?
**Ponto a Confirmar:** "Gestor de Tecnologia" é usado como aprovador único em Periféricos (034), Incidentes (038), Ambiente de Infra TI (040) e Manutenção (044). Já o Playbook de Controle de Licenças (039) usa "Gestor da Área (Tecnologia ou Negócios), conforme a área à qual o colaborador pertence" — sugerindo que pode existir também um "Gestor de Negócios" equivalente para colaboradores fora da área de Tecnologia.
**Pergunta Objetiva:** "Gestor de Tecnologia" (papel único, citado nos demais Playbooks) é a mesma pessoa referida como "Gestor da Área" quando a área é Tecnologia, no Playbook 039? E existe de fato um "Gestor de Área" equivalente para Negócios que deveria ser adicionado à lista padrão de papéis do projeto? R: Sim, para ambas perguntas.

### T12. Papéis novos não catalogados: "Esteira de DevOps" e "Tech Lead"
**Ponto a Confirmar:** O Playbook 040 introduz dois papéis que não aparecem em nenhum dos outros 13 Playbooks nem na lista de nomenclatura padrão do projeto: "Esteira de DevOps" (executa criação de subscriptions/recursos Azure, mantém templates de pipeline) e "Tech Lead" (aprova criação de novo template de pipeline, exceto quando o próprio solicitante for o Tech Lead).
**Pergunta Objetiva:** "Esteira de DevOps" é uma equipe distinta da "Infraestrutura TI" (ex.: mesma pessoa/equipe atuando com um chapéu diferente para assuntos de nuvem/pipelines, ou um time realmente separado)? "Tech Lead" é um papel por squad/projeto (podendo haver vários na empresa), diferente do "Gestor de Tecnologia" (papel único)? Ambos devem ser incorporados à lista padrão de papéis e nomenclatura do projeto? R: É uma equipe separada. Tech Lead são vários na empresa e normalmente um por projeto, mas um deles pode ter n projetos.

### T13. Escopo do papel "gestão de Operações" como aprovador de elegibilidade a telecom
**Ponto a Confirmar:** O Playbook 042 cita "decisão da gestão de Operações" como um dos três critérios de elegibilidade a linha/aparelho corporativo, e depois, em Exceções Tratadas, esclarece que "cada gestão de Operações decide individualmente se concede linha e/ou aparelho aos seus colaboradores" — sugerindo que pode haver mais de uma "gestão de Operações" (por squad/célula), e não uma liderança única.
**Pergunta Objetiva:** A "gestão de Operações" citada no Playbook 042 se refere à liderança de cada célula/squad operacional (podendo haver várias pessoas decidindo, cada uma por seus próprios colaboradores), ou a um papel único de liderança da área de Operações da Mosten? Padronize para Gestor da Área (Negócios ou Tecnologia, igual no PB 034).

### T14. Billing profile da Zurich ausente da lista de billing profiles Azure (Playbook 040)
**Ponto a Confirmar:** O Playbook 040 lista os billing profiles Azure hoje existentes: *"Mosten (subscriptions internas), TSG, MLG e BTC (subscriptions de clientes externos, cada um pagando a própria fatura)."* A Zurich, cliente recorrente nos demais Playbooks (036, 047), não aparece nessa lista.
**Pergunta Objetiva:** A Zurich não utiliza recursos de nuvem Azure faturados pela Mosten (billing profile próprio) — sendo por isso corretamente ausente dessa lista —, ou essa omissão foi um esquecimento e a Zurich deveria constar como um quinto billing profile?Não usa e não deve ser mencionada neste PB.

### T15. Playbook 039 ("Controle de Licenças") cobre apenas parte do que a Ata MO003-TI-25 descreve como dois processos distintos
**Ponto a Confirmar:** A Ata MO003-TI-25 trata "Aquisição e Gestão de Softwares e Licenças" (item 7 — contratos de software, inventário completo, custo, verificação de redundância, controle centralizado, hoje disperso entre áreas) como um processo **distinto** de "Controle de Licenças" (item 10 — atribuição de licença por perfil de colaborador, hoje já coberto pelo Playbook 039). O Playbook 039 atual documenta apenas a segunda frente (concessão/remoção de licença por promoção/mudança de perfil), sem tratar da aquisição/gestão de contratos de software em si.
**Pergunta Objetiva:** O item 7 da Ata (aquisição e gestão de contratos de software, inventário e redundância) permanece como um Playbook totalmente separado a ser elaborado no futuro (conforme já registrado como pendência), ou parte desse conteúdo deveria ser incorporada ao próprio Playbook 039 em uma revisão futura, já que os nomes são muito parecidos e podem gerar confusão? São processos diferentes e não devem ser misturados.

---
## Parte 2 — Pontos a Confirmar por Playbook

### PLAYBOOK 034/26 — Aquisição e Gestão de Periféricos
1. **[A CONFIRMAR explícito, Etapa 5]** Não há prazo definido para a BackOffice/Administrativo elaborar e enviar o orçamento inicial ao Gestor de Tecnologia, nem prazo de resposta do Gestor de Tecnologia para essa primeira aprovação.
   **Pergunta Objetiva:** Qual é o prazo (em dias úteis) para a BackOffice/Administrativo elaborar e enviar o orçamento inicial (Etapa 5), e qual é o prazo de resposta do Gestor de Tecnologia para essa primeira aprovação? 5 dias úteis para BackOffice e 1 dia útil para o Gestor de Tecnologia.

### PLAYBOOK 035/26 — Chamados (Recebimento, Gestão e Classificação de Chamado)
1. O "Catálogo de SLA por Prioridade" é explicitamente descrito no próprio documento como uma **"Proposta"**, baseada em benchmark de mercado adaptado à realidade de um único analista.
   **Pergunta Objetiva:** O Catálogo de SLA por Prioridade (Alta/Média/Baixa) já pode ser considerado o padrão oficial vigente da Mosten, ou ainda depende de validação formal da gestão antes de ser cobrado na prática? (Relevante também porque o Playbook 038 – Controle de Incidentes reaproveita essa mesma escala.) Depende de aprovação ainda, mas isso não precisa ser mencionado diretamente no documento.

### PLAYBOOK 036/26 — Compra de Máquinas
*(ver também T1, T2, T3, T4 — que se originam neste Playbook)*
1. **Papel "Controladoria" mencionado sem estar em "Envolvidos".** A seção "Monitoramento" cita: *"Se passarem mais de 5 dias úteis sem retorno da Controladoria sobre a conclusão do orçamento solicitado..."* — mas a Controladoria não consta na lista de Envolvidos, e o Fluxo do Processo atribui a elaboração/conclusão dos orçamentos ao "time de Compras" (não à Controladoria).
   **Pergunta Objetiva:** A Controladoria participa da conclusão dos orçamentos de compra de máquinas Zurich? Se sim, qual é exatamente o seu papel (elabora o orçamento? apenas valida?), e ela deve ser incluída na lista de Envolvidos e na Etapa 1.2 do Fluxo? Time de Compras = Controladoria.
2. **Segundo fornecedor não decidido.** *"Foi discutida a possibilidade de contratar um segundo fornecedor para reduzir o risco de indisponibilidade, mas a decisão não foi fechada."*
   **Pergunta Objetiva:** Essa decisão sobre um segundo fornecedor já foi tomada desde o mapeamento? Se sim, deve ser incorporada ao Playbook; se não, permanece apenas registrada em "Dores Mapeadas"? Não, isso permanece em aberto.

### PLAYBOOK 037/26 — Controle de Equipamentos e Máquinas (GLPI)
*(ver também T3, T5, T9 — que envolvem este Playbook)*
1. Os prazos de SLA (1 dia útil para separação/entrega) e a periodicidade trimestral da auditoria foram definidos "a partir de benchmarks de mercado adaptados" e, segundo o próprio documento, "ainda não passaram por validação formal da gestão nem por um período de operação real".
   **Pergunta Objetiva:** Esses prazos e essa periodicidade já podem ser tratados como aprovados oficialmente, ou devem permanecer sinalizados como proposta sujeita a ajuste? Não foram aprovados oficialmente, mas isso não precisa ser mencionado diretamente no documento.
2. A "Vinculação de usuário a cada máquina no GLPI" está listada como melhoria "em fase de implementação".
   **Pergunta Objetiva:** Essa melhoria já foi concluída? Se sim, o texto deve deixar de descrevê-la como algo "em implementação" e passar a fazer parte do Fluxo do Processo padrão (Critérios de Aceitação da Etapa 5 — Atribuição da máquina). R: Ainda não foi implementado.

### PLAYBOOK 038/26 — Controle de Incidentes de TI
1. O documento afirma que a Wiki do projeto Mosten Core "está em fase de estruturação e ainda não possui histórico de post-mortems".
   **Pergunta Objetiva:** A Wiki já está estruturada e pronta para receber os registros de post-mortem descritos neste Playbook (com os campos obrigatórios definidos), ou essa estruturação técnica ainda é um pré-requisito pendente antes de o processo poder ser seguido na prática? R: Ainda não foi estruturada e pronta.

### PLAYBOOK 039/26 — Controle de Licenças
*(ver também T15)*
1. Perfis elegíveis ao "cursor" já existem (Líder Técnico, Dev, Analista de Dados), mas **sem tipo de licença/plano definido por perfil**, e o provisionamento efetivo está restrito a uma única pessoa.
   **Pergunta Objetiva:** Qual é o tipo/plano de licença do "cursor" aplicável a cada um dos três perfis elegíveis? E quem, além da pessoa hoje responsável, pode/deve ser habilitado a provisionar esse acesso? R: Mantenha tudo de Controle de Licenças em aberto, pois ainda não foi implementado, é apenas um "esboço", mas isso não precisa ser mencionado diretamente no documento.
2. Para Azure DevOps, "hoje não existem perfis elegíveis definidos — o acesso é tratado caso a caso".
   **Pergunta Objetiva:** Quais perfis devem ser considerados elegíveis a acesso no Azure DevOps, para que esse acesso deixe de ser tratado apenas caso a caso? R: Mantenha tudo de Controle de Licenças em aberto, pois ainda não foi implementado, é apenas um "esboço", mas isso não precisa ser mencionado diretamente no documento.
3. Não há SLA formal definido para a execução da concessão/remoção de licenças (Etapa 4) — apenas para a etapa de aprovação (Etapa 3).
   **Pergunta Objetiva:** Deve ser definido um prazo formal (SLA) para a execução da Etapa 4, ou a execução "imediata" sem SLA formal é intencional? R: Mantenha tudo de Controle de Licenças em aberto, pois ainda não foi implementado, é apenas um "esboço", mas isso não precisa ser mencionado diretamente no documento.

### PLAYBOOK 040/26 — Gestão de Ambiente de Infraestrutura de TI
*(documento com o maior número de marcadores `[A CONFIRMAR]` explícitos; ver também T3, T12, T14)*
1. **[A CONFIRMAR explícito, Etapa 1]** Não há prazo definido entre a solicitação de subscription/recurso Azure e sua aprovação/criação.
   **Pergunta Objetiva:** Qual é o prazo esperado (SLA) entre o envio do e-mail de solicitação ao Gestor de Tecnologia e a efetiva criação da subscription/recurso pela Esteira de DevOps?
2. **[A CONFIRMAR explícito, Etapa 3 — inteira]** O processo de "Repasse de custo ao cliente por billing profile" está com Descrição, Gatilho, Solicitante, Aprovador, Responsável, Duração/Prazo e Critérios de Aceitação todos em aberto.
   **Pergunta Objetiva:** Como funcionará esse processo: qual sistema fará a extração automatizada de custo por billing profile, quais campos de tag serão usados para o controle interno, qual a periodicidade da extração, e qual papel/área será responsável pela execução (rotina automática ou com solicitante humano)?
3. **[A CONFIRMAR explícito, Etapa 4]** Não há prazo definido entre a solicitação de um novo template de pipeline e sua disponibilização.
   **Pergunta Objetiva:** Qual é o prazo esperado (SLA) entre a solicitação de um novo template de pipeline de CI/CD (com aprovação do Tech Lead, quando aplicável) e sua disponibilização pela Esteira de DevOps?
4. **[A CONFIRMAR explícito]** Periodicidade de revisão do próprio Playbook — sugestão de semestral, alinhada ao Playbook 030/25.
   **Pergunta Objetiva:** A periodicidade de revisão deste Playbook deve ser semestral, conforme sugerido, ou outra periodicidade é preferida?
5. **[A CONFIRMAR explícito, Exceções Tratadas]** Uso de AWS em vez de Azure em casos excepcionais.
   **Pergunta Objetiva:** Quando a infraestrutura for provisionada em AWS (casos excepcionais por custo/especificidade do cliente), o mesmo fluxo de formalização e aprovação (e-mail ao Gestor de Tecnologia com devops@mosten.com em cópia) se aplica integralmente, ou existe um fluxo/aprovador diferente para AWS?
6. **[A CONFIRMAR explícito, Histórico de Alterações]** Data de criação do Playbook e confirmação do autor não preenchidos.
   **Pergunta Objetiva:** Qual é a data de criação deste Playbook (para constar no Histórico de Alterações), e o autor/responsável é "OPERAÇÕES", como nos demais documentos?
7. Não existe hoje processo de consolidação/encerramento de subscriptions ao se atingir o limite de 10 subscriptions ativas simultâneas.
   **Pergunta Objetiva:** Deve ser criado, nesta revisão, um processo (ainda que simples) para consolidação/encerramento de subscriptions ao atingir esse limite, ou o ponto permanece apenas registrado como dor, sem tratamento formal por ora?
R: Tudo de Gestão de Ambiente de Infraestrutura de TI mantenha em aberto e não altere nada.

### PLAYBOOK 041/26 — Gestão de Contrato de Termos de Uso de Máquinas e Celulares
*(ver também T3, T9)*
1. **[A CONFIRMAR explícito, Etapa 3.4]** Não há prazo máximo definido para o colaborador assinar o Termo de Uso antes de o equipamento ser considerado pendente/bloqueável.
   **Pergunta Objetiva:** Qual é o prazo máximo (em dias corridos ou úteis) que o colaborador tem para assinar o Termo de Uso no ClickSign, a partir do qual o equipamento passaria a ser considerado pendente para fins de um futuro bloqueio automatizado? 5 dias úteis.
### PLAYBOOK 042/26 — Gestão de Telecom
*(ver também T5, T6, T7)*
1. **[A CONFIRMAR explícito, Etapa 4]** Não há prazo definido para o retorno da Vivo em solicitações de nova linha corporativa.
   **Pergunta Objetiva:** Existe um SLA contratual ou de referência com a Vivo para ativação de uma nova linha corporativa? Se sim, qual é esse prazo (semelhante ao prazo já mapeado de ~10 dias úteis para compra de aparelho)? Mantenha como A CONFIRMAR.

### PLAYBOOK 043/26 — Gestão de Wi-Fi
1. Os Access Points (AP-01 e AP-02) têm atualização de firmware disponível e ainda não aplicada, "sem rotina formal de atualização".
   **Pergunta Objetiva:** Existe um prazo ou responsável formal para aplicar essa atualização de firmware pendente, ou isso permanece apenas como dor mapeada, sem tratamento formal nesta revisão? Ignore esse cenário e exclua-o do documento caso o mesmo se encontre lá.

### PLAYBOOK 044/26 — Manutenção Corretiva e Preventiva
*(ver também T2, T8 — os achados mais relevantes deste Playbook)*
1. A vida útil de referência padrão (5 anos, depreciação linear de 20% ao ano) da Tabela de Referência de Depreciação por Modelo é descrita como "proposta baseada em benchmark de mercado".
   **Pergunta Objetiva:** Esse padrão de 5 anos / 20% ao ano já pode ser adotado como referência oficial, ou depende de validação formal da gestão antes de embasar decisões de substituição de equipamento? Ainda não foi aprovado formalmente, mas não há necessidade de mencionar isso diretamente no documento.
2. O checklist de manutenção preventiva do estoque (item 2.3) é descrito como "proposta baseada em benchmark de mercado, a validar".
   **Pergunta Objetiva:** Esse checklist pode ser adotado diretamente como está descrito no Playbook, ou precisa de validação/ajuste da gestão antes de entrar em prática?Ainda não foi aprovado formalmente, mas não há necessidade de mencionar isso diretamente no documento.

### PLAYBOOK 045/26 — Onboarding de Novos Colaboradores
1. Não há SLA formal definido para a criação de usuário e e-mail corporativo (Etapa 4), apesar de sistema (Microsoft 365 Admin Center) e responsável (Infraestrutura TI) já confirmados.
   **Pergunta Objetiva:** Deve ser definido um prazo (SLA) formal para a Etapa 4 (ex.: mesmo dia da notificação, X horas úteis)? Não aplicável.
2. Não há SLA definido para o cadastro na plataforma OnFly nem para a separação/entrega do kit de onboarding pelo BackOffice/Administrativo (Etapas 8 e 9).
   **Pergunta Objetiva:** Deve ser definido um prazo formal para essas duas etapas do BackOffice/Administrativo? Não aplicável.
3. O conteúdo padrão do kit de onboarding "ainda não está especificado".
   **Pergunta Objetiva:** Qual é o conteúdo padrão do kit de onboarding (lista de itens) a ser documentado neste Playbook? Não é necessário.

### PLAYBOOK 046/26 — Solicitação de Códigos de Envio para Logística TI
*(ver também T3)*
1. A seção "Dores do Processo Atual" está **vazia** (só contém a frase introdutória padrão, sem nenhum ponto de atrito listado) — diferente de todos os outros 13 Playbooks, que trazem pelo menos 2 itens.
   **Pergunta Objetiva:** A ausência de dores mapeadas é intencional (processo sem pontos de atrito identificados), ou há pontos de atrito do mapeamento que ainda não foram registrados nessa seção (ex.: dependência do WhatsApp pessoal da GeP para envio do código de rastreio, ausência de SLA definido pelos Correios para postagem/entrega)? R: Realmente não há.
2. O texto do Objetivo afirma *"Esta revisão amplia o escopo do Playbook para também padronizar o envio direto..."*, sugerindo uma versão anterior — mas o Histórico de Alterações mostra apenas a versão 1.0 (criação), sem nenhuma versão anterior registrada.
   **Pergunta Objetiva:** Esse trecho deve ser ajustado (removendo a referência a "revisão", já que esta é a criação original do documento), ou o Histórico de Alterações deveria registrar uma v1.0 (escopo de devolução) e uma v1.1 (ampliação para envio direto de onboarding) para refletir essa evolução? R: Pode remover a menção à revisão.
### PLAYBOOK 047/26 — Solicitação e Recebimento de Máquinas e Credenciais (Zurich)
*(ver também T3, T10 — os achados mais relevantes deste Playbook)*
1. Já foi identificado um caso de profissional com duas máquinas simultâneas ativas (nova + anterior não devolvida), sem que exista uma etapa formal de verificação no momento do envio.
   **Pergunta Objetiva:** Deve ser incluída, no Fluxo do Processo (ex.: antes da Etapa 6 — Separação da máquina), uma verificação formal de que o profissional não possui outra máquina Zurich ainda ativa/não devolvida, para evitar a duplicidade já registrada em "Dores do Processo Atual"? R: Não.
2. A referência a "PLAYBOOK de Compra de Máquinas" (em "Não inclui") deve ser corrigida para incluir "(Zurich)", assim que a T1 for confirmada.
   **Pergunta Objetiva:** *(consolidada em T1 — nenhuma ação adicional necessária além da correção de nome já perguntada ali.)*

---
## Tabela-Resumo — Pendências por Playbook

| Playbook | `[A CONFIRMAR]` explícitos | Pontos adicionais da análise | Envolvido em questão transversal (Parte 1) |
|---|---|---|---|
| 034 – Periféricos | 1 | 0 | — |
| 035 – Chamados | 0 | 1 | — |
| 036 – Compra de Máquinas | 0 | 2 | T1, T2, T3, T4 |
| 037 – Controle de Equip. (GLPI) | 0 | 2 | T3, T5, T9 |
| 038 – Controle de Incidentes | 0 | 1 | — |
| 039 – Controle de Licenças | 0 | 3 | T15 |
| 040 – Ambiente de Infra TI (Azure) | 6 | 1 | T3, T12, T14 |
| 041 – Termos de Uso | 1 | 0 | T3, T9 |
| 042 – Telecom | 1 | 0 | T5, T6, T7 |
| 043 – Wi-Fi | 0 | 1 | — |
| 044 – Manutenção Corretiva/Preventiva | 0 | 2 | T2, T8 |
| 045 – Onboarding | 0 | 3 | — |
| 046 – Logística/Códigos de Envio | 0 | 2 | T3 |
| 047 – Máquinas e Credenciais (Zurich) | 0 | 2 | T3, T10 |
| **Questões transversais (Parte 1)** | — | **15** | — |

**Total de pontos a confirmar identificados nesta análise: 15 transversais + 21 específicos de Playbook = 36 itens.**
