# Guia de Manutenção — Automação de Faturas SaaS

**Plataforma:** n8n 2.33.4 (self-hosted)
**Banco de dados:** PostgreSQL
**Armazenamento:** Microsoft OneDrive (via Microsoft Graph)

---

## 1. Para que serve este documento

Esta automação recebe as faturas das ferramentas de software contratadas pela Mosten, extrai os dados de cada documento, arquiva o comprovante e, uma vez por mês, envia ao financeiro uma planilha pronta para importação no Omie, acompanhada dos recibos.

Este guia descreve o funcionamento de cada um dos cinco workflows que compõem a automação, nó a nó: o que cada nó faz, por que foi escolhido, do que depende e o que quebra se for alterado. Ele serve tanto para quem precisa corrigir uma falha quanto para quem vai assumir a manutenção sem ter participado da construção.

A seção 2 traz um roteiro de teste de ponta a ponta, da base vazia até a planilha enviada. Use-o depois de qualquer alteração estrutural e antes de ativar em produção.

**Este documento não substitui a leitura do fluxo no n8n.** Ele explica o porquê; o n8n mostra o quê.

---

## 2. Roteiro de teste de ponta a ponta

Este roteiro valida a automação inteira, do e-mail que chega até a planilha que sai. Use-o depois de qualquer alteração estrutural, ao migrar de conta Microsoft, ao trocar o provedor de modelo de linguagem, ou antes de ativar em produção.

O roteiro parte de uma base vazia e usa e-mails montados de propósito, um para cada caminho que o fluxo pode tomar. Ele leva cerca de uma hora, quase toda de espera pelo poll de 5 minutos da Ingestão.

> **Este roteiro apaga dados.** Ele começa esvaziando a tabela `faturas_saas`. Não execute em um ambiente onde existam lançamentos que ainda não foram enviados ao financeiro. Se houver, exporte antes: `COPY faturas_saas TO '/tmp/backup_faturas.csv' CSV HEADER;`

### 2.1 Preparação

**1. Exportar os workflows.** Em cada um, menu de três pontos → Download. É o rollback caso algo seja alterado durante o teste.

**2. Confirmar as Settings.** `Workflow Ingestão`, `Workflow Fechamento` e `Infra - Monitor Client Secret` devem ter Error Workflow apontando para `Infra - Notificar Erro` e Timezone `America/Sao_Paulo`.

**3. Separar os PDFs de teste.** São necessários três arquivos:

| Arquivo | Como obter |
|---|---|
| Fatura A | Recibo real de uma plataforma, com valor, data e fornecedor legíveis |
| Fatura B | Recibo real de outra plataforma, para testar dois lançamentos no mesmo fechamento |
| PDF sem texto | Qualquer página impressa e digitalizada, ou um PDF gerado a partir de uma imagem (`.png` exportado como PDF serve) |

O terceiro arquivo é o que valida a retenção por campos faltantes. Sem ele, o caminho `incompleto` não é exercitado.

**4. Limpar a base:**

```sql
TRUNCATE TABLE faturas_saas RESTART IDENTITY;
SELECT count(*) FROM faturas_saas;   -- deve retornar 0
```

O `RESTART IDENTITY` zera a sequence, então os ids do teste começam em 1 e ficam fáceis de acompanhar.

**5. Limpar o OneDrive.** Apagar `/Faturas-SaaS/Documentos/` e `/Faturas-SaaS/Fechamentos/` inteiros, preservando `/Faturas-SaaS/_template/`. Apagar as pastas é parte do teste: as duas árvores devem ser recriadas sozinhas.

> **Não apague `/Faturas-SaaS/_template/`.** O `template_file_id` do `Parametros` aponta para o arquivo dentro dela, e um arquivo recriado ganha id novo.

### 2.2 E-mails de teste

Todos são enviados da conta autenticada para ela mesma, porque o `Tem PDF` filtra por remetente. Envie um de cada vez, aguardando o ciclo de poll entre eles, para que cada resultado seja atribuível.

| # | Assunto | Anexo | Resultado esperado |
|---|---|---|---|
| 1 | `Teste automacao - fatura A` | Fatura A | Lançamento `pendente`, PDF arquivado |
| 2 | `Teste automacao - fatura B` | Fatura B | Segundo lançamento `pendente` |
| 3 | `Teste automacao - sem anexo` | nenhum | Descartado pelo `Tem PDF` |
| 4 | `Teste automacao - PDF escaneado` | PDF sem texto | Lançamento `incompleto`, PDF arquivado |
| 5 | `Faturamento e Recibo de Ferramentas de Software - teste` | Fatura A | Descartado pela trava anti-realimentação |
| 6 | `Teste automacao - fatura A reenvio` | Fatura A | **Novo** lançamento, id diferente |

Observações sobre três deles:

**O e-mail 3 deve ser enviado com assinatura contendo imagem**, se a conta tiver uma. É exatamente esse o caso que o `hasAttachments` classifica como verdadeiro e que só a segunda condição do `Tem PDF` barra. Sem imagem na assinatura, o teste vira apenas o caso trivial.

**O e-mail 5 valida a trava mais importante do filtro.** O assunto precisa conter a frase exata do campo `assunto` do `Parametros` do Fechamento. Se este e-mail virar lançamento, o fluxo tem realimentação: o próprio e-mail de fechamento seria ingerido como fatura.

**O e-mail 6 gera um lançamento novo, e isso é o comportamento correto.** A deduplicação é por `message_id_graph`, e reenviar o mesmo PDF cria uma mensagem nova, com id novo. O que a dedupe protege é o reprocessamento da mesma mensagem, não o envio repetido do mesmo documento. Depois de conferir, apague esse registro:

```sql
DELETE FROM faturas_saas WHERE id = (SELECT max(id) FROM faturas_saas);
```

### 2.3 Executar a Ingestão

Ative o `Workflow Ingestão` e envie os e-mails. O trigger roda a cada 5 minutos; acompanhe em **Executions**.

Depois de todos processados:

```sql
SELECT id, status, plataforma, fornecedor, moeda, valor,
       data_emissao, data_vencimento, numero_documento,
       campos_faltantes, caminho_arquivo
  FROM faturas_saas ORDER BY id;
```

O que conferir:

| Verificação | Esperado |
|---|---|
| Quantidade de registros | 3 antes do e-mail 6, 4 depois |
| E-mails 3 e 5 | **Não** produziram registro |
| Faturas A e B | `pendente`, com todos os campos preenchidos |
| PDF escaneado | `incompleto`, com `campos_faltantes` listando os campos |
| `caminho_arquivo` | Preenchido nos três, com id do OneDrive |
| `data_vencimento` | Dia 15 do mês corrente em todos |

**Conferir os valores contra os PDFs, campo a campo.** Esta é a única etapa da automação onde um dado pode nascer errado sem nada acusar depois. Abra as faturas A e B lado a lado com o resultado e confira fornecedor, valor, moeda, data de emissão e número do documento. Atenção especial ao fornecedor: o modelo já confundiu o emissor com o destinatário.

**No OneDrive**, confirmar que `/Faturas-SaaS/Documentos/{ano}/{ano-mes}/` foi criada sozinha e contém os PDFs com nome no formato `{plataforma}_{numero}_{emissao}.pdf`. O PDF escaneado aparece como `DESCONHECIDA_SEM-NUMERO-xxxxxxxx_sem-data.pdf`, arquivado no mês corrente.

Ao terminar, **desative o `Workflow Ingestão`** para que ele não interfira no teste do Fechamento.

### 2.4 Executar o Fechamento

O Fechamento só roda no dia de corte. Para testar em qualquer dia, o portão é contornado com dado fixado.

**1.** Abrir o nó `E dia de fechar?` → **Test step**. Conferir na saída: `dataAlvo` coerente com o `DIA_CORTE`, e `feriadosConsiderados: 32`.

**2.** Fixar a saída (ícone de **Pin**). Se `ehHoje` vier `false`, editar o valor fixado para `true`.

**3.** **Test workflow.**

Conferências durante a execução:

| Nó | Esperado |
|---|---|
| `Buscar Pendentes` | 2 itens. O registro `incompleto` **não** aparece |
| `Tem Lancamentos?` | Ramo verdadeiro |
| `Buscar Cotacoes` | `cotacao_ptax` plausível, `data_cotacao` igual ou anterior à emissão |
| `Reler Lancamentos Convertidos` | `valor_brl` preenchido, `qtd_incompletos: 1` |
| `Enviar Copia` | `name` = `Omie_Contas_Pagar_{competencia}.xlsx`, `parentReference.path` terminando na pasta do mês |
| `Escrever Lancamentos` | Sem erro. Um 404 aqui significa que o id do `Enviar Copia` não foi lido |
| `Juntar Anexos` | `totalDocumentos: 2` |
| `Conferir Marcacao` | Verde, sem erro |

**No OneDrive**, confirmar que `/Faturas-SaaS/Fechamentos/{ano}/{ano-mes}/` foi criada sozinha e contém a planilha.

**Na planilha**, abrir e conferir:

- Dados a partir da linha 6, uma linha por lançamento
- Coluna C com o fornecedor, F com o valor em BRL
- Colunas I, J e K exibindo datas legíveis, não números de cinco dígitos
- **Nenhuma linha residual com data 15/06/2026** abaixo dos lançamentos
- Coluna S com as observações, incluindo a moeda original

**No e-mail**, conferir assunto com a competência, contagem de lançamentos e de documentos, os três anexos (planilha mais dois PDFs) e a linha final avisando de 1 documento retido.

**Na base:**

```sql
SELECT id, status, valor_brl, cotacao_ptax, data_cotacao, data_exportacao
  FROM faturas_saas ORDER BY id;
```

As duas faturas devem estar `exportado` com `data_exportacao` preenchida; o escaneado continua `incompleto`.

### 2.5 Testes complementares

**Reexecução no mesmo mês.** Rodar **Test workflow** de novo, sem alterar nada. O esperado é o ramo falso do `Tem Lancamentos?`, porque não há mais pendentes, e o `Send a message` disparando. Se quiser exercitar a sobrescrita da planilha, promova um registro de volta antes:

```sql
UPDATE faturas_saas
   SET status = 'pendente', valor_brl = NULL, cotacao_ptax = NULL,
       data_cotacao = NULL, data_exportacao = NULL
 WHERE id = 1;
```

O arquivo do mês deve ser substituído no lugar, e não gerar `Omie_Contas_Pagar_{competencia} 1.xlsx`.

**Promoção de um registro retido.** Completar os campos do escaneado à mão e devolvê-lo ao fluxo:

```sql
UPDATE faturas_saas
   SET plataforma = 'AWS', fornecedor = 'Amazon Web Services, Inc.',
       moeda = 'USD', valor = 10.00, data_emissao = '2026-07-01',
       status = 'pendente'
 WHERE status = 'incompleto';
```

Rodar o Fechamento de novo. O registro deve entrar na planilha, e o e-mail deve trazer a frase de que nenhum documento ficou retido.

**Calendário de feriados.** Para testar a antecipação, alterar temporariamente `DIA_CORTE` e o mês dentro do `E dia de fechar?`, rodar **Test step** e conferir o `dataAlvo`. Um caso bom é `DIA_CORTE = 20` em novembro, que deve antecipar por causa do dia 20; outro é `DIA_CORTE = 9` em julho, que deve antecipar pelo feriado estadual. Desfazer as duas alterações em seguida.

