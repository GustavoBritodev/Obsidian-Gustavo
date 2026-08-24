---
tags:
  - tipo/geral
status: rascunho
---

# Guia de Implementação: Automação de Faturas SaaS no N8N

**Ambiente:** n8n self-hosted, versão 2.33.4, em VM própria da Mosten.

Sempre que aparecer um bloco destacado começando com "Isto ainda depende de você", é um ponto que não pode ser preenchido sem uma decisão sua. Nada foi resolvido por suposição.

## Premissas, regras e restrições do desenho

Esta seção reúne o que vale para toda a automação. Se alguma destas premissas mudar, o impacto não fica contido em um passo só.

**Premissas assumidas**

1. As cinco plataformas (AWS, Azure DevOps, Sentry, Cursor, OpenAI) enviam recibo ou fatura por e-mail com o PDF **anexado**, para uma caixa dedicada.
2. Todas as cobranças caem no mesmo cartão corporativo (`Visa Caixa -7346`) e são descontadas na data de emissão, o que permite tratar emissão, registro e pagamento como a mesma data.
3. O volume mensal fica na casa de unidades de lançamentos, não dezenas.
4. As faturas chegam em USD. Qualquer moeda diferente de BRL usa o mesmo caminho de conversão; BRL passa direto.
5. O arquivo final é consumido pelo **importador de contas a pagar do Omie**, não por leitura humana. Layout manda mais que estética.

**Regras permanentes do desenho**

1. **O modelo nunca é editado.** Toda execução produz um arquivo novo a partir dele. Execução com defeito não contamina o mês seguinte.
2. **Nada é inferido.** Campo que não está literalmente no documento vira `null` e entra em `campos_faltantes`. Palpite silencioso na contabilidade é pior que campo vazio sinalizado.
3. **Status muda depois do envio, nunca antes.** Falha no e-mail mantém tudo como `pendente` e o lançamento entra no ciclo seguinte.
4. **Deduplicação por `message_id_graph`**, com `UNIQUE` no banco. O mesmo e-mail reprocessado não gera segundo registro.
5. **Conversão cambial pela PTAX de venda do Banco Central**, com data de referência na emissão e recuo para o último dia útil anterior quando não há publicação.
6. **Todo valor calculado em execução é persistido no banco antes de ser usado.** Nenhum passo pode depender de um dado que só existe em memória num ramo lateral do fluxo.

**Restrições conhecidas**

| Restrição | Efeito prático |
|---|---|
| O importador do Omie lê o range `B6:BJ10005` (declarado na aba `Config`) | Não há limite prático de linhas. O limite de 32 é só de formatação pré-existente |
| Só as linhas 6 a 37 do modelo têm validação de data e formatação | Acima de 32 lançamentos, é preciso aplicar formatação nas linhas novas |
| As linhas de exemplo do modelo vêm com conteúdo em B, E, H, K, M, N, X, Y, AA | Escrita e limpeza precisam neutralizar esse conteúdo, não só ignorá-lo |
| Upload simples do Graph é síncrono só até 4 MB | Acima disso, o caminho de cópia muda (ver alternativa no Passo 5) |
| `POST /copy` do Graph é sempre assíncrono | Não devolve o `id` do arquivo novo. Não usar |
| A PTAX é cotação oficial, o cartão embute spread e IOF | Os dois números não batem. Não é defeito, é conciliação |
| Fatura que chega só como link do Stripe | Fora de escopo. É descartada no filtro da Ingestão |
| Client secret do Entra ID tem validade | Vencido, a automação falha em silêncio. Daí o Workflow 3 |

## Status do projeto

**O Workflow 1 está montado e validado ponta a ponta**, com dois lançamentos de teste, um deles emitido em fim de semana para exercitar o recuo da cotação. Falta apenas o tratamento de erro (Passo 11) e a volta para produção (Passo 14).

| Item | Status |
|---|---|
| Banco de dados (PostgreSQL) | **Pronto.** Credenciais ativas no n8n |
| Credencial Microsoft (Outlook + OneDrive) | **Pronta.** Aplicação registrada e autenticando |
| Armazenamento (pastas do OneDrive) | **Definido: OneDrive.** Estrutura de pastas a montar — ver Etapa 1.3 |
| Mecanismo de escrita da planilha | **Definido.** Workbook API do Microsoft Graph — ver Workflow 1, Passo 6 |

## Como usar este guia

O guia tem duas partes. A **Etapa 1** cobre o que é compartilhado por tudo e só precisa ser feito uma vez: banco, credencial e armazenamento. Depois vêm **três tutoriais independentes**, um para cada workflow do n8n — Fechamento, Ingestão e Monitoramento. Cada tutorial é construído do início ao fim dentro da própria seção, sem pedir para você voltar a outra parte no meio: onde um nó precisa de uma explicação mais longa, ela está ali mesmo, não num apêndice separado.

A ordem recomendada é: Etapa 1 → Workflow 1 (Fechamento) → Workflow 2 (Ingestão) → Workflow 3 (Monitoramento). O Fechamento vem primeiro porque concentra o risco técnico — é onde a planilha do Omie pode ser corrompida se algo sair errado.

---

# ETAPA 1: Infraestrutura compartilhada

## 1.1 Banco de dados — concluído

O banco `automacoes`, o usuário `automacoes_app`, a tabela `faturas_saas` e a credencial `Postgres Automacoes` no n8n já estão criados e testados. Nenhuma ação necessária aqui.

Guarde esta referência para quando precisar consultar as colunas da tabela ou recriar o ambiente:

<details>
<summary>Esquema da tabela <code>faturas_saas</code> (referência)</summary>

```sql
CREATE TABLE faturas_saas (
  id                SERIAL PRIMARY KEY,
  message_id_graph  TEXT UNIQUE NOT NULL,
  plataforma        TEXT,
  fornecedor        TEXT,
  valor             NUMERIC(18,2),
  moeda             TEXT,
  valor_brl         NUMERIC(18,2),
  cotacao_ptax      NUMERIC(10,4),
  data_cotacao      DATE,
  data_emissao      DATE,
  data_vencimento   DATE,
  tipo_documento    TEXT,
  numero_documento  TEXT,
  parcela           INTEGER,
  total_parcelas    INTEGER,
  campos_faltantes  TEXT,
  observacoes       TEXT,
  caminho_arquivo   TEXT,
  payload_parser    JSONB,
  status            TEXT NOT NULL DEFAULT 'pendente',
  data_exportacao   TIMESTAMP,
  criado_em         TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_faturas_status  ON faturas_saas (status);
CREATE INDEX idx_faturas_emissao ON faturas_saas (data_emissao);
```

Três colunas merecem lembrete:

- **`message_id_graph`** guarda o identificador único que a Microsoft dá a cada e-mail. A restrição `UNIQUE` é o que impede a mesma fatura de ser lançada duas vezes.
- **`payload_parser`** guarda a resposta bruta da inteligência artificial em JSON, para reprocessar um lançamento errado sem voltar ao e-mail original.
- **`status`** nasce como `pendente` e vira `exportado` só depois de o e-mail mensal sair com sucesso.

Credencial no n8n: **Postgres Automacoes**, tipo `Postgres`.

</details>

<details>
<summary>Como recriar a tabela via n8n, sem acesso direto à VM (referência)</summary>

A tabela foi criada sem acesso direto à VM, através de um workflow dedicado no próprio n8n. Isso serve como referência caso o ambiente precise ser recriado (nova VM, novo banco, etc.).

Workflow: `Infra - Setup Tabela Faturas (NAO ATIVAR)`

- **Gatilho:** Manual Trigger — nunca Schedule Trigger, para que o DDL só rode quando disparado manualmente
- **Nó Postgres:** Credential `Postgres Automacoes`, Operation `Execute Query`, com o DDL da seção 1.1 acrescido de `IF NOT EXISTS` na tabela e nos dois índices, tornando a execução idempotente e segura contra reexecução acidental
- **Validação:** `SELECT COUNT(*) FROM faturas_saas;` retornando `0` sem erro
- **Estado permanente:** o workflow fica **sempre inativo** (Active desligado) e isolado — nunca reaproveitado dentro do Fechamento, Ingestão ou Monitoramento — para que o DDL não conviva com lógica de produção

Essa abordagem foi escolhida no lugar de rodar o DDL direto na VM (via psql ou cliente SQL) porque não exige acesso à VM, só a credencial já configurada no n8n. O tradeoff aceito: perde-se a separação entre infraestrutura e automação, compensado pelo `IF NOT EXISTS` e pelo workflow permanecer isolado e nunca ativado.

</details>

## 1.2 Fuso horário da instância

> **Isto ainda depende de você.** A instância reporta `America/New_York` no Schedule Trigger. Todo cron do projeto (`0 8 * * *`) dispara no fuso da instância, então o fechamento sai às 09:00 de Brasília no horário atual, e às 10:00 quando Nova York entra no horário de verão. Os nós de data deste guia raciocinam em UTC e não são afetados, mas o `Calcular Dias` do Workflow 3 usa hora local e fica sujeito à mesma defasagem.

Para corrigir na origem, defina nas variáveis de ambiente da VM e reinicie o n8n:

```
GENERIC_TIMEZONE=America/Sao_Paulo
TZ=America/Sao_Paulo
```

Isso vale para todos os workflows de uma vez. Se a VM hospedar outras automações da Mosten, confirme o impacto antes de alterar. Alternativa sem mexer na VM: definir o fuso em `Settings → Timezone` de cada workflow, o que precisa ser repetido em cada workflow novo.

## 1.3 Credencial da Microsoft — concluída

O registro da aplicação `n8n-Mosten-Faturas` no Entra ID está feito, e duas credenciais já existem no n8n:

- **Microsoft Outlook OAuth2 API** — usada para ler e enviar e-mail
- **Microsoft OneDrive OAuth2 API** — usada para arquivos, e também reutilizada nos nós **HTTP Request** que chamam a Workbook API (Workflow 1). Nesses nós, a autenticação é `Predefined Credential Type` → `Microsoft OneDrive OAuth2 API`, porque o token dela já cobre o caminho `/workbook/` do Microsoft Graph.

Nenhuma ação necessária aqui, a menos que a senha precise ser renovada — nesse caso, veja o procedimento no Workflow 3, Passo 8.

<details>
<summary>Se precisar diagnosticar um problema de autenticação (referência)</summary>

