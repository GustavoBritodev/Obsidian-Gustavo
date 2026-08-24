---
tags:
  - tipo/geral
status: rascunho
---

# Portal Tecon — Gestão de Calendários para Carga Geral
### Origem: CAL-01 a CAL-07
---
## 🎯 Objetivo Raiz (Hipótese)

Introduzir segregação obrigatória por tipo de carga na camada de gestão de calendários do Portal de Agendamento (tela `Planejamento → Calendário`), adicionando o campo `Tipo de Carga` (Contêiner | Carga Geral) como classificador primário. Os efeitos colaterais esperados são:

- **(a)** filtragem e exibição contextual no grid principal;
- **(b)** ocultação dinâmica de campos irrelevantes para Carga Geral no pop-up de criação/edição;
- **(c)** filtragem de documentos de entrada/saída conforme o tipo de operação (Entrega/Retirada);
- **(d)** criação de calendário segmentado por transportadora;
- **(e)** enforcement que bloqueia o uso cruzado de calendários entre tipos de carga.

Nenhum dos sete requisitos detalha comportamento de fallback, critérios de elegibilidade de calendários concorrentes ou modelo de dados de suporte.

---

## 🚨 Alertas de Risco & Casos de Borda

---

### 1. Erro de Numeração

> **CAL-06 (5.1.2):** Criar opção para criar calendário por transportadora.
>
> **CAL-06 (5.1.3):** Após salvar/editar calendário, janelas devem ser disponibilizadas conforme filtros e aparecer no monitoramento de gate para ajuste de quantidades.

CAL-06 aparece duas vezes com semânticas completamente distintas: uma em 5.1.2 ("Nova opção para criar calendário por transportadora") e outra em 5.1.3 ("Disponibilização e monitoramento de janelas no gate"). Isso gera ambiguidade de rastreamento em todo ciclo de vida da EF, caderno de testes e gestão de backlog.

**Pergunta:** O requisito de criação de calendário por transportadora deve ser renumerado como CAL-06 e o de disponibilização/monitoramento como CAL-07, deslocando a segregação obrigatória para CAL-08. Confirmar com o time antes da próxima versão da EF?

---

### 2. Risco de Escopo Semântico

> **CAL-01:** Adicionar filtro "Tipo de carga" com opções: Contêiner | Carga Geral (carga solta e entrega de granel).
>
> **CAL-07:** Impedir uso de calendário de contêiner para agendar carga e vice-versa (segregação total por tipo de carga).

==CAL-01 agrupa `carga solta` e `entrega de granel` sob o rótulo único "Carga Geral". Entretanto, o restante da EF trata Bulk e Breakbulk como subtipos com fluxos operacionais, telas e regras de N4 distintas (seções 5.3.3 e 5.3.5). Se o calendário não discrimina Bulk de Breakbulk no momento da criação, a regra de segregação em CAL-07 pode ser insuficiente para impedir, por exemplo, que um agendamento Break Bulk consuma vagas de um calendário configurado para Bulk.==

**Pergunta:** O campo `Tipo de Carga` no calendário deve ser um seletor de dois valores (Contêiner | Carga Geral) ou de três valores (Contêiner | Break Bulk | Bulk), para que a segregação em CAL-07 opere com a granularidade necessária para os fluxos de Retirada?

---

### 3. Requisito Aberto Crítico

> **CAL-05:** Se Tipo de calendário = Retirada: incluir "todos os tipos de documentos que autorizam a retirada" (ex.: ADM e leilão). *Listar todos os tipos de documentos que autorizam a retirada.*

O asterisco `*Listar todos os tipos de documentos que autorizam a retirada` é um gap explícito não resolvido. Sem esse inventário, é impossível especificar o campo de filtro de documentos no calendário de Retirada, escrever regras de validação ou definir quais grooves o N4 precisa suportar.

==**Pergunta:** A CSN consegue fornecer, antes da próxima versão da EF, a lista exaustiva de tipos de documento que autorizam retirada de Carga Geral no N4 (ex: ADM, leilão, DTA, outros)?==

---

### 4. Ambiguidade de Campo

> **CAL-04:** Quando Tipo de carga = Carga Geral, ocultar os campos: Refrigerado, Status, IMO e OOG.

O campo `Status` não está descrito em nenhum outro ponto do bloco CAL. Não está claro se refere-se ao status ativo/inativo do próprio calendário ou a um atributo de carga. Ocultar o status do calendário sem definir um valor default abre risco de calendários em estado indeterminado, invisíveis para o monitoramento de gate referenciado em CAL-06/CAL-07.

