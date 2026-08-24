# Perguntas para Elaboração da EF: Agendamento de Entrega de Carga

**Base:** Especificação Funcional Portal Tecon (v01, 30/01/2026) | ENT-01 a ENT-14 · GEN-02 · GEN-04
**Modelo de referência estrutural:** EF013 — Gestão de Calendários para Carga Geral (v0.1)

---

Se for longo curso: Campo tipo de recepção deverá ser habilidade com as opções NF-e, DAT e DTA. -> O que é longo curso?

## 1. Permissões e Perfis de Acesso

==**P01.** `[ENT-01 / RN]` A segregação entre quem registra (qualquer perfil externo com o BL) e quem agenda (CNPJ do registrante + transportadora responsável) é controlada por perfil de acesso no portal, por CNPJ logado ou por combinação dos dois?==

==**P02.** `[ENT-01 / RF]` Quando o usuário logado tem permissão apenas para registrar, mas não para agendar, as etapas de transporte e janela são ocultadas, desabilitadas ou exibidas com mensagem de restrição?==

ENT-01 — Quem registra e quem agenda
• Registrar: qualquer perfil externo pode registrar se possuir o número da reserva (BL).
• Agendar: somente pessoas vinculadas ao CNPJ que fez o registro e a transportadora responsável pelo frete.

**P03.** `[ENT-01 / RN]` A vinculação "transportadora responsável pelo frete", que habilita o agendamento, é derivada de um campo do BL no N4 ou é uma configuração interna do portal?

---

## 4. Pesquisa por BL e Retorno do N4

**P09.** `[ENT-05 / RN]` Quando o BL existe no N4 mas não atende às condições de retorno (ser de carga e ser de exportação ou storage), o sistema exibe mensagem distinta para cada condição não atendida ou uma mensagem genérica única?

---

## 5. Grid de Itens do BL

**P14.** `[ENT-06 / RNF]` O grid de itens exibe todos os registros de uma vez ou é paginado? Se paginado, qual é o número de itens por página? Paginado

==**P16.** `[ENT-07 / RF]` Itens com saldo zero permanecem visíveis no grid (com indicação de esgotado) ou são removidos da listagem após o vínculo completo da quantidade?==

ENT-07 — Cálculo e regra de saldo
Saldo disponível deve ser calculado no portal e nunca pode ficar menor que zero.

---

## 6. Vínculo de Documento de Entrada

==**P18.** `[ENT-09 / RN]` O que define se um BL é de "longo curso", condição que habilita os tipos NF-e, DAT e DTA no campo de tipo de recepção? Essa informação é um campo do BL no N4 ou é determinada por outra regra?==

==**P19.** `[ENT-09 / RN]` Para BLs que não são de longo curso, quais tipos de documento são aceitos no vínculo? Esses documentos vem daquela tabela igual a de Calendário?==

**P20.** `[ENT-09 / RF]` O sistema valida o formato da chave NF-e (44 dígitos numéricos) antes de aceitar o vínculo? Existem regras de formato equivalentes para DAT e DTA?

**P21.** `[ENT-09 / RN]` É permitido vincular o mesmo item com dois documentos de tipos diferentes, usando parte da quantidade para cada um? Se sim, cada par item-documento gera um registro independente na lista de vínculos?

==**P22.** `[ENT-09 / RN]` O mesmo número de documento pode amparar itens de BLs diferentes dentro da mesma viagem?==

ENT-09 — Informar documento que ampara entrada
Sistema solicita documento (ex.: chave NF-e, DAT, DTA, entre outros) e, ao incluir, abate do saldo disponível.
Se for longo curso: Campo tipo de recepção deverá ser habilidade com as opções NF-e, DAT e DTA.
Ao lado do campo tipo de documento o portal deverá ter uma “?” para explicar o que é cada documento.

---

## 7. Múltiplos BLs por Viagem

