Home Page:
Acessei um Evento qualquer e tentei Favoritar não está funcionando os Favoritar
![[Pasted image 20260409200840.png]]
```
## Error Type
Runtime Error

## Error Message
Erro ao favoritar evento


    at favoriteEventApi (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0jk2sm2._.js:836:24)
    at async useToggleFavorite.useMutation[favorite] [as mutationFn] (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0jk2sm2._.js:898:21)

Next.js version: 16.2.2 (Turbopack)

```

Pagina de Eventos faltou a possibilidade de filtras por cidades já que na home page é possível fazer esse filtro. além disso onde está por Ordenar só é possível ordenar por Relevância mas como está sendo calculado a Relavância do Evento ? Precisamos considerar isso e validar se está correto além disso seria bom também ser possível ordenar por Valor ou Data TAMBÉM
http://localhost:8080/eventos
![[Pasted image 20260409201450.png]]


Verificar a questão das Colecoes pois já tenho Eventos cadastrados que possuem as tags então ao explorar por coleção deveria estar aparecendo os respectivos EVENTOS referente a colecao
![[Pasted image 20260409201619.png]]![[Pasted image 20260409201655.png]]


Sobre a Home page.
Podemos manter a section de TOP 10 Eventos da semana mas mudar o nome para Em alta nas últimas 24h para manter a estrutura que ja existe nessa section com 10 enventos sendo exibidos e a section de em alta nas ultimas 24 h podemos excluir pois é redundante

Além disso  o critério para classificar os Eventos que serão por visualização única por IP
![[Pasted image 20260409202521.png]]


página pages/sobre 
Precisamos melhorar a página que explica sobre quem somos a ballon tickets esa page está muito crua

Ná paginas de cliente/perfil  temos a opção de atualizar o nome Completo e o Tefelone ao alterar essas informações e clicar em salvar alterações aparece o pop de alterações salvas com sucesso mas no banco de dados as informações não são atualizadas. Mesma coisa para o Endereço desse usuario que também não seria atualizado
![[Pasted image 20260409203405 1.png]]
![[Pasted image 20260409203251 1.png]]

Sessão de Segurança para alterar senha está completamente funcional porem precisamos adicionar um validação por E-mail. Antes da possa poder definitamente alterar a senha jogar o condigo de confirmação enviado por E-mail da mesma forma que é feito no processo de criação de contas o mesmo vale para os produtores.
![[Pasted image 20260409203851 1.png]]

Testando a funcionalidade de Exclusão de contas.
Primeiro de tudo corrigir o POP-UP e segundo também implementar a confirmação por E-mail para exclusão de conta. Funcionalidade de eXCLUSÃO DE CONTAS NÃO ESTÁ FUNCIONANDO
 DELETE /api/proxy/users/me 500 in 14.0s (next.js: 34ms, application-code: 14.0s)

![[Pasted image 20260409204254 1.png]]
![[Pasted image 20260409204056 1.png]]

