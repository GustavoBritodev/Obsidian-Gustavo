- Back end + Bando de dados:
	Linguagens: Java e SQL
	Frameworks: Spring Boot
	Banco de dados: H2 (banco para testes) e PostgresSQL (banco para implementação em nuvem)

- Front end
	Linguagens: HTML/CSS e Javascript
	Frameworks/Lib: ReactJS

Front end conversa com o back end por meio de requisições web (HTTP/JSON)
HTTP é o protocolo que processa requisições na web
Os dados que vierem das requisições estarão em formato JSON

**API Rest**
Padrão Rest
- Cliente/Servidor com HTTP (Nem todo sistema Cliente/Servidor é Rest, mas se for Rest é Cliente/Servidor)
- Comunicação stateless (Stateless = sem estado. Essa comunicação não guarda estado. Quando eu faço uma requisição, o resultado dessa requisição não depende de algo que foi salvo previamente. Não é necessário se preocupar se na sessão do usuário está salvo alguma coisa que possa vir a dar algum resultado diferente. Vantagens: Se minha API é stateless isso vai simplificar o processo de projetar e implementar o sistema)
- Interface uniforme, formato padronizado(Exemplo na imagem)
- Cache (é possível salvar algumas informações para obter de forma mais rápida)
- Sistema em camadas
- Código sob demanda (opcional)

Imagem padronização: 
![[Pasted image 20250123211150.png]]




O front end conversará com o back end. O back end será dividido em 3 camadas, ele terá controladores REST que conversarão com componentes da camada de serviço que conversarão com a camada de acesso a dados que é a camada que faz consultas ao banco de dados. Entre a camada de acesso a dados e a camada de serviço iremos comunicar objetos do tipo entidade (entities). Já entre a camada de serviço e a camada de controladores irão trafegar objetos do tipo DTO (Data Transfer Objects)

![[Pasted image 20250123211116.png]]

ORM = Mapeamento objeto relacional

DTO = Data Transfer Objects (A funcionalidade do DTO é filtrar dados da camada de serviço e levar até os controladores apenas os dados filtrados.  O problema seria eu buscar eventualmente na minha entidade que tem muitos dados mas eu querer levar até a API um conjunto menor de dados, então para projetar esse conjunto menor de dados o padrão utilizado é o DTO)

O controlador recebe de serviço objetos DTO

Na arquitetura de camadas o repository (camada de acesso a dados) será um objeto de acesso a dados que fará a consulta no banco e trará do banco de dados os "games" (tema do projeto) e devolverá isso para uma classe/componente de service (camada de serviço) e o service por sua vez devolverá o DTO equivalente para o controlador (controladores REST).

O repository é um objeto responsável por fazer consultas ao banco de dados.

O projeto usa o desenvolvimento orientado por domínio, ou seja, como no projeto temos a entidade game logo o repository que for trabalhar com game se chamará GameRepository, se no sistema a entidade fosse cliente então se chamaria ClienteRepository. Dessa forma é possível padronizar o nome das classes usando o nome da entidade/domínio + sufixo do tipo de componente que é. Ex: GameRepository (Camada de acesso a dados), GameService (Camada de serviço) e GameController (Camada de controladores REST). Essa prática serve para padronizar os nomes dos componentes que serão utilizados no sistema.

O componente service é o responsável por implementar a regra de negócio.

O controller é responsável por implementar a API. O controlador que expõe o endpoint para o front end, após isso o controlador irá chamar o serviço que irá chamar o repository que irá chamar o banco de dados.

A API é a "interface" do back-end, o front-end chama os dados do back-end por meio da API.

Na arquitetura de camadas o controller injeta o service enquanto o service por sua vez injeta o repository

O DTO é usado para customizar os dados de saída da API

No CORS_ORIGINS é necessário especificar quais hostings/endereços estão autorizados a acessar seu back-end. Exemplo: Implantei o back-end na nuvem e criei um site chamado lojadogustavo.com, a lojadogustavo.com precisa estar autorizada dentro da variável CORS_ORIGINS para o back-end responda por ela.

Idempotência: Uma operação é idempotente quando ela executada uma ou mais vezes ela produz o mesmo resultado (Verbo PUT). Quando você executa uma operação e em cada execução diferente produz resultados diferentes então não é idempotente (Verbo POST)


![[Pasted image 20250126221718.png]]

O print acima mostra o exemplo do funcionamento do List Replacement