==**Pergunta: O campo `Status` listado em CAL-04 é o campo de status operacional do calendário (ativo/inativo)? Se sim, qual deve ser o valor default quando oculto para Carga Geral, e esse valor deve ser propagado para o N4 via groove?==

---

### 5. Underspecification Total

> **CAL-06 (5.1.2):** Criar opção para criar calendário por transportadora.

O requisito completo é: ==*"Criar opção para criar calendário por transportadora."* Sem definição de: **(a)** quais campos adicionais aparecem; **(b)** se é exclusivo por transportadora ou compartilhado; **(c)** como interage com CAL-07 (a segregação se aplica também dentro do escopo da transportadora?); **(d)** quem pode criar; **(e)** o que acontece quando a transportadora é desativada no sistema.==

**Pergunta:** O "calendário por transportadora" é uma modalidade de criação (um filtro adicional no pop-up de CAL-03) ou uma tela/fluxo separado? E a transportadora pode ter mais de um calendário ativo simultaneamente para Carga Geral?

---

### 6. Edge Case: Edição com Troca de Tipo de Carga

> **CAL-03:** Adicionar campo obrigatório "Tipo de Carga" com opções: Contêiner | Carga Geral.
>
> **CAL-04:** Quando Tipo de carga = Carga Geral, ocultar os campos: Refrigerado, Status, IMO e OOG.

Em modo de edição de um calendário existente de Contêiner, o usuário pode alterar `Tipo de Carga` para `Carga Geral`, causando a ocultação de campos (Refrigerado, Status, IMO, OOG) que já possuem valores preenchidos. O comportamento dos valores persistidos nesses campos ocultos não está definido: são zerados? mantidos silenciosamente? bloqueiam a edição?

**Pergunta:** Ao editar um calendário e alterar o `Tipo de Carga`, os valores dos campos ocultados por CAL-04 devem ser **(a)** limpos/zerados e não persistidos, **(b)** mantidos na base mas ignorados na operação, ou **(c)** a alteração de tipo em calendários com agendamentos vinculados deve ser bloqueada?

---

### 7. Edge Case: Migração de Calendários Existentes

> **CAL-03:** Adicionar campo obrigatório "Tipo de Carga" com opções: Contêiner | Carga Geral.

A introdução do campo obrigatório `Tipo de Carga` impacta todos os calendários já cadastrados no portal. Atualmente, presume-se que todos são de Contêiner, mas essa presunção não está declarada na EF. Sem uma estratégia de migração ou classificação retroativa, o campo obrigatório pode tornar inacessíveis ou inconsistentes registros históricos.

**Pergunta:** Os calendários existentes devem ser migrados automaticamente para `Tipo de Carga = Contêiner` como parte do release desta EF, ou o campo será opcional para registros legados?

---

### 8. Risco de Integração: Monitoramento de Gate

> **CAL-06 (5.1.3):** Após salvar/editar calendário, janelas devem ser disponibilizadas conforme filtros e aparecer no monitoramento de gate para ajuste de quantidades.

O requisito pressupõe uma chamada ao N4 via groove no evento de `save`. Não estão definidos: **(a)** o comportamento em caso de falha técnica do groove (rollback do calendário ou persistência com janela indisponível no gate?); **(b)** se a atualização é síncrona (bloqueia o save) ou assíncrona (o save ocorre e o gate é atualizado depois).

**Pergunta de Mitigação:** Se o groove de disponibilização de janelas no monitoramento de gate falhar durante o save do calendário, o registro do calendário no portal deve ser **(a)** revertido via rollback, **(b)** salvo em estado "pendente de sincronização", ou **(c)** salvo normalmente com alerta ao usuário interno?

---

### 9. Edge Case: Enforcement de CAL-07, Momento e UX do Bloqueio

> **CAL-07:** Impedir uso de calendário de contêiner para agendar carga e vice-versa (segregação total por tipo de carga).

==CAL-07 determina "impedir uso de calendário de contêiner para agendar carga e vice-versa", mas não define: **(a)** em qual tela/evento o bloqueio é ativado; **(b)** qual a mensagem de erro exibida; **(c)** se o usuário é impedido de selecionar o calendário ou se o erro aparece somente ao tentar confirmar o agendamento.==

**Pergunta:** O enforcement de CAL-07 deve operar de forma preventiva, ocultando/não listando calendários incompatíveis durante a seleção de janela, ou de forma reativa, exibindo erro ao tentar confirmar agendamento com calendário do tipo errado?