**Notificação de erro.** O Error Trigger **não** dispara em execução manual. Para testá-lo é preciso ativar um workflow e provocar a falha em execução de produção: por exemplo, apontar temporariamente o `template_file_id` para um id inexistente e aguardar o disparo agendado. Confirmar que o e-mail chega com nome do nó, mensagem e URL da execução.

**Monitor de secret.** Alterar temporariamente `data_expiracao` no `CONFIG_SECRET` para uma data a 30 dias de hoje, rodar **Test workflow** e confirmar o e-mail com severidade `AVISO`. Repetir com data a 3 dias, esperando `URGENTE`, e com data passada, esperando `CRITICO - JA EXPIRADO`. **Restaurar a data real ao final** — um `data_expiracao` errado silencia o monitor permanentemente.

### 2.6 Encerramento

1. **Remover todos os pins.** Um pin esquecido no `E dia de fechar?` faz o fechamento rodar todo dia.
2. Restaurar `data_expiracao`, `DIA_CORTE`, `template_file_id` e qualquer outro valor alterado durante os testes.
3. Limpar a base de teste: `TRUNCATE TABLE faturas_saas RESTART IDENTITY;`
4. Apagar as pastas de teste no OneDrive, preservando `_template`.
5. Reativar `Workflow Ingestão` e `Workflow Fechamento`.
6. Conferir de novo o Error Workflow e o Timezone nas Settings.

> **O teste não substitui a homologação no Omie.** A planilha só é considerada aceita depois de importada com sucesso no ambiente de homologação, com dados de faturas reais. Registros sintéticos servem para validar o fluxo, não o formato aceito pelo Omie.

---

## 3. Convenções deste documento

### Campos destacados

Valores marcados assim: ==valor de teste== estão hoje configurados com dados de teste e **precisam ser alterados antes da entrada em produção**. A seção 11 consolida todos eles numa única tabela.

### Nomes de nós

Nomes de nós aparecem entre crases: `Buscar Pendentes`. Eles são reproduzidos exatamente como estão no n8n, incluindo ausência de acentos e eventuais duplicações de espaço, porque as expressões `$('Nome do No')` fazem correspondência literal. Renomear um nó sem atualizar quem o referencia quebra o fluxo em tempo de execução, sem aviso prévio.

### Marcações de atenção

> **Atenção:** comportamento não óbvio que já causou falha, ou que causará se alterado sem cuidado.

---

## 4. Visão geral da arquitetura

### Os cinco workflows

| Workflow | Gatilho | Frequência | Função |
|---|---|---|---|
| `Infra - Setup Tabela Faturas` | Manual | Uma vez | Cria a tabela e os índices no banco |
| `Workflow Ingestão` | Outlook Trigger | A cada 5 minutos | Lê e-mails, extrai dados do PDF, arquiva e grava no banco |
| `Workflow Fechamento` | Schedule | Diário às 08:00 | No dia de corte, gera a planilha do Omie e envia ao financeiro |
| `Infra - Notificar Erro` | Error Trigger | Sob demanda | Envia e-mail quando qualquer workflow falha |
| `Infra - Monitor Client Secret` | Schedule | Diário às 08:00 | Avisa antes de a credencial da Microsoft expirar |

### Fluxo de dados

```
E-mail com PDF
      |
      v
[Workflow Ingestão]  ----->  PDF arquivado no OneDrive (/Faturas-SaaS/Documentos/{ano}/{ano-mes})
      |
      v
  faturas_saas (status = 'pendente')
      |
      v
[Workflow Fechamento]  ----->  Planilha no OneDrive (/Faturas-SaaS/Fechamentos/{ano}/{ano-mes})
      |                        E-mail ao financeiro com planilha + PDFs
      v
  faturas_saas (status = 'exportado')
      |
      v
  Importação manual no Omie
```

A tabela `faturas_saas` é o único ponto de acoplamento entre a Ingestão e o Fechamento. Os dois workflows não se conhecem: um escreve registros `pendente`, o outro consome registros `pendente` e os marca como `exportado`.

### Separação de responsabilidades

Uma regra estruturante, que explica várias decisões adiante: **a Ingestão nunca converte moeda e o Fechamento nunca lê e-mail.** A Ingestão registra o valor na moeda original do documento; a conversão para BRL acontece no Fechamento, pela cotação PTAX da data de emissão. Isso permite reprocessar a conversão sem reprocessar o e-mail, e permite que uma fatura recebida hoje seja convertida com a cotação correta mesmo que o fechamento ocorra semanas depois.

---

## 5. Infraestrutura compartilhada

### 5.1 Credenciais

| Nome no n8n | Tipo | Usada por |
|---|---|---|
| `Microsoft account` | Microsoft OAuth2 API | Trigger do Outlook na Ingestão, todos os nós OneDrive, todos os HTTP Request para o Graph, `Enviar Alerta` do Monitor |
| `Microsoft Outlook account` | Microsoft Outlook OAuth2 API | Nós Microsoft Outlook do Fechamento e do `Infra - Notificar Erro`, e o `Enviar Fechamento` |
| `Postgres account` | Postgres | Todos os nós Postgres dos três workflows |
| `Groq account` | Groq API | `Groq Chat Model` da Ingestão |

> **Atenção:** as duas credenciais Microsoft apontam para a mesma aplicação registrada no Entra ID e compartilham o mesmo client secret, mas são objetos distintos no n8n, com escopos distintos. Ao renovar o secret, **as duas precisam ser atualizadas**. Atualizar só uma faz metade da automação continuar funcionando, o que é pior do que parar por inteiro: o sintoma fica parcial e a causa fica escondida.

A conta Microsoft autenticada determina três coisas ao mesmo tempo: qual caixa de e-mail o trigger vigia, em qual OneDrive os arquivos são gravados, e qual endereço aparece como remetente dos envios. Trocar a conta muda as três.

### 5.2 Estrutura de pastas no OneDrive

```
/Faturas-SaaS/
    /_template/
        Controle_de_ferramentas_e_assinaturas.xlsx     (modelo do Omie, nunca editado)
    /Documentos/
        /{ano}/{ano-mes}/                              (PDFs, pela competência de emissão)
    /Fechamentos/
        /{ano}/{ano-mes}/                              (planilhas, pela competência de envio)
```

**Por que os PDFs e as planilhas ficam em árvores separadas.** As duas competências são diferentes por natureza: uma fatura emitida em julho entra no fechamento de agosto. Além disso, a separação permite conceder acesso de leitura aos comprovantes sem expor os arquivos de fechamento.

**As duas árvores criam as pastas sozinhas.** Tanto a Ingestão quanto o Fechamento gravam por caminho (`PUT .../root:/caminho/arquivo:/content`), e nesse modo o Graph cria as pastas intermediárias que não existirem. Nenhuma pasta de ano ou de mês precisa ser criada à mão.

### 5.3 A tabela `faturas_saas`

Estrutura completa, conforme criada pelo `Infra - Setup Tabela Faturas`:

| Coluna | Tipo | Preenchida por | Observação |
|---|---|---|---|
| `id` | SERIAL PRIMARY KEY | Banco | Nunca mapeada em nenhum INSERT |
| `message_id_graph` | TEXT UNIQUE NOT NULL | Ingestão | Id da mensagem no Graph. Base da deduplicação |
| `plataforma` | TEXT | Ingestão (parser) | AWS, Azure DevOps, Sentry, Cursor, OpenAI |
| `fornecedor` | TEXT | Ingestão (parser) | Razão social do emissor. Vai para a coluna C da planilha |
| `valor` | NUMERIC(18,2) | Ingestão (parser) | Na moeda original |
| `moeda` | TEXT | Ingestão (parser) | ISO 4217 |
| `valor_brl` | NUMERIC(18,2) | Fechamento | Nulo até a conversão rodar |
| `cotacao_ptax` | NUMERIC(10,4) | Fechamento | Cotação efetivamente usada |
| `data_cotacao` | DATE | Fechamento | Pode ser anterior à emissão (fim de semana, feriado) |
| `data_emissao` | DATE | Ingestão (parser) | Base do arquivamento e da cotação |
| `data_vencimento` | DATE | Ingestão | Sempre dia 15 do mês de processamento |
| `tipo_documento` | TEXT | Ingestão (parser) | Recibo ou Nota Fiscal |
| `numero_documento` | TEXT | Ingestão (parser) | Invoice Number ou equivalente |
| `parcela` | INTEGER | Ingestão (parser) | Só quando o documento explicita parcelamento |
| `total_parcelas` | INTEGER | Ingestão (parser) | Idem |
| `campos_faltantes` | TEXT | Ingestão | Lista dos campos que o parser não encontrou |
| `observacoes` | TEXT | Ingestão | Vai para a coluna S da planilha |
| `caminho_arquivo` | TEXT | Ingestão | **Id do arquivo no OneDrive**, não um caminho |
| `payload_parser` | JSONB | Ingestão | Resposta bruta do parser, para reprocessamento |
| `status` | TEXT NOT NULL DEFAULT 'pendente' | Ambos | `pendente`, `incompleto` ou `exportado` |
| `data_exportacao` | TIMESTAMP | Fechamento | Preenchida na marcação |
| `criado_em` | TIMESTAMP NOT NULL DEFAULT now() | Banco | |

Índices: `idx_faturas_status` sobre `status`, `idx_faturas_emissao` sobre `data_emissao`.

> **Atenção:** apesar do nome, `caminho_arquivo` guarda o **id** do arquivo no OneDrive, não o caminho textual. Essa escolha é deliberada: o id sobrevive a renomeações e movimentações da pasta, o caminho não. O nó `Baixar Documentos` do Fechamento depende disso.

### 5.4 Estados e transições

Um registro tem três estados:

- **`pendente`** — gravado pela Ingestão quando o parser encontrou todos os campos essenciais. Entra no próximo fechamento.
- **`incompleto`** — gravado pela Ingestão quando falta ao menos um campo essencial (`valor`, `moeda`, `data_emissao` ou `fornecedor`). Fica retido: nenhuma consulta do Fechamento o enxerga.
- **`exportado`** — marcado pelo Fechamento, **depois** do envio do e-mail. Nunca mais é lido.

`incompleto` é o único estado que exige ação humana. Depois de completar os campos na base, a promoção é manual:

```sql
UPDATE faturas_saas SET status = 'pendente' WHERE id = <ID>;
```

O e-mail de fechamento informa quantos registros estão nesse estado, para que a retenção não passe despercebida.

A marcação como `exportado` acontece após o envio, e não antes, de propósito: se o envio falhar, os registros continuam pendentes e entram no ciclo seguinte, em vez de sumirem sem terem sido enviados.

---

## 6. Workflow: `Infra - Setup Tabela Faturas`

**Gatilho:** manual. **Frequência:** execução única, na implantação.

Cria a tabela `faturas_saas` e seus dois índices. Roda uma vez e depois fica parado. Não deve ser ativado.

### Nós

| # | Nó | Tipo |
|---|---|---|
| 1 | `When clicking 'Execute workflow'` | Manual Trigger |
| 2 | `CREATE TABLE` | Postgres |
| 3 | `Execute a SQL query1` | Postgres |

### 6.1 `CREATE TABLE`

Executa o DDL completo da tabela e dos índices, todo com `IF NOT EXISTS`.

