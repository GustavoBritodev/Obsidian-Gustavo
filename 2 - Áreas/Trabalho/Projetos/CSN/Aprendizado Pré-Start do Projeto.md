# Glossário Solicitação de Liberação de Carga Solta:
## Bill Of Lading (BL):
O Bill of Lading (BL), ou Conhecimento de Embarque, é o documento mais importante do modal aquaviário no comércio exterior, atuando como contrato de transporte, recibo de entrega da mercadoria e título de crédito (documento de propriedade). 

Emitido pelo transportador (armador) ao expedidor, ele contém informações essenciais como:
- Identificação das Partes: Dados do remetente, consignatário e destinatário. 
- Descrição da Carga: Quantidade, tipo e classificação fiscal das mercadorias.
- Rotas: Porto de embarque e porto de destino. 
- Termos: Condições e responsabilidades do transporte.

Para retirar a carga no destino final, o possuidor legítimo do BL original deve apresentá-lo ao transportador, validando assim o direito sobre a mercadoria.

Dentre as principais finalidades do BL, podemos elencar:

1. Recibo de entrega da mercadoria: a bordo do navio ou ao transportador. A posse do BL é a comprovação documental do armador de recebimento da carga para transporte;
2. Título de Crédito: é o documento de retirada da mercadoria junto ao transportador no destino final;
3. Contrato de Transporte entre o embarcador e o transportador, sendo emitido após o embarque da carga contratada.

O BL deve constar as seguintes informações:
- A denominação da empresa emissora;
- O número de ordem do documento;
- A data da emissão;
- Os nomes e endereços completos do embarcador e do consignatário;
- O lugar de partida e o destino;
- A espécie e a quantidade ou peso da mercadoria, a quantidade e natureza dos volumes, bem como sinais externos dos mesmos (marcas e números);
- A importância do frete, com a declaração de que é pago (prepaid) ou a pagar (collect);
- A assinatura do emitente

O BL deve indicar também o estado aparente das mercadorias. A cláusula clean on board indica que as mercadorias estão em bom estado aparente, de acordo com as marcas e numeração fornecidas pelo embarcador.
Do mesmo modo, o B/L deverá identificar a unidade de carga em que a mercadoria por ele coberta esteja contida (Regulamento Aduaneiro, artigo 41, § 2º).

