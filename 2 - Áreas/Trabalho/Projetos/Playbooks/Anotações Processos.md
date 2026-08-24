---
tags:
  - tipo/trabalho/projeto/playbooks
---
# Processo de Controle de Equipamentos e Máquinas ✅
Dentro do GLPI na aba Ativos e tela Computadores tem a lista de todas as máquinas contendo o nome, entidade, número de inventário, status, número de série, modelo, rede e comentários

Problemática:
Lista máquinas como livres 

Quando um colaborador precisa de uma máquina o gestor abre um chamado e solicita a máquina nova, após isso a TI interna pega a máquina no estoque, seleciona a máquina do estoque no GLPI pelo número de patrimônio e adiciona o nome do colaborador que utilizará a máquina no campo de Nome no GLPI.

Quando uma máquina é devolvida, ela é formatada e alterada para Status ESTOQUE dentro do GLPI e também removido o nome do usuário da máquina.

caso a máquina não esteja no inventários da GLPI, clica no botão adicionar e inclui as informações da máquina

Para celulares a administração passou a lista de celulares e foram cadastrados no GLPI

Nota: Hoje há uma enorme quantidade de máquinas no estoque, e o GLPI não está 100% alinhado com a quantidade de notebooks em estoque.

---
# Processo de Controle de Licenças ⏳
Dentro do bitwarden possui a lista de todas as credenciais da empresa, sejam essas credenciais de softwares, servidores, VMs, Wi-Fi. Basicamente, a lista de credenciais de usuários de todos os softwares da empresa.

Para controle de licenças hoje é feito dentro do admin.cloud.microsoft, acessando o módulo de cobranças na tela Licenças. Nessa tela apresenta uma tabela contendo o nome das licenças, a quantidade de licenças disponíveis, a quantidade de licenças atribuídas e o tipo de conta.

### ==FALTA LISTAR SOFTWARES E LICENÇAS==

---
# Processo de Aquisição de Softwares, Licenças e Periféricos ⏳
Para o processo de aquisição de periféricos hoje não há um processo definido, para aquisição de carregadores, pilhas, itens de limpeza de equipamentos e etc, esses itens entram na planilha de compras mensal, onde todo mês a Infra TI tem 1000 reais para aquisição de itens. Para periféricos como teclado e mouse a empresa não fornece, porém há um estoque disso (ponto a validar do processo).

### ==FALTA LISTAR SOFTWARES E LICENÇAS==

---
# Processo de Compra de Máquinas ⏳

Para aquisição de máquinas Zurich é obrigatório ter sempre de 3-4 máquinas que atendam às especificações Zurich em estoque para caso de entrada de novos colaboradores.

Para solicitação de novas máquinas é enviado um e-mail para o compras@mosten.com contendo os itens e as especificações e para qual projeto.

Pega a máquina do estoque (GLPI de controle de ainda precisa ser ajustado)

Envia os dados da máquina pra Maylla (Service Tag, RAM, Processador e SSD)

Após isso envia e-mail pro Freitas aprovar e depois pra Priscila para chamar o motoboy pra enviar a máquina pra Zurich

Chegando lá a Zurich configura

Após algo em torno de 5 dias cobra a Maylla sobre se a máquina já está disponível para retirada

Com a devolutiva positiva da Maylla

solicita aprovação e busca de motoboy igual processo de envio

Ao receber a máquina, pega uma fonte e guarda em uma mochila e comunica que o kit do colaborador está pronto

### ==As próximas etapas precisam ser validadas.==

Problemas/Gaps:
Controle de estoque no GLPI está em uso, mas ainda não reflete a totalidade das máquinas.
Definir periodicidade para revisão de estoque.

---
# Processo de Bloqueio de Acessos e Devolução de Equipamentos ⏳
Entrevista Responsável TI:
Para o processo de bloqueio de acessos, o responsável de Gente e Performance envia um e-mail solicitando o desligamento do colaborador com a data e horário do bloqueio de acesso.

Após isso o responsável de Infra TI abre o admin.cloud.microsoft, vai na aba Usuários na tela Usuários Ativos e busca o nome do colaborador, após localizado clica em bloquear entrada. PROCESSO ATUALMENTE AUTOMATIZADO

Após isso o Infra TI vai no pfSense, vai em System/User Manager/Users e busca o nome do usuário e então o exclui.

Para excluir o acesso físico ao escritório do usuário o infra TI vai no InControl com acesso via Servidor da Mosten, então clica na aba Usuários na tela Usuários, pesquisa o nome do colaborador e ao selecionar aperta em Excluir.

Entrevista Responsável GeP:
O gestor informa sobre o desligamento do colaborador para demissão ou orienta a pessoa a procurar o GeP ou também por parte do colaborador mesmo para pedido de demissão ele que procura GeP para pedir demissão.

Após isso GeP envia um e-mail para o suporte@mosten.com sinalizando entrada ou saída de pessoas (Entrada/Saida de pessoas é um grupo com gestores que podem ser necessários tomar alguma ação ou ficar ciente).

No conteúdo do e-mail GeP sinaliza o último dia de trabalho da pessoa, sinalizando que a partir dessa data é responsabilidade da TI a sequência (bloqueio de acessos e etc).


---
# Processo de Gestão de Wi-Fi ⏳
Para liberação de acesso à internet é feito no Unify para cadastro do MAC da máquina do solicitante

---
# Auditoria Zurich ✅

---
# Solicitação e Recebimento de Máquinas e Credenciais ✅
Problemas/Gaps:
●        Ausência de prazo formal com o Backoffice para retirada e entrega da máquina via motoboy: hoje o prazo varia entre o mesmo dia e até 2 dias, gerando custo financeiro pela demora no início de atuação do profissional.

●        Envio de máquinas com base em modelo que a Zurich já havia retirado da lista de homologados, sem aviso prévio ao Gestor de Contas — gerou atraso relevante em caso recente de contratação.

●        Falta de controle consolidado de qual máquina está com qual profissional, incluindo casos de desligamento em que a máquina permanece com o ex-profissional por período superior a 20 dias sem devolução.

●        Processo de aprovação de retirada/envio de máquina em transição, sem responsável formalmente definido desde a saída do aprovador anterior da área.

●        Dependência da Zurich para informar atualizações na lista de homologados e o prazo de validade de cada modelo, sem periodicidade de comunicação definida pelo cliente. 