**Por que `IF NOT EXISTS` e não `DROP TABLE` seguido de `CREATE`.** Executar este workflow por engano com dados em produção precisa ser inofensivo. Com `IF NOT EXISTS`, uma execução acidental não faz nada; com `DROP`, apaga o histórico de lançamentos.

**Consequência prática:** este workflow **não** aplica alterações de estrutura. Se um dia for preciso acrescentar uma coluna, editar o DDL aqui não terá efeito sobre a tabela existente. A alteração precisa ser um `ALTER TABLE` executado à parte.

**Restrições que este DDL cria e que o resto da automação depende:**

- `message_id_graph TEXT UNIQUE NOT NULL` — é a segunda linha de defesa da deduplicação, abaixo do nó `Ja Processado?` da Ingestão. Se o `Ja Processado?` falhar, o INSERT duplicado é barrado aqui, e a execução falha de forma visível em vez de gravar o lançamento duas vezes.
- `status TEXT NOT NULL DEFAULT 'pendente'` — o Fechamento consulta por `status = 'pendente'`. Um registro inserido sem status entra no fechamento por padrão, que é o comportamento desejado.
- `payload_parser JSONB` — recebe texto JSON vindo do `Gravar Lancamento`. O nó Postgres em modo `Insert` converte o tipo automaticamente.

### 6.2 `Execute a SQL query1`

Nó de verificação, com a consulta `SELECT id, payload_parser FROM faturas_saas ORDER BY id DESC LIMIT 1;`.

Serve apenas para confirmar, logo após a criação, que a tabela responde e que o `payload_parser` está gravando. **Não faz parte do processo.** Mantém o nome padrão do n8n, o que sinaliza que é auxiliar.

---

## 7. Workflow: `Workflow Ingestão`

**Gatilho:** Microsoft Outlook Trigger. **Frequência:** a cada 5 minutos.

Recebe e-mails, filtra os que trazem fatura em PDF, extrai os dados do documento, arquiva o PDF no OneDrive e grava o lançamento no banco como `pendente`.

### Cadeia de nós

```
Trigger Faturas -> Tem PDF -> Checar Duplicidade -> Ja Processado? (true)
  -> Parametros -> Selecionar PDF -> Extrair Texto -> Extrair Dados
  -> Normalizar -> Arquivar PDF -> Gravar Lancamento
```

O `Groq Chat Model` fica pendurado no `Extrair Dados` como sub-nó de modelo de linguagem, não na cadeia principal.

O ramo falso do `Ja Processado?` fica desconectado. E-mail já processado não precisa de tratamento.

### 7.1 `Trigger Faturas` — Microsoft Outlook Trigger

| Parâmetro | Valor |
|---|---|
| Credential | `Microsoft account` |
| Poll Times | Every X, 5, minutes |
| Trigger On | Message Received |
| Output | **Raw** |
| Filters → Folders to Include | Caixa de Entrada (id fixo da pasta) |
| Options → Download Attachments | ativado |
| Options → Attachments Prefix | `attachment_` |

**Por que `Output: Raw` e não `Simplified`.** O filtro seguinte depende de três campos: `id`, `hasAttachments` e `from.emailAddress.address`. O modo Raw garante o objeto completo do Graph. O modo simplificado entrega um recorte que pode variar entre versões do nó.

**Por que o prefixo `attachment_`.** Um e-mail pode ter vários anexos, e o n8n nomeia as propriedades binárias sequencialmente (`attachment_0`, `attachment_1`). O nó `Selecionar PDF` não depende desses nomes: ele varre os binários procurando o `mimeType` de PDF. O prefixo existe para tornar previsível de onde os binários vêm, não para ser referenciado.

**Dependências que este nó cria:**

- O `id` de cada mensagem vira o `message_id_graph` no banco.
- A pasta filtrada está gravada por **id do Graph**, não por nome. Se a caixa mudar, ou se a credencial passar a autenticar outra conta, esse id deixa de existir e o trigger para de encontrar mensagens.
- ==A credencial `Microsoft account` autentica hoje a conta `gustavo.brito@mosten.com`, e portanto o trigger vigia a caixa dessa conta, não a caixa `faturas@mosten.com`.==

### 7.2 `Tem PDF` — Filter

Quatro condições, todas obrigatórias (`AND`):

| # | Condição | Motivo |
|---|---|---|
| 1 | `{{ $json.hasAttachments }}` é verdadeiro | Descarte barato da maioria |
| 2 | Expressão booleana sobre os binários, reproduzida abaixo da tabela | `hasAttachments` fica verdadeiro para assinatura de e-mail com imagem embutida. Só esta condição garante que existe PDF de fato |
| 3 | `{{ $json.from.emailAddress.address.toLowerCase() }}` **is equal to** ==`gustavo.brito@mosten.com`== | Restringe às plataformas conhecidas |
| 4 | `{{ $json.subject }}` **does not contain** `Faturamento e Recibo de Ferramentas de Software` | Trava anti-realimentação |

Expressão exata da condição 2:

```
{{ Object.values($binary || {}).some(b => b.mimeType === 'application/pdf') }}
```

**A condição 2 não é redundante.** O `hasAttachments` do Graph retorna verdadeiro para qualquer anexo, inclusive a imagem embutida na assinatura de e-mail. Sem a condição 2, esses e-mails passariam o filtro e derrubariam a execução no `Selecionar PDF`, que lança erro ao não encontrar PDF.

**O `toLowerCase()` da condição 3 é obrigatório.** O Graph devolve o endereço com a capitalização que o remetente usou, e a comparação de string do n8n é sensível a maiúsculas.

**A condição 4 impede um laço de realimentação.** O e-mail de fechamento leva PDFs anexados e é enviado pela mesma conta autenticada. Sem esta condição, e com o filtro apontando para um endereço interno, o e-mail gerado pelo Fechamento é ingerido como se fosse uma fatura, vira lançamento novo, e gera outro fechamento no ciclo seguinte. **Este cenário já ocorreu em teste.** O valor comparado é o mesmo do campo `assunto` do nó `Parametros` do Fechamento: alterar um exige alterar o outro.

> **Este é o único nó do workflow que precisa mudar para entrar em produção.** A condição 3 passa a listar os remetentes reais das plataformas.

### 7.3 `Checar Duplicidade` — Postgres

```sql
SELECT $1::text AS message_id_graph,
       (SELECT id FROM faturas_saas WHERE message_id_graph = $1) AS existente;
```

Query Parameters: `{{ $json.id }}`. Retry on Fail ativado, 3 tentativas, 5000 ms.

**Por que a query devolve o próprio id do e-mail.** A forma intuitiva (`SELECT id FROM faturas_saas WHERE message_id_graph = $1`) não devolve linha nenhuma quando o e-mail é novo, que é justamente o caso que segue o fluxo. O item chegaria vazio aos nós seguintes e o `message_id_graph` se perderia, tornando impossível recuperar o anexo correto no `Selecionar PDF`. Devolvendo sempre uma linha, com o id do e-mail e um `existente` nulo quando não há duplicata, o pareamento sobrevive.

**Por que o nó Postgres, e não uma consulta dentro de um Code.** O nó Postgres reusa a credencial e o pool de conexões; um Code node precisaria de driver e credencial próprios.

**Dependência de saída:** o `Selecionar PDF` usa o `message_id_graph` devolvido aqui para localizar o e-mail correspondente na saída do `Tem PDF`. Alterar o alias da coluna quebra esse nó.

### 7.4 `Ja Processado?` — If

| Parâmetro | Valor |
|---|---|
| Condition Type | Number |
| Value 1 | `{{ $json.existente }}` |
| Operation | is empty |

Ramo verdadeiro (nada encontrado) segue o fluxo. Ramo falso desconectado.

**Por que o tipo Number e não String.** A coluna `id` é inteira, e o operador `is empty` do tipo Number trata `null` como vazio. Com o tipo String, `null` pode não ser considerado vazio conforme a versão do nó, e o efeito é o pior possível: todo e-mail novo cai no ramo falso e é descartado em silêncio, sem erro e sem registro.

**Esta é a primeira linha de defesa da deduplicação.** A segunda é a constraint `UNIQUE` da tabela.

### 7.5 `Parametros` — Set

| Campo | Valor |
|---|---|
| `pasta_documentos` | `/Faturas-SaaS/Documentos` |
| Options → Include Other Input Fields | **ativado** |

**O caminho é puro: sem barra no final e sem prefixo `root:`.** O prefixo é montado pelo `Arquivar PDF`. Se vier embutido aqui, a URL final fica duplicada e o Graph responde `invalidRequest` sem explicar a causa.

**O `Include Other Input Fields` é obrigatório.** Sem ele, o Manual Mapping descarta o `message_id_graph` vindo do `Checar Duplicidade`, e o `Selecionar PDF` falha no primeiro item.

**Dependência:** o `Normalizar` lê este valor com `$('Parametros').first().json.pasta_documentos` para montar a pasta de destino.

### 7.6 `Selecionar PDF` — Code

Modo `Run Once for All Items`.

Recupera o anexo do `Tem PDF`, pareando pelo id do e-mail, identifica o PDF pelo `mimeType` e o renomeia para a propriedade binária `pdf`.

**Existe por dois motivos que só aparecem em execução:**

1. **O nó Postgres não repassa binários.** Depois do `Checar Duplicidade`, o item perdeu o anexo. Ele precisa ser buscado de volta no `Tem PDF`.
2. **O `Extract from File` exige nome fixo de propriedade binária**, e o prefixo `attachment_` gera nomes dinâmicos. Este nó normaliza para `pdf`.

**O pareamento é pelo id do e-mail, nunca por posição.** O `Tem PDF` é um Filter: ele descarta itens, então os índices de entrada e saída não correspondem.

**Os dois `throw` são intencionais.** Falhar de forma visível é preferível a gravar um lançamento com o PDF errado. O primeiro (`nao encontrado na saida do Tem PDF`) indica quebra de pareamento; o segundo (`passou pelo filtro sem PDF anexo`) indica que a condição 2 do `Tem PDF` foi removida ou alterada.

**Limitação registrada:** e-mail com mais de um PDF anexo processa apenas o primeiro. O campo `total_anexos_pdf` na saída existe para tornar isso detectável ao inspecionar a execução.

### 7.7 `Extrair Texto` — Extract from File

| Parâmetro | Valor |
|---|---|
| Operation | Extract From PDF |
| Input Binary Field | `pdf` |

Nesta versão do nó não existe a opção de escolher o campo de saída. O texto é gravado no campo `text`, junto de metadados do PDF.

**Por que extrair o texto antes de mandar ao modelo, em vez de enviar o PDF.** Texto é muito mais barato em contexto do que documento binário, e a extração local é determinística. O custo é a limitação abaixo.

**Limitação registrada:** PDF que seja imagem escaneada, sem camada de texto, produz `text` vazio. O fluxo não quebra: o parser devolve todos os campos nulos e os lista em `campos_nao_encontrados`, o PDF é arquivado normalmente no OneDrive e o lançamento é gravado com status `incompleto`, fora do alcance do Fechamento. Se isso passar a ocorrer com alguma plataforma, a saída é enviar o PDF direto a um modelo com leitura de imagem.

**Dependência:** o `Extrair Dados` lê `{{ $json.text }}`. Se uma atualização do n8n mudar o nome desse campo, é o único ponto a ajustar.

### 7.8 `Extrair Dados` — Information Extractor + `Groq Chat Model`

**Nó principal:**