| Mensagem | O que significa | O que fazer |
|---|---|---|
| `AADSTS50194` | Aplicação está como tenant único | Alterar para multitenant em Authentication → Manifest, trocando `signInAudience` para `AzureADMultipleOrgs` |
| `Unable to sign without access token` | O Connect nunca foi concluído | Refazer o Connect na credencial |
| `invalid_client` | Secret ID no lugar do Value, ou senha vencida | Conferir o campo copiado em Certificates & secrets |
| Autentica mas nada acontece | Endereço de retorno divergente | Conferir as variáveis `WEBHOOK_URL` / `N8N_EDITOR_BASE_URL` da VM |
| Pede aprovação de administrador | Tenant não permite consentimento de usuário | Chamado para a TI |

</details>

## 1.4 Armazenamento — definido: OneDrive

Dois conjuntos de arquivos precisam de lugar: a planilha modelo (lida todo mês) e os PDFs de recibos e notas fiscais (arquivados). Ficou definido que os dois ficam no **OneDrive da conta de serviço**, usando a credencial já criada na Etapa 1.3.

> **Isto ainda depende de você.** Falta definir quem precisa de permissão de leitura na pasta dos documentos arquivados, e se existe política de retenção a aplicar sobre eles. Não bloqueia o restante da implementação.

**Estrutura de pastas proposta:**

```
/Faturas-SaaS/
  /_template/
      Controle_de_ferramentas_e_assinaturas.xlsx
  /2026/
      /2026-08/
          AWS_INV-12345_2026-08-03.pdf
          Cursor_INV-98765_2026-08-11.pdf
      /2026-09/
```

Os PDFs seguem o padrão `Plataforma_NumeroDocumento_DataEmissao.pdf`. Quando o número do documento não é extraído do PDF, ele é substituído por um identificador derivado do e-mail, garantindo que dois arquivos nunca colidam.

**Passos:**

1. Monte a estrutura acima na pasta escolhida
2. Suba `Controle_de_ferramentas_e_assinaturas.xlsx` para `_template`
3. Deixe `_template` com permissão somente leitura, se o ambiente permitir
4. Anote o **File ID** do modelo — você vai precisar dele no Workflow 1. Para obter: use um nó Microsoft OneDrive temporário (Resource: File, Operation: Search, Query com parte do nome do arquivo) e leia o campo `id` do resultado, ou consulte via Graph Explorer com `GET /me/drive/root:/Faturas-SaaS/_template/Controle de ferramentas e assinaturas.xlsx`

**Regra permanente do desenho:** a automação sempre lê o modelo original e produz um arquivo novo. Ela nunca grava por cima dele — isso garante que uma execução com defeito não contamine o mês seguinte.

---

# WORKFLOW 1: Fechamento

**O que faz:** uma vez por mês, busca no banco tudo que ainda não foi enviado, copia a planilha modelo, escreve os lançamentos nessa cópia através da API do Excel, e manda por e-mail com os PDFs anexados.

**Quando roda:** todo dia 20, ou no último dia útil anterior se cair em fim de semana ou feriado.

**Por que primeiro:** é aqui que a planilha do Omie pode ser corrompida se algo sair errado, então vale validar isto antes de montar os outros dois workflows.

No n8n, crie um workflow novo chamado `Faturas SaaS - Fechamento`.

## Nomes dos nós: leia antes de começar

As expressões `$('Nome do No')` são **sensíveis a maiúsculas, minúsculas e acentos**, e não fazem correspondência aproximada. Um nó chamado `Enviar copia` não é encontrado por `$('Enviar Copia')`, e o erro que aparece (`Referenced node doesn't exist`) só surge em tempo de execução, no nó que consome, não no que foi renomeado.

**Regra deste workflow: nomes sem acento, sem cedilha, com inicial maiúscula em cada palavra.** Estes são os nomes exatos, na ordem do fluxo:

| # | Nó | Tipo | Referenciado | Execute Once |
|---|---|---|---|---|
| 1 | `Schedule Trigger` | Schedule Trigger | | |
| 2 | `E Dia de Fechar?` | Code | | |
| 3 | `Verificar Data` | If | | |
| 4 | `Buscar Pendentes` | Postgres | sim | |
| 5 | `Tem Lancamentos?` | If | | |
| 6 | `Parametros` | Set | **sim** | |
| 7 | `Buscar Cotacoes` | Code | | |
| 8 | `Gravar Conversao` | Postgres | | |
| 9 | `Reler Lancamentos Convertidos` | Postgres | **sim** | **sim** |
| 10 | `Resolver Pasta Mes` | Microsoft OneDrive | **sim** | **sim** |
| 11 | `Baixar Modelo` | Microsoft OneDrive | | **sim** |
| 12 | `Enviar Copia` | Microsoft OneDrive | **sim** | **sim** |
| 13 | `Montar Valores da Planilha` | Code | **sim** | |
| 14 | `Escrever Lancamentos` | HTTP Request | | |
| 15 | `Sobrou Linha de Exemplo?` | If | | |
| 16 | `Limpar Linhas Excedentes` | HTTP Request | | |
| 17 | `Baixar Planilha Final` | Microsoft OneDrive | **sim** | |
| 18 | `Listar Documentos` | Code | | |
| 19 | `Baixar Documentos` | Microsoft OneDrive | **sim** | |
| 20 | `Juntar Anexos` | Code | | |
| 21 | `Montar Envio` | Code | | |
| 22 | `Enviar Fechamento` | HTTP Request | | |
| 23 | `Marcar Exportados` | Postgres | | **sim** |
| 24 | `Conferir Marcacao` | Code | | |

Os marcados como referenciados são os que quebram o fluxo se forem renomeados sem atualizar as expressões. Se você duplicar um nó por acidente, o n8n acrescenta um sufixo numérico (`Buscar PTAX1`), criando um órfão que parece igual ao original no canvas. Vale conferir a lista acima ao final da montagem.

## Três regras de expressão que valem para o workflow inteiro

Praticamente todo erro de montagem deste fluxo caiu em uma destas três. Vale ler antes, não depois.

**1. Nó que roda uma vez só é referenciado com `.first()`, nunca com `.item`.**

`.item` significa "o item do nó referenciado que corresponde ao item que estou processando agora". Essa correspondência só existe quando os dois lados têm a mesma cardinalidade. Como o `Reler Lancamentos Convertidos` produz um item por lançamento e os nós de OneDrive produzem um item só, o n8n não consegue parear e devolve `Multiple matches found`.

Neste workflow, `Parametros`, `Resolver Pasta Mes`, `Enviar Copia` e `Montar Valores da Planilha` sempre produzem um item. Use `.first()` para todos eles, em qualquer campo, de qualquer nó. `.item` só permanece onde o nó de destino processa vários itens e cada um precisa do seu par: `Gravar Conversao` e `Baixar Documentos`.

**2. Não digite `=` no início de um campo de expressão.**

No JSON exportado, um campo em modo expressão aparece como `"value": "=root:{{ ... }}"`. Esse `=` é como o n8n armazena a marcação; ele não é digitado. Digitando, ele vira parte do valor: o arquivo nasce chamado `=Omie_Contas_Pagar_2026-08.xlsx` e o Graph responde `invalidRequest` sem dizer por quê.

**O preview embaixo do campo é a verdade.** Se ele começa com `=`, sobra um sinal. Campos que começam direto com `{{` não correm esse risco; o problema aparece nos que têm texto fixo antes da expressão.

**3. Nó que age sobre o fechamento inteiro precisa de Execute Once.**

Sem isso, `Resolver Pasta Mes`, `Baixar Modelo` e `Enviar Copia` rodam uma vez por lançamento e criam uma cópia da planilha por fatura. Com um lançamento só em teste, o defeito não aparece. A coluna Execute Once da tabela acima indica quais nós precisam do ajuste.

## Passo 1 — Gatilho e verificação de data

- Adicione um **Schedule Trigger**
- Trigger Rules: **Custom (Cron)**
- Expressão: `0 8 * * *`

Cron sozinho não sabe o que é feriado nem sabe antecipar para o dia útil anterior, então um segundo nó decide isso:

- Adicione um nó **Code**, renomeado para `E Dia de Fechar?`

```javascript
// Feriados nacionais com data movel (Carnaval, Sexta-Feira Santa, Corpus Christi)
// nao sao calculaveis por regra simples. Mantenha a lista abaixo atualizada
// uma vez por ano, ou remova-a se a decisao for tratar apenas fins de semana.
const FERIADOS = [
  '2026-01-01', '2026-02-16', '2026-02-17', '2026-04-03', '2026-04-21',
  '2026-05-01', '2026-06-04', '2026-09-07', '2026-10-12', '2026-11-02',
  '2026-11-15', '2026-12-25',
];

function ehDiaUtil(d) {
  const diaSemana = d.getUTCDay();
  if (diaSemana === 0 || diaSemana === 6) return false;
  return !FERIADOS.includes(d.toISOString().slice(0, 10));
}

const hoje = new Date();
const ano = hoje.getUTCFullYear();
const mes = hoje.getUTCMonth();

const DIA_CORTE = 20;   // dia alvo do fechamento

let alvo = new Date(Date.UTC(ano, mes, DIA_CORTE));
while (!ehDiaUtil(alvo)) {
  alvo.setUTCDate(alvo.getUTCDate() - 1);
}

const ehHoje = hoje.toISOString().slice(0, 10) === alvo.toISOString().slice(0, 10);
return [{ json: { ehHoje, dataAlvo: alvo.toISOString().slice(0, 10) } }];
```

> **Nunca escreva o dia com zero à esquerda.** `Date.UTC(ano, mes, 07)` é notação octal legada: funciona por acidente em modo permissivo e lança `SyntaxError` em modo estrito, derrubando o nó inteiro. Use `7`, não `07`. A constante `DIA_CORTE` existe para você alterar o dia num lugar só durante os testes, sem editar a chamada.

> **Cuidado com o fuso.** O código raciocina em UTC e o Schedule Trigger dispara no fuso da instância do n8n. Às 08:00 de São Paulo (11:00 UTC) a data é a mesma nos dois relógios, então funciona. Se algum dia o horário do gatilho for movido para depois das 21:00 local, a data UTC já virou e o fechamento dispara no dia errado. Se mudar o horário, revalide este nó.
- Adicione um nó **If**, renomeado para `Verificar Data`

| Campo | Valor |
|---|---|
| Condition Type | `Boolean` |
| Value 1 | `{{ $json.ehHoje }}` |
| Operation | `is true` |

- Ligue o ramo verdadeiro ao Passo 2

> A lista de feriados exige manutenção anual. Se preferir eliminar essa manutenção, dá para tratar apenas sábado e domingo, ao custo de disparar em algum feriado ocasional.

## Passo 2 — Buscar os lançamentos pendentes

- Adicione um nó **Postgres**, renomeado para `Buscar Pendentes`

