---
tags:
  - tipo/trabalho/projeto/gestao_de_inventrio_mosten
---
#TarefasLuiz/EasyInventory

Easy Inventory era onde faziam a gestão de patrimônio da empresa, no EI adicionavam qual é a máquina (número de patrimônio), com quem está a máquina e etc.
Vantagem: Permitia geo localização da máquina.

A gestão de patrimônio era feita usando planilhas e o Easy Inventory.


GLPI tem uma seção de Ativos dentro da entidade mãe "Mosten", nessa tela o André cadastrou todas as  máquinas que estão em uso por pessoa

Desvantagem do Easy Inventory era que por exemplo os Macs da empresa não conseguiam ser cadastrados, diferentemente do GLPI que o processo de cadastro de patrimônio é manual e permite 

Easy Inventory possui funcionalidades de visualizar os softwares instalados na máquina, a geolocalização, dados de performance da máquina, todas as informações do harware da máquina, campos de data de garantia da máquina e meses até depreciação, também contém um campo para inclusão da nota fiscal da compra da máquina.
O Easy Inventory permite a exportação desses dados para .XLSX, PDF e CSV.

Pensando em Gestão de Inventários simples a forma atual (nativa) o GLPI atende, visto que antigamente a gestão de inventários era feita com manutenção de planilhas e uso do Easy Inventory. Na forma atual no GLPI o cadastro de máquina vem com título do responsável e tag do projeto para casos específicos, também é incluído o número de inventário e em alguns casos (Máquinas Mosten) também o ServiceTag. A classificação das máquinas é por responsável da mesma.

Atualmente todas as máquinas Mosten em uso estão mapeadas e inventariadas no GLPI, porém existem máquinas e periféricos guardadas ainda não estão inventariadas e analisadas se possuem avarias ou não.

Nativo no GLPI existe o módulo de Ativos onde tem telas para Dashboard, Computadores, Monitores, Softwares, Dispositivos de rede, Periféricos, Impressoras, Cartuchos, Telefones, Racks, Chassis, PDUs, Dispositivos Passivos, Cabos, Cartão SIM Itens.

Hoje temos de inventário mapeado as máquinas em uso e os monitores da empresa.

Como potencial de melhoria para o GLPI existe o Plugin GLPI Inventory que traz inventário de hardware da máquina