```
                         │ │
│ │         │   │   (b'sec-fetch-mode', b'cors'),                       
                         │ │
│ │         │   │   (b'user-agent', b'node'),                           
                         │ │
│ │         │   │   (b'accept-encoding', b'gzip, deflate'),             
                         │ │
│ │         │   │   (b'content-length', b'25')                          
                         │ │
│ │         │   ],                                                      
                         │ │
│ │         │   'state': {'request_id': 'dccf2592-0543-4fcd-bbcf-986b29b5091d'},              │ │
│ │         │   'method': 'DELETE',                                     
                         │ │
│ │         │   ... +10                                                 
                         │ │
│ │         }                                                           
                         │ │
│ │  self = APIRoute(path='/api/v1/users/me', name='delete_my_account', methods=['DELETE'])      │ │
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────╯ │
│                                                                       
                           │
│ C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\routing.py:77 in app                │
│                                                                       
                           │
│    74 │   │   │   │   response = await run_in_threadpool(func, request)                │
│    75 │   │   │   await response(scope, receive, send)                
                           │
│    76 │   │                                                           
                           │
│ ❱  77 │   │   await wrap_app_handling_exceptions(app, request)(scope, receive, send)             │
│    78 │                                                               
                           │
│    79 │   return app                                                  
                           │
│    80                                                                 
                           │
│                                                                       
                           │
│ ╭─────────────────────────────────────────── locals ───────────────────────────────────────────╮ │
│ │ request = <starlette.requests.Request object at 0x00000231FF409A30> 
                         │ │
│ │   scope = {                                                         
                         │ │
│ │           │   'type': 'http',                                       
                         │ │
│ │           │   'asgi': {'version': '3.0', 'spec_version': '2.3'},    
                         │ │
│ │           │   'http_version': '1.1',                                
                         │ │
│ │           │   'server': ('127.0.0.1', 8000),                        
                         │ │
│ │           │   'client': ('127.0.0.1', 51231),                       
                         │ │
│ │           │   'scheme': 'http',                                     
                         │ │
│ │           │   'root_path': '',                                      
                         │ │
│ │           │   'headers': [                                          
                         │ │
│ │           │   │   (b'host', b'localhost:8000'),                     
                         │ │
│ │           │   │   (b'connection', b'keep-alive'),                   
                         │ │
│ │           │   │   (                                                 
                         │ │
│ │           │   │   │   b'authorization',                             
                         │ │
│ │           │   │   │   b'Bearer                                      
                         │ │
│ │           eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzU3Nzk2MTksImlhdCI6MTc3'+163     │ │
│ │           │   │   ),                                                
                         │ │
│ │           │   │   (b'content-type', b'text/plain;charset=UTF-8'),   
                         │ │
│ │           │   │   (b'accept', b'*/*'),                              
                         │ │
│ │           │   │   (b'accept-language', b'*'),                       
                         │ │
│ │           │   │   (b'sec-fetch-mode', b'cors'),                     
                         │ │
│ │           │   │   (b'user-agent', b'node'),                         
                         │ │
│ │           │   │   (b'accept-encoding', b'gzip, deflate'),           
                         │ │
│ │           │   │   (b'content-length', b'25')                        
                         │ │
│ │           │   ],                                                    
                         │ │
│ │           │   'state': {'request_id': 'dccf2592-0543-4fcd-bbcf-986b29b5091d'},              │ │
│ │           │   'method': 'DELETE',                                   
                         │ │
│ │           │   ... +10                                               
                         │ │
│ │           }                                                         
                         │ │
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────╯ │
│                                                                       
                           │
│ C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_exception_handler.py:75 in           │
│ wrapped_app                                                           
                           │
│                                                                       
                           │
│   72 │   │   │   │   handler = typing.cast(HTTPExceptionHandler, handler)                │
│   73 │   │   │   │   conn = typing.cast(Request, conn)                
                           │
│   74 │   │   │   │   if is_async_callable(handler):                   
                           │
│ ❱ 75 │   │   │   │   │   response = await handler(conn, exc)          
                           │
│   76 │   │   │   │   else:                                            
                           │
│   77 │   │   │   │   │   response = await run_in_threadpool(handler, conn, exc)                │
│   78 │   │   │   │   await response(scope, receive, sender)           
                           │
│                                                                       
                           │
│ ╭─────────────────────────────────────────── locals ───────────────────────────────────────────╮ │
│ │               conn = <starlette.requests.Request object at 0x00000231FF409A30>              │ │
│ │ exception_handlers = {                                              
                         │ │
│ │                      │   <class 'starlette.exceptions.HTTPException'>: <function             │ │
│ │                      http_exception_handler at 0x00000231FAB9E020>, 
                         │ │
│ │                      │   <class 'starlette.exceptions.WebSocketException'>: <bound method    │ │
│ │                      ExceptionMiddleware.websocket_exception of     
                         │ │
│ │                      <starlette.middleware.exceptions.ExceptionMiddleware object at          │ │
│ │                      0x00000231FE8A91C0>>,                          
                         │ │
│ │                      │   <class 'fastapi.exceptions.RequestValidationError'>: <function      │ │
│ │                      validation_exception_handler at 0x00000231FE83C040>,              │ │
│ │                      │   <class 'fastapi.exceptions.WebSocketRequestValidationError'>:       │ │
│ │                      <function websocket_request_validation_exception_handler at             │ │
│ │                      0x00000231FAB9E160>,                           
                         │ │
│ │                      │   <class 'sqlalchemy.exc.SQLAlchemyError'>: <function              │ │
│ │                      sqlalchemy_exception_handler at 0x00000231FE813F60>              │ │
│ │                      }                                              
                         │ │
│ │   response_started = False                                          
                         │ │
│ │              scope = {                                              
                         │ │
│ │                      │   'type': 'http',                            
                         │ │
│ │                      │   'asgi': {'version': '3.0', 'spec_version': '2.3'},              │ │
│ │                      │   'http_version': '1.1',                     
                         │ │
│ │                      │   'server': ('127.0.0.1', 8000),             
                         │ │
│ │                      │   'client': ('127.0.0.1', 51231),            
                         │ │
│ │                      │   'scheme': 'http',                          
                         │ │
│ │                      │   'root_path': '',                           
                         │ │
│ │                      │   'headers': [                               
                         │ │
│ │                      │   │   (b'host', b'localhost:8000'),          
                         │ │
│ │                      │   │   (b'connection', b'keep-alive'),        
                         │ │
│ │                      │   │   (                                      
                         │ │
│ │                      │   │   │   b'authorization',                  
                         │ │
│ │                      │   │   │   b'Bearer                           
                         │ │
│ │                      eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzU3Nzk2MTksImlhdCI6M… │ │
│ │                      │   │   ),                                     
                         │ │
│ │                      │   │   (b'content-type', b'text/plain;charset=UTF-8'),              │ │
│ │                      │   │   (b'accept', b'*/*'),                   
                         │ │
│ │                      │   │   (b'accept-language', b'*'),            
                         │ │
│ │                      │   │   (b'sec-fetch-mode', b'cors'),          
                         │ │
│ │                      │   │   (b'user-agent', b'node'),              
                         │ │
│ │                      │   │   (b'accept-encoding', b'gzip, deflate'),
                         │ │
│ │                      │   │   (b'content-length', b'25')             
                         │ │
│ │                      │   ],                                         
                         │ │
│ │                      │   'state': {'request_id': 'dccf2592-0543-4fcd-bbcf-986b29b5091d'},    │ │
│ │                      │   'method': 'DELETE',                        
                         │ │
│ │                      │   ... +10                                    
                         │ │
│ │                      }                                              
                         │ │
│ │    status_handlers = {}                                             
                         │ │
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────╯ │
│                                                                       
                           │
│ C:\Users\Jonathan Relva\Documents\Projetos Pessoais\Balloon           
                           │
│ Tickets\backend-api\app\middleware\error_handler.py:69 in validation_exception_handler           │
│                                                                       
                           │
│    66 │   │   method=request.method,                                  
                           │
│    67 │   )                                                           
                           │
│    68 │                                                               
                           │
│ ❱  69 │   return JSONResponse(                                        
                           │
│    70 │   │   status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,       
                           │
│    71 │   │   content={                                               
                           │
│    72 │   │   │   "detail": _sanitize_errors(exc.errors()),           
                           │
│                                                                       
                           │
│ ╭─────────────────────────────────────────── locals ───────────────────────────────────────────╮ │
│ │     exc = RequestValidationError([{'type': 'model_attributes_type', 'loc': ('body',), 'msg': │ │
│ │           'Input should be a valid dictionary or object to extract fields from', 'input':    │ │
│ │           b'{"password":"Hptgrj@321"}', 'url':                      
                         │ │
│ │           'https://errors.pydantic.dev/2.5/v/model_attributes_type'}])              │ │
│ │ request = <starlette.requests.Request object at 0x00000231FF409A30> 
                         │ │
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────╯ │
│                                                                       
                           │
│ C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\responses.py:180 in __init__          │
│                                                                       
                           │
│   177 │   │   media_type: typing.Optional[str] = None,                
                           │
│   178 │   │   background: typing.Optional[BackgroundTask] = None,     
                           │
│   179 │   ) -> None:                                                  
                           │
│ ❱ 180 │   │   super().__init__(content, status_code, headers, media_type, background)            │
│   181 │                                                               
                           │
│   182 │   def render(self, content: typing.Any) -> bytes:             
                           │
│   183 │   │   return json.dumps(                                      
                           │
│                                                                       
                           │
│ ╭─────────────────────────────────────────── locals ───────────────────────────────────────────╮ │
│ │  background = None                                                  
                         │ │
│ │     content = {                                                     
                         │ │
│ │               │   'detail': [                                       
                         │ │
│ │               │   │   {                                             
                         │ │
│ │               │   │   │   'type': 'model_attributes_type',          
                         │ │
│ │               │   │   │   'loc': ('body',),                         
                         │ │
│ │               │   │   │   'msg': 'Input should be a valid dictionary or object to extract    │ │
│ │               fields from',                                         
                         │ │
│ │               │   │   │   'input': b'{"password":"Hptgrj@321"}',    
                         │ │
│ │               │   │   │   'url': 'https://errors.pydantic.dev/2.5/v/model_attributes_type'   │ │
│ │               │   │   }                                             
                         │ │
│ │               │   ],                                                
                         │ │
│ │               │   'type': 'validation_error'                        
                         │ │
│ │               }                                                     
                         │ │
│ │     headers = None                                                  
                         │ │
│ │  media_type = None                                                  
                         │ │
│ │        self = <starlette.responses.JSONResponse object at 0x00000231FF777BC0>              │ │
│ │ status_code = 422                                                   
                         │ │
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────╯ │
│                                                                       
                           │
│ C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\responses.py:39 in __init__           │
│                                                                       
                           │
│    36 │   │   if media_type is not None:                              
                           │
│    37 │   │   │   self.media_type = media_type                        
                           │
│    38 │   │   self.background = background                            
                           │
│ ❱  39 │   │   self.body = self.render(content)                        
                           │
│    40 │   │   self.init_headers(headers)                              
                           │
│    41 │                                                               
                           │
│    42 │   def render(self, content: typing.Any) -> bytes:             
                           │
│                                                                       
                           │
│ ╭─────────────────────────────────────────── locals ───────────────────────────────────────────╮ │
│ │  background = None                                                  
                         │ │
│ │     content = {                                                     
                         │ │
│ │               │   'detail': [                                       
                         │ │
│ │               │   │   {                                             
                         │ │
│ │               │   │   │   'type': 'model_attributes_type',          
                         │ │
│ │               │   │   │   'loc': ('body',),                         
                         │ │
│ │               │   │   │   'msg': 'Input should be a valid dictionary or object to extract    │ │
│ │               fields from',                                         
                         │ │
│ │               │   │   │   'input': b'{"password":"Hptgrj@321"}',    
                         │ │
│ │               │   │   │   'url': 'https://errors.pydantic.dev/2.5/v/model_attributes_type'   │ │
│ │               │   │   }                                             
                         │ │
│ │               │   ],                                                
                         │ │
│ │               │   'type': 'validation_error'                        
                         │ │
│ │               }                                                     
                         │ │
│ │     headers = None                                                  
                         │ │
│ │  media_type = None                                                  
                         │ │
│ │        self = <starlette.responses.JSONResponse object at 0x00000231FF777BC0>              │ │
│ │ status_code = 422                                                   
                         │ │
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────╯ │
│                                                                       
                           │
│ C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\responses.py:183 in render            │
│                                                                       
                           │
│   180 │   │   super().__init__(content, status_code, headers, media_type, background)            │
│   181 │                                                               
                           │
│   182 │   def render(self, content: typing.Any) -> bytes:             
                           │
│ ❱ 183 │   │   return json.dumps(                                      
                           │
│   184 │   │   │   content,                                            
                           │
│   185 │   │   │   ensure_ascii=False,                                 
                           │
│   186 │   │   │   allow_nan=False,                                    
                           │
│                                                                       
                           │
│ ╭─────────────────────────────────────────── locals ───────────────────────────────────────────╮ │
│ │ content = {                                                         
                         │ │
│ │           │   'detail': [                                           
                         │ │
│ │           │   │   {                                                 
                         │ │
│ │           │   │   │   'type': 'model_attributes_type',              
                         │ │
│ │           │   │   │   'loc': ('body',),                             
                         │ │
│ │           │   │   │   'msg': 'Input should be a valid dictionary or object to extract fields │ │
│ │           from',                                                    
                         │ │
│ │           │   │   │   'input': b'{"password":"Hptgrj@321"}',        
                         │ │
│ │           │   │   │   'url': 'https://errors.pydantic.dev/2.5/v/model_attributes_type'       │ │
│ │           │   │   }                                                 
                         │ │
│ │           │   ],                                                    
                         │ │
│ │           │   'type': 'validation_error'                            
                         │ │
│ │           }                                                         
                         │ │
│ │    self = <starlette.responses.JSONResponse object at 0x00000231FF777BC0>              │ │
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────╯ │
│                                                                       
                           │
│ C:\Anaconda\envs\ballontickets\Lib\json\__init__.py:238 in dumps      
                           │
│                                                                       
                           │
│   235 │   │   skipkeys=skipkeys, ensure_ascii=ensure_ascii,           
                           │
│   236 │   │   check_circular=check_circular, allow_nan=allow_nan, indent=indent,                │
│   237 │   │   separators=separators, default=default, sort_keys=sort_keys,                │
│ ❱ 238 │   │   **kw).encode(obj)                                       
                           │
│   239                                                                 
                           │
│   240                                                                 
                           │
│   241 _default_decoder = JSONDecoder(object_hook=None, object_pairs_hook=None)                │
│                                                                       
                           │
│ ╭─────────────────────────────────────────── locals ───────────────────────────────────────────╮ │
│ │      allow_nan = False                                              
                         │ │
│ │ check_circular = True                                               
                         │ │
│ │        default = None                                               
                         │ │
│ │   ensure_ascii = False                                              
                         │ │
│ │         indent = None                                               
                         │ │
│ │             kw = {}                                                 
                         │ │
│ │            obj = {                                                  
                         │ │
│ │                  │   'detail': [                                    
                         │ │
│ │                  │   │   {                                          
                         │ │
│ │                  │   │   │   'type': 'model_attributes_type',       
                         │ │
│ │                  │   │   │   'loc': ('body',),                      
                         │ │
│ │                  │   │   │   'msg': 'Input should be a valid dictionary or object to extract │ │
│ │                  fields from',                                      
                         │ │
│ │                  │   │   │   'input': b'{"password":"Hptgrj@321"}', 
                         │ │
│ │                  │   │   │   'url':                                 
                         │ │
│ │                  'https://errors.pydantic.dev/2.5/v/model_attributes_type'              │ │
│ │                  │   │   }                                          
                         │ │
│ │                  │   ],                                             
                         │ │
│ │                  │   'type': 'validation_error'                     
                         │ │
│ │                  }                                                  
                         │ │
│ │     separators = (',', ':')                                         
                         │ │
│ │       skipkeys = False                                              
                         │ │
│ │      sort_keys = False                                              
                         │ │
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────╯ │
│                                                                       
                           │
│ C:\Anaconda\envs\ballontickets\Lib\json\encoder.py:200 in encode      
                           │
│                                                                       
                           │
│   197 │   │   # This doesn't pass the iterator directly to ''.join() because the                │
│   198 │   │   # exceptions aren't as detailed.  The list call should be roughly                │
│   199 │   │   # equivalent to the PySequence_Fast that ''.join() would do.                │
│ ❱ 200 │   │   chunks = self.iterencode(o, _one_shot=True)             
                           │
│   201 │   │   if not isinstance(chunks, (list, tuple)):               
                           │
│   202 │   │   │   chunks = list(chunks)                               
                           │
│   203 │   │   return ''.join(chunks)                                  
                           │
│                                                                       
                           │
│ ╭─────────────────────────────────────────── locals ───────────────────────────────────────────╮ │
│ │    o = {                                                            
                         │ │
│ │        │   'detail': [                                              
                         │ │
│ │        │   │   {                                                    
                         │ │
│ │        │   │   │   'type': 'model_attributes_type',                 
                         │ │
│ │        │   │   │   'loc': ('body',),                                
                         │ │
│ │        │   │   │   'msg': 'Input should be a valid dictionary or object to extract fields    │ │
│ │        from',                                                       
                         │ │
│ │        │   │   │   'input': b'{"password":"Hptgrj@321"}',           
                         │ │
│ │        │   │   │   'url': 'https://errors.pydantic.dev/2.5/v/model_attributes_type'          │ │
│ │        │   │   }                                                    
                         │ │
│ │        │   ],                                                       
                         │ │
│ │        │   'type': 'validation_error'                               
                         │ │
│ │        }                                                            
                         │ │
│ │ self = <json.encoder.JSONEncoder object at 0x00000231FF4B2A50>      
                         │ │
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────╯ │
│                                                                       
                           │
│ C:\Anaconda\envs\ballontickets\Lib\json\encoder.py:258 in iterencode  
                           │
│                                                                       
                           │
│   255 │   │   │   │   markers, self.default, _encoder, self.indent, floatstr,                │
│   256 │   │   │   │   self.key_separator, self.item_separator, self.sort_keys,                │
│   257 │   │   │   │   self.skipkeys, _one_shot)                       
                           │
│ ❱ 258 │   │   return _iterencode(o, 0)                                
                           │
│   259                                                                 
                           │
│   260 def _make_iterencode(markers, _default, _encoder, _indent, _floatstr,                │
│   261 │   │   _key_separator, _item_separator, _sort_keys, _skipkeys, _one_shot,                │
│                                                                       
                           │
│ ╭─────────────────────────────────────────── locals ───────────────────────────────────────────╮ │
│ │    _encoder = <built-in function encode_basestring>                 
                         │ │
│ │ _iterencode = <_json.Encoder object at 0x00000231FF5B70A0>          
                         │ │
│ │   _one_shot = True                                                  
                         │ │
│ │     markers = {                                                     
                         │ │
│ │               │   2413758260928: {                                  
                         │ │
│ │               │   │   'detail': [                                   
                         │ │
│ │               │   │   │   {                                         
                         │ │
│ │               │   │   │   │   'type': 'model_attributes_type',      
                         │ │
│ │               │   │   │   │   'loc': ('body',),                     
                         │ │
│ │               │   │   │   │   'msg': 'Input should be a valid dictionary or object to        │ │
│ │               extract fields from',                                 
                         │ │
│ │               │   │   │   │   'input': b'{"password":"Hptgrj@321"}',
                         │ │
│ │               │   │   │   │   'url':                                
                         │ │
│ │               'https://errors.pydantic.dev/2.5/v/model_attributes_type'              │ │
│ │               │   │   │   }                                         
                         │ │
│ │               │   │   ],                                            
                         │ │
│ │               │   │   'type': 'validation_error'                    
                         │ │
│ │               │   },                                                
                         │ │
│ │               │   2413759991296: [                                  
                         │ │
│ │               │   │   {                                             
                         │ │
│ │               │   │   │   'type': 'model_attributes_type',          
                         │ │
│ │               │   │   │   'loc': ('body',),                         
                         │ │
│ │               │   │   │   'msg': 'Input should be a valid dictionary or object to extract    │ │
│ │               fields from',                                         
                         │ │
│ │               │   │   │   'input': b'{"password":"Hptgrj@321"}',    
                         │ │
│ │               │   │   │   'url': 'https://errors.pydantic.dev/2.5/v/model_attributes_type'   │ │
│ │               │   │   }                                             
                         │ │
│ │               │   ],                                                
                         │ │
│ │               │   2413760003264: {                                  
                         │ │
│ │               │   │   'type': 'model_attributes_type',              
                         │ │
│ │               │   │   'loc': ('body',),                             
                         │ │
│ │               │   │   'msg': 'Input should be a valid dictionary or object to extract fields │ │
│ │               from',                                                
                         │ │
│ │               │   │   'input': b'{"password":"Hptgrj@321"}',        
                         │ │
│ │               │   │   'url': 'https://errors.pydantic.dev/2.5/v/model_attributes_type'       │ │
│ │               │   },                                                
                         │ │
│ │               │   2413759992240: b'{"password":"Hptgrj@321"}'       
                         │ │
│ │               }                                                     
                         │ │
│ │           o = {                                                     
                         │ │
│ │               │   'detail': [                                       
                         │ │
│ │               │   │   {                                             
                         │ │
│ │               │   │   │   'type': 'model_attributes_type',          
                         │ │
│ │               │   │   │   'loc': ('body',),                         
                         │ │
│ │               │   │   │   'msg': 'Input should be a valid dictionary or object to extract    │ │
│ │               fields from',                                         
                         │ │
│ │               │   │   │   'input': b'{"password":"Hptgrj@321"}',    
                         │ │
│ │               │   │   │   'url': 'https://errors.pydantic.dev/2.5/v/model_attributes_type'   │ │
│ │               │   │   }                                             
                         │ │
│ │               │   ],                                                
                         │ │
│ │               │   'type': 'validation_error'                        
                         │ │
│ │               }                                                     
                         │ │
│ │        self = <json.encoder.JSONEncoder object at 0x00000231FF4B2A50>              │ │
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────╯ │
│                                                                       
                           │
│ C:\Anaconda\envs\ballontickets\Lib\json\encoder.py:180 in default     
                           │
│                                                                       
                           │
│   177 │   │   │   │   return super().default(o)                       
                           │
│   178 │   │                                                           
                           │
│   179 │   │   """                                                     
                           │
│ ❱ 180 │   │   raise TypeError(f'Object of type {o.__class__.__name__} '                │
│   181 │   │   │   │   │   │   f'is not JSON serializable')            
                           │
│   182 │                                                               
                           │
│   183 │   def encode(self, o):                                        
                           │
│                                                                       
                           │
│ ╭──────────────────────────── locals ────────────────────────────╮    
                           │
│ │    o = b'{"password":"Hptgrj@321"}'                            │    
                           │
│ │ self = <json.encoder.JSONEncoder object at 0x00000231FF4B2A50> │    
                           │
│ ╰────────────────────────────────────────────────────────────────╯    
                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
TypeError: Object of type bytes is not JSON serializable

INFO:     127.0.0.1:51231 - "DELETE /api/v1/users/me HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
  + Exception Group Traceback (most recent call last):
  |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_utils.py", line 85, in collapse_excgroups
  |     yield
  |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 190, in __call__
  |     async with anyio.create_task_group() as task_group:
  |                ^^^^^^^^^^^^^^^^^^^^^^^^^
  |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\anyio\_backends\_asyncio.py", line 783, in __aexit__
  |     raise BaseExceptionGroup(
  | ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)   
  +-+---------------- 1 ----------------
    | Traceback (most recent call last):
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\uvicorn\protocols\http\httptools_impl.py", line 419, in run_asgi
    |     result = await app(  # type: ignore[func-returns-value]       
    |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 84, in __call__
    |     return await self.app(scope, receive, send)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\fastapi\applications.py", line 1054, in __call__
    |     await super().__call__(scope, receive, send)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\applications.py", line 123, in __call__
    |     await self.middleware_stack(scope, receive, send)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    |     raise exc
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    |     await self.app(scope, receive, _send)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\cors.py", line 83, in __call__
    |     await self.app(scope, receive, send)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    |     with collapse_excgroups():
    |          ^^^^^^^^^^^^^^^^^^^^
    |   File "C:\Anaconda\envs\ballontickets\Lib\contextlib.py", line 158, in __exit__
    |     self.gen.throw(value)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    |     raise exc
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    |     response = await self.dispatch_func(request, call_next)       
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
    |   File "C:\Users\Jonathan Relva\Documents\Projetos Pessoais\Balloon Tickets\backend-api\app\middleware\rate_limit.py", line 189, in dispatch
    |     response = await call_next(request)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    |     raise app_exc
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    |     await self.app(scope, receive_or_disconnect, send_no_error)   
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    |     with collapse_excgroups():
    |          ^^^^^^^^^^^^^^^^^^^^
    |   File "C:\Anaconda\envs\ballontickets\Lib\contextlib.py", line 158, in __exit__
    |     self.gen.throw(value)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    |     raise exc
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    |     response = await self.dispatch_func(request, call_next)       
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
    |   File "C:\Users\Jonathan Relva\Documents\Projetos Pessoais\Balloon Tickets\backend-api\app\middleware\request_logging.py", line 56, in dispatch
    |     response = await call_next(request)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    |     raise app_exc
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    |     await self.app(scope, receive_or_disconnect, send_no_error)   
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\exceptions.py", line 62, in __call__
    |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_exception_handler.py", line 64, in wrapped_app
    |     raise exc
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    |     await app(scope, receive, sender)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\routing.py", line 762, in __call__
    |     await self.middleware_stack(scope, receive, send)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\routing.py", line 782, in app
    |     await route.handle(scope, receive, send)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\routing.py", line 297, in handle
    |     await self.app(scope, receive, send)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\routing.py", line 77, in app
    |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_exception_handler.py", line 75, in wrapped_app
    |     response = await handler(conn, exc)
    |                ^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "C:\Users\Jonathan Relva\Documents\Projetos Pessoais\Balloon Tickets\backend-api\app\middleware\error_handler.py", line 69, in validation_exception_handler
    |     return JSONResponse(
    |            ^^^^^^^^^^^^^
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\responses.py", line 180, in __init__
    |     super().__init__(content, status_code, headers, media_type, background)
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\responses.py", line 39, in __init__
    |     self.body = self.render(content)
    |                 ^^^^^^^^^^^^^^^^^^^^
    |   File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\responses.py", line 183, in render
    |     return json.dumps(
    |            ^^^^^^^^^^^
    |   File "C:\Anaconda\envs\ballontickets\Lib\json\__init__.py", line 238, in dumps
    |     **kw).encode(obj)
    |           ^^^^^^^^^^^
    |   File "C:\Anaconda\envs\ballontickets\Lib\json\encoder.py", line 200, in encode
    |     chunks = self.iterencode(o, _one_shot=True)
    |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "C:\Anaconda\envs\ballontickets\Lib\json\encoder.py", line 258, in iterencode
    |     return _iterencode(o, 0)
    |            ^^^^^^^^^^^^^^^^^
    |   File "C:\Anaconda\envs\ballontickets\Lib\json\encoder.py", line 180, in default
    |     raise TypeError(f'Object of type {o.__class__.__name__} '     
    | TypeError: Object of type bytes is not JSON serializable
    +------------------------------------

During handling of the above exception, another exception occurred:     

Traceback (most recent call last):
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\uvicorn\protocols\http\httptools_impl.py", line 419, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 84, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\fastapi\applications.py", line 1054, in __call__
    await super().__call__(scope, receive, send)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\applications.py", line 123, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    raise exc
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\cors.py", line 83, in __call__
    await self.app(scope, receive, send)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    with collapse_excgroups():
         ^^^^^^^^^^^^^^^^^^^^
  File "C:\Anaconda\envs\ballontickets\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    raise exc
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    response = await self.dispatch_func(request, call_next)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Jonathan Relva\Documents\Projetos Pessoais\Balloon Tickets\backend-api\app\middleware\rate_limit.py", line 189, in dispatch    
    response = await call_next(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    raise app_exc
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 189, in __call__
    with collapse_excgroups():
         ^^^^^^^^^^^^^^^^^^^^
  File "C:\Anaconda\envs\ballontickets\Lib\contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_utils.py", line 91, in collapse_excgroups
    raise exc
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 191, in __call__
    response = await self.dispatch_func(request, call_next)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Jonathan Relva\Documents\Projetos Pessoais\Balloon Tickets\backend-api\app\middleware\request_logging.py", line 56, in dispatch
    response = await call_next(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 165, in call_next
    raise app_exc
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\base.py", line 151, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\middleware\exceptions.py", line 62, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_exception_handler.py", line 64, in wrapped_app
    raise exc
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\routing.py", line 762, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\routing.py", line 782, in app
    await route.handle(scope, receive, send)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\routing.py", line 297, in handle
    await self.app(scope, receive, send)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\routing.py", line 77, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\_exception_handler.py", line 75, in wrapped_app
    response = await handler(conn, exc)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Jonathan Relva\Documents\Projetos Pessoais\Balloon Tickets\backend-api\app\middleware\error_handler.py", line 69, in validation_exception_handler
    return JSONResponse(
           ^^^^^^^^^^^^^
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\responses.py", line 180, in __init__
    super().__init__(content, status_code, headers, media_type, background)
  File "C:\Anaconda\envs\ballontickets\Lib\site-packages\starlette\responses.py", line 39, in __init__
nses.py", line 183, in render
    return json.dumps(
           ^^^^^^^^^^^
  File "C:\Anaconda\envs\ballontickets\Lib\json\__init__.py", line 238, in dumps   
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "C:\Anaconda\envs\ballontickets\Lib\json\encoder.py", line 200, in encode   
    chunks = self.iterencode(o, _one_shot=True)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Anaconda\envs\ballontickets\Lib\json\encoder.py", line 258, in iterencode
    return _iterencode(o, 0)
           ^^^^^^^^^^^^^^^^^
  File "C:\Anaconda\envs\ballontickets\Lib\json\encoder.py", line 180, in default  
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type bytes is not JSON serializable


```