| Campo | Valor |
|---|---|
| Credential | `Postgres Automacoes` |
| Operation | `Execute Query` |
| Query | ver abaixo |
| Options → Always Output Data | ativado |

```sql
SELECT
  *,
  TO_CHAR(data_emissao,    'YYYY-MM-DD') AS data_emissao_txt,
  TO_CHAR(data_vencimento, 'YYYY-MM-DD') AS data_vencimento_txt
FROM faturas_saas
WHERE status = 'pendente'
ORDER BY data_emissao, id;
```

> **Por que as duas colunas `_txt`.** O nó Postgres devolve colunas `DATE` como data serializada, não como a string `AAAA-MM-DD` que os passos seguintes esperam. Na prática chega algo como `2026-08-05T00:00:00.000Z`, e o `.split('-')` do `Preparar Cotacao` produz `dataCotacaoApi = "08-05T00:00:00.000Z-2026"`, que o Banco Central rejeita. Pior: a serialização pode deslocar a data em um dia dependendo do fuso da conexão, e um deslocamento de um dia na cotação passa despercebido. Convertendo para texto dentro do próprio SQL, o formato fica garantido na origem. **Todos os passos adiante usam `data_emissao_txt` e `data_vencimento_txt`, nunca as colunas originais.**

> O nome do nó importa: passos mais adiante o referenciam como `$('Buscar Pendentes')`. Se mudar o nome depois, as referências quebram.

> Sem **Always Output Data**, um mês sem lançamentos faz a execução parar sem deixar rastro claro do motivo.

- Adicione um nó **If**, renomeado para `Tem Lancamentos?`

| Campo | Valor |
|---|---|
| Condition Type | `Number` |
| Value 1 | `{{ Object.keys($input.first().json).length }}` |
| Operation | `is greater than` |
| Value 2 | `0` |

> **Não use `{{ $items().length }}` nem `{{ $input.all().length }}` aqui. Este é o erro mais fácil de cometer neste guia inteiro, porque a versão errada não dá erro: ela simplesmente deixa passar.** O `Always Output Data` do `Buscar Pendentes` emite um item vazio (`{}`) quando não há pendências, exatamente para a execução não morrer em silêncio — mas esse item vazio ainda conta como 1 item. Contar itens faz `Tem Lancamentos?` dar sempre verdadeiro, mesmo sem nenhum lançamento real, anulando a proteção. Contar as chaves do primeiro item resolve: um registro real tem várias chaves (`id`, `data_emissao`, etc.); o item vazio do `Always Output Data` tem zero.

- Ramo verdadeiro → Passo 3. Ramo falso → uma notificação de erro (nunca um envio de planilha vazia)

Com cinco assinaturas recorrentes ativas, sempre haverá movimento no período — este nó é uma proteção contra algo ter quebrado na ingestão, não um cenário de negócio esperado.

<details>
<summary>Como inserir um registro de teste, sem esperar a Ingestão rodar (referência)</summary>

Para testar o Fechamento isoladamente, sem depender do Workflow 2 (Ingestão) já estar funcionando, insira um lançamento de teste direto na tabela — pelo mesmo mecanismo descrito na Etapa 1.1 (nó Postgres, Execute Query, credencial `Postgres Automacoes`):

```sql
INSERT INTO faturas_saas
  (message_id_graph, plataforma, fornecedor, valor, moeda,
   data_emissao, data_vencimento, tipo_documento, numero_documento,
   parcela, total_parcelas, status)
VALUES
  ('TESTE-MANUAL-0001', 'Cursor', 'Cursor AI Inc.', 20.00, 'USD',
   '2026-08-05', '2026-08-15', 'Recibo', 'INV-TESTE-0001',
   1, 1, 'pendente');
```

Pontos importantes:

- `message_id_graph` precisa ser único — use um valor claramente identificável como teste, para não colidir com um `message_id_graph` real do Graph API depois.
- `data_emissao` em dia útil evita cair no laço de recuo do `Preparar Cotacao`/`Recuar Um Dia` logo no primeiro teste.
- `valor_brl`, `cotacao_ptax` e `data_cotacao` ficam de fora do INSERT — nascem `NULL` e são o que `Calcular BRL` (Passo 4e) deve preencher, servindo de prova de que o fluxo funcionou ponta a ponta.
- Depois do teste, apague o registro (`DELETE FROM faturas_saas WHERE message_id_graph = 'TESTE-MANUAL-0001';`) ou marque como `exportado`, para não ele não se misturar com dados reais no primeiro Fechamento de verdade.

</details>

## Passo 3 — Parâmetros do fechamento

- Adicione um nó **Set**, renomeado para `Parametros`
- Mode: **Manual Mapping**, todos os campos do tipo String:

| Campo | Valor |
|---|---|
| `email_destino` | `financeiro@mosten.com` |
| `assunto` | `Faturamento e Recibo de Ferramentas de Software` |
| `template_file_id` | o File ID anotado na Etapa 1.4 |
| `pasta_destino_planilha` | `/Faturas-SaaS/{{ $now.format('yyyy') }}/{{ $now.format('yyyy-MM') }}` |

> **Mantenha este campo como caminho puro, sem prefixo.** O Passo 5a (`Resolver Pasta Mes`) já monta o prefixo `root:` na frente deste valor. Se `pasta_destino_planilha` também tiver `/drive/root:` embutido, o resultado fica duplicado (`root:/drive/root:/Faturas-SaaS/...`) e a chamada falha com `invalidRequest`.
| `pasta_documentos` | o caminho raiz onde os PDFs são arquivados (Etapa 1.4) |
| `nome_aba` | `Omie_Contas_Pagar` |
| `competencia` | `{{ $now.format('yyyy-MM') }}` |
| Options → Include Other Input Fields | **ativado** |

> **Todo campo que contém `{{ }}` precisa estar em modo expressão.** No n8n isso corresponde a um `=` no início do valor (visível no JSON exportado como `"value": "={{ ... }}"`). Se o campo ficar em modo texto fixo, o valor não é avaliado e segue literal: `competencia` vira a string `{{ $now.format('yyyy-MM') }}`, e o arquivo do mês nasce chamado `Omie_Contas_Pagar_{{ $now.format('yyyy-MM') }}.xlsx`. Nesta tabela, os campos `pasta_destino_planilha` e `competencia` são expressão; os demais são texto fixo. Confira um a um antes de seguir.

> **Não deixe espaço depois do `=`.** Um valor escrito como `= {{ ... }}` resolve com um espaço na frente. Em campo de texto isso passa despercebido; em campo de ID de pasta ou de arquivo, o Graph devolve `invalidRequest` e o erro não diz qual é o problema.

> Sem **Include Other Input Fields**, o modo Manual Mapping descarta tudo que vem de `Buscar Pendentes` (`data_emissao_txt`, `valor`, `id` de cada fatura) e mantém só os sete campos definidos acima. O resultado aparece só no passo seguinte: `Preparar Cotacao` recebe `data_emissao_txt` como `undefined` e para com o erro de data inválida. Com a opção ativada, os campos globais somam aos campos originais de cada item, em vez de substituí-los.

## Passo 4 — Conversão cambial

As faturas chegam em dólar e o Omie recebe reais. A conversão usa a PTAX de venda do Banco Central, com data de referência na emissão de cada documento.

São três nós em sequência, sem ramificação.

**A consulta ao Banco Central acontece dentro de um único nó Code, não como uma cadeia de nós com laço.** A versão anterior deste guia usava um laço no canvas (`Buscar PTAX` → `Merge` → `Tem Cotacao?` → `Recuar Um Dia` → volta), e ele falha de um jeito silencioso: quando um lançamento entra no recuo e outro não, os nós a jusante disparam na primeira passagem, sem esperar o laço terminar. O resultado é o fechamento seguir com um lançamento ainda sem cotação. Fazendo tudo dentro de um nó, o estado fica local a cada item e não existe pareamento posicional para desalinhar.

**4a — Code, `Buscar Cotacoes`**

Modo `Run Once for All Items`.

```javascript
const MAX_RECUOS = 10;                 // cobre feriados prolongados
const httpRequest = this.helpers.httpRequest;
const cache = {};                      // varias faturas do mesmo dia: uma chamada so

async function cotacaoDe(dataISO) {
  if (cache[dataISO] !== undefined) return cache[dataISO];

  const [a, m, d] = dataISO.split('-');
  const url =
    'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/' +
    `CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='${m}-${d}-${a}'&$format=json`;

  const resp = await httpRequest({ method: 'GET', url, json: true });
  const valor = resp && resp.value && resp.value.length
    ? Number(resp.value[0].cotacaoVenda)   // cotacaoVenda e a referencia usual para despesa
    : null;

  cache[dataISO] = valor;
  return valor;
}

function diaAnterior(dataISO) {
  const dt = new Date(dataISO + 'T00:00:00Z');
  dt.setUTCDate(dt.getUTCDate() - 1);
  return dt.toISOString().slice(0, 10);
}

const saida = [];

for (const item of $input.all()) {
  const j = item.json;
  const base = j.data_emissao_txt;

  if (!base || !/^\d{4}-\d{2}-\d{2}$/.test(base)) {
    throw new Error(
      `Lancamento id=${j.id} sem data de emissao valida (recebido: ${base}). ` +
      `Confira se a query do Buscar Pendentes inclui data_emissao_txt.`
    );
  }

  const moeda = (j.moeda || 'USD').toUpperCase();

  // Lancamento ja em reais nao passa por conversao.
  if (moeda === 'BRL') {
    saida.push({
      json: {
        ...j,
        cotacao_ptax: 1,
        data_cotacao: base,
        valor_brl: Number(Number(j.valor).toFixed(2)),
      },
    });
    continue;
  }

  // Recua ate achar dia com publicacao: fim de semana e feriado nao tem PTAX.
  let dataConsulta = base;
  let taxa = null;
  let recuos = 0;

  while (taxa === null && recuos <= MAX_RECUOS) {
    taxa = await cotacaoDe(dataConsulta);
    if (taxa === null) {
      dataConsulta = diaAnterior(dataConsulta);
      recuos += 1;
    }
  }

  if (taxa === null) {
    throw new Error(
      `Sem cotacao PTAX para o lancamento id=${j.id} (emissao ${base}) ` +
      `apos ${MAX_RECUOS} recuos. Verificar se a API do Banco Central responde.`
    );
  }

  saida.push({
    json: {
      ...j,
      cotacao_ptax: taxa,
      data_cotacao: dataConsulta,
      valor_brl: Number((Number(j.valor) * taxa).toFixed(2)),
    },
  });
}

return saida;
```