---

### 10. Lacuna: "Tipo de Calendário" como Pré-requisito de CAL-05

> **CAL-05:** Se Tipo de calendário = Entrega: documento para filtro deve ser a reserva (BL). Se Tipo de calendário = Retirada: incluir todos os tipos de documentos que autorizam a retirada.

==CAL-05 referencia `Tipo de calendário = Entrega` e `Tipo de calendário = Retirada` como condição para definição do documento de filtro. Esse campo não é introduzido, definido ou localizado em nenhum ponto do bloco CAL-01 a CAL-07. Não está claro se é um campo existente no pop-up atual ou um campo novo a ser criado em conjunto com `Tipo de Carga`.==

**Pergunta:** O campo `Tipo de calendário` (Entrega/Retirada) já existe no pop-up de criação/edição do calendário atual, ou deve ser criado como parte desta EF? Se novo, quais são seus valores e regras de obrigatoriedade?

---

## 📋 Pauta de Validação para a Reunião

---

### 1. Estratégia, Negócios e OKRs

**1.1**
> **CAL-07:** Impedir uso de calendário de contêiner para agendar carga e vice-versa (segregação total por tipo de carga).

CAL-07 propõe segregação total e permanente entre calendários de Contêiner e Carga Geral. Existe algum cenário operacional, como períodos de baixa movimentação ou janelas compartilhadas por necessidade, em que essa segregação deva ser flexibilizada por permissão de perfil interno?

**1.2**
> **CAL-06 (5.1.2):** Criar opção para criar calendário por transportadora.

O calendário por transportadora implica que a própria transportadora teria janelas exclusivas. Isso representa uma mudança no modelo de precificação ou SLA contratual com as transportadoras parceiras do Tecon?

**1.3**
> **CAL-01:** Adicionar filtro "Tipo de carga" com opções: Contêiner | Carga Geral (carga solta e entrega de granel).
>
> **CAL-06 (5.1.2):** Criar opção para criar calendário por transportadora.

A EF não define volumetria. Qual a estimativa de calendários ativos simultâneos para Carga Geral esperada no go-live, considerando a quantidade atual de transportadoras operando no Tecon?

---

### 2. Governança, Compliance e Riscos

**2.1**
> **CAL-06 (5.1.2):** Criar opção para criar calendário por transportadora.

==O requisito não define matriz de acesso para a criação desse calendário. O perfil de criação de calendário por transportadora deve ser exclusivo do usuário interno do Tecon (operação/planejamento), ou a própria transportadora terá acesso para criar e gerir seu calendário no portal?==

**2.2**
> **CAL-05:** Se Tipo de calendário = Retirada: incluir "todos os tipos de documentos que autorizam a retirada" (ex.: ADM e leilão). *Listar todos os tipos de documentos que autorizam a retirada.*

==CAL-05 menciona ADM e leilão como exemplos de documentos de autorização de retirada. Há documentos de autorização com restrição de exibição ou uso, como documentos judiciais ou de apreensão, que não devem ser listados no portal para todos os perfis?==

---

### 3. Engenharia e Arquitetura de Software

**3.1**
> **CAL-03:** Adicionar campo obrigatório "Tipo de Carga" com opções: Contêiner | Carga Geral.
>
> **CAL-04:** Quando Tipo de carga = Carga Geral, ocultar os campos: Refrigerado, Status, IMO e OOG.

O campo `Tipo de Carga` do calendário no N4 (ou na base do portal) já existe como atributo, ou o groove precisará criar um novo campo/entidade no N4 para suportar esse dado? *(Aguardando definição CSN. Impacto direto no groove de save do calendário.)*

**3.2**
> **CAL-06 (5.1.3):** Após salvar/editar calendário, janelas devem ser disponibilizadas conforme filtros e aparecer no monitoramento de gate para ajuste de quantidades.

O groove de disponibilização de janelas deve receber como parâmetro o `Tipo de Carga` do calendário para filtrar corretamente no gate. O N4 já possui um atributo de `Tipo de Carga` na entidade de janela/calendário, ou o groove precisará criar essa extensão?

**3.3**
> **CAL-07:** Impedir uso de calendário de contêiner para agendar carga e vice-versa (segregação total por tipo de carga).

O enforcement do bloqueio de uso cruzado deve ser implementado exclusivamente no portal (regra de negócio no front/backend do portal) ou também deve ser validado no N4 via groove, ou seja, o N4 deve recusar um appointment se o calendário for do tipo incompatível com a carga?