Atualizar Termos de uso e melhorar visual, estilização etc

![[Pasted image 20260409205004 1.png]]
http://localhost:8080/pages/termos

http://localhost:8080/pages/privacidade

http://localhost:8080/pages/contato

Essa page não foi implementado absolutamente nada não sei oq deveria ter aqui e nem se é necessário
http://localhost:8080/seguranca


```
## Error Type
Console Error

## Error Message
404 Error: User attempted to access non-existent route: "/seguranca"


    at createConsoleError (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_115brz8._.js:2333:71)
    at handleConsoleError (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_115brz8._.js:3119:54)
    at console.error (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_115brz8._.js:3266:57)
    at NotFound.useEffect (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/_0ux1v2j._.js:22:21)
    at Object.react_stack_bottom_frame (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:15087:22)
    at runWithFiberInDEV (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:965:74)
    at commitHookEffectListMount (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:7255:167)
    at commitHookPassiveMountEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:7290:60)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8779:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at ClientPageRoot (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_0cj6fq1._.js:21159:50)

Next.js version: 16.2.2 (Turbopack)

```

Duvidas frequentes não está implementado
http://localhost:8080/duvidas-frequentes

```
## Error Type
Console Error

## Error Message
404 Error: User attempted to access non-existent route: "/duvidas-frequentes"


    at createConsoleError (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_115brz8._.js:2333:71)
    at handleConsoleError (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_115brz8._.js:3119:54)
    at console.error (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_115brz8._.js:3266:57)
    at NotFound.useEffect (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/_0ux1v2j._.js:22:21)
    at Object.react_stack_bottom_frame (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:15087:22)
    at runWithFiberInDEV (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:965:74)
    at commitHookEffectListMount (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:7255:167)
    at commitHookPassiveMountEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:7290:60)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8779:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8778:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at reconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8793:17)
    at recursivelyTraverseReconnectPassiveEffects (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_next_dist_compiled_react-dom_058-ah~._.js:8766:13)
    at ClientPageRoot (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/node_modules_0cj6fq1._.js:21159:50)

Next.js version: 16.2.2 (Turbopack)

```