> A validação de formato no início não é decorativa. Sem ela, uma data mal serializada não quebra aqui: vira uma URL inválida, o Banco Central devolve array vazio, o recuo roda dez vezes, e o erro que chega até você fala de "cotação não encontrada", apontando para o lugar errado.

> A PTAX é a cotação oficial, mas a fatura do cartão embute spread e IOF. Os dois números não vão bater exatamente. Não é defeito, é conciliação, e vale alinhar com a Controladoria antes do primeiro envio.

**4b — Postgres, `Gravar Conversao`**

Este nó é obrigatório, e o motivo é o defeito mais silencioso que este fluxo já teve: sem ele, `valor_brl` existe apenas na memória deste ramo, enquanto o `Montar Valores da Planilha` (Passo 6) lê os registros de volta do banco. O resultado é uma planilha com a coluna de valor vazia, depois de todo o cálculo ter rodado corretamente.

| Campo | Valor |
|---|---|
| Credential | `Postgres Automacoes` |
| Operation | `Execute Query` |
| Options → Execute Once | **desativado** (roda uma vez por lançamento) |

```sql
UPDATE faturas_saas
   SET valor_brl    = $1,
       cotacao_ptax = $2,
       data_cotacao = $3
 WHERE id = $4;
```

Query Parameters, nesta ordem: `{{ $json.valor_brl }}`, `{{ $json.cotacao_ptax }}`, `{{ $json.data_cotacao }}`, `{{ $json.id }}`.

> Persistir aqui também dá rastreabilidade: se a Controladoria questionar um valor três meses depois, a cotação usada e a data dela estão gravadas na linha, não só no log de execução do n8n, que expira.

**4c — Postgres, `Reler Lancamentos Convertidos`**

Depois do `UPDATE`, releia os registros já completos. É essa saída que os Passos 6, 8 e 10 vão consumir.

| Campo | Valor |
|---|---|
| Credential | `Postgres Automacoes` |
| Operation | `Execute Query` |
| Options → Execute Once | **ativado** (uma leitura só, não uma por item) |

```sql
SELECT
  *,
  TO_CHAR(data_emissao,    'YYYY-MM-DD') AS data_emissao_txt,
  TO_CHAR(data_vencimento, 'YYYY-MM-DD') AS data_vencimento_txt
FROM faturas_saas
WHERE status = 'pendente'
ORDER BY data_emissao, id;
```

> É a mesma consulta do Passo 2, de propósito. A diferença é o momento: aqui os registros já têm `valor_brl` preenchido.

## Passo 5 — Copiar o modelo

A planilha nunca é editada diretamente — sempre uma cópia nova, conforme a regra da Etapa 1.4.

**5a — Microsoft OneDrive, `Resolver Pasta Mes`**

O campo `Parent Reference → Path` do Copy costuma devolver erro genérico (`invalidRequest`, 400) mesmo com o caminho aparentemente correto — é uma instabilidade conhecida dessa chamada específica da API do Graph. É mais confiável resolver o **ID real da pasta** antes, usando a mesma sintaxe de endereçamento por caminho já usada na Etapa 1.4 para achar o `File ID` do modelo.

- Adicione um nó **Microsoft OneDrive**, renomeado para `Resolver Pasta Mes`

| Campo | Valor |
|---|---|
| Credential | Microsoft OneDrive OAuth2 API |
| Resource | `File` |
| Operation | `Get` |
| File ID | `root:{{ $('Parametros').item.json.pasta_destino_planilha }}` |

Isso monta algo como `root:/Faturas-SaaS/2026/2026-08` — sintaxe que o Graph reconhece como endereçamento por caminho, devolvendo os metadados da pasta, incluindo o `id` real dela.

> **Pré-requisito:** a pasta do mês (`/Faturas-SaaS/{ano}/{ano-mes}`) precisa já existir no OneDrive antes desta chamada — o Graph não cria pastas intermediárias automaticamente. A Etapa 1.4 pede para montar a estrutura manualmente; como o padrão é mensal, é preciso lembrar de criar a subpasta do mês seguinte com antecedência, ou este passo falha com o mesmo tipo de erro genérico.

**A cópia é feita por download e reupload, nunca pela operação Copy do OneDrive.** O `POST .../copy` do Graph é sempre assíncrono: devolve `202 Accepted` e não informa o `id` do arquivo novo, o que exigiria um laço de verificação de status. O upload simples é síncrono para arquivos até 4 MB e devolve o `id` direto na resposta. O modelo tem cerca de 25 KB, bem dentro do limite.

**5b — Microsoft OneDrive, `Baixar Modelo`**

| Campo | Valor |
|---|---|
| Credential | Microsoft OneDrive OAuth2 API |
| Resource | `File` |
| Operation | `Download` |
| File ID | `{{ $('Parametros').item.json.template_file_id }}` |

- Nas opções, renomeie a propriedade binária de saída para `modelo`

**5c — Microsoft OneDrive, `Enviar Copia`**

| Campo | Valor |
|---|---|
| Credential | Microsoft OneDrive OAuth2 API |
| Resource | `File` |
| Operation | `Upload` |
| File Name | `Omie_Contas_Pagar_{{ $('Parametros').item.json.competencia }}.xlsx` |
| Parent Reference → ID (ou campo equivalente de pasta de destino) | `{{ $('Resolver Pasta Mes').item.json.id }}` |
| Binary Data | ativado, propriedade `modelo` |

> **Nomes de campo podem variar por versão do nó**, como já visto nos outros passos com o OneDrive — confira se aparecem como campos diretos ou agrupados em Additional Fields/Parent Reference, e ajuste conforme a tela real. Teste o step: a saída deve trazer o `id` do arquivo novo direto, sem necessidade de laço de verificação.

A saída traz um `id` novo — é esse `id`, não mais o do modelo, que os próximos passos usam.

> **Se algum dia o modelo passar de 4 MB**, o upload simples deixa de servir e passa a exigir upload em sessões. Nesse cenário, a alternativa é voltar ao `POST .../copy` com laço de verificação sobre a URL do cabeçalho `Location`, atualizando as referências de `id` dos Passos 6 e 7.

## Passo 6 — Escrever os lançamentos na planilha

**A escrita é feita pela Workbook API do Microsoft Graph, nunca manipulando o arquivo.** A planilha do Omie carrega validações de data, uma aba `Config` com o intervalo de importação e uma imagem incorporada. Editar o `.xlsx` como ZIP (descompactando e reescrevendo o XML) corrompe o arquivo. A Workbook API é o mesmo mecanismo que o Excel Online usa: quem garante a integridade é o serviço da Microsoft, não o n8n, e nada precisa ser instalado na VM.

A API só escreve o intervalo de células indicado, então tudo que já está formatado fora dele — validações, aba `Config`, imagem — permanece intocado.

**6a — Code, `Montar Valores da Planilha`**

**Três regras que este código precisa respeitar, e o motivo de cada uma:**

1. **A origem dos dados é `Reler Lancamentos Convertidos`, nunca `Buscar Pendentes`.** O `Buscar Pendentes` traz a foto anterior à conversão cambial, com `valor_brl` em `NULL`. Ler de lá produz planilha com a coluna de valor vazia.
2. **Célula que deve ficar vazia recebe `""`, não `null`.** Na Workbook API, `null` significa "não altere esta célula", e as linhas de exemplo do modelo **têm conteúdo** nas colunas que o fluxo não preenche. Enviar `null` preserva esse conteúdo: toda linha sairia com Data do Pagamento 15/06/2026, e a primeira ainda herdaria Projeto `MOSTEN-26` e Valor do Pagamento `0,01`. Enviar `""` limpa de verdade.
3. **A escrita começa na coluna B, não na C.** A coluna B (`Código de Integração`) vem com `0` em todas as linhas do modelo e está dentro do range de importação do Omie. Deixá-la de fora significa mandar 32 linhas com código de integração repetido.

```javascript
// ===== Monta os valores para escrita via Workbook API =====
const LINHA_INICIAL = 6;
const ULTIMA_LINHA_EXEMPLO = 37;   // linhas de exemplo pre-formatadas no modelo
const COLUNAS = [
  'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',
  'S','T','U','V','W','X','Y','Z','AA',
];

function paraSerial(dataISO) {
  if (!dataISO) return null;
  const ms = Date.UTC(
    Number(dataISO.slice(0, 4)),
    Number(dataISO.slice(5, 7)) - 1,
    Number(dataISO.slice(8, 10))
  );
  return Math.floor((ms - Date.UTC(1899, 11, 30)) / 86400000);
}

// Converte um registro do banco nas colunas da planilha do Omie.
// Coluna ausente deste mapa recebe string vazia, limpando o conteudo
// de exemplo que o modelo traz nas linhas 6 a 37.
function paraColunas(r) {
  if (r.valor_brl === null || r.valor_brl === undefined) {
    throw new Error(
      `Lancamento id=${r.id} sem valor_brl. A conversao cambial nao foi gravada. ` +
      `Confira o no Gravar Conversao (Passo 4f).`
    );
  }

  return {
    B:  '',                            // Codigo de Integracao: o modelo traz 0, limpamos
    C:  r.fornecedor,
    D:  'Software e Aplicativos',
    E:  'Visa Caixa -7346',
    F:  Number(r.valor_brl),
    I:  paraSerial(r.data_emissao_txt),
    J:  paraSerial(r.data_emissao_txt),   // Data de Registro e igual a Data de Emissao
    K:  paraSerial(r.data_vencimento_txt),
    S:  r.observacoes,
    T:  r.tipo_documento,
    U:  r.numero_documento,
    V:  r.parcela,
    W:  r.total_parcelas,
    AA: 'Cartão de crédito',
    // M/N (Data e Valor do Pagamento): em branco por decisao. O modelo traz
    // 15/06/2026 em M e 0,01 em N nas linhas de exemplo, entao precisam ser
    // limpas explicitamente pelo '' do preenchimento padrao abaixo.
    // Y/Z (Nota Fiscal e Chave da NF-e): aguardando definicao (ver pendencias).
  };
}

function paraLinha(r) {
  const colunas = paraColunas(r);
  // '' limpa a celula; null NAO limpa, apenas preserva o que ja esta la.
  return COLUNAS.map((c) => {
    const v = c in colunas ? colunas[c] : '';
    return v === null || v === undefined ? '' : v;
  });
}

const registros = $('Reler Lancamentos Convertidos').all().map((i) => i.json);
if (!registros.length) throw new Error('Nenhum lancamento a escrever');

const CAPACIDADE = ULTIMA_LINHA_EXEMPLO - LINHA_INICIAL + 1;
if (registros.length > CAPACIDADE) {
  throw new Error(
    `Fechamento com ${registros.length} lancamentos excede as ${CAPACIDADE} ` +
    `linhas pre-formatadas do modelo. Ver limitacao no final deste passo.`
  );
}

const valores = registros.map(paraLinha);
const linhaFinal = LINHA_INICIAL + valores.length - 1;

const enderecoEscrita = `B${LINHA_INICIAL}:AA${linhaFinal}`;
const enderecoLimpeza = linhaFinal < ULTIMA_LINHA_EXEMPLO
  ? `B${linhaFinal + 1}:AA${ULTIMA_LINHA_EXEMPLO}`
  : null;

return [{
  json: { valores, enderecoEscrita, enderecoLimpeza, linhas: valores.length },
}];
```