**P24.** `[ENT-10 / RF]` Os itens de um BL extra associado à viagem são exibidos no mesmo grid do BL principal (lista unificada) ou em seções separadas por BL?

**P25.** `[ENT-10 / RN]` Há restrição sobre quais BLs podem ser associados na mesma viagem? Por exemplo: todos devem pertencer ao mesmo navio e viagem no N4, ou a associação é livre por número de BL?

ENT-10 — Múltiplas inclusões e múltiplos BL
Permitir repetir a inclusão quantas vezes necessário para registrar cargas da viagem; permitir associação de mais de um BL na mesma viagem.

---

## 8. Dados do Transporte

**P26.** `[ENT-11 / RT]` Qual é a origem da lista de transportadoras: a mesma base utilizada no campo "Transportadora" da EF013 (Gestão de Calendários), integração com o SILOG ou outra fonte?

**P27.** `[ENT-11 / RT]` A lista de motoristas disponíveis por transportadora é carregada do SILOG, de uma base interna do portal ou de outra integração? O motorista precisa estar previamente cadastrado para ser selecionável?

**P28.** `[ENT-11 / RF]` O sistema aceita placas no formato antigo (ABC-1234) e no formato Mercosul (ABC1D23), ou somente um deles? Os dois

**P29.** `[ENT-11 / RF]` O campo "Placa do Cavalo 2" é sempre exibido no formulário (desabilitado por padrão) ou aparece somente quando o usuário indica que o veículo é bitrem? Ver depois

---

## 9. Validação SILOG

==**P30.** `[ENT-12 / RF]` A validação no SILOG é acionada por botão explícito do usuário ou automaticamente ao tentar avançar para a próxima etapa?==

**P32.** `[ENT-12 / RN]` Se a validação SILOG for bem-sucedida e o usuário alterar a placa ou o motorista depois, o sistema exige nova validação antes de permitir o avanço? Sim

**P33.** `[GEN-02 / RF]` Em falha técnica no SILOG, o usuário pode tentar novamente livremente ou existe número máximo de tentativas antes de o processo ser encerrado? Tenta novamente

ENT-12 — Validação SILOG (motorista/placa)
Antes de avançar, integrar com SILOG para validar cadastro de motorista e placa.
Regras SILOG (Entrega):
• Falha técnica: exibir erro de comunicação (não barra cadastro, mas impede agendamento).
• Não cadastrado: erro “Motorista/Veículo não cadastrado no Silog” (bloqueante; encerra processo).
• Sucesso: prossegue.

---

## 10. Seleção de Janela e Calendário

==**P34.** `[ENT-13 / RN]` O critério de "calendário com maior detalhe", usado para seleção automática quando há mais de um calendário apto, precisa ser definido: quais atributos do calendário determinam o grau de detalhe? A presença de Transportadora específica, Área ou Cliente têm peso diferente entre si?==

**P35.** `[ENT-13 / RF]` O nome ou identificador do calendário selecionado automaticamente deve ser exibido ao usuário junto com as janelas disponíveis ou a seleção é completamente transparente?

**P36.** `[ENT-13 / RF]` Quando não existe nenhum calendário de Carga Geral disponível para o período, o sistema exibe mensagem específica ou apresenta apenas uma lista vazia de janelas?

==**P37.** `[ENT-13 / RN]` Existe antecedência mínima obrigatória para selecionar uma janela? O campo "Antecedência para Remoção" dos calendários de Carga Geral (EF013) impacta diretamente a disponibilidade das janelas exibidas nesta tela?==

==**P38.** `[ENT-13 / RF]` Janelas com zero vagas disponíveis aparecem na lista como esgotadas (visíveis, mas não selecionáveis) ou são omitidas completamente?==

ENT-13 — Exibição de janelas e seleção automática de calendário
Exibir janelas disponíveis; sistema escolhe calendário conforme filtros e disponibiliza vagas por janelas. 
Caso o registro tenha mais de um calendário que seja apto para o agendamento, utilizar o que possuí maior detalhes com a carga a ser agendada.

