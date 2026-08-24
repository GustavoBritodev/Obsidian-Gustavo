### Bloqueantes

**Ingestão — filtro de remetentes**

- A condição 3 do `Tem PDF` aponta para `gustavo.brito@mosten.com`, endereço usado nos testes → substituir pela lista real de remetentes, numa condição só: `{{ ['a@x.com','b@y.com'].includes($json.from.emailAddress.address.toLowerCase()) }}` é verdadeiro
- Não existe o remetente real de AWS, Azure DevOps, Sentry e OpenAI → abrir uma fatura de cada na caixa e copiar o campo De
- O Cursor está mapeado pela metade, `receipts@stripe.com` ou `billing@cursor.com` → confirmar qual dos dois é o remetente efetivo
- Com o filtro aberto no endereço de teste, qualquer PDF que chegue na caixa vira lançamento contábil → a lista fechada é o que impede isso. A trava de assunto anti-realimentação permanece como quarta condição, independente dessa mudança

**Ingestão — caixa vigiada e responsável pelo OneDrive**

- A credencial `Microsoft account` autentica a conta `gustavo.brito@mosten.com`, e o trigger vigia a caixa de quem autenticou, não `faturas@mosten.com` → definir qual usuário será o responsável pela automação e criar a credencial com essa conta, ou apontar o trigger para a caixa compartilhada
- A estrutura `/Faturas-SaaS` vive hoje no OneDrive de `gustavo.brito@mosten.com` → migrar as pastas `_template`, `Documentos` e `Fechamentos` para o OneDrive do usuário definido, preservando os caminhos
- Trocar a credencial muda o drive de destino e a conta remetente → revalidar `Arquivar PDF`, `Baixar Modelo`, `Enviar Copia` e `Enviar Fechamento` após a migração, e atualizar o `template_file_id`, que é um ID de arquivo e muda ao mover de drive. É o item de maior impacto colateral da lista

**Fechamento — destinatário do envio**

- `email_destino` no `Parametros` está em `gustavo.brito@mosten.com` → trocar para `financeiro@mosten.com`

**Infra - Notificar Erro — destinatários**

- O campo `To` está em `gustavo.brito@mosten.com`, o que faz a notificação depender de uma pessoa só → trocar para três destinatários. Os nomes cogitados são `joao.russio@mosten.com`, `emerson.menezes@mosten.com` e `iane.cunha@mosten.com`, mas ainda precisam de validação sobre se serão essas mesmas pessoas
- Quem for definido precisa de acesso ao Entra ID → sem isso o alerta chega a quem não pode agir sobre ele

### Decisões que dependem de terceiros

**Provedor de LLM definitivo**

- O Groq é stand-in de teste, e o texto integral da fatura sai da VM para um provedor externo levando valor, fornecedor e às vezes os últimos dígitos do cartão → decidir se documento financeiro pode sair da rede. É política de dados, não escolha técnica
- Se a decisão for negativa, o desenho do nó de extração muda → reservar tempo de reteste do parser junto com a troca, porque cada modelo se comporta diferente com o schema estruturado

==**Permissão de leitura da pasta `Documentos==`**

- Após a migração do OneDrive, só quem acessar a conta do usuário responsável enxergará os PDFs arquivados; quem precisar de um comprovante antigo dependerá dessa pessoa → compartilhar `Faturas-SaaS/Documentos` com leitura para quem for definido. A separação entre `Documentos` e `Fechamentos` foi feita para permitir isso sem expor os fechamentos
- Se ninguém precisar de acesso → registrar essa resposta como decisão, em vez de deixar o item em aberto

**Retenção dos documentos arquivados**

- Não se sabe se existe política de guarda aplicável, e sem ela a pasta cresce indefinidamente → verificar se a Mosten tem política e aplicá-la. Com cinco assinaturas o volume é irrelevante por muitos anos, e decidir que não há política também é resposta válida

==**Conciliação PTAX x fatura do cartão, com a Controladoria**==

- A planilha leva o valor pela PTAX de venda da data de emissão, mas a Mosten paga o que o cartão cobrar, com cotação do dia da compensação mais spread e IOF; os números não vão bater → alinhar com a Controladoria como tratar a diferença: lançamento de ajuste cambial, edição na baixa, ou conciliação mensal em bloco
- A rastreabilidade já existe, com `cotacao_ptax` e `data_cotacao` gravadas por lançamento e `Moeda original: USD` nas Observações → o que falta é o combinado, não o dado
- Se a resposta for "queremos o valor exato do cartão", o desenho muda, porque não daria para lançar sem esperar a fatura chegar → por isso a conversa precisa acontecer antes do primeiro envio, não depois.