| Parâmetro | Valor |
|---|---|
| Text | `{{ $json.text }}` |
| Schema Type | Manual (JSON Schema definido no nó) |
| Options → System Prompt Template | As regras absolutas (abaixo) |

**Sub-nó de modelo:**

| Parâmetro | Valor |
|---|---|
| Credential | ==`Groq account`== |
| Model | ==`openai/gpt-oss-120b`== |
| Options → Temperature | **0** |

**Por que Information Extractor e não um Basic LLM Chain com prompt livre.** O Information Extractor força a saída ao JSON Schema declarado, o que elimina a necessidade de parsear texto livre e garante que os campos existam com os tipos certos. Os `enum` do schema restringem `plataforma` e `tipo_documento` a valores conhecidos.

**Por que temperatura zero.** Extração de dado estruturado não pode variar entre execuções do mesmo documento. Com a temperatura padrão, o mesmo PDF processado duas vezes já produziu fornecedores diferentes em teste, um deles pegando o destinatário da fatura em vez do emissor.

**As regras do prompt não são recomendações.** Cada uma corresponde a um modo de erro concreto:

| Regra | O que previne |
|---|---|
| 1 e 2 (não inferir, campo ausente vira `null` e entra em `campos_nao_encontrados`) | Dado inventado que parece plausível e passa por todas as validações seguintes |
| 3 (data ambígua) | `03/04/2026` numa fatura em inglês é 4 de março, não 3 de abril |
| 3b (rótulos aceitos para a data, e período não é data) | Cada plataforma nomeia a data de um jeito. Sem a lista, um recibo do Stripe que traz `Date Paid` sai sem data de emissão; sem a ressalva do período, o modelo pega a data inicial da cobrança em vez da data do documento |
| 4 (valor numérico, ponto decimal) | Separador de milhar virando parte do número |
| 5 (nunca converter moeda) | Conversão é responsabilidade exclusiva do Fechamento |
| 6 e 7 (tipo e número do documento) | Padroniza campos que aparecem com nomes diferentes em cada plataforma |
| 7b (fornecedor é quem emite) | O modelo já confundiu emissor com destinatário e gerou uma conta a pagar para a própria Mosten |
| 8 (parcelamento explícito, e ausência esperada não é campo faltante) | Assinatura mensal recorrente não é parcelamento. Sem a segunda parte, `parcela` e `total_parcelas` entram em `campos_nao_encontrados` em toda fatura e poluem a coluna Observações da planilha com um alerta que não exige ação |
| 9 (na dúvida, `null`) | Regra geral de fechamento |

**A regra 3b é a que mais tende a exigir manutenção.** Ela lista os rótulos sob os quais a data do documento aparece: `Invoice Date`, `Date of Issue`, `Issue Date`, `Date Paid`, `Payment Date`. Recibo emitido via Stripe, por exemplo, usa `Date Paid` e não traz nenhum dos três primeiros. A lista precisa acomodar o rótulo de cada plataforma nova, e a ressalva sobre período de cobrança (`Period`, `Billing Period`, `Service Period`) precisa continuar valendo: num recibo emitido no dia 5 cobrindo do dia 1 ao 30, a data do documento é o dia 5.

**Como o erro se manifesta quando a regra 3b não cobre o rótulo.** O parser devolve `data_emissao` nula e o registro é gravado como `incompleto`, fora do fechamento. O PDF é arquivado com nome terminado em `_sem-data.pdf`, na pasta do mês corrente em vez da pasta da competência de emissão. Um documento arquivado num mês diferente dos demais da mesma leva é o sinal visível desse caso.

> **Este é o único ponto da automação onde um dado pode nascer errado sem nada acusar depois.** Um valor plausível e errado passa pelo `Normalizar`, entra na planilha e chega ao Omie. Toda vez que uma plataforma nova entrar, ou que o modelo for trocado, é obrigatório conferir a primeira fatura campo a campo contra o documento.

**Alternativa registrada:** se uma troca de modelo quebrar o suporte a saída estruturada, a substituição é um **Basic LLM Chain** com **Structured Output Parser** e Auto-fixing ativado.

**Dependência de saída:** o `Normalizar` lê o resultado em `.output`. Uma mudança na versão do nó que altere esse envelope faz todos os campos saírem nulos, sem erro.

### 7.9 `Normalizar` — Code

Modo `Run Once for All Items`. Transforma a saída do parser no registro que vai ao banco e monta o destino do arquivo.

**Regras que este nó aplica:**

| Campo gerado | Regra |
|---|---|
| `data_vencimento` | Sempre dia 15 do mês em que o e-mail é processado |
| `observacoes` | Plataforma, mais moeda original, mais a lista de campos não extraídos, separados por barra vertical |
| `campos_faltantes` | Mesma lista, separada por vírgula, ou `null` |
| `nome_arquivo` | `{plataforma}_{numero}_{emissao}.pdf`, higienizado |
| `pasta_destino` | `{pasta_documentos}/{ano}/{competencia}` |
| `payload_parser` | Resposta bruta do parser, serializada |
| `status` | `incompleto` quando falta campo essencial, `pendente` caso contrário |

**O pareamento com o `Selecionar PDF` é por índice, e aqui isso é seguro.** Entre os dois nós a cadeia é um para um (o `Extrair Texto` e o `Extrair Dados` produzem um item por item de entrada). O que **não** seria seguro é usar `$('Tem PDF').first()`: dois e-mails no mesmo ciclo de poll receberiam o mesmo `message_id_graph`, o segundo INSERT bateria na constraint `UNIQUE` e a fatura desapareceria sem gravar.

**Defesas embutidas, e o que cada uma evita:**

- Data de emissão inválida ou ausente → arquiva no mês corrente, em vez de gerar pasta com nome quebrado.
- `numero_documento` ausente → gera `SEM-NUMERO-{últimos 8 do id}`, mantendo o nome de arquivo único.
- Higienização do nome de arquivo → `numero_documento` vem do PDF e pode trazer barra ou dois-pontos, que o OneDrive rejeita.

**A classificação do status é a defesa do Fechamento contra dado incompleto.** Quatro campos são tratados como essenciais:

```javascript
const CRITICOS = ['valor', 'moeda', 'data_emissao', 'fornecedor'];
```

A escolha não é arbitrária. Sem `data_emissao`, o `Buscar Cotacoes` do Fechamento lança erro e **derruba o fechamento inteiro**, não apenas o lançamento defeituoso. Sem `valor`, o cálculo produz `0` em vez de nulo, e a linha chega à planilha com valor zerado sem disparar nenhuma validação, porque o `throw` do `Montar Valores da Planilha` só protege contra nulo. Os outros dois entram porque uma conta a pagar sem fornecedor ou sem moeda não é importável.

**Este nó é o último ponto onde o binário do PDF ainda está no item.** Ele repassa `binary: base.binary` explicitamente, porque o `Arquivar PDF` precisa do anexo.

### 7.10 `Arquivar PDF` — HTTP Request

| Parâmetro | Valor |
|---|---|
| Method | PUT |
| URL | `https://graph.microsoft.com/v1.0/me/drive/root:{{ $json.pasta_destino }}/{{ $json.nome_arquivo }}:/content` |
| Authentication | Predefined Credential Type → Microsoft OAuth2 API → `Microsoft account` |
| Body Content Type | n8n Binary File |
| Input Data Field Name | `pdf` |
| Retry on Fail | ativado, 3 tentativas, 5000 ms |

**Por que HTTP Request e não o nó Microsoft OneDrive.** O nó OneDrive exige o id da pasta de destino, o que obrigaria a resolver (e criar, quando ausente) as pastas de ano e mês antes de gravar. O upload por caminho do Graph cria as pastas intermediárias sozinho. **Comportamento confirmado empiricamente**, não documentado pela Microsoft: um `PUT` para um caminho com pastas inexistentes retorna 201 e cria a hierarquia.

**Reupload do mesmo caminho sobrescreve em vez de duplicar**, por isso o Retry on Fail é seguro aqui.

**Dependência crítica de saída:** a resposta traz o `id` do arquivo, que o `Gravar Lancamento` grava em `caminho_arquivo`. É esse id que o Fechamento usa meses depois para anexar o comprovante ao e-mail.

### 7.11 `Gravar Lancamento` — Postgres

Operation `Insert`, tabela `public.faturas_saas`, mapeamento manual de 16 colunas.

Quinze colunas vêm de `$('Normalizar').item.json.*`; apenas `caminho_arquivo` vem de `{{ $json.id }}`, porque é a resposta do nó anterior.

> **O `status` é expressão, não valor fixo.** Ele lê `{{ $('Normalizar').item.json.status }}`. Se este campo voltar a ser preenchido com o literal `pendente`, o `Normalizar` continuará classificando corretamente e o INSERT gravará `pendente` para todo mundo, anulando a retenção sem nenhum sinal.

**Colunas deliberadamente fora do mapeamento:**

| Coluna | Motivo |
|---|---|
| `id` | Atribuída pela sequence. Mapeá-la com valor fixo faz o segundo INSERT violar a chave primária |
| `valor_brl`, `cotacao_ptax`, `data_cotacao` | Preenchidas pelo Fechamento. Gravar zero aqui destruiria o sinal de que a conversão ainda não rodou |
| `data_exportacao` | Preenchida na marcação |
| `criado_em` | `DEFAULT now()` |

**Por que Operation `Insert` e não `Execute Query`.** O campo Query Parameters do nó Postgres trata vírgula como separador entre parâmetros distintos. Tanto `observacoes` quanto `campos_faltantes` carregam vírgula quando há mais de um campo não extraído, e os valores seriam fatiados no meio. O modo `Insert` passa os valores como dados, sem esse risco.

**O `payload_parser` é JSONB e recebe texto.** O modo `Insert` converte pelo tipo declarado no schema da tabela.

---

## 8. Workflow: `Workflow Fechamento`

**Gatilho:** Schedule Trigger, cron `0 8 * * *`. **Frequência:** verifica diariamente, executa uma vez por mês.

No dia de corte, converte os lançamentos pendentes para BRL, escreve a planilha de importação do Omie, anexa os comprovantes e envia ao financeiro.

### Cadeia de nós

```
Schedule Trigger -> E dia de fechar? -> Verificar Data -> Buscar Pendentes
  -> Tem Lancamentos? --(true)--> Parametros -> Buscar Cotacoes -> Gravar Conversao
     -> Reler Lancamentos Convertidos -> Baixar modelo
     -> Enviar Copia -> Montar Valores da Planilha -> Escrever Lancamentos
     -> Sobrou Linha de Exemplo? --(true)--> Limpar Linhas  Excedentes --v
                                 --(false)-------------------------------> Baixar Planilha Final
     -> Listar Documentos -> Baixar Documentos -> Juntar Anexos
     -> Montar Envio -> Enviar Fechamento -> Marcar Exportados -> Conferir Marcacao
  Tem Lancamentos? --(false)--> Send a message
```

> **Atenção ao nome `Limpar Linhas  Excedentes`:** ele contém **dois espaços** entre "Linhas" e "Excedentes". O nome está assim no n8n e precisa ser reproduzido literalmente em qualquer expressão que venha a referenciá-lo.

### 8.1 `Schedule Trigger`

Cron `0 8 * * *`. Dispara todos os dias às 08:00.