Fonte: [Link de consulta completo sobre BL](https://www.fazcomex.com.br/comex/bill-of-lading-bl-o-que-e/)

---
## DUIMP:
A DUIMP (Declaração Única de Importação) é o novo documento eletrônico central do Novo Processo de Importação (NPI) no Brasil, que substitui as antigas Declaração de Importação (DI) e Declaração Simplificada (DSI).  Ela unifica em um único registro digital todas as informações aduaneiras, administrativas, comerciais, financeiras, fiscais e tributárias necessárias para o controle das importações pelo Portal Único de Comércio Exterior. 

O principal objetivo da implementação da DUIMP é reduzir a burocracia e agilizar o desembaraço, permitindo que o importador realize o registro antecipado antes mesmo da chegada da carga.  Entre as vantagens estão a eliminação de redundâncias de dados, a centralização de licenças através do módulo LPCO (Licenças, Permissões, Certificados e Outros Documentos) e a integração automática com o Catálogo de Produtos para padronizar descrições e reduzir erros. 

A obrigatoriedade da DUIMP está sendo implementada gradualmente pela Receita Federal:
- A partir de outubro de 2024: Obrigatória para regimes aduaneiros especiais como RECOF, REPETRO e Admissão Temporária.
- Expansão progressiva: A obrigatoriedade está sendo estendida para outros modais (aéreo e terrestre) e modalidades de licenciamento. 
- Desligamento do sistema antigo: O sistema anterior de LI/DI está previsto para ser desligado no final de 2025, transferindo todas as operações para o Portal Único.

--- 
## Carga Solta:
Carga solta refere-se a mercadorias transportadas individualmente, sem estarem agrupadas ou embaladas de maneira uniforme em paletes ou contêineres padrão.  Essa modalidade é amplamente utilizada para itens de diferentes tipos, formas e tamanhos, como máquinas industriais, equipamentos pesados, tubos, barras de metal e produtos agrícolas em sacarias. 

As principais características e implicações da carga solta incluem:
- Flexibilidade e Adaptação: Permite o transporte de produtos diversificados sem a necessidade de unitização, sendo ideal para empresas com volumes variáveis ou itens que não se encaixam em contêineres. 
- Custo e Eficiência: Pode reduzir custos ao permitir o pagamento apenas pelo espaço utilizado (especialmente em operações LCL - Less than Container Load) e evitar a espera para preencher um contêiner inteiro, embora possa demandar equipamentos especiais como guindastes ou empilhadeiras. 
- Riscos e Manuseio: Exige maior cuidado operacional, pois a falta de embalagem padronizada aumenta o risco de avarias e o tempo de carregamento/descarregamento, necessitando de fixação adequada e proteção das mercadorias. 
- Diferenciação: Diferente da carga unitizada (em contêineres ou paletes), a carga solta é manuseada individualmente, o que facilita o rastreamento de cada peça, mas complexifica a logística de armazenamento e movimentação em armazéns.

Fonte: [Link de consulta completo sobre Carga Solta](https://www.selflogistica.com.br/blog/carga-solta)

---
## API Siscomex:
A API do Portal Único Siscomex (PUCOMEX) é a interface baseada em arquitetura REST que permite a integração entre sistemas privados e os órgãos públicos de comércio exterior, utilizando formatos XML (com validação XSD) e JSON com codificação UTF-8. 
Para operar, é necessário realizar autenticação via certificado digital (e-CNPJ) enviando uma requisição POST ao endpoint de autenticação, definindo o Role-Type adequado ao perfil do interveniente. 

As principais funcionalidades e áreas de atuação incluem:

- Controle de Carga e Trânsito (CCT): Permite registrar a custódia, recepção, unitização, desunitização, consolidação, entrega e acompanhamento de cargas de exportação e importação via webservice. 
- DUIMP (Importação): Facilita o envio, atualização, retificação e consulta de status da Declaração Única de Importação, integrando-se a módulos como Catálogo de Produtos e Tratamento Tributário. 
- Recintos Aduaneiros: Oferece endpoints para eventos como atracação, desatracação e controle de acesso, com recentes atualizações em validações e novos campos (Notícia Siscomex nº 004/2024). 
- Dados Públicos: Disponibiliza consultas abertas, como a API de nomenclatura NCM para download de dados em JSON. 

Os ambientes de desenvolvimento e uso são divididos em:

- Validação/Treinamento: https://val.portalunico.siscomex.gov.br
- Produção: https://portalunico.siscomex.gov.br

Importante: A partir de 18 de março de 2025, o Portal Único não dará mais suporte a conexões utilizando protocolos TLSv1.0 ou TLSv1.1, sendo obrigatório o uso da versão TLSv1.2.  A documentação técnica completa está disponível em docs.portalunico.siscomex.gov.br.

---
## Portal TECON (CSN):
O Portal do Cliente TECON refere-se às plataformas online operadas pela Wilson Sons para a gestão logística de seus terminais de contêineres.  O acesso principal e o cadastro de usuários são realizados através do endereço https://portal.teconsvonline.com.br. 

Este portal oferece serviços específicos para o Tecon Salvador e outras unidades, incluindo:
- Consulta de faturamento e 2ª via de notas fiscais.
- Agendamento de entrega e retirada de contêineres. 
- Consulta da programação de navios e status de booking. 
- Agendamento de serviços internos, como vistorias e fumigação.

Para obter acesso, é necessário solicitar login e senha através do próprio site clicando em "Cadastre-se!", preenchendo os dados da razão social e enviando procurações se for despachante. O suporte é realizado pelos e-mails atendimento.tcsv@wilsonsons.com.br ou pelo WhatsApp (71) 2106-1500. 

Existem outras unidades do grupo com portais distintos, como o Tecon Rio Grande (acesso via Teconline) e o Sepetiba Tecon (operado pela CSN, com portal próprio em portaltecon.csn.com.br).

Fonte: [Site CSN Tecon](https://www.csn.com.br/quem-somos/grupo-csn/sepetiba-tecon/), [Portal Tecon](https://portaltecon.csn.com.br/)

---
## Solicitação de liberação de importação:
A liberação da importação é concluída quando o processo é aprovado pela alfândega, permitindo que a mercadoria entre no país. O pedido é considerado "liberado na alfândega de importação" quando todas as verificações legais, aduaneiras e documentais foram atendidas com sucesso. 

A agilidade desse processo depende de fatores como:
- Documentação correta: Ausência de erros ou omissões nos documentos de importação. 
- Classificação fiscal: Adequação da Nomenclatura Comum do Mercosul (NCM) da mercadoria.
- Inspeções físicas: A alfândega pode realizar vistorias para confirmar a conformidade dos produtos. 

Para produtos que exigem controle específico, é necessário obter a Licença de Importação (LI) ou autorização de órgãos anuentes (como Anvisa, Inmetro, Ibama) antes do embarque, o que pode levar até 60 dias para deferimento.  A falta dessa autorização pode resultar em retenção da carga e multas.

Fonte: [Link consulta sobre Licença de Importação](https://www.gruposerpa.com.br/licenca-de-importacao/)

---
## DI Comex:
A Declaração de Importação (DI) é o documento eletrônico que formaliza e regulariza as informações do processo de importação de mercadorias no Brasil, servindo como base para o despacho aduaneiro junto à Receita Federal.  Elaborada por meio do Siscomex Web, ela reúne dados comerciais, fiscais, cambiais e tributários da operação. 

Atualmente, o Brasil está em transição para o Novo Processo de Importação (NPI), no qual a DI será substituída pela DUIMP (Declaração Única de Importação).  A DUIMP unifica informações aduaneiras, administrativas e fiscais em um único registro digital, integrando-se ao Portal Único de Comércio Exterior para reduzir burocracia e aumentar a eficiência. 

Principais Aspectos da DI:
- Funcionamento: Registra informações gerais da operação e dados específicos das mercadorias (valores, impostos, origem). 
- Vinculação: Pode estar associada a uma Licença de Importação (LI), quando necessária para certas mercadorias, ou ser independente. 
- Transição: A migração para a DUIMP visa eliminar redundâncias e permitir o início do processo antes da chegada da mercadoria.

Fonte: [Link consulta sobre DI](https://toexceed.com.br/blog/2026/01/27/entenda-a-declaracao-de-importacao-di-no-comercio-exterior/)

---
## Carta de Correção de Retificação da DI:
A retificação de DI (Declaração de Importação) é o processo de correção de informações prestadas previamente ou inclusão de novos dados no Siscomex, permitindo ajustes em dados comerciais, fiscais e cambiais durante o trânsito da mercadoria. 

Este processo é realizado via sistema Siscomex e depende da aprovação da Receita Federal, que homologa as alterações e recolhe diferenças de crédito tributário, se houver. 

- O que pode ser alterado: Informações relacionadas ao transporte, carga e tributos devidos. 
- Consequência do indeferimento: Se a retificação for indeferida, o desembaraço da mercadoria não pode prosseguir, permanecendo o processo pendente até uma nova solicitação. 
- Diferença da Carta de Correção: Diferente da Carta de Correção Eletrônica (CC-e) da NF-e, que é um evento anexado ao documento fiscal, a retificação da DI modifica diretamente os dados cadastrais e operacionais no sistema aduaneiro.

Fonte: [Link consulta sobre Retificação de DI](https://conexoscloud.com.br/o-que-e-a-retificacao-de-di/)

---
# Glossário Gate e Portal Tecon:
## SCG:
No contexto do Comércio Exterior (Comex), SCG refere-se ao Sistema Global de Preferências Comerciais entre Países em Desenvolvimento (em inglês, System of Global Preferential Commercialization). 

Trata-se de um acordo comercial firmado no âmbito da UNCTAD (Conferência das Nações Unidas sobre Comércio e Desenvolvimento) em 1988, que visa promover o comércio Sul-Sul entre nações em desenvolvimento da África, Ásia e América Latina. 

Principais características:
- Objetivo: Conceder preferências tarifárias (redução de impostos de importação) entre os países membros, fortalecendo laços econômicos sem depender exclusivamente de mercados desenvolvidos. 
- Membros: Atualmente conta com 43 países participantes, incluindo Brasil (como parte do Mercosul), Índia, China, Argentina, entre outros. 
- Benefício: Exportadores brasileiros podem obter redução de tarifas ao venderem para outros países signatários, desde que cumpram as Regras de Origem e apresentem o Certificado de Origem do SGPC, emitido por federações industriais credenciadas (como FIESP, FIESC, etc.). 

É importante não confundir com Siscomex (Sistema Integrado de Comércio Exterior), que é a plataforma digital do governo brasileiro para registro e controle de operações de importação e exportação.

---
## Bulk:
No contexto de Comércio Exterior (Comex), o termo Bulk refere-se a carga a granel, ou seja, mercadorias transportadas sem embalagem individualizada (soltas). 

Os principais conceitos associados são:
- Bulk Cargo: A própria carga a granel, como grãos, minérios ou combustíveis líquidos. 
- Bulk Carrier: O navio graneleiro, embarcação especializada e equipada com porões amplos para transportar esse tipo de carga. 
- Break Bulk: Uma categoria distinta que se refere ao transporte de carga solta ou em grandes unidades (como maquinários, veículos ou peças de construção), que não são a granel, mas também não são contêineres padrão. 
- Bulk Container: Contêineres especiais com aberturas (escotilhas) no teto, utilizados especificamente para acomodar carga sólida a granel.

---
## IMO:
No contexto do Comércio Exterior (Comex), IMO refere-se à Organização Marítima Internacional (International Maritime Organization) e, especificamente, ao conceito de Carga IMO, que designa cargas perigosas. 

São substâncias que, devido às suas características físicas e químicas, oferecem riscos à segurança pública, à saúde ou ao meio ambiente durante o transporte. Para fins de classificação e manipulação segura, essas cargas são divididas em 9 classes:
- Classe 1: Explosivos.
- Classe 2: Gases.
- Classe 3: Líquidos inflamáveis. 
- Classe 4: Sólidos inflamáveis.
- Classe 5: Substâncias combustíveis e materiais oxidantes. 
- Classe 6: Substâncias tóxicas e infecciosas. 
- Classe 7: Materiais radioativos.
- Classe 8: Substâncias corrosivas. 
- Classe 9: Mercadorias perigosas diversas.

Além da segurança, o termo IMO também está associado a regulamentações ambientais, como as mudanças de 2020, que visam reduzir a emissão de óxido de enxofre nos navios para preservar o meio ambiente.

---
## OOG:
Carga OOG (Out of Gauge) no comércio exterior refere-se a mercadorias que possuem dimensões excedentes (altura, largura ou comprimento) em relação às normas padrão de contêineres, resultando em custos mais altos de frete devido à ocupação de espaço adicional no navio (perda de slots). 

Para esse tipo de transporte, utiliza-se equipamentos específicos:
- Open Top: contêiner sem teto, ideal para cargas com excesso de altura que permitem carregamento pela parte superior.
- Flat Rack: contêiner sem laterais e teto, destinado a equipamentos grandes, máquinas industriais ou veículos com dimensões fora do padrão. 
- Plataforma: variação extrema do Flat Rack, usada para cargas com excesso simultâneo de altura, largura e comprimento. 

A escolha do equipamento depende da natureza da carga e das condições de transporte, sendo essencial evitar a utilização de contêineres Dry Box padrão para evitar danos e garantir a segurança da operação.

---
## DTA:
DTA (Declaração de Trânsito Aduaneiro) é o documento utilizado no Siscomex-Trânsito para autorizar o transporte de mercadorias importadas ou exportadas dentro do território nacional, ainda sob regime aduaneiro, sem a necessidade de desembaraço imediato. 

- Função Principal: Permite a transferência de cargas de uma Zona Primária (portos/aeroportos de entrada) para uma Zona Secundária (portos secos, CLIAs ou depósitos alfandegados), mantendo a suspensão dos tributos até o destino final. 
- Vantagens: Reduz custos de armazenagem e manuseio em zonas primárias, otimiza prazos logísticos e permite que o importador escolha o local mais estratégico para o desembaraço aduaneiro. 
- Requisitos Obrigatórios: O transporte deve ser realizado por transportadoras habilitadas pela Receita Federal, seguindo rotas pré-definidas, com uso de lacs de segurança e monitoramento do trânsito. 
- Penalidades: O descumprimento das normas, como desvio de rota ou extravio de carga, acarreta multas severas (ex: 10% a 50% do Imposto de Importação) ou até o perdimento da mercadoria e do veículo.

---
## DAT:
No contexto do comércio exterior brasileiro, DAT possui duas definições distintas dependendo da esfera operacional:

Documento de Acompanhamento de Trânsito: É o documento eletrônico utilizado para amparar o trânsito aduaneiro nacional de mercadorias já desembaraçadas, permitindo sua movimentação entre recintos alfandegados (zonas primárias e secundárias) sem a necessidade de novo desembaraço imediato.  Pode ser do tipo completo (vinculado a um veículo específico) ou simplificado (para transporte "em mãos" ou meios próprios).
Incoterm DAT (Delivered at Terminal): Era um termo comercial internacional que significava "Entregue no Terminal", onde o vendedor assumia todos os riscos e custos até deixar a mercadoria descarregada no terminal de destino designado.  Importante: Este Incoterm foi descontinuado na versão 2020 e substituído pelo DPU (Delivered at Place Unloaded - Entregue no Lugar Descarregado). 
Em resumo, se a dúvida refere-se a logística interna e alfândega, DAT é o documento de trânsito.  Se refere a contratos de venda internacional, refere-se a um termo extinto (agora DPU).

---
## Cargo Lot:
Carga lotação no contexto do Comércio Exterior (Comex) refere-se ao transporte exclusivo de uma única mercadoria ou embarcação, onde o veículo ou contêiner é destinado integralmente a um único remetente e destinatário. 

Diferente do transporte fracionado (LCL), que consolida cargas de múltiplos clientes, a lotação oferece:
- Exclusividade: O veículo ou contêiner não compartilha espaço com outras cargas.
- Agilidade: Menos manipulções e rotas mais diretas, reduzindo o tempo de trânsito.
- Segurança: Risco menor de avarias ou extravios devido ao manuseio reduzido.
- Ideal para: Cargas grandes, de alto valor, perecíveis ou que necessitam de cuidados especiais. 

Empresas de logística integrada, como a Total Comex e a Comex Cargo, oferecem soluções de transporte em lotação para operações de importação e exportação, garantindo rastreio e segurança desde a origem até o destino final nos principais portos e aeroportos do Brasil.

---
## Gate Transaction:
No contexto do Comex (Comércio Exterior), gate transaction refere-se ao ato de depositar o contêiner no terminal portuário, conhecido como "gate in". 
- Definição: É a data em que o terminal portuário abre seus portões para receber o contêiner estufado (carregado) com a carga para exportação. 
- Importância: Este evento é crucial porque só após o "gate in" o despachante aduaneiro pode iniciar o processo de desembaraço e liberação para embarque no navio. 
- Prazos: O "dia do gate" antecede a dead line (data limite de entrega da carga no porto).  Falhar nessa etapa pode resultar na perda da reserva do contêiner no navio (booking) e incidência de multas por demurrage (sobreestadia no porto).

---
## Gate Configuration:
No contexto do Comex (comércio exterior), o termo "gate" refere-se principalmente a dois conceitos distintos: a data limite de entrada do contêiner no terminal e uma taxa operacional associada a esse evento. 

1. Gate-in (Data Limite)
É a data em que o terminal portuário abre os portões para receber o contêiner estufado (carregado) com a carga para exportação. Esta data é crítica porque:

- Antecede o dead line do despachante aduaneiro.
- É o momento em que o embarcador deve depositar o contêiner para permitir que o despachante inicie o desembaraço aduaneiro.
- O atraso na entrada do contêiner após o "gate-in" pode resultar na perda do booking (reserva no navio) e na incidência de taxas de demurrage. 

2. Gate-in Fee (Taxa)
É uma taxa local de origem cobrada pelos agentes de cargas ou armadores, definida como a taxa de recepção das unidades no terminal.  Ela compensa os custos operacionais do terminal pela entrada e manuseio inicial do contêiner vazio ou carregado.

Em resumo, a "gate configuration" ou gestão do gate envolve o planejamento para garantir que o contêiner entre no terminal antes da data limite (gate-in date) para evitar multas e atrasos, considerando também o custo da gate-in fee.

---
## Desembaraço Aduaneiro:
O desembaraço aduaneiro é a etapa final do processo de comércio exterior, consistindo na liberação de mercadorias pela Receita Federal para entrada (importação) ou saída (exportação) do território nacional. 

Trata-se do ato formal que conclui a conferência aduaneira, confirmando que a carga está em conformidade com as normas legais, fiscais e sanitárias, o que permite a emissão do Comprovante de Importação e a entrega da mercadoria ao importador. 

Principais Características:
- Objetivo: Garantir o cumprimento da legislação aduaneira e a regularidade da operação. 
- Responsabilidade: A fiscalização é feita pela Receita Federal, mas o processo deve ser conduzido por um despachante aduaneiro credenciado contratado pelo importador. 
- Diferença do Despacho: Enquanto o despacho aduaneiro envolve todo o trâmite burocrático e de conferência de dados, o desembaraço é especificamente a liberação física e legal da carga.

---
## Gate IN e Gate OUT
Em operações de comércio exterior, Gate In e Gate Out são registros técnicos que definem a entrada e a saída física de contêineres nos terminais portuários ou depósitos alfandegados. 

- Gate In: Refere-se ao momento em que o contêiner (vazio para estufagem ou cheio para embarque) entra no recinto alfandegado. É a data crítica que antecede o dead line do embarque, permitindo o início do desembaraço aduaneiro. Em 2026, a conferência de peso é feita eletronicamente neste momento, integrando-se ao Portal Único Siscomex. 
- Gate Out: Significa a saída oficial do contêiner do terminal ou porto. Na importação, ocorre após a descarga do navio e liberação aduaneira, quando o caminhoneiro retira a carga para entrega no destino final. Na exportação, refere-se à retirada do contêiner vazio após a descarga ou do cheio após o embarque, dependendo do acordo. 

Esses registros são fundamentais para o cálculo de taxas como Demurrage (permanência da carga no terminal além do tempo livre) e Detention (retenção do equipamento fora do terminal além do prazo), variando conforme o armador e as condições contratuais.