Central de ajuda nao esta implementado está me redirecionando direto para a page de Contato
![[Pasted image 20260409205103 1.png]]


Cliquei em area do produtor no futter e me redirecinou para apagina de login e pedindo pra logar mesmo eu já estando logado na sessão e caso eu não seja um produtor o correto seria me redirecionar para completar o cadastro de produtor ![[Pasted image 20260409205315 1.png]]: 
![[Pasted image 20260409205226 1.png]]

Na pagina de cadastro de produtor se eu clicar em próximo sem preencher nada não aparece nenhum indicativo visual que é necessário preencher ou selecionar os campoes obrigatórios

![[Pasted image 20260409205431 1.png]]

No Fluxo de compra de ingresso que estou testando agora percebi que aparece mensagems de checkout seguro mas o usuario não consegue saber qual o meio de pagamento que é utilizado no nosso caso estamos utilizand o mercado pago seria necessário exibir isso de alguma forma

![[Pasted image 20260409205955 1.png]]

Na parte de pagar ao selecionar as parcelas seria interessantes deixar explicito que as taxas é cobrada diretamente do mercado pago. além disso se possível mostrar também o quanto + é do valor original dependendo de quantas parcelas escolher

![[Pasted image 20260409210334 1.png]]
![[Pasted image 20260409210346 1.png]]