**Por que diário, se o fechamento é mensal.** Cron não sabe o que é feriado nem sabe antecipar para o dia útil anterior. A decisão de "hoje é o dia?" é tomada pelo nó seguinte, em código, onde há espaço para essa lógica.

### 8.2 `E dia de fechar?` — Code

O nó calcula o dia alvo do mês: parte do `DIA_CORTE` e recua até encontrar um dia útil, pulando fins de semana e feriados. Devolve `ehHoje`, `dataAlvo` e `feriadosConsiderados`.

Uma única constante exige decisão humana:

| Constante | Valor atual | Observação |
|---|---|---|
| `DIA_CORTE` | ==`11`== | Valor de teste. O dia de corte definido para produção é 20 |

**Os feriados são calculados, não listados.** A função `feriadosDoAno(ano)` monta a lista a partir do ano corrente, sem manutenção anual:

| Grupo | Datas |
|---|---|
| Nacionais fixos | 01/01, 21/04, 01/05, 07/09, 12/10, 02/11, 15/11, 20/11, 25/12 |
| Estadual e municipais fixos | 26/01 (Aniversário de Santos), 09/07 (Revolução Constitucionalista), 08/09 (Nossa Senhora do Monte Serrat) |
| Móveis, derivados da Páscoa | Carnaval (segunda e terça), Sexta-Feira Santa, Corpus Christi |

São 16 datas por ano. O nó carrega o ano corrente **e o anterior**, porque o recuo pode atravessar a virada quando o corte cai nos primeiros dias de janeiro. Daí `feriadosConsiderados: 32` na saída.

**Como os móveis são calculados.** Os quatro derivam da Páscoa: Carnaval é Páscoa menos 48 e 47 dias, Sexta-Feira Santa menos 2, Corpus Christi mais 60. A Páscoa sai pelo algoritmo de Meeus/Jones/Butcher, que é aritmética pura sobre o ano, sem tabela e sem rede.

**Por que cálculo local e não uma API de feriados.** O cron casa com um único dia do mês. Uma indisponibilidade da API naquela manhã derrubaria o nó e o mês inteiro passaria sem fechamento, até alguém notar. Uma regra que muda uma vez por século não justifica esse modo de falha. Além disso, as APIs gratuitas de feriado brasileiro costumam cobrir apenas os nacionais, e é justamente o calendário local que interessa aqui.

**Sobre os feriados de Santos.** Sexta-Feira Santa e Corpus Christi são feriado municipal na cidade e já entram pelo cálculo móvel. Carnaval e Quarta-feira de Cinzas constam do decreto municipal como **ponto facultativo**, não feriado; os dois dias de Carnaval foram mantidos na lista mesmo assim, porque o financeiro não opera e antecipar o fechamento é o comportamento desejado. Pontos facultativos mudam a cada ano por decreto e não são calculáveis, então ficam de fora por definição.

**Feriado local afeta o fechamento, não a cotação.** O `Buscar Cotacoes` não consulta esta lista: ele recua um dia por vez até a API do Banco Central devolver cotação, resolvendo o calendário bancário empiricamente. Acrescentar ou remover data aqui não tem efeito nenhum sobre a conversão cambial.

### 8.3 `Verificar Data` — If

Condição booleana sobre `{{ $json.ehHoje }}`. Ramo verdadeiro segue; ramo falso encerra a execução sem erro.

**Por que a decisão está separada do cálculo.** O Code calcula e o If decide. Isso permite inspecionar `dataAlvo` na execução para entender por que um dia foi ou não escolhido, o que seria invisível se a lógica estivesse dentro de um único nó.

### 8.4 `Buscar Pendentes` — Postgres

```sql
SELECT *,
  TO_CHAR(data_emissao,    'YYYY-MM-DD') AS data_emissao_txt,
  TO_CHAR(data_vencimento, 'YYYY-MM-DD') AS data_vencimento_txt
FROM faturas_saas
WHERE status = 'pendente'
ORDER BY data_emissao, id;
```

Always Output Data ativado. Retry on Fail ativado.

**Por que os campos `_txt`.** O nó Postgres devolve `DATE` como objeto de data com fuso, e o deslocamento de fuso pode mudar o dia. Os dois campos textuais garantem a data exata como está no banco, e são eles que alimentam a consulta de cotação e a conversão para serial do Excel.

**Por que Always Output Data.** Sem ele, uma consulta sem resultados não emite item nenhum, e o `Tem Lancamentos?` não chega a executar. A execução terminaria sem passar pelo ramo de "nada a fazer".

**Sem filtro de competência, de propósito.** A consulta traz todo pendente, independentemente da data de emissão. Uma fatura que chegou atrasada entra no próximo fechamento, em vez de ficar órfã.

### 8.5 `Tem Lancamentos?` — If

Condição: `{{ Object.keys($input.first().json).length }}` **maior que** `0`.

**Por que contar chaves e não testar um campo.** Com Always Output Data, uma consulta vazia devolve um item vazio (`{}`), não a ausência de item. Testar um campo específico funcionaria, mas contar chaves é imune a mudanças de nome de coluna.

Ramo verdadeiro segue para o fechamento. Ramo falso vai para o `Send a message`.

### 8.6 `Send a message` — Microsoft Outlook (ramo vazio)

| Parâmetro | Valor |
|---|---|
| Credential | `Microsoft Outlook account` |
| To | ==`gustavo.brito@mosten.com`== |
| Subject | ==`Deu ruim na automação`== |
| Body | ==`TESTE Automação Faturas`== |

**Este nó avisa que o dia de corte passou sem lançamentos pendentes.** O conteúdo atual é de teste e não descreve o que aconteceu. Em produção, o assunto e o corpo precisam informar que o fechamento do mês não teve lançamentos, para que o silêncio não seja confundido com falha.

### 8.7 `Parametros` — Set

| Campo | Valor | Destaque |
|---|---|---|
| `email_destino` | ==`gustavo.brito@mosten.com`== | Destinatário do fechamento |
| `assunto` | `Faturamento e Recibo de Ferramentas de Software` | **Acoplado à condição 4 do `Tem PDF` da Ingestão** |
| `template_file_id` | `0122TQE3AKWNGWOMYTKRFI7E5N72U5BHOE` | Id do modelo no OneDrive |
| `pasta_destino_planilha` | `/Faturas-SaaS/Fechamentos/{{ $now.format('yyyy') }}/{{ $now.format('yyyy-MM') }}` | Caminho puro, sem `root:` e sem barra final |
| `nome_aba` | `Omie_Contas_Pagar` | Nome da aba na planilha do Omie |
| `competencia` | `{{ $now.format('yyyy-MM') }}` | Usada no nome do arquivo e no corpo do e-mail |

Include Other Input Fields ativado.

**O `template_file_id` é um id de arquivo, e ids são específicos do drive.** Se a automação passar a rodar sob outra conta Microsoft, o modelo terá outro id e este campo precisa ser atualizado. Mover ou recriar o arquivo também gera id novo.

**Por que os nós referenciam este Set com `.first()` e não `.item`.** O `Parametros` sempre produz um item só, enquanto os nós que o consomem processam vários lançamentos. Com `.item`, o n8n tenta parear cardinalidades diferentes e devolve `Multiple matches found`.

### 8.8 `Buscar Cotacoes` — Code

Consulta a API PTAX do Banco Central e calcula `valor_brl` para cada lançamento.

**Mecânica:**

- Cache interno por data: várias faturas do mesmo dia consomem uma chamada só.
- Lançamento com `moeda = BRL` não passa por conversão: recebe cotação 1.
- Fim de semana e feriado não têm publicação PTAX, então o código **recua um dia por vez até encontrar cotação**, com limite de 10 recuos.
- A cotação usada é a **de venda** (`cotacaoVenda`).

**Por que Code com `this.helpers.httpRequest`, e não um nó HTTP Request.** O recuo até o dia útil anterior é um laço com número variável de iterações por item. Feito no canvas, exigiria laço com nó de decisão e agregação, com muito mais superfície de falha.

**Validações que interrompem a execução:**

| Verificação | Motivo |
|---|---|
| Formato de `data_emissao_txt` | Sem ela, uma data mal serializada gera URL inválida, o Banco Central devolve lista vazia, o recuo roda dez vezes e o erro final fala de "cotação não encontrada", apontando para o lugar errado |
| Sem cotação após 10 recuos | Indica indisponibilidade da API, não feriado prolongado |

> **Limitação registrada:** o endpoint consultado é `CotacaoDolarDia`, específico do dólar. Lançamentos em moeda diferente de USD e BRL seriam convertidos pela cotação do dólar, silenciosamente. Hoje todas as plataformas faturam em USD, mas se alguma passar a faturar em EUR, este nó precisa ser revisto antes.

> **Limitação de negócio:** a PTAX é a cotação oficial, e a fatura do cartão de crédito embute spread cambial e IOF, além de usar a cotação do dia da compensação. Os valores da planilha e da fatura do cartão não vão coincidir. A `cotacao_ptax` e a `data_cotacao` ficam gravadas por lançamento justamente para permitir a conciliação.

### 8.9 `Gravar Conversao` — Postgres

```sql
UPDATE faturas_saas
   SET valor_brl = $1, cotacao_ptax = $2, data_cotacao = $3
 WHERE id = $4;
```

Query Parameters: `{{ $json.valor_brl }}, {{ $json.cotacao_ptax }}, {{ $json.data_cotacao }}, {{ $json.id }}`.

Execute Once **desativado**: roda uma vez por lançamento.

**Este nó é obrigatório e a razão não é óbvia.** Sem ele, `valor_brl` existiria apenas na memória deste ramo, enquanto o `Montar Valores da Planilha` relê os registros do banco. O resultado seria uma planilha com a coluna de valor vazia, depois de todo o cálculo ter rodado corretamente.

**Persistir também dá rastreabilidade:** se a Controladoria questionar um valor meses depois, a cotação usada e a data dela estão na linha, não apenas no log de execução do n8n, que expira.

**Aqui a vírgula no Query Parameters é correta**, porque são quatro parâmetros distintos e nenhum dos valores contém vírgula.

### 8.10 `Reler Lancamentos Convertidos` — Postgres

```sql
SELECT
  f.*,
  TO_CHAR(f.data_emissao,    'YYYY-MM-DD') AS data_emissao_txt,
  TO_CHAR(f.data_vencimento, 'YYYY-MM-DD') AS data_vencimento_txt,
  (SELECT count(*) FROM faturas_saas WHERE status = 'incompleto') AS qtd_incompletos
FROM faturas_saas f
WHERE f.status = 'pendente'
ORDER BY f.data_emissao, f.id;
```

Execute Once ativado, Always Output Data ativado.

**É a mesma consulta do `Buscar Pendentes`, de propósito. A diferença é o momento:** aqui os registros já têm `valor_brl` preenchido.

**A subconsulta `qtd_incompletos` vem junto para evitar um nó a mais.** Ela repete o mesmo número em todas as linhas do resultado, o que é irrelevante: o `Montar Envio` lê apenas do primeiro item. Sem ela, os registros retidos ficariam invisíveis na base por tempo indeterminado.

**Este nó é a fonte de verdade de três etapas distintas:**

| Consumidor | Uso |
|---|---|
| `Montar Valores da Planilha` | Monta as linhas da planilha |
| `Listar Documentos` | Descobre quais PDFs anexar |
| `Marcar Exportados` | Monta a lista de ids a marcar |
| `Conferir Marcacao` | Compara a quantidade esperada com a marcada |