---

### 4. Automação e Integração de Sistemas

**4.1**
> **CAL-05:** Se Tipo de calendário = Entrega: documento para filtro deve ser a reserva (BL). Se Tipo de calendário = Retirada: incluir todos os tipos de documentos que autorizam a retirada.

Esse filtro por documento na criação do calendário é consultado no N4 em tempo real via groove de leitura, ou é uma lista estática configurada no próprio portal?

**4.2**
> **CAL-06 (5.1.3):** Após salvar/editar calendário, janelas devem ser disponibilizadas conforme filtros e aparecer no monitoramento de gate para ajuste de quantidades.

O evento de trigger para o groove é exclusivamente o `save` do calendário, ou edições parciais como ajuste de quantidade de vagas também devem disparar a atualização no gate do N4?

**4.3**
> **CAL-06 (5.1.3):** Após salvar/editar calendário, janelas devem ser disponibilizadas conforme filtros e aparecer no monitoramento de gate para ajuste de quantidades.
>
> **CAL-07:** Impedir uso de calendário de contêiner para agendar carga e vice-versa (segregação total por tipo de carga).

Existe algum mecanismo de reconciliação/batch entre o portal e o N4 para garantir que calendários de Carga Geral e suas janelas estejam sincronizados em caso de falha técnica pontual de um groove?

---

### 5. Operação, UI/UX e Front-end

**5.1**
> **CAL-04:** Quando Tipo de carga = Carga Geral, ocultar os campos: Refrigerado, Status, IMO e OOG.

A ocultação deve ser imediata ao selecionar `Tipo de Carga = Carga Geral` (comportamento dinâmico sem reload), e os campos devem ser removidos visualmente do layout ou apenas desabilitados/readonly?

**5.2**
> **CAL-01:** Adicionar filtro "Tipo de carga" com opções: Contêiner | Carga Geral (carga solta e entrega de granel).

==O filtro `Carga Geral` deve retornar tanto registros de carga solta quanto de granel no mesmo grid, ou haverá um sub-filtro adicional para distinguir os dois subtipos dentro de Carga Geral?==

**5.3**
> **CAL-06 (5.1.2):** Criar opção para criar calendário por transportadora.

==No pop-up de criação do calendário, o campo `Transportadora` deve ser um campo de busca/autocomplete integrado à base de transportadoras cadastradas no portal/SILOG, ou um seletor estático?==

**5.4**
> **CAL-02:** Adicionar coluna "Tipo de carga" no grid principal.

A coluna `Tipo de carga` adicionada ao grid deve ser ordenável e agrupável, e qual é a ordenação default da tela `Planejamento → Calendário` após a implementação?

---

### 6. Suporte e Sustentação

**6.1**
> **CAL-07:** Impedir uso de calendário de contêiner para agendar carga e vice-versa (segregação total por tipo de carga).

CAL-07 irá gerar situações onde usuários tentarão agendar carga em calendários incompatíveis. Qual deve ser a mensagem de erro exata exibida, e ela deve indicar explicitamente qual o tipo de calendário disponível para aquela carga ou apenas bloquear com mensagem genérica?

**6.2**
> **CAL-05:** Se Tipo de calendário = Retirada: incluir "todos os tipos de documentos que autorizam a retirada". *Listar todos os tipos de documentos que autorizam a retirada.*

Quando um tipo de documento não constar na lista do portal, o sistema deve exibir erro orientando o usuário a acionar o suporte/operação, ou há um campo de "outro documento" como fallback?

---

## 🔎 Outros Pontos de Atenção

**Consistência Terminológica:** A EF usa "janela", "vaga" e "slot" de forma intercambiável ao longo do documento. No bloco CAL, os termos aparecem em CAL-06 ("janelas devem ser disponibilizadas") sem definição formal. Recomenda-se estabelecer um glossário controlado antes da versão final da EF para evitar ambiguidade nos critérios de aceite e caderno de testes.

**Ausência de Regra de Unicidade:** Nenhum dos requisitos CAL define se pode existir mais de um calendário ativo de `Carga Geral` para o mesmo período/turno, e se há regra de unicidade por tipo de operação (Entrega/Retirada), por transportadora (CAL-06), ou por combinação. Essa lacuna impacta diretamente a lógica de seleção automática de calendário descrita em ENT-13 e RET-13, que dependem de um calendário unívoco mais aderente à carga.