**6b — HTTP Request, `Escrever Lancamentos`**

| Campo | Valor |
|---|---|
| Method | `PATCH` |
| URL | `https://graph.microsoft.com/v1.0/me/drive/items/{{ $('Enviar Copia').item.json.id }}/workbook/worksheets('{{ $('Parametros').item.json.nome_aba }}')/range(address='{{ $json.enderecoEscrita }}')` |
| Authentication | `Predefined Credential Type` |
| Credential Type | `Microsoft OneDrive OAuth2 API` |
| Send Body | ativado |
| Body Content Type | `JSON` |
| Specify Body | `Using JSON` |
| JSON | `{{ JSON.stringify({ values: $json.valores }) }}` |

> **Use o parâmetro, não o literal.** O nome da aba já está definido em `Parametros.nome_aba`. Deixar `'Omie_Contas_Pagar'` escrito na URL cria um parâmetro que existe e ninguém lê, e é exatamente o tipo de coisa que engana na próxima manutenção: alguém muda o parâmetro, testa, e nada acontece.

> Confirme que o valor de `nome_aba` bate exatamente com o nome da aba na planilha, incluindo maiúsculas e acentos.

> **Comportamento confirmado em execução.** Na Workbook API, string vazia apaga o conteúdo da célula e `null` preserva o que já está lá. É por isso que o `paraLinha` normaliza tudo para `''`. Trocar por `null` faz as linhas escritas herdarem a Data do Pagamento e o Projeto das linhas de exemplo do modelo.

**6c — Limpar linhas de exemplo que sobrarem**

O modelo tem 32 linhas de exemplo pré-formatadas (6 a 37). O fechamento normalmente não usa todas, e o que sobra precisa ser limpo. Concretamente, cada linha não utilizada carrega `Código de Integração = 0`, `Conta Corrente = Visa Caixa -7346`, `Data de Vencimento = 15/06/2026`, `Data do Pagamento = 15/06/2026` e `Forma de Pagamento = Cartão de crédito`, tudo dentro do range que o Omie importa, e nenhum fornecedor. É linha inválida com aparência de linha preenchida.

- Adicione um nó **If**, renomeado para `Sobrou Linha de Exemplo?`

| Campo | Valor |
|---|---|
| Condition Type | `String` |
| Value 1 | `{{ $('Montar Valores da Planilha').item.json.enderecoLimpeza }}` |
| Operation | `is not empty` |

> **Não use `$json` aqui.** Este nó recebe a saída do `Escrever Lancamentos`, que é um HTTP Request: ele substitui o item pela resposta da API do Graph, e `enderecoLimpeza` não existe mais em `$json`. A referência precisa apontar diretamente para o nó que produziu o valor.

- Ramo verdadeiro → nó **HTTP Request**, renomeado para `Limpar Linhas Excedentes`:

| Campo | Valor |
|---|---|
| Method | `POST` |
| URL | `https://graph.microsoft.com/v1.0/me/drive/items/{{ $('Enviar Copia').item.json.id }}/workbook/worksheets('{{ $('Parametros').item.json.nome_aba }}')/range(address='{{ $('Montar Valores da Planilha').item.json.enderecoLimpeza }}')/clear` |
| Authentication | `Predefined Credential Type` |
| Credential Type | `Microsoft OneDrive OAuth2 API` |
| Send Body | ativado |
| Body Content Type | `JSON` |
| Specify Body | `Using JSON` |
| JSON | `{"applyTo": "Contents"}` |

- Ramo falso → segue direto para o Passo 7 (nada a limpar)

> **Ligue os dois ramos ao Passo 7.** Se só o ramo verdadeiro seguir, um fechamento que use exatamente as 32 linhas nunca chega ao envio, e a execução termina sem erro e sem e-mail.

> **Limitação a observar, agora com o tamanho certo.** A aba `Config` do modelo declara o range de importação como `B6:BJ10005`, ou seja, **o Omie lê até a linha 10005**. O limite de 32 não é de aceite do arquivo, é só de formatação e validação de data pré-existentes, que só existem nas linhas 6 a 37. Passando de 32 lançamentos, o arquivo continua importável; o que se perde é a formatação de data das linhas novas, e o Omie pode recusar uma data escrita como número de série sem formato de data. A solução, quando chegar a hora, é aplicar `numberFormat` (`dd/mm/yyyy`) nas colunas I, J, K, L, M e R das linhas excedentes via Workbook API, ou copiar a formatação para baixo com `range/copyFrom`. Com cinco assinaturas o volume está bem abaixo disso, mas o `throw` do `Montar Valores` avisa antes de gerar arquivo silenciosamente torto.

## Passo 7 — Baixar a planilha final para anexar

A escrita aconteceu direto no OneDrive, então o arquivo precisa voltar para o n8n como binário para ser anexado no e-mail.

- Adicione um nó **Microsoft OneDrive**, renomeado para `Baixar Planilha Final`

| Campo | Valor |
|---|---|
| Credential | Microsoft OneDrive OAuth2 API |
| Resource | `File` |
| Operation | `Download` |
| File ID | `{{ $('Enviar Copia').item.json.id }}` |
| Options → Put Output File in Field | `planilha` |

> **Baixe pelo `id`, não pelo caminho.** O `id` devolvido pelo `Enviar Copia` é a única referência garantida ao arquivo do mês. Montar o caminho por texto reintroduz a dependência de a pasta existir com o nome exato.

> **Este nó precisa rodar depois da limpeza, não em paralelo.** Se ele executar antes do `Limpar Linhas Excedentes`, o binário baixado ainda contém as linhas residuais, e o e-mail sai com o arquivo errado enquanto a planilha no OneDrive fica correta. É um erro difícil de enxergar, porque conferir o arquivo no OneDrive não revela o problema.

## Passo 8 — Buscar os documentos do período

Os recibos e notas fiscais arquivados pela Ingestão vão anexados no mesmo e-mail, para que o financeiro tenha o comprovante ao lado do lançamento.

**8a — Code, `Listar Documentos`**

Monta um item por documento a baixar, filtrando registros sem arquivo arquivado.

```javascript
const registros = $('Reler Lancamentos Convertidos').all().map((i) => i.json);

const comArquivo = registros.filter((r) => r.caminho_arquivo);
const semArquivo = registros.filter((r) => !r.caminho_arquivo);

// Registro sem PDF arquivado nao impede o fechamento, mas precisa ser visivel
// no corpo do e-mail para que o financeiro saiba que falta comprovante.
return [
  ...comArquivo.map((r) => ({
    json: {
      id: r.id,
      caminho_arquivo: r.caminho_arquivo,
      fornecedor: r.fornecedor,
      numero_documento: r.numero_documento,
    },
  })),
  ...(semArquivo.length
    ? [{ json: { _resumoSemArquivo: semArquivo.map((r) => r.id) } }]
    : []),
];
```

**8b — Microsoft OneDrive, `Baixar Documentos`**

| Campo | Valor |
|---|---|
| Credential | Microsoft OneDrive OAuth2 API |
| Resource | `File` |
| Operation | `Download` |
| File ID | `{{ $json.caminho_arquivo }}` |
| Options → Put Output File in Field | `documento` |
| Settings → Always Output Data | ativado |
| Settings → On Error | `Continue (using error output)` |

> **Um PDF ausente não pode derrubar o fechamento.** Se um `caminho_arquivo` apontar para um arquivo movido ou apagado, o `Continue` mantém o fluxo vivo e o e-mail sai com os demais anexos. O oposto (falhar tudo) transformaria um problema de arquivamento em um mês sem fechamento.

**8c — Code, `Juntar Anexos`**

O nó de e-mail precisa de todos os binários em um único item, com nomes de propriedade distintos.

```javascript
const anexos = {};

// A planilha e sempre o primeiro anexo.
const planilha = $('Baixar Planilha Final').first();
anexos.planilha = planilha.binary.planilha;

// Cada documento recebe uma propriedade propria: documento_1, documento_2...
let n = 0;
for (const item of $('Baixar Documentos').all()) {
  if (item.binary && item.binary.documento) {
    n += 1;
    anexos[`documento_${n}`] = item.binary.documento;
  }
}

return [{
  json: { totalAnexos: n + 1, totalDocumentos: n },
  binary: anexos,
}];
```

> **Não crie propriedades vazias de reserva.** O envio do Passo 9 é dinâmico e monta um anexo para cada propriedade que encontrar. Qualquer placeholder criado aqui vira um arquivo de verdade no e-mail do financeiro. A guarda de tamanho fica no `Montar Envio`, não aqui.

## Passo 9 — Enviar o e-mail

O envio é feito por chamada direta ao Graph, não pelo nó Microsoft Outlook. O motivo é o campo de anexos: o nó só aceita uma propriedade binária fixa por bloco de Attachment, e o número de documentos varia a cada mês. Passar `{{ Object.keys($binary).join(',') }}` não funciona, o nó procura uma propriedade chamada literalmente `planilha,documento_1,documento_2`. A alternativa de criar dez blocos fixos com placeholders vazios funciona, mas manda arquivos `vazio_N.txt` junto no e-mail.

**9a — Code, `Montar Envio`**

Modo `Run Once for All Items`.