> **Consequência importante:** o conjunto que entra na planilha, o conjunto que vira anexo e o conjunto que é marcado como exportado são necessariamente o mesmo. Se qualquer um deles passasse a reconsultar a tabela por conta própria, um lançamento gravado pela Ingestão durante a execução do fechamento entraria na marcação sem ter entrado no arquivo enviado.

### 8.11 `Baixar modelo` — Microsoft OneDrive

Operation `Download`, File ID vindo do `template_file_id`, binário em `modelo`. Execute Once ativado.

### 8.12 `Enviar Copia` — HTTP Request

| Parâmetro | Valor |
|---|---|
| Method | PUT |
| URL | `https://graph.microsoft.com/v1.0/me/drive/root:{{ $('Parametros').first().json.pasta_destino_planilha }}/Omie_Contas_Pagar_{{ $('Parametros').first().json.competencia }}.xlsx:/content` |
| Authentication | Predefined Credential Type → Microsoft OAuth2 API → `Microsoft account` |
| Body Content Type | n8n Binary File |
| Input Data Field Name | `modelo` |
| Execute Once | ativado |
| Retry on Fail | ativado, 5000 ms |

**Por que HTTP Request por caminho e não o nó OneDrive.** O nó OneDrive grava por `parentId`, o que exigiria resolver a pasta do mês antes, com um `GET` que falha quando a pasta ainda não existe. O upload por caminho cria a hierarquia sozinho, do mesmo jeito que o `Arquivar PDF` da Ingestão faz com os PDFs. É por isso que nenhuma pasta de fechamento precisa ser criada à mão.

**Por que baixar e reenviar em vez de usar a cópia nativa do Graph (`POST .../copy`).** A cópia do Graph é assíncrona: devolve um cabeçalho `Location` que precisa ser consultado em laço até a operação concluir, e só então o id do novo arquivo fica disponível. O download seguido de upload devolve o id direto, num nó.

**Reexecutar o fechamento no mesmo mês sobrescreve o arquivo**, em vez de gerar `Omie_Contas_Pagar_2026-08 1.xlsx`. O nome é idempotente, o que é desejável, mas a versão anterior deixa de existir no OneDrive.

**Limitação da escolha:** vale enquanto o modelo estiver abaixo de 4 MB. Acima disso o upload simples deixa de servir e passa a exigir upload em sessões.

**O Execute Once deste nó e do `Baixar modelo` é obrigatório.** Sem ele, eles rodam uma vez por lançamento e sobrescrevem a mesma planilha repetidas vezes com o modelo em branco. **Com um único lançamento em teste, o defeito não aparece.**

**Dependência de saída:** o `id` devolvido aqui é usado por `Escrever Lancamentos`, `Limpar Linhas  Excedentes` e `Baixar Planilha Final`. É o identificador da planilha do mês.

### 8.13 `Montar Valores da Planilha` — Code

Converte os registros nas linhas da planilha do Omie e calcula os endereços de escrita e de limpeza.

**Constantes de layout:**

| Constante | Valor | Significado |
|---|---|---|
| `LINHA_INICIAL` | 6 | Primeira linha de dados do modelo |
| `ULTIMA_LINHA_EXEMPLO` | 37 | Última linha pré-formatada do modelo |
| `COLUNAS` | B até AA | Faixa escrita |

**Mapeamento das colunas:**

| Coluna | Conteúdo | Origem |
|---|---|---|
| B | vazia | O modelo traz `0` e a coluna está dentro do range de importação |
| C | Fornecedor | `fornecedor` |
| D | `Software e Aplicativos` | Fixo |
| E | `Visa Caixa -7346` | Fixo |
| F | Valor da conta | `valor_brl` |
| I, J | Data de Emissão e Data de Registro | `data_emissao`, convertida a serial do Excel |
| K | Data de Vencimento | `data_vencimento`, idem |
| S | Observações | `observacoes` |
| T, U | Tipo e número do documento | |
| V, W | Parcela e total de parcelas | Normalmente vazias |
| AA | `Cartão de crédito` | Fixo |
| M, N | vazias | Data e Valor do Pagamento, por decisão |
| Y, Z | vazias | Nota Fiscal e Chave da NF-e. Nenhuma das plataformas emite documento fiscal brasileiro |

**Três regras deste código, e por que existem:**

1. **A origem é o `Reler Lancamentos Convertidos`, nunca o `Buscar Pendentes`.** O `Buscar Pendentes` é a foto anterior à conversão, com `valor_brl` nulo. Ler de lá produz planilha com a coluna de valor vazia.
2. **Célula que deve ficar vazia recebe `""`, nunca `null`.** Na Workbook API, `null` significa "não altere esta célula", e as linhas de exemplo do modelo **têm conteúdo**. Enviar `null` faz esse conteúdo vazar para o arquivo entregue: todas as linhas sairiam com Data do Pagamento 15/06/2026, e a primeira herdaria também Projeto e Valor do Pagamento. **Comportamento confirmado em execução.**
3. **A escrita começa na coluna B, não na C.** A coluna B (Código de Integração) vem com `0` em todas as linhas do modelo e está dentro do range que o Omie importa.

**Dois `throw` de proteção:** lançamento sem `valor_brl` (indica falha no `Gravar Conversao`) e lançamento sem data de vencimento.

**Limitação registrada:** acima de 32 lançamentos, o `throw` de capacidade interrompe. A aba `Config` do modelo declara o range de importação até a linha 10005, então o limite não é de aceite do arquivo, e sim de formatação: apenas as linhas 6 a 37 trazem formatação e validação de data. Passando disso, a solução é aplicar `numberFormat` nas colunas de data das linhas novas via Workbook API. Com cinco assinaturas, o volume está muito abaixo.

### 8.14 `Escrever Lancamentos` — HTTP Request

`PATCH` no endereço `range(address='{{ enderecoEscrita }}')` da Workbook API, com o corpo `{ values: [...] }`.

**Por que a Workbook API e não manipulação do arquivo.** A planilha do Omie carrega validações de data, uma aba `Config` com o range de importação e uma imagem incorporada. Editar o `.xlsx` como ZIP corrompe o arquivo. A Workbook API é o mesmo mecanismo que o Excel Online usa: a integridade é garantida pelo serviço da Microsoft, e nada precisa ser instalado na VM. A API escreve apenas o intervalo indicado, então tudo que está fora dele permanece intocado.

**O nome da aba vem de `Parametros.nome_aba`, não escrito na URL.** Precisa coincidir exatamente com o nome da aba na planilha, incluindo maiúsculas.

### 8.15 `Sobrou Linha de Exemplo?` — If

Condição: `$('Montar Valores da Planilha').first().json.enderecoLimpeza` **is not empty**.

**Por que a referência é ao nó de origem e não a `$json`.** Este If recebe a saída do `Escrever Lancamentos`, que é um HTTP Request: o item foi substituído pela resposta do Graph, e `enderecoLimpeza` não existe mais em `$json`.

**Os dois ramos convergem no `Baixar Planilha Final`.** Se apenas o ramo verdadeiro seguisse, um fechamento que usasse exatamente as 32 linhas nunca chegaria ao envio, e a execução terminaria sem erro e sem e-mail.

### 8.16 `Limpar Linhas  Excedentes` — HTTP Request

`POST` em `range(address='{{ enderecoLimpeza }}')/clear` com `{"applyTo": "Contents"}`.

**Por que a limpeza é necessária.** Cada linha de exemplo não utilizada carrega Código de Integração `0`, Conta Corrente, Data de Vencimento 15/06/2026, Data do Pagamento e Forma de Pagamento, tudo dentro do range que o Omie importa, e nenhum fornecedor. É linha inválida com aparência de linha preenchida.

**Este nó precisa rodar antes do download, não em paralelo.** Se o `Baixar Planilha Final` executasse antes, o binário anexado ao e-mail conteria as linhas residuais enquanto o arquivo no OneDrive ficaria correto. Conferir o arquivo no OneDrive não revelaria o problema.

### 8.17 `Baixar Planilha Final` — Microsoft OneDrive

Download pelo id do `Enviar Copia`, binário em `planilha`.

**Baixa pelo id, não pelo caminho.** O id é a única referência garantida ao arquivo do mês; montar o caminho por texto reintroduziria a dependência de a pasta existir com o nome exato.

### 8.18 `Listar Documentos` — Code

Filtra os registros que têm `caminho_arquivo` preenchido e emite um item por documento.

Retorna lista vazia quando nenhum lançamento tem PDF arquivado. Nesse caso o fechamento segue apenas com a planilha.

### 8.19 `Baixar Documentos` — Microsoft OneDrive

Download pelo `caminho_arquivo`, binário em `documento`. Always Output Data ativado.

**On Error: `Continue (using error output)`.** Um PDF ausente ou com id inválido sai pela saída de erro e **não derruba o fechamento**. O lançamento continua na planilha; o que falta é apenas o comprovante.

**Retry on Fail deliberadamente desativado neste nó.** Insistir três vezes em um arquivo que não existe apenas atrasa o fechamento.

**As duas saídas ligam no `Juntar Anexos`.** O nó seguinte distingue os itens pelo binário, não pela origem.

### 8.20 `Juntar Anexos` — Code

Monta um único item com todos os binários: `planilha` primeiro, depois `documento_1`, `documento_2` e assim por diante. Devolve `totalAnexos` e `totalDocumentos`.

**A leitura `$('Baixar Documentos').all()` retorna apenas a saída de índice 0**, a de sucesso. Os itens que caíram no ramo de erro ficam de fora sem necessidade de tratamento adicional. A verificação `item.binary && item.binary.documento` é a segunda proteção.

### 8.21 `Montar Envio` — Code

Monta o corpo da chamada `POST /me/sendMail`, convertendo cada binário para base64 no formato `#microsoft.graph.fileAttachment`.

**Por que montar o envio à mão em vez de usar o nó Microsoft Outlook.** O nó Outlook não aceita uma lista de anexos com múltiplos binários; ele espera uma propriedade por vez. Com planilha mais N documentos, o envio precisa ser montado como chamada direta ao Graph. **Comportamento confirmado em execução.**

**Usa `this.helpers.getBinaryDataBuffer`**, que funciona tanto com binário em memória quanto em disco, conforme o modo de armazenamento do n8n.

**Trava de tamanho:** 3 MB no total dos anexos. O Graph rejeita mensagens acima de aproximadamente 4 MB. Ultrapassando, o nó falha com instrução explícita: enviar apenas a planilha e substituir os PDFs por link da pasta do mês.

**O corpo do e-mail declara competência, quantidade de lançamentos e de documentos anexados.** A quantidade de lançamentos vem do `Reler Lancamentos Convertidos`, o que permite ao financeiro conferir se o número de linhas da planilha bate com o esperado.

**A última linha do corpo reporta os registros retidos.** Lê `qtd_incompletos` do `Reler Lancamentos Convertidos` e, quando maior que zero, avisa que existem documentos recebidos que não entraram na planilha por falta de campos essenciais. Quando é zero, declara isso explicitamente, para que a ausência do aviso não seja confundida com falha do próprio aviso.

### 8.22 `Enviar Fechamento` — HTTP Request

`POST https://graph.microsoft.com/v1.0/me/sendMail`, autenticação por Predefined Credential Type → Microsoft Outlook OAuth2 API. Retry on Fail ativado.