---

## 11. Múltiplos Agendamentos e Guias

==**P39.** `[ENT-14 / RF]` Após a confirmação do primeiro agendamento, o fluxo de geração de guias adicionais ocorre na mesma tela ou redireciona para uma nova instância do formulário com os dados de transporte pré-preenchidos?==

==**P40.** `[ENT-14 / RN]` Cada guia adicional exige um novo conjunto de documentos de entrada vinculados, ou os vínculos do primeiro agendamento podem ser reaproveitados?==

==**P41.** `[ENT-14 / RN]` Existe limite máximo de guias que podem ser geradas para o mesmo conjunto (placa frontal, placa traseira e motorista)?==

**P42.** `[ENT-14 / RF]` A guia impressa usa como identificador o Ticket ID (número do truck visit appointment retornado pelo N4, conforme ENT-17) ou um número sequencial gerado pelo portal?

ENT-14 — Múltiplos agendamentos
Portal de agendamento de entrega de carga deverá possuir a função para gerar múltiplas guias de agendamento. Após a realização do primeiro agendamento, habilitar a função de emitir múltiplas guias que deverá pertencer a janelas diferente para o conjunto. A depender da quantidade de guias a serem utilizadas pelo transportador, deve-se haver um ou mais documentos de entrada para cada agendamento. Essa função deverá consumir vagas disponíveis normalmente.

---

## 12. Integrações Finais com o N4

**P43.** `[ENT-15 / RN]` Quando um item possui dois documentos de tipos diferentes vinculados (ex.: parte da quantidade com NF-e e parte com DAT), o sistema cria dois appointments distintos no N4, cada um com sua quantidade e documento? Esse entendimento está correto?

**P44.** `[ENT-16 / RN]` Para veículos não bitrem, o agrupamento do truck visit appointment considera apenas placa do cavalo 1 e motorista, sem a placa traseira? Qual é o campo exato de agrupamento no N4?

**P45.** `[ENT-17 / RF]` O Ticket ID retornado pelo N4 é exibido apenas na tela de confirmação ou também é enviado ao usuário por e-mail ou outro canal de notificação?

**P46.** `[ENT-18 / RT]` A regra de associar novo appointment ao truck visit já existente (mesma placa frontal, motorista e janela) é verificada pelo portal antes de chamar o N4 ou é tratada inteiramente pelo N4?

**P47.** `[ENT-15, GEN-03 / RN]` Em erro funcional retornado pelo N4 durante a criação do appointment, o sistema reverte os vínculos de documentos e libera o saldo, ou mantém os vínculos e apenas bloqueia o agendamento até nova tentativa?

---
## 14. Prevenção de Conflitos e Comportamento Geral

**P52.** `[GEN-04 / RN]` O conflito de agendamento verificado no GEN-04 é identificado por veículo (mesmo conjunto placa + motorista), por janela (qualquer veículo na mesma janela) ou por ambos os critérios simultaneamente?

==**P53.** `[GEN-04 / RF]` Quando um conflito é detectado, quais dados devem ser exibidos ao usuário: tipo de operação conflitante, número do agendamento existente, janela em conflito ou combinação desses elementos?==

GEN-04 — Agendamento simultâneo
• Sistema deverá impedir conflitos de agendamento de entrega de carga, entrega de contêiner, retirada de contêiner, retirada de bulk e autorização de janela dentro do mesmo período. Sempre exibir para o usuário qual o conflito.

**P54.** `[Geral / RNF]` Os dados preenchidos em cada etapa são persistidos automaticamente ou ficam apenas em memória de sessão? Se o usuário fechar o navegador ou a sessão expirar entre as etapas, os dados são recuperáveis?

**P55.** `[Geral / RF]` Ao clicar em "Voltar" entre etapas, os dados da etapa de origem são preservados ou a etapa é reiniciada do zero?