```javascript
// ===== Monta o corpo da chamada POST /me/sendMail =====
const LIMITE_TOTAL_MB = 3;   // o Graph rejeita mensagens acima de ~4 MB

const item = $input.first();
const propriedades = Object.keys(item.binary || {});

if (!propriedades.length) {
  throw new Error('Nenhum anexo recebido do Juntar Anexos.');
}

const anexos = [];
let bytesTotais = 0;

for (const prop of propriedades) {
  // getBinaryDataBuffer funciona tanto com binario em memoria quanto em disco.
  const buffer = await this.helpers.getBinaryDataBuffer(0, prop);
  const meta = item.binary[prop];

  bytesTotais += buffer.length;

  anexos.push({
    '@odata.type': '#microsoft.graph.fileAttachment',
    name: meta.fileName || `${prop}.bin`,
    contentType: meta.mimeType || 'application/octet-stream',
    contentBytes: buffer.toString('base64'),
  });
}

if (bytesTotais > LIMITE_TOTAL_MB * 1024 * 1024) {
  throw new Error(
    `Anexos somam ${(bytesTotais / 1024 / 1024).toFixed(2)} MB e excedem o ` +
    `limite de ${LIMITE_TOTAL_MB} MB do envio via Graph. Enviar apenas a ` +
    `planilha e substituir os PDFs por link da pasta do mes.`
  );
}

const p = $('Parametros').first().json;
const lancamentos = $('Reler Lancamentos Convertidos').all().length;
const totalDocumentos = item.json.totalDocumentos;

const corpo = [
  'Segue a planilha de importação de contas a pagar referente às faturas de',
  'ferramentas de software do período, acompanhada dos recibos e notas fiscais.',
  '',
  `Competência: ${p.competencia}`,
  `Lançamentos: ${lancamentos}`,
  `Documentos anexados: ${totalDocumentos}`,
  `Gerado em: ${new Date().toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' })}`,
  '',
  'Valores convertidos para BRL pela cotação PTAX de venda do Banco Central, com',
  'referência na data de emissão de cada documento. A cotação utilizada está',
  'registrada na base, por lançamento.',
  '',
  'Registros com campos não extraídos automaticamente estão sinalizados na coluna',
  'Observações e requerem conferência antes da importação no Omie.',
].join('\n');

return [{
  json: {
    message: {
      subject: `${p.assunto} - ${p.competencia}`,
      body: { contentType: 'Text', content: corpo },
      toRecipients: [{ emailAddress: { address: p.email_destino } }],
      attachments: anexos,
    },
    saveToSentItems: true,
  },
}];
```

Três decisões embutidas neste código:

- **`getBinaryDataBuffer`** em vez de ler `.data` direto. Se a instância estiver com armazenamento de binário em disco, `.data` vem vazio e o anexo sai corrompido sem erro. O helper funciona nos dois modos.
- **O nome do arquivo vem do metadado**, então os PDFs mantêm o nome original em vez de `documento_1.pdf`.
- **Guarda de tamanho** antes de montar a requisição, porque a mensagem de erro do Graph para mensagem grande demais não é clara.

**9b — HTTP Request, `Enviar Fechamento`**

| Campo | Valor |
|---|---|
| Method | `POST` |
| URL | `https://graph.microsoft.com/v1.0/me/sendMail` |
| Authentication | `Predefined Credential Type` |
| Credential Type | `Microsoft Outlook OAuth2 API` |
| Send Body | ativado |
| Body Content Type | `JSON` |
| Specify Body | `Using JSON` |
| JSON | `{{ JSON.stringify($json) }}` |

A URL é texto fixo, sem expressão. O campo JSON precisa estar em modo expressão.

> A credencial precisa ter escopo `Mail.Send`. Se der `403`, é aí que está.

> **O `sendMail` responde `202 Accepted` com corpo vazio.** No canvas isso aparece como "node executed, but no items were sent on this branch". É sucesso, não erro. O nó seguinte não depende de nada da resposta, mas também não há confirmação automática de entrega: nos primeiros ciclos, confira a caixa de entrada.

## Passo 10 — Marcar como enviados

**10a — Postgres, `Marcar Exportados`**

| Campo | Valor |
|---|---|
| Credential | `Postgres Automacoes` |
| Operation | `Execute Query` |
| Options → Execute Once | ativado |

```sql
UPDATE faturas_saas
   SET status = 'exportado',
       data_exportacao = now()
 WHERE id = ANY(string_to_array($1, '|')::int[])
   AND status = 'pendente';
```

Query Parameters:

```
{{ $('Reler Lancamentos Convertidos').all().map(i => i.json.id).join('|') }}
```

> **O separador é a barra vertical, nunca a vírgula.** O campo Query Parameters do nó Postgres trata vírgula como separador entre parâmetros distintos. Passando `2,3`, o n8n entende `$1 = 2` e `$2 = 3`; como a query só usa `$1`, apenas o primeiro lançamento é marcado. O sintoma é traiçoeiro: o fechamento funciona, o e-mail sai completo, e no dia seguinte uma execução manual reenvia os lançamentos que ficaram para trás. Pelo mesmo motivo, não use `JSON.stringify` aqui: além da vírgula, os colchetes produzem `malformed array literal` no Postgres.

**A posição deste nó é deliberada: depois do envio, nunca antes.** Se o e-mail falhar, os registros continuam pendentes e entram no ciclo seguinte, em vez de sumirem sem terem sido enviados.

> **Marque exatamente o que foi enviado.** A lista de `id` vem do `Reler Lancamentos Convertidos`, o mesmo conjunto que alimentou a planilha. Reconsultar a tabela por `status = 'pendente'` neste ponto marcaria também qualquer lançamento que a Ingestão tenha gravado durante a execução do fechamento, e que não está no arquivo enviado.

> O `AND status = 'pendente'` é uma trava: reexecutando o fluxo sobre registros já marcados, a `data_exportacao` original é preservada.

**10b — Code, `Conferir Marcacao`**

Marcação incompleta é silenciosa e só aparece como lançamento duplicado no ciclo seguinte. Este nó transforma isso em erro visível.

```javascript
const esperado = $('Reler Lancamentos Convertidos').all().length;
const marcados = $input.first().json.affectedRows ?? null;

if (marcados !== null && marcados !== esperado) {
  throw new Error(
    `Fechamento enviado com ${esperado} lancamentos, mas apenas ${marcados} ` +
    `foram marcados como exportados. Os nao marcados serao reenviados no ` +
    `proximo ciclo. Verificar o no Marcar Exportados.`
  );
}

return $input.all();
```

O e-mail já saiu neste ponto, então o erro não desfaz nada. O que ele faz é disparar o Error Workflow para que alguém corrija antes do fechamento seguinte.

## Passo 11 — Tratamento de erro

O fechamento é mensal. Uma falha que não avise ninguém pode passar semanas despercebida, e quando for descoberta o mês já virou.

**11a — Workflow de notificação**

Crie um workflow novo chamado `Infra - Notificar Erro`, com dois nós:

- **Error Trigger**
- **Microsoft Outlook**, Operation `Send`, para os mesmos três destinatários do Workflow 3

Assunto: `[FALHA] {{ $json.workflow.name }}`

Corpo:

```
O workflow {{ $json.workflow.name }} falhou.

Nó: {{ $json.execution.lastNodeExecuted }}
Erro: {{ $json.execution.error.message }}
Horário: {{ $json.execution.startedAt }}

Execução: {{ $json.execution.url }}
```

**11b — Apontar o Error Workflow**

- Em **Settings** do `Faturas SaaS - Fechamento`, selecione `Infra - Notificar Erro` no campo **Error Workflow**
- Repita nos workflows de Ingestão e Monitoramento

> **Teste antes de confiar.** Force um erro (aponte o `template_file_id` para um ID inexistente e execute) e confirme que o e-mail chega. Error Workflow configurado e nunca testado é o mesmo que não ter.

**11c — Retentativa nos nós de rede**

Nos nós que dependem de serviço externo, ative **Retry on Fail** com 3 tentativas e 5 segundos de espera: `Buscar PTAX`, `Resolver Pasta Mes`, `Baixar Modelo`, `Enviar Copia`, `Escrever Lancamentos`, `Limpar Linhas Excedentes`, `Baixar Planilha Final`, `Enviar Fechamento`.

Falha de rede momentânea não deve custar um ciclo mensal inteiro.

## Passo 12 — Testar com dados fictícios

```sql
INSERT INTO faturas_saas
  (message_id_graph, plataforma, fornecedor, valor, moeda, data_emissao,
   data_vencimento, tipo_documento, numero_documento, observacoes, status)
VALUES
  ('teste-001', 'AWS', 'Amazon Web Services, Inc.', 128.44, 'USD',
   '2026-07-03', '2026-08-15', 'Recibo', 'INV-2026-0731',
   'AWS | Moeda original: USD', 'pendente'),
  ('teste-002', 'Cursor', 'Anysphere & Co', 20.00, 'USD',
   '2026-07-11', '2026-08-15', 'Recibo', 'INV-998',
   'Cursor | Moeda original: USD', 'pendente');
```

> O segundo registro tem um `&` no nome do fornecedor de propósito — é o caractere que mais frequentemente causa problema em escrita malfeita. Confira que ele chega intacto na célula.

- Desconecte temporariamente o Schedule Trigger, coloque um **Manual Trigger** no lugar, e execute
- Baixe a planilha gerada e confira:

| O que verificar | Critério |
|---|---|
| A aba escrita é a `Omie_Contas_Pagar` | Nome conferido no arquivo |
| O arquivo abre no Excel | Sem aviso de reparo |
| **Coluna F (Valor da Conta)** | Preenchida em todas as linhas, em reais, nenhuma vazia e nenhuma com `0,01` |
| **Coluna M (Data do Pagamento)** | Vazia em todas as linhas |
| **Coluna N (Valor do Pagamento)** | Vazia em todas as linhas |
| **Coluna H (Projeto) na primeira linha** | Vazia |
| **Coluna B (Código de Integração)** | Vazia em todas as linhas, inclusive nas residuais |
| **Nome do arquivo** | `Omie_Contas_Pagar_2026-08.xlsx`, com a competência resolvida, não com `{{ }}` literal |
| Validações de data (colunas I, J, K, L, M, R) | Presentes ao clicar na célula |
| Aba `Config` | Preservada, intervalo íntegro |
| Imagem incorporada | Visível |
| Datas | Formatadas como data, alinhadas à direita |
| Linhas de exemplo residuais | Nenhuma com conta corrente preenchida e fornecedor vazio |
| Fornecedor com `&` | Aparece correto na célula |
| Importação de homologação no Omie | Aceita sem erro de layout |

As últimas quatro linhas são o critério de aceite real — até a importação de homologação passar, tudo antes disso é hipótese confirmada por inspeção, não pelo sistema que de fato consome o arquivo.

## Passo 13 — Teste da segunda execução

Antes de considerar o workflow pronto, execute **duas vezes seguidas** com os mesmos registros de teste.

| Execução | Esperado |
|---|---|
| 1 | E-mail com a planilha e os documentos, lançamentos marcados como `exportado` |
| 2 | Ramo falso do `Tem Lancamentos?`, sem e-mail de fechamento e sem planilha nova |

Se a segunda execução gerar e-mail, algum lançamento não foi marcado, e a causa quase certa é o separador do `Marcar Exportados` (Passo 10a).

```sql
SELECT count(*) FROM faturas_saas WHERE status = 'pendente';
```