> **Ressalva registrada:** `sendMail` não é idempotente. Se o envio ocorrer e apenas a resposta se perder, a retentativa gera um segundo e-mail. É um cenário improvável, e o tradeoff foi assumido: e-mail duplicado incomoda menos que fechamento perdido.

### 8.23 `Marcar Exportados` — Postgres

```sql
UPDATE faturas_saas
   SET status = 'exportado', data_exportacao = now()
 WHERE id = ANY(string_to_array($1, '|')::int[])
   AND status = 'pendente'
RETURNING id;
```

Query Parameters: `{{ $('Reler Lancamentos Convertidos').all().map(i => i.json.id).join('|') }}`

Execute Once ativado, Always Output Data ativado, Retry on Fail ativado.

> **O separador é a barra vertical, nunca a vírgula.** O campo Query Parameters do nó Postgres trata vírgula como separador entre parâmetros distintos: passando `2,3`, o n8n entende `$1 = 2` e `$2 = 3`, e como a query só usa `$1`, apenas o primeiro lançamento é marcado. O sintoma é traiçoeiro: o fechamento funciona, o e-mail sai completo, e uma execução posterior reenvia os lançamentos que ficaram para trás. Pelo mesmo motivo, não usar `JSON.stringify`: além da vírgula, os colchetes produzem `malformed array literal`.

**O `RETURNING id` não é decorativo.** O nó Postgres não devolve `affectedRows`; sem o `RETURNING`, o `Conferir Marcacao` não teria como saber quantas linhas foram atualizadas. O Always Output Data garante que um UPDATE que não atinja nenhuma linha ainda produza item, para que a verificação seguinte execute.

**O `AND status = 'pendente'` é uma trava:** reexecutando o fluxo sobre registros já marcados, a `data_exportacao` original é preservada.

**A posição, depois do envio, é deliberada.** Ver seção 5.4.

### 8.24 `Conferir Marcacao` — Code

Compara a quantidade de lançamentos enviados com a quantidade de linhas efetivamente marcadas e lança erro quando divergem.

```javascript
const esperado = $('Reler Lancamentos Convertidos').all().length;
const marcados = $input.all().filter((i) => i.json.id !== undefined).length;
```

**Marcação incompleta é silenciosa e só apareceria como lançamento duplicado no ciclo seguinte.** Este nó transforma isso em erro visível, que dispara o `Infra - Notificar Erro`.

**A contagem é sobre os ids devolvidos pelo `RETURNING`.** Uma versão anterior lia `affectedRows`, campo que este nó Postgres não devolve, e o resultado era uma verificação que nunca disparava: o alarme parecia armado e não estava.

---

## 9. Workflow: `Infra - Notificar Erro`

**Gatilho:** Error Trigger. **Frequência:** sob demanda, quando outro workflow falha.

Dois nós. É o error workflow apontado nas Settings dos demais.

### 9.1 `Error Trigger`

Sem configuração.

> **Este workflow não precisa ser ativado.** Workflows com Error Trigger executam mesmo inativos.

> **O Error Trigger só dispara em execuções de produção.** Uma falha em execução manual, disparada pelo botão Execute workflow do editor, **não** aciona o error workflow. Ao testar, é preciso ativar o workflow e deixar o gatilho real dispará-lo.

### 9.2 `Send a message` — Microsoft Outlook

| Parâmetro | Valor |
|---|---|
| Credential | `Microsoft Outlook account` |
| To | ==`gustavo.brito@mosten.com`== |
| Subject | `[FALHA] {{ $json.workflow.name }}` |
| Body | Nó, erro, horário e URL da execução |

**As expressões do corpo usam encadeamento opcional, e isso é essencial:**

```
No: {{ $json.execution?.lastNodeExecuted || 'falha no gatilho' }}
Erro: {{ $json.execution?.error?.message || $json.trigger?.error?.message || 'sem mensagem' }}
Horario: {{ $json.execution?.startedAt || $now }}
Execucao: {{ $json.execution?.url || 'sem URL' }}
```

**Quando o erro ocorre no próprio nó de gatilho**, o payload que chega ao Error Trigger tem forma diferente: o objeto `execution` vem reduzido, sem `id` nem `url`, e a informação fica em `trigger`. Sem o encadeamento opcional, o próprio e-mail de falha falharia justamente no cenário de credencial vencida, que é o mais importante de capturar.

**A URL da execução depende de `N8N_EDITOR_BASE_URL` (ou `WEBHOOK_URL`) estar definida nas variáveis de ambiente da instância.** Sem isso, o link vem vazio.

> **As Settings deste workflow devem ter o campo Error Workflow vazio.** Um workflow com Error Trigger usa a si mesmo como error workflow por padrão; se o envio do Outlook falhar, isso produz realimentação.

---

## 10. Workflow: `Infra - Monitor Client Secret`

**Gatilho:** Schedule Trigger, cron `0 8 * * *`. **Frequência:** diária.

Avisa por e-mail antes de o client secret da aplicação no Entra ID expirar.

**Por que existe.** O secret não é usado a cada execução: o n8n usa um token de curta duração renovado automaticamente, e é a renovação que exige o secret. Quando ele vence, a automação continua funcionando por até uma hora, usando o último token válido, e só então começa a falhar. Como o ciclo do Fechamento é mensal, poderiam passar semanas até alguém perceber. **Um secret vencido derruba a Ingestão e o Fechamento ao mesmo tempo**, porque as duas credenciais Microsoft dependem dele.

### 10.1 `Schedule Trigger`

Cron `0 8 * * *`.

**Sem verificação de dia útil, diferente do Fechamento.** Secret vence em sábado do mesmo jeito.

### 10.2 `CONFIG_SECRET` — Set

| Campo | Valor atual |
|---|---|
| `data_expiracao` | `2028-08-05` |
| `indentificacao_app` | `n8n-Mosten-Faturas` |
| `client_id` | ==`cb40c678-15fe-4bcc-9edc-3677ce006d54`== |
| `destinatarios` | ==`gustavo.brito@mosten.com`== |

> **O campo está grafado `indentificacao_app`**, com "n" a mais. O corpo do e-mail no `Enviar Alerta` referencia `$json.identificacao_app`, sem o "n". Os dois nomes não coincidem, e a consequência é que o nome da aplicação sai vazio no e-mail. Ver seção 12.

**O formato da data importa.** O `Calcular Dias` concatena `T00:00:00` ao valor. Uma data em formato brasileiro produziria data inválida.

### 10.3 `Calcular Dias` — Code

Calcula os dias restantes até a expiração e decide se hoje é dia de alertar.

```javascript
const marcos = [90, 60, 30, 15];
const deveAlertar = marcos.includes(diasRestantes) || diasRestantes <= 7;
```

| Faixa | Severidade |
|---|---|
| Mais de 7 dias | `AVISO` |
| De 0 a 7 dias | `URGENTE` |
| Vencido | `CRITICO - JA EXPIRADO` |

**Por que marcos espaçados no início e alerta diário na última semana.** Um e-mail único enviado com 90 dias de antecedência se perde na caixa como qualquer outro. E marcos isolados nos últimos dias seriam frágeis: se a instância estivesse fora do ar no dia exato do marco, aquele aviso se perderia. Com `<= 7`, a última semana alerta todo dia e um dia perdido não custa nada.

**O `throw` na data inválida é a proteção mais importante deste workflow.** Sem ele, uma data mal digitada produz `NaN`, nenhuma comparação é verdadeira, e o workflow roda verde todo dia sem nunca alertar. É a pior falha possível num monitor: ele parece vivo e não está.

**Nota sobre fuso horário:** o `new Date()` usa o relógio do container, não o Timezone configurado nas Settings do workflow. Como o gatilho dispara às 08:00, a diferença de fuso não altera a data calculada.

### 10.4 `Deve Alertar?` — If

Condição booleana sobre `{{ $json.deveAlertar }}`. Ramo falso desconectado.

### 10.5 `Enviar Alerta` — Microsoft Outlook

| Parâmetro | Valor |
|---|---|
| Credential | `Microsoft account` (Microsoft OAuth2 API) |
| To | `{{ $json.destinatarios }}` |
| Subject | `[{{ $json.severidade }}] Client Secret do n8n expira em {{ $json.diasRestantes }} dias` |

**Quando o secret estiver vencido, o assunto dirá "expira em -3 dias".** Fica estranho de ler, mas a severidade no início deixa o estado claro, e um texto condicional não compensa a complexidade para um caso que só ocorre se todos os avisos anteriores forem ignorados.

### 10.6 Duas limitações registradas

**O monitor usa a credencial que ele monitora.** Enquanto o secret está válido, funciona. Depois de vencido, o alerta de "já expirou" não consegue ser enviado, porque o envio depende do mesmo secret. É aceitável, já que a função do monitor é avisar **antes**. O que não cobre é o cenário de a instância estar fora do ar durante toda a janela de aviso.

**A data é manual.** Existe API do Graph para consultar `passwordCredentials` da aplicação e obter a expiração real, o que eliminaria o passo manual. Exige a permissão `Application.Read.All`, que é permissão de diretório e normalmente requer aprovação de administrador. Fica registrado como melhoria possível.

### 10.7 Procedimento de renovação do client secret

Uma aplicação do Entra ID aceita mais de um secret válido simultaneamente, então a renovação não exige parada:

1. Criar o novo secret no Azure, **antes** de o atual vencer
2. Copiar o campo **Value** imediatamente — ele só é exibido uma vez
3. Atualizar o Client Secret nas **duas** credenciais do n8n: `Microsoft account` e `Microsoft Outlook account`
4. Refazer o Connect das credenciais, se necessário
5. Testar com uma leitura simples, executando o `Trigger Faturas` da Ingestão
6. **Atualizar o `data_expiracao` no `CONFIG_SECRET`**
7. Só então remover o secret antigo no Azure

> **O passo 6 é o que mantém o monitoramento vivo.** Sem ele, o monitor silencia permanentemente e passa uma falsa sensação de segurança.

---

## 11. Campos a alterar antes da produção

Todos os valores destacados ao longo do documento, consolidados. Nenhum destes é defeito: são valores de teste, coerentes com o estado atual de validação.

| # | Workflow | Nó | Campo | Valor atual | Valor de produção |
|---|---|---|---|---|---|
| 1 | Ingestão | `Tem PDF` | Condição 3, remetente | ==`gustavo.brito@mosten.com`== | Lista dos remetentes reais das plataformas |
| 2 | Ingestão | `Trigger Faturas` | Credencial / caixa vigiada | ==Conta `gustavo.brito@mosten.com`== | Conta de serviço, ou caixa compartilhada `faturas@mosten.com` |
| 3 | Ingestão | `Groq Chat Model` | Credencial e modelo | ==Groq / `openai/gpt-oss-120b`== | Provedor definitivo, após decisão sobre dados |
| 4 | Fechamento | `E dia de fechar?` | `DIA_CORTE` | ==`11`== | `20` |
| 5 | Fechamento | `Parametros` | `email_destino` | ==`gustavo.brito@mosten.com`== | `financeiro@mosten.com` |
| 6 | Fechamento | `Send a message` | To, Subject e Body | ==Conteúdo de teste== | Destinatário real e texto que descreva o ciclo sem lançamentos |
| 7 | Notificar Erro | `Send a message` | To | ==`gustavo.brito@mosten.com`== | Três destinatários com acesso ao Entra ID |
| 8 | Monitor | `CONFIG_SECRET` | `destinatarios` | ==`gustavo.brito@mosten.com`== | Mesmos três destinatários |
| 9 | Monitor | `CONFIG_SECRET` | `client_id` | ==`cb40c678-15fe-4bcc-9edc-3677ce006d54`== | Application ID confirmado (ver seção 12) |