Ao clickar em Pagar ele VOLTOU DIRETAMENTE PARA ESSE ESTADO e me lembro que existe um processando pagamento etc extremamente necessário corrigir isso também pois como é pagamento tem que ser extremamente confiavel
![[Pasted image 20260409210435 1.png]]

``` Retorno do backend
2026-04-10T00:00:52.384544Z [info     ] request_completed              [app.middleware.request_logging] method=POST process_time=9.135s request_id=0a917ab1-700a-4bb2-b1aa-2d1a7e9de1e0 status_code=201 url=http://localhost:8000/api/v1/orders/
INFO:     127.0.0.1:62974 - "POST /api/v1/orders/ HTTP/1.1" 201 Created
2026-04-10T00:00:52.912132Z [info     ] request_started                [app.middleware.request_logging] client_host=127.0.0.1 method=POST request_id=3c6c39de-94cf-4d2e-bb6c-e36ccafc6cdd url=http://localhost:8000/api/v1/payments
2026-04-10T00:00:52.916663Z [info     ] request_completed              [app.middleware.request_logging] method=POST process_time=0.005s request_id=3c6c39de-94cf-4d2e-bb6c-e36ccafc6cdd status_code=307 url=http://localhost:8000/api/v1/payments        
INFO:     127.0.0.1:62089 - "POST /api/v1/payments HTTP/1.1" 307 Temporary Redirect
2026-04-10T00:00:52.927764Z [info     ] request_started                [app.middleware.request_logging] client_host=127.0.0.1 method=POST request_id=e6fe99f8-b76a-4117-b108-e277f817d71c url=http://localhost:8000/api/v1/payments/
2026-04-09 21:00:53,506 INFO sqlalchemy.engine.Engine BEGIN (implicit)
BEGIN (implicit)
2026-04-09 21:00:53,509 INFO sqlalchemy.engine.Engine SELECT users.id, users.name, users.last_name, users.email, users.password, users.birth, users.phone, users.document, users.document_type_id, users.address_id, users.user_gender_type_id, users.receive_news, users.email_verified_at, users.email_verification_code_hash, users.email_verification_expires_at, users.email_verification_sent_at, users.email_verification_attempt_count, users.email_verification_attempt_window_start, users.google_sub   
FROM users
WHERE users.id = $1::UUID
SELECT users.id, users.name, users.last_name, users.email, users.password, users.birth, users.phone, users.document, users.document_type_id, users.address_id, users.user_gender_type_id, users.receive_news, users.email_verified_at, users.email_verification_code_hash, users.email_verification_expires_at, users.email_verification_sent_at, users.email_verification_attempt_count, users.email_verification_attempt_window_start, users.google_sub
FROM users
WHERE users.id = $1::UUID
2026-04-09 21:00:53,511 INFO sqlalchemy.engine.Engine [cached since 4734s ago] (UUID('d63dada5-1816-4c01-beb2-c33346fcf9b3'),)
[cached since 4734s ago] (UUID('d63dada5-1816-4c01-beb2-c33346fcf9b3'),)
2026-04-09 21:00:53,912 INFO sqlalchemy.engine.Engine SELECT orders.id, orders.order_number, orders.status, orders.subtotal, orders.tax, orders.total, orders.service_fee, orders.service_fee_absorbed, orders.discount, orders.coupon_id, orders.promo_code, orders.promoter_id, orders.payment_method, orders.payment_intent_id, orders.created_at, orders.updated_at, orders.user_id, orders.event_id
FROM orders
WHERE orders.id = $1::UUID
SELECT orders.id, orders.order_number, orders.status, orders.subtotal, orders.tax, orders.total, orders.service_fee, orders.service_fee_absorbed, orders.discount, orders.coupon_id, orders.promo_code, orders.promoter_id, orders.payment_method, orders.payment_intent_id, orders.created_at, orders.updated_at, orders.user_id, orders.event_id
FROM orders
WHERE orders.id = $1::UUID
2026-04-09 21:00:53,914 INFO sqlalchemy.engine.Engine [generated in 0.00239s] (UUID('e97c0e80-92e8-40bb-9cd6-8f2745ce4c80'),)
[generated in 0.00239s] (UUID('e97c0e80-92e8-40bb-9cd6-8f2745ce4c80'),)
2026-04-09 21:00:55,478 INFO sqlalchemy.engine.Engine INSERT INTO payments (id, order_id, mp_payment_id, mp_preference_id, amount, currency, payment_method, payment_type, status, mp_status, mp_status_detail, pix_qr_code, pix_qr_code_text, pix_expiration, boleto_url, boleto_barcode, boleto_expiration, installments, error_message, created_at, updated_at) VALUES ($1::UUID, $2::UUID, $3::VARCHAR, $4::VARCHAR, $5::NUMERIC(10, 2), $6::VARCHAR, $7::VARCHAR, $8::VARCHAR, $9::paymentstatus, $10::VARCHAR, $11::VARCHAR, $12::VARCHAR, $13::VARCHAR, $14::TIMESTAMP WITH TIME ZONE, $15::VARCHAR, $16::VARCHAR, $17::DATE, $18::INTEGER, $19::VARCHAR, $20::TIMESTAMP WITH TIME ZONE, $21::TIMESTAMP WITH TIME ZONE)
INSERT INTO payments (id, order_id, mp_payment_id, mp_preference_id, amount, currency, payment_method, payment_type, status, mp_status, mp_status_detail, pix_qr_code, pix_qr_code_text, pix_expiration, boleto_url, boleto_barcode, boleto_expiration, installments, error_message, created_at, updated_at) VALUES ($1::UUID, $2::UUID, $3::VARCHAR, $4::VARCHAR, $5::NUMERIC(10, 2), $6::VARCHAR, $7::VARCHAR, $8::VARCHAR, $9::paymentstatus, $10::VARCHAR, $11::VARCHAR, $12::VARCHAR, $13::VARCHAR, $14::TIMESTAMP WITH TIME ZONE, $15::VARCHAR, $20::TIMESTAMP WITCHAR, $20::TIMESTAMP WITH TIME ZONE, $21::TIMESTAMP WITH TIME ZONE)
2026-04-09 21:00:55,480 INFO sqlalchemy.engine.Engine [generated in 0.00246s] (UUID('c72f8143-4c14-4d6b-9fc7-15b6ee8e224d'), UUID('e97c0e80-92e8-40bb-9cd6-8f2745ce4c80'), None, None, Decimal('803.00'), 'BRL', 'credit_card', 'credit_card', 'pending', None, None, None, None, None, None, None, None, 1, None, datetime.datetime(2026, 4, 10, 0, 0, 55, 478339), datetime.datetime(2026, 4, 10, 0, 0, 55, 478339))
[generated in 0.00246s] (UUID('c72f8143-4c14-4d6b-9fc7-15b6ee8e224d'), UUID('e97c0e80-92e8-40bb-9cd6-8f2745ce4c80'), None, None, Decimal('803.00'), 'BRL', 'credit_card', 'credit_card', 'pending', None, None, None, None, None, None, None, None, 1, None, datetime.datetime(2026, 4, 10, 0, 0, 55, 478339), datetime.datetime(2026, 4, 10, 0, 0, 55, 478339))
Card payment record created: c72f8143-4c14-4d6b-9fc7-15b6ee8e224d for order e97c0e80-92e8-40bb-9cd6-8f2745ce4c80
2026-04-09 21:00:56,447 INFO sqlalchemy.engine.Engine COMMIT
COMMIT
2026-04-10T00:00:56.641750Z [info     ] request_completed              [app.middleware.request_logging] method=POST process_time=3.714s request_id=e6fe99f8-b76a-4117-b108-e277f817d71c status_code=201 url=http://localhost:8000/api/v1/payments/
INFO:     127.0.0.1:62974 - "POST /api/v1/payments/ HTTP/1.1" 201 Created

```


Outra coisa não faz sentido aparecer para os compradores Eventos em que a data de termino já passou e  muito menos ser possíver comprar ingressos desses eventos o certo é Eventos que já passaram aparecerem apenas no catálogo de Eventos das produtoras e ter uma sections para Eventos Anteriores apenas para esses Eventos que já passaram a data. 
http://localhost:8080/o/produtora-exemplo

ao acessar essa produtora não deveria estar tentando buscar o perfil do organizador logado eu acredito já que eu como comprador quero so visualizar os eventos de uma produtora
![[Pasted image 20260409211957 1.png]]
```
## Error Type
Console Error

## Error Message
Erro ao buscar perfil do organizador logado


    at getCurrentProducer (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0bu58e1._.js:1701:15)
    at async Dashboard.useEffect.fetchData (file://C:/Users/Jonathan Relva/Documents/Projetos Pessoais/Balloon Tickets/frontend-generator/.next/dev/static/chunks/app_0bu58e1._.js:3335:58)

Next.js version: 16.2.2 (Turbopack)

```