Deve retornar `0` depois da primeira execução.

## Passo 14 — Devolver o workflow à configuração de produção

Antes de ativar, desfaça tudo que foi ajustado para teste. Cada item desta lista já causou confusão em algum ciclo:

| Item | Valor de teste | Valor de produção |
|---|---|---|
| `DIA_CORTE` no `E Dia de Fechar?` | dia usado no teste | `20` |
| `email_destino` no `Parametros` | endereço pessoal | `financeiro@mosten.com` |
| Gatilho | Manual Trigger | Schedule Trigger reconectado |
| Registros de teste no banco | presentes | apagados ou marcados como `exportado` |
| Arquivos de teste no OneDrive | presentes | apagados da pasta do mês |
| Nó de notificação do ramo falso | assunto de teste | mensagem real |

```sql
DELETE FROM faturas_saas WHERE message_id_graph LIKE 'teste-%'
                            OR message_id_graph LIKE 'TESTE-%';
```

Depois disso, clique em **Active** no canto superior direito.

> **Ative só depois de a importação de homologação no Omie passar.** Tudo antes disso é hipótese confirmada por inspeção, não pelo sistema que de fato consome o arquivo.

---

# WORKFLOW 2: Ingestão

**O que faz:** a cada e-mail recebido em `faturas@mosten.com`, lê o PDF anexo, extrai os dados, arquiva o documento e grava o lançamento no banco como `pendente`.

**Quando roda:** continuamente, a cada 5 minutos, verificando novos e-mails.

No n8n, crie um workflow novo chamado `Faturas SaaS - Ingestao`.

## Passo 1 — Gatilho

- Adicione um **Microsoft Outlook Trigger**

| Campo | Valor |
|---|---|
| Credential | Microsoft Outlook OAuth2 API |
| Poll Times | `Every 5 Minutes` |
| Resource | `Message` |
| Event | `Message Received` |
| Folder | Inbox de `faturas@mosten.com` |
| Download Attachments | ativado |
| Output Binary Field Prefix | `attachment_` |

## Passo 2 — Filtrar o que não interessa

Descarta e-mails sem PDF antes de gastar chamada de inteligência artificial.

- Adicione um nó **Filter**, renomeado para `Tem PDF`, com duas condições obrigatórias:

| Tipo | Condição |
|---|---|
| Boolean | `{{ $json.hasAttachments }}` é verdadeiro |
| Boolean | `{{ Object.values($binary \|\| {}).some(b => b.mimeType === 'application/pdf') }}` é verdadeiro |

> **Isto ainda depende de você.** O filtro hoje só verifica se há PDF anexo, o que é largo demais. Preciso do endereço remetente de AWS, Azure DevOps, Sentry e OpenAI — só o Cursor está identificado (`receipts@stripe.com` ou `billing@cursor.com`). Encaminhar um e-mail real de cada plataforma resolve; quando a lista existir, entra aqui uma condição sobre `{{ $json.from.emailAddress.address }}`.

> **Cenário deixado de fora de propósito.** Sentry e Cursor às vezes enviam só um link do Stripe em vez do PDF anexo — esses e-mails são descartados por este filtro. Quando entrar em escopo, vai exigir seguir o link e baixar o documento hospedado.

## Passo 3 — Evitar duplicidade

- Adicione um nó **Postgres**, renomeado para `Checar Duplicidade`

| Campo | Valor |
|---|---|
| Credential | `Postgres Automacoes` |
| Operation | `Execute Query` |
| Query | `SELECT id FROM faturas_saas WHERE message_id_graph = $1;` |
| Query Parameters | `{{ $json.id }}` |
| Options → Always Output Data | ativado |

- Adicione um nó **If**, renomeado para `Ja Processado?`

| Campo | Valor |
|---|---|
| Condition Type | `String` |
| Value 1 | `{{ $json.id }}` |
| Operation | `is empty` |

- Ramo verdadeiro (nada encontrado no banco) segue o fluxo

## Passo 4 — Extrair o texto do PDF

- Adicione um nó **Extract from File**

| Campo | Valor |
|---|---|
| Operation | `Extract From PDF` |
| Input Binary Field | o binário do anexo (prefixo `attachment_`, do Passo 1) |
| Destination Output Field | `pdf_texto` |

> Se algum PDF vier como imagem escaneada, sem camada de texto, este nó devolve vazio. Se isso acontecer com alguma plataforma, a alternativa é enviar o PDF direto a um modelo com leitura de imagem.

## Passo 5 — Extrair os dados com IA

- Adicione um **Information Extractor** (ou **Basic LLM Chain** + Structured Output Parser)
- Conecte o modelo de sua escolha
- Text: `{{ $json.pdf_texto }}`
- Estrutura de saída:

```json
{
  "type": "object",
  "properties": {
    "plataforma":        { "type": ["string","null"], "enum": ["Azure DevOps","AWS","Sentry","Cursor","OpenAI",null] },
    "fornecedor":        { "type": ["string","null"] },
    "tipo_documento":    { "type": ["string","null"], "enum": ["Recibo","Nota Fiscal",null] },
    "numero_documento":  { "type": ["string","null"] },
    "data_emissao":      { "type": ["string","null"] },
    "moeda":             { "type": ["string","null"] },
    "valor":             { "type": ["number","null"] },
    "parcela":           { "type": ["integer","null"] },
    "total_parcelas":    { "type": ["integer","null"] },
    "campos_nao_encontrados": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["campos_nao_encontrados"]
}
```

Instruções de sistema:

```
Você extrai dados de recibos e notas fiscais de plataformas de software.

REGRAS ABSOLUTAS:
1. Extraia apenas informação literalmente presente no documento.
2. NUNCA infira, deduza, calcule ou complete dados ausentes. Campo não
   localizado retorna null e o nome do campo entra em campos_nao_encontrados.
3. Datas no formato AAAA-MM-DD. Em documentos em inglês, 03/04/2026 é 4 de
   março, não 3 de abril. Se o formato for ambíguo e o documento não permitir
   desambiguar, retorne null e registre em campos_nao_encontrados.
4. valor é numérico, ponto decimal, sem símbolo de moeda e sem separador de
   milhar.
5. moeda em código ISO 4217. NUNCA converta entre moedas.
6. tipo_documento é "Recibo" ou "Nota Fiscal", conforme o documento declarar.
7. numero_documento corresponde a Invoice Number, Receipt Number ou
   equivalente.
8. parcela e total_parcelas somente quando o documento explicitar
   parcelamento. Assinatura recorrente mensal NÃO é parcelamento.
9. Na dúvida sobre qualquer campo, retorne null. Nunca chute.
```

A regra 2 é o que garante que campo não extraído sai vazio com ressalva, em vez de um palpite que passaria despercebido na contabilidade.

## Passo 6 — Normalizar os dados

- Adicione um nó **Code**, renomeado para `Normalizar`

```javascript
const saida = [];

for (const item of $input.all()) {
  const p = item.json;                       // saida do parser
  const email = $('Tem PDF').first().json;
  const faltantes = p.campos_nao_encontrados || [];

  // Data de Vencimento: sempre dia 15 do mes de competencia do envio da
  // planilha, independente da data de emissao. Como a ingestao roda antes
  // do fechamento, a competencia e o mes corrente no momento do processamento.
  const agora = new Date();
  const dataVencimento = `${agora.getUTCFullYear()}-${String(agora.getUTCMonth() + 1).padStart(2, '0')}-15`;

  // A conversao para BRL acontece no fechamento, nao aqui.
  const blocoMoeda = p.moeda ? `Moeda original: ${p.moeda}` : null;

  const partes = [p.plataforma || 'PLATAFORMA NAO IDENTIFICADA'];
  if (blocoMoeda) partes.push(blocoMoeda);
  if (faltantes.length) partes.push(`CAMPOS NAO EXTRAIDOS: ${faltantes.join(', ')}`);
  const observacoes = partes.join(' | ');

  const numero = p.numero_documento || `SEM-NUMERO-${String(email.id).slice(-8)}`;
  const plataforma = (p.plataforma || 'DESCONHECIDA').replace(/[^A-Za-z0-9]/g, '');
  const emissao = p.data_emissao || 'sem-data';
  const nomeArquivo = `${plataforma}_${numero}_${emissao}.pdf`;

  const competencia = (p.data_emissao || '').slice(0, 7);
  const raiz = $('Parametros').first().json.pasta_documentos;
  const pastaDestino = `${raiz}/${competencia.slice(0, 4)}/${competencia}`;

  saida.push({
    json: {
      message_id_graph: email.id,
      plataforma: p.plataforma,
      fornecedor: p.fornecedor,
      valor: p.valor,
      moeda: p.moeda,
      data_emissao: p.data_emissao,
      data_vencimento: dataVencimento,
      tipo_documento: p.tipo_documento,
      numero_documento: p.numero_documento,
      parcela: p.parcela,
      total_parcelas: p.total_parcelas,
      campos_faltantes: faltantes.join(', '),
      observacoes,
      payload_parser: p,
      nome_arquivo: nomeArquivo,
      pasta_destino: pastaDestino,
      status: 'pendente',
    },
    binary: item.binary,
  });
}

return saida;
```

Regras que este nó aplica:

- **Data de Emissão e Data de Registro** recebem a data de emissão do documento
- **Data de Vencimento** é sempre dia 15 do mês de competência do envio — se o fechamento é de agosto, todas as linhas vencem em 15/08
- **Categoria, Conta Corrente e Forma de Pagamento** são valores fixos
- **Observações** recebe a plataforma mais a ressalva de campos não extraídos

> **Isto ainda depende de você: parcelas.** Uma assinatura mensal recorrente não é parcelamento; um plano anual cobrado em doze vezes seria. Minha leitura é que quase tudo cai no primeiro caso e as colunas V/W ficam vazias, mas está a validar com a Cleide antes de virar código.

> **Isto ainda depende de você: nota fiscal.** As colunas Y e Z (Nota Fiscal e Chave da NF-e) dependem de saber se alguma das cinco plataformas emite documento fiscal brasileiro.

> **Nota sobre a data de vencimento.** Ela usa o mês em que o e-mail é processado, não o mês do fechamento. Nos dias entre a data de corte e a virada do mês, uma fatura recebida já é gravada com vencimento do mês seguinte — que é justamente o ciclo em que será enviada. Correto, mas vale conferir na primeira virada de mês em produção.

## Passo 7 — Arquivar o PDF

- Adicione um nó **Microsoft OneDrive**

| Campo | Valor |
|---|---|
| Credential | Microsoft OneDrive OAuth2 API |
| Resource | `File` |
| Operation | `Upload` |
| File Name | `{{ $json.nome_arquivo }}` |
| Parent Folder | `{{ $json.pasta_destino }}` |
| Input Binary Field | o binário do anexo original |

## Passo 8 — Gravar no banco

- Adicione um nó **Postgres**

| Campo | Valor |
|---|---|
| Credential | `Postgres Automacoes` |
| Operation | `Insert` |
| Table | `faturas_saas` |
| Columns | mapeadas da saída do `Normalizar`, acrescentando `caminho_arquivo` do retorno do upload (Passo 7) |

## Passo 9 — Ativar

Depois de testar com um e-mail real, clique em **Active** no canto superior direito. Sem isso, o gatilho só funciona em execuções manuais de teste.

---

# WORKFLOW 3: Monitoramento

**O que faz:** verifica todo dia se a senha da aplicação Microsoft está perto de vencer, e avisa por e-mail antes que isso aconteça.

**Por que existe:** a senha não é usada a cada execução — o n8n usa um acesso de curta duração renovado sozinho, e é a renovação que exige a senha. Quando ela vence, a automação continua funcionando por até uma hora (usando o último acesso válido) e só então começa a falhar, em silêncio. Como o ciclo do Fechamento é mensal, pode levar semanas até alguém perceber.

No n8n, crie um workflow novo chamado `Infra - Monitor Client Secret`.

## Passo 1 — Gatilho

- Adicione um **Schedule Trigger**, Custom (Cron): `0 8 * * *` (todo dia às 08:00)

## Passo 2 — Configuração

- Adicione um nó **Set**, renomeado para `CONFIG_SECRET`

| Campo | Valor |
|---|---|
| `data_expiracao` | a data de expiração do secret atual, formato `AAAA-MM-DD` |
| `identificacao_app` | `n8n-Mosten-Faturas` |
| `client_id` | o Application ID |
| `destinatarios` | `joao.russio@mosten.com, emerson.menezes@mosten.com, iane.cunha@mosten.com` |

Três destinatários evitam depender de uma pessoa só.

> **Vale conferir:** pelo menos um dos três precisa ter acesso ao Entra ID para gerar a nova senha. O alerta serve de pouco se ninguém notificado puder agir.

## Passo 3 — Calcular dias restantes

- Adicione um nó **Code**, renomeado para `Calcular Dias`

```javascript
const p = $input.first().json;
const hoje = new Date();
hoje.setHours(0, 0, 0, 0);
const exp = new Date(p.data_expiracao + 'T00:00:00');
const diasRestantes = Math.round((exp - hoje) / 86400000);

const marcos = [30, 15, 7, 3, 1, 0];
const deveAlertar = marcos.includes(diasRestantes) || diasRestantes < 0;

let severidade = 'AVISO';
if (diasRestantes <= 7 && diasRestantes >= 0) severidade = 'URGENTE';
if (diasRestantes < 0) severidade = 'CRITICO - JA EXPIRADO';

return [{ json: { ...p, diasRestantes, deveAlertar, severidade } }];
```

Os marcos em 30, 15, 7, 3, 1 e zero dias, mais o alerta diário depois de vencido, existem porque um e-mail único enviado com trinta dias de antecedência se perde na caixa como qualquer outro.

## Passo 4 — Decidir se alerta

- Adicione um nó **If**

| Campo | Valor |
|---|---|
| Condition Type | `Boolean` |
| Value 1 | `{{ $json.deveAlertar }}` |
| Operation | `is true` |

## Passo 5 — Enviar o alerta

- Adicione um nó **Microsoft Outlook**

| Campo | Valor |
|---|---|
| Credential | Microsoft Outlook OAuth2 API |
| Resource | `Message` |
| Operation | `Send` |
| To | `{{ $json.destinatarios }}` |
| Subject | `[{{ $json.severidade }}] Client Secret do n8n expira em {{ $json.diasRestantes }} dias` |

Corpo:

```
O client secret da aplicação {{ identificacao_app }} no Entra ID expira em
{{ diasRestantes }} dias, em {{ data_expiracao }}.

Quando isso ocorrer, a automação de coleta de faturas de ferramentas de
software deixará de funcionar e nenhuma planilha será enviada.

Application (client) ID: {{ client_id }}
```

## Passo 6 — Testar forçando a data

- Altere temporariamente `data_expiracao` para hoje mais 30 dias, execute manualmente, confirme o e-mail
- Teste também com uma data no passado, confirmando severidade crítica
- Restaure a data real e ative o workflow

## Passo 7 — Duas limitações registradas

**Usa a mesma credencial que monitora.** Enquanto a senha está válida, funciona. Depois de vencida, o alerta de "já expirou" não consegue ser enviado — mas isso é aceitável, porque a função do monitor é avisar antes, quando a credencial ainda funciona. Não cobre o cenário de o workflow estar desativado ou a VM fora do ar durante toda a janela de aviso.

**A data é manual.** Se a senha for renovada e a data aqui não for atualizada, o monitoramento silencia e passa uma falsa sensação de segurança.

## Passo 8 — Como renovar a senha sem parar nada

Uma aplicação aceita mais de uma senha válida ao mesmo tempo:

1. Crie a nova senha no Azure, antes de a atual vencer
2. Copie o campo Value imediatamente
3. Atualize o Client Secret nas credenciais do n8n (Outlook e OneDrive)
4. Refaça o Connect das credenciais, se necessário
5. Teste com uma leitura simples
6. **Atualize a data no nó `CONFIG_SECRET` deste workflow**
7. Só então remova a senha antiga no Azure

O passo 6 é o que mantém o monitoramento vivo. Sem ele, ele silencia permanentemente.

---

# Validação final antes de ativar tudo

Execute na ordem. Não avance com etapa reprovada.

| O que verificar | Critério |
|---|---|
| O n8n lê o banco | A consulta de contagem retorna zero sem erro |
| A credencial da Microsoft conecta | Leitura de mensagens funciona, sem erro de tenant |
| A cópia do modelo funciona | `Enviar Copia` retorna um `id` novo, diferente do template |
| A escrita via Workbook API funciona | `Escrever Lancamentos` retorna sucesso (200) |
| Só uma planilha é criada por fechamento | Um único arquivo na pasta do mês |
| O nome do arquivo não tem `=` | `Omie_Contas_Pagar_2026-08.xlsx` |
| O recuo de cotação funciona | Lançamento emitido em sábado fecha com a PTAX de sexta |
| O e-mail traz só os anexos reais | Nenhum arquivo `vazio_N.txt` |
| Todos os lançamentos são marcados | Segunda execução seguida cai no ramo falso do `Tem Lancamentos?` |
| A conversão cambial é persistida | Após o fechamento, `valor_brl` e `cotacao_ptax` estão preenchidos no banco |
| O valor em reais chega na planilha | Coluna F preenchida, conferida contra `valor × cotacao_ptax` |
| As linhas de exemplo foram neutralizadas | Colunas B, H, M e N vazias nas linhas escritas e nas residuais |
| A planilha final abre sem aviso de reparo | Testado no Workflow 1, Passo 12 |
| O gatilho de e-mail dispara e o filtro funciona | E-mail sem PDF não avança |
| O parser devolve vazio quando o dado não existe | Nenhum campo preenchido por inferência |
| A consulta de câmbio funciona a partir da VM | A API do Banco Central responde, sem bloqueio de firewall |
| O fallback de câmbio funciona | Forçando uma data de sábado, a cotação vem do último dia útil anterior |
| A deduplicação funciona | Reenviar o mesmo e-mail não cria um segundo registro |
| O PDF é arquivado com o nome correto | Arquivo presente na pasta e legível |
| O e-mail de fechamento chega com a planilha e os documentos | Anexos abrem e correspondem ao período |
| A planilha anexada é a versão já limpa | O arquivo do e-mail e o do OneDrive são idênticos |
| Um PDF ausente não derruba o fechamento | Apontando um `caminho_arquivo` inexistente, o e-mail sai com os demais anexos |
| O Error Workflow dispara | Forçando um erro, o e-mail de falha chega |
| Os registros só viram exportados após o envio | Uma falha de envio mantém tudo como pendente |
| O monitoramento da senha dispara | Forçando a data, o alerta chega |
| **Importação de homologação no Omie** | Arquivo aceito sem erro de layout |

---

# O que ainda trava o projeto

**Bloqueantes:**

- **Remetentes das plataformas** (Workflow 2, Passo 2). Falta o endereço remetente de AWS, Azure DevOps, Sentry e OpenAI — só o Cursor está mapeado


**Não bloqueantes:**

- **Permissão de leitura e retenção dos PDFs arquivados** (Etapa 1.4): quem acessa a pasta no OneDrive e se há política de retenção a aplicar
- **Critério de parcelamento**, a validar com a Cleide (Workflow 2, Passo 6)
- **Colunas de nota fiscal e chave da NF-e**, se alguma plataforma emite documento fiscal brasileiro (Workflow 2, Passo 6)
- **Tratamento de feriados na data de corte**, se vale manter a lista com manutenção anual (Workflow 1, Passo 1)
- **Provedor de LLM** para o parser, a definir no momento da implementação (Workflow 2, Passo 5)
- **Formatação acima de 32 linhas** (Workflow 1, Passo 6): não é limite de importação, é limite de formatação. Precisa de solução antes de o volume se aproximar desse número
- **Divergência de domínio nos endereços** (`mosten.com` neste guia, `mosten.com.br` no estudo de viabilidade): confirmar qual é o correto antes de ativar
- **Fuso horário da instância** (Etapa 1.2): definido como `America/New_York`, deslocando o horário de disparo dos três workflows

**Já validado em execução (Workflow 1 completo):** gatilho e verificação de data, leitura dos pendentes, conversão cambial com recuo para dia útil anterior, persistência da cotação no banco, cópia do modelo por download e reupload, escrita via Workbook API preservando validações e aba `Config`, limpeza das linhas residuais, anexo da planilha e dos PDFs, envio via Graph e marcação dos lançamentos como exportados. Testado também o ciclo vazio: segunda execução seguida cai no ramo falso sem gerar arquivo.

**Confirmado empiricamente:** na Workbook API, string vazia apaga a célula e `null` preserva o conteúdo. O nó Microsoft Outlook não aceita lista de anexos separada por vírgula, daí o envio por `POST /me/sendMail`. O campo Query Parameters do nó Postgres trata vírgula como separador entre parâmetros.

**Ainda não exercitado:** PDF ausente ou com `caminho_arquivo` inválido, que deve sair pelo ramo de erro do `Baixar Documentos` sem derrubar o fechamento. E o Error Workflow, que precisa de um erro forçado para validar.