### Sobre o item 2, que tem alcance maior que os demais

Trocar a conta Microsoft altera três coisas ao mesmo tempo: a caixa vigiada pelo trigger, o OneDrive de destino dos arquivos e o endereço remetente dos envios. A migração exige:

- Mover `/Faturas-SaaS` inteiro para o OneDrive da conta nova, preservando a estrutura de pastas
- Atualizar o `template_file_id` no `Parametros` do Fechamento, porque ids de arquivo são específicos do drive
- Atualizar o filtro de pasta do `Trigger Faturas`, que guarda o id da Caixa de Entrada da conta atual
- Revalidar `Arquivar PDF`, `Baixar modelo`, `Enviar Copia`, `Baixar Planilha Final` e `Baixar Documentos`

---

## 12. Divergências identificadas na configuração atual

Diferente da seção anterior, estes são pontos que merecem correção independentemente da entrada em produção.

### 12.1 Nome de campo divergente no Monitor

O `CONFIG_SECRET` define o campo como `indentificacao_app`. O corpo do e-mail no `Enviar Alerta` referencia `{{ $json.identificacao_app }}`. Os nomes não coincidem, e o e-mail de alerta sai com o nome da aplicação em branco.

**Correção:** renomear o campo no `CONFIG_SECRET` para `identificacao_app`, alinhando com a expressão.

### 12.2 Client ID a confirmar

O `client_id` configurado (`cb40c678-15fe-4bcc-9edc-3677ce006d54`) é o mesmo identificador que aparece nas respostas do Graph no campo `createdBy.application.id`, cujo `displayName` é "Microsoft Graph". Isso levanta a possibilidade de o valor ser o identificador da aplicação de primeira parte da Microsoft, e não o Application ID da aplicação registrada `n8n-Mosten-Faturas`.

**Correção:** conferir no Portal do Azure, em Microsoft Entra ID → App registrations → `n8n-Mosten-Faturas` → Overview → Application (client) ID, e corrigir se divergir. O campo é informativo, usado apenas no corpo do e-mail de alerta, então o erro não afeta o funcionamento, mas envia quem for renovar o secret para a aplicação errada.

### 12.3 Espaço duplo no nome de um nó

O nó `Limpar Linhas  Excedentes` tem dois espaços no nome.

**Correção opcional:** renomear para espaço simples. Nenhuma expressão o referencia hoje, então a mudança é segura. Se ficar como está, o nome precisa ser reproduzido literalmente em qualquer referência futura.

### 12.4 Espaço final na expressão cron do Monitor

O cron do `Infra - Monitor Client Secret` está gravado como `0 8 * * * `, com espaço ao final. O n8n aceita e o disparo funciona.

**Correção opcional:** remover o espaço, para evitar dúvida em manutenção futura.

### 12.5 Nó auxiliar com nome padrão

O nó `Execute a SQL query1` do `Infra - Setup Tabela Faturas` mantém o nome padrão do n8n.

**Correção opcional:** renomear para algo como `Conferir Tabela`, deixando explícito que é verificação e não parte da criação.

### 12.6 Configurações não verificáveis pelo JSON exportado

As Settings de workflow (Error Workflow e Timezone) não constam da exportação de nós. É necessário conferir na interface, workflow a workflow:

| Workflow | Error Workflow esperado | Timezone esperado |
|---|---|---|
| `Workflow Ingestão` | `Infra - Notificar Erro` | `America/Sao_Paulo` |
| `Workflow Fechamento` | `Infra - Notificar Erro` | `America/Sao_Paulo` |
| `Infra - Monitor Client Secret` | `Infra - Notificar Erro` | `America/Sao_Paulo` |
| `Infra - Notificar Erro` | **vazio** | `America/Sao_Paulo` |
| `Infra - Setup Tabela Faturas` | indiferente | indiferente |

---

## 13. Manutenção periódica

| Periodicidade                       | Tarefa                                                                                                | Onde                           |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------ |
| A cada fechamento | Conferir no e-mail se há registros retidos como `incompleto` e completá-los na base | Banco |
| Anual, opcional | Conferir as 16 datas calculadas contra o decreto de feriados da Prefeitura de Santos. Só exige alteração se a Prefeitura criar ou extinguir feriado | `E dia de fechar?`, Fechamento |
| Conforme o alerta                   | Renovar o client secret e atualizar `data_expiracao`                                                  | Seção 10.7                      |
| A cada plataforma nova              | Acrescentar o remetente ao `Tem PDF` e o valor ao `enum` de `plataforma` no schema do `Extrair Dados` | Ingestão                       |
| A cada plataforma nova              | Conferir a primeira fatura campo a campo contra o PDF                                                 | Ingestão                       |
| A cada troca de modelo de linguagem | Reconferir a extração com uma fatura de cada plataforma                                               | Ingestão                       |

---

## 14. Diagnóstico de falhas

### O fechamento não rodou no dia esperado

1. Verificar em Executions se houve execução no dia. Sem execução, o problema é o Schedule Trigger ou o workflow está inativo.
2. Havendo execução curta, abrir o `E dia de fechar?` e conferir `dataAlvo`. Se o dia de corte caiu em fim de semana ou feriado, o alvo foi antecipado.
3. Conferir `DIA_CORTE`. Para saber qual feriado antecipou o alvo, comparar a `dataAlvo` com o calendário do ano: as 16 datas estão descritas na seção 8.2.

### O fechamento rodou mas não enviou e-mail

- Ramo falso do `Tem Lancamentos?`: não havia pendentes. Confirmar com `SELECT status, count(*) FROM faturas_saas GROUP BY status;`. Se houver registros em `incompleto` e nenhum em `pendente`, o parser não conseguiu extrair os campos essenciais e todos ficaram retidos.
- Execução vermelha: o e-mail de falha do `Infra - Notificar Erro` indica o nó.

### A planilha chegou com a coluna de valor vazia

Falha no `Gravar Conversao`: a conversão não foi persistida. O `Montar Valores da Planilha` lança erro explícito nesse caso, então a execução deve estar vermelha.

### A planilha chegou com linhas a mais, com data 15/06/2026

As linhas de exemplo do modelo não foram limpas. Verificar o `Sobrou Linha de Exemplo?` e o `Limpar Linhas  Excedentes`, e confirmar que o `Baixar Planilha Final` roda depois da limpeza.

### Lançamentos foram reenviados no ciclo seguinte

Marcação incompleta. Conferir o separador no Query Parameters do `Marcar Exportados`: precisa ser `join('|')`. Com o `Conferir Marcacao` funcionando, isso derruba a execução em vez de passar despercebido.

### Uma fatura não virou lançamento

Percorrer o funil na Ingestão, na ordem:

1. O e-mail chegou na caixa vigiada pela credencial?
2. Passou nas quatro condições do `Tem PDF`? Remetente e assunto são as causas mais comuns.
3. O `Ja Processado?` caiu no ramo falso? O e-mail já foi processado antes.
4. O `Extrair Texto` devolveu texto? PDF escaneado devolve vazio.
5. O registro foi gravado como `incompleto`? Ele existe na base, mas o Fechamento não o enxerga. Conferir `campos_faltantes`.
6. O `Gravar Lancamento` falhou por `message_id_graph` duplicado?

### Dois registros parecem ter o mesmo `message_id_graph`

Os ids do Outlook têm cerca de 150 caracteres e compartilham um prefixo longo, comum a toda a caixa. A diferença fica nos últimos caracteres, e qualquer visualização que trunque a coluna mostra valores aparentemente idênticos. Confirmar com:

```sql
SELECT count(*) AS total, count(DISTINCT message_id_graph) AS distintos
  FROM faturas_saas;
```

### A planilha chegou sem um dos lançamentos esperados

Conferir o status do registro na base. Se estiver `incompleto`, ele foi retido por falta de campo essencial e o e-mail do fechamento traz a contagem. Completar os campos e promover para `pendente`; ele entra no ciclo seguinte.

### Erro `Referenced node doesn't exist`

Algum nó foi renomeado sem atualizar as expressões que o referenciam. As expressões `$('Nome do No')` fazem correspondência literal.

### Erro `Multiple matches found`

Uso de `.item` para referenciar um nó que produz um item só, a partir de um nó que processa vários. Trocar para `.first()`.

---

## 15. Limitações conhecidas

Nenhuma destas bloqueia a operação. Estão registradas para que não sejam redescobertas como se fossem defeito.

| Limitação                                        | Efeito                                               | Contorno                                                         |
| ------------------------------------------------ | ---------------------------------------------------- | ---------------------------------------------------------------- |
| E-mail com mais de um PDF processa só o primeiro | A segunda fatura não é registrada                    | `total_anexos_pdf` na saída do `Selecionar PDF` permite detectar |
| Fatura enviada apenas como link, sem anexo       | E-mail é descartado pelo filtro                      | Lançamento manual                                                |
| PDF escaneado, sem camada de texto | Registro retido como `incompleto`, fora do fechamento | PDF fica arquivado; completar os campos e promover para `pendente` |
| Conversão sempre pela cotação do dólar           | Moeda diferente de USD e BRL seria convertida errado | Hoje todas as plataformas faturam em USD                         |
| PTAX não coincide com a fatura do cartão         | Diferença de spread e IOF                            | Conciliação pelo financeiro, com `cotacao_ptax` gravada          |
| Acima de 32 lançamentos, sem formatação de data  | O `throw` interrompe antes de gerar arquivo torto    | Aplicar `numberFormat` via Workbook API quando o volume exigir   |
| Modelo acima de 4 MB quebra o `Enviar Copia`     | Upload simples deixa de servir                       | Upload em sessões                                                |
| Anexos acima de 3 MB no total                    | O `Montar Envio` interrompe                          | Enviar só a planilha e linkar a pasta                            |
| `Enviar Fechamento` pode duplicar em retentativa | E-mail repetido                                      | Tradeoff assumido                                                |
| Monitor depende do secret que monitora | Não alerta depois de vencido | A função é avisar antes |
| Reexecução no mesmo mês sobrescreve a planilha | A versão anterior deixa de existir no OneDrive | Nome de arquivo idempotente, tradeoff assumido |
| Pontos facultativos não são calculáveis | Fechamento pode rodar em dia de expediente reduzido | E-mail aguarda na caixa, sem prejuízo |
| `data_expiracao` é manual                        | Silencia se não for atualizada na renovação          | Passo 6 da seção 10.7                                             |

---

## 16. Decisões de escopo registradas

| Decisão | Situação |
|---|---|
| Parcelamento | Fora de escopo. `parcela` e `total_parcelas` só são preenchidos quando o documento explicita |
| Colunas Y e Z (Nota Fiscal e Chave da NF-e) | Permanecem vazias. Nenhuma das plataformas emite documento fiscal brasileiro |
| Data e Valor do Pagamento (colunas M e N) | Permanecem vazias por decisão |
| Categoria, Conta Corrente e Forma de Pagamento | Valores fixos, aplicados no `Montar Valores da Planilha` |
| Importação no Omie | Manual. A automação entrega o arquivo pronto, não importa |
