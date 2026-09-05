# Guia de Implementação — Bot de Agenda (Telegram + n8n + Google Calendar)

Documento vivo de implementação. Cobre: deploy do n8n no Railway, criação do bot no Telegram, credenciais do Google Calendar, credencial do LLM gratuito, e a construção node a node do workflow (criação, edição e cancelamento de eventos, com confirmação e idempotência).

---

## 0. Visão geral do fluxo final

```
                         ┌─────────────────────────────┐
                         │   Telegram Trigger (n8n)     │
                         │ updates: message, callback   │
                         └──────────────┬────────────────┘
                                        │
                              IF: é message ou callback_query?
                                        │
        ┌───────────────────────────────┴───────────────────────────────┐
        │ RAMO A — nova mensagem                    │ RAMO B — botão confirmado/cancelado
        ▼                                            ▼
  Filtro de segurança (chat_id)              Buscar pending_event no Postgres pelo id
        │                                            │
  Information Extractor (LLM) → JSON          Switch: confirmado? cancelado? expirado?
        │                                            │
  Code: normalizar data/ano/duração                  ├─ confirmado → Switch por intenção
        │                                            │     ├─ criar   → Google Calendar: Create
  Postgres: INSERT pending_event                     │     ├─ editar  → Google Calendar: Search + Update
  (idempotência por telegram_message_id)             │     └─ cancelar→ Google Calendar: Search + Delete
        │                                            │
  Telegram: enviar resumo + botões                   Postgres: UPDATE status
  [Confirmar] [Cancelar]                              │
                                              Telegram: mensagem final (✅/❌)
```

Duas "entradas" no mesmo workflow, diferenciadas pelo tipo de update do Telegram. Toda a "memória" entre a pergunta de confirmação e o clique no botão fica em uma tabela `pending_events` no próprio Postgres que já roda junto do n8n — sem custo adicional.

---

## 1. Contas e ferramentas necessárias

| Ferramenta | Para quê | Custo |
|---|---|---|
| Railway | hospedar n8n + Postgres | trial de US$5 (30 dias), depois plano Hobby ~US$5/mês (ver nota abaixo) |
| Telegram | canal de entrada do bot | gratuito |
| Google Cloud Console | credencial OAuth do Google Calendar | gratuito |
| Google AI Studio | chave da API do Gemini (LLM parser) | gratuito (free tier) |

**Nota sobre o Railway:** ele não é mais gratuito indefinidamente — hoje funciona com um crédito trial de ~US$5 por 30 dias e, depois disso, um plano Hobby com piso de ~US$5/mês (cobrança por uso). Isso é relevante porque n8n + Postgres rodando 24/7 provavelmente exige o Hobby depois do trial. Como você já decidiu usar Railway, sigo com ele — mas deixo registrado que "custo zero" nesse projeto se aplica com segurança ao LLM (é isso que crescia com volume de mensagens), não necessariamente à hospedagem. Se quiser custo zero total, a alternativa seria rodar o n8n localmente (Docker, sempre ligado) — posso detalhar depois se fizer sentido.

---

## 2. Parte A — Deploy do n8n no Railway

1. Acesse [railway.com](https://railway.com) e crie uma conta (pode ser via GitHub).
2. Use o template oficial **"n8n with Postgres"** (busque por "n8n" na galeria de templates ou acesse `railway.com/deploy/n8n-with-postgres`). Ele já sobe dois serviços conectados: `n8n` e `postgres`.
3. Clique em **Deploy Now**. Railway provisiona os dois serviços automaticamente (leva ~1-3 minutos).
4. No serviço **n8n**, vá em **Settings → Networking** e clique em **Generate Domain** para obter uma URL pública (ex.: `seu-projeto.up.railway.app`).
5. No serviço **n8n**, vá em **Variables** e confira/ajuste:
   - `N8N_ENCRYPTION_KEY` — **crítica**. Se o template já gerou uma automaticamente e ela está persistida no volume, ótimo; apenas confirme que existe e **copie o valor para um cofre de senhas seu** (1Password, Bitwarden, etc.). Se essa chave mudar ou for perdida, todas as credenciais salvas no n8n (inclusive a do Google Calendar) ficam ilegíveis e você tem que recadastrar tudo.
   - `WEBHOOK_URL` — defina como `https://seu-projeto.up.railway.app/` (a URL gerada no passo 4). Sem isso, o node do Telegram Trigger gera uma URL de webhook errada.
   - `GENERIC_TIMEZONE` — defina como `America/Sao_Paulo`.
   - `TZ` — defina também como `America/Sao_Paulo` (garante que o container e os cálculos de data internos do n8n usem o fuso certo).
6. Aguarde o redeploy (Railway reinicia o serviço ao salvar variáveis).
7. Abra a URL pública no navegador. Na primeira vez, o n8n pede para criar a conta *owner* (seu e-mail e senha) — este login protege o **editor** do n8n, não o bot em si.

---

## 3. Parte B — Criar o bot no Telegram

1. No Telegram, procure por **@BotFather** e inicie uma conversa.
2. Envie `/newbot`.
3. Escolha um nome de exibição (ex.: "Agenda Bot") e um username terminado em `bot` (ex.: `gustavo_agenda_bot`).
4. O BotFather devolve um **token** no formato `123456789:ABCdefGhIJKlmNoPQRstuVWXyz`. Guarde-o — será usado na credencial do n8n.
5. Descubra o seu **chat_id** (para o filtro de segurança do passo 5): procure por **@userinfobot** no Telegram, inicie conversa, e ele responde com seu `Id` numérico. Guarde esse número.

---

## 4. Parte C — Credenciais do Google Calendar

1. Acesse [console.cloud.google.com](https://console.cloud.google.com) e crie um novo projeto (ex.: "agenda-bot").
2. No menu, vá em **APIs & Services → Library**, busque **Google Calendar API** e clique em **Enable**.
3. Vá em **APIs & Services → OAuth consent screen**:
   - User type: **External**.
   - Preencha nome do app, e-mail de suporte e e-mail do desenvolvedor (o seu).
   - Em **Scopes**, não precisa adicionar nada manualmente agora (o n8n solicita o escopo certo na hora de autorizar).
   - Em **Test users**, adicione o seu próprio e-mail do Google (enquanto o app estiver em modo "Testing", só e-mails cadastrados aqui conseguem autorizar — o que é bom, reforça a segurança).
4. Vá em **APIs & Services → Credentials → Create Credentials → OAuth client ID**:
   - Application type: **Web application**.
   - Em **Authorized redirect URIs**, adicione:
     `https://seu-projeto.up.railway.app/rest/oauth2-credential/callback`
   - Salve e copie o **Client ID** e o **Client Secret** gerados.
5. No n8n, vá em **Credentials → New → Google Calendar OAuth2 API**:
   - Cole o Client ID e Client Secret.
   - Clique em **Connect my account**, faça login com sua conta Google e autorize.
   - Salve a credencial com o nome `Google Calendar - Pessoal`.

---

## 5. Parte D — Credencial do LLM gratuito

### Opção recomendada: Google Gemini (via Google AI Studio)

Motivos: suporta **structured output / function calling** nativamente (essencial para o parser confiável), tem contexto grande, e a cota gratuita diária é folgada para o volume de um bot pessoal (algumas dezenas de mensagens por dia, no máximo).

1. Acesse [aistudio.google.com](https://aistudio.google.com), faça login com a mesma conta Google.
2. Vá em **Get API key → Create API key**. Copie a chave.
3. No n8n, vá em **Credentials → New → Google Gemini (PaLM) API** (ou "Google AI" dependendo da versão) e cole a chave.
4. Modelo sugerido: **`gemini-2.5-flash`** (ou a variante "flash-lite" se quiser ainda mais folga de cota, com qualidade ligeiramente menor — para esse caso de uso simples, ambos funcionam bem).

⚠️ Os limites exatos da cota gratuita (requisições por minuto/dia) mudam com frequência — hoje giram na faixa de centenas a ~1.500 requisições/dia dependendo do modelo, o que é muito acima do que um bot pessoal de agenda vai usar. Vale conferir os números atuais em `ai.google.dev/pricing` antes de ir para produção, só para confirmar que não houve mudança recente.

### Opção alternativa/backup: Groq

Groq também tem free tier generoso e é bem rápido (útil se algum dia quiser resposta quase instantânea), hospedando modelos abertos como Llama 3.3 70B. Serve como plano B caso a cota do Gemini aperte, ou se quiser comparar qualidade de extração. Setup é análogo: criar conta em `console.groq.com`, gerar API key, criar credencial no n8n do tipo **Groq**.

Não recomendo depender de modelo local (Ollama) rodando no próprio Railway — o plano básico não tem RAM/CPU suficiente para rodar um modelo com qualidade aceitável para extração estruturada, e isso empurraria o custo de infraestrutura para cima, o que vai contra o seu objetivo de custo mínimo.

---

## 6. Parte E — Tabela de apoio no Postgres (`pending_events`)

Essa tabela guarda o evento "proposto" pelo parser enquanto aguarda sua confirmação, e também garante idempotência (mensagem duplicada do Telegram não gera pergunta duplicada).

1. No n8n, crie uma credencial **Postgres** apontando para o mesmo banco que já roda no Railway (os dados de conexão — host, porta, usuário, senha, database — aparecem na aba **Variables** do serviço `postgres` no Railway, variáveis `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`).
2. Crie um workflow auxiliar temporário (ou use um node **Postgres → Execute Query** dentro do próprio editor, modo manual) e rode uma vez:

```sql
CREATE TABLE IF NOT EXISTS pending_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_chat_id BIGINT NOT NULL,
    telegram_message_id BIGINT NOT NULL,
    intencao TEXT NOT NULL,              -- 'criar' | 'editar' | 'cancelar'
    titulo TEXT,
    data_evento DATE,
    hora_inicio TIME,
    duracao_min INTEGER DEFAULT 60,
    local TEXT,
    referencia_evento TEXT,              -- usado em editar/cancelar
    google_event_id TEXT,                -- preenchido após localizar o evento (editar/cancelar)
    confianca TEXT,                      -- 'alta' | 'media' | 'baixa'
    status TEXT NOT NULL DEFAULT 'pending', -- 'pending' | 'confirmado' | 'cancelado' | 'expirado'
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (telegram_message_id)
);
```

O `UNIQUE (telegram_message_id)` é o que garante idempotência: se o Telegram reenviar o mesmo webhook (comum em timeouts), o segundo INSERT falha silenciosamente (tratamos isso no node com `ON CONFLICT DO NOTHING`) e o workflow para sem mandar uma segunda pergunta de confirmação.

---

## 7. Parte F — Construção do workflow no n8n (node a node)

Crie um novo workflow chamado **"Agenda Bot"**.

### Node 1 — Telegram Trigger

- Tipo: **Telegram Trigger**
- Credencial: crie uma nova credencial **Telegram API**, colando o token do BotFather (Parte B).
- **Updates**: marque `message` e `callback_query`.
- Isso cria o webhook automaticamente na primeira ativação do workflow.

### Node 2 — IF: mensagem ou clique em botão?

- Tipo: **IF**
- Condição: `{{ $json.message !== undefined }}`
  - **true** → Ramo A (nova mensagem)
  - **false** → Ramo B (callback_query, ou seja, clique em Confirmar/Cancelar)

---

## RAMO A — Nova mensagem de texto

### Node 3 — Filtro de segurança (whitelist)

- Tipo: **IF**
- Condição: `{{ $json.message.chat.id }}` **Equals** `SEU_CHAT_ID` (o número obtido com @userinfobot na Parte B).
- **false** → conecte a um node **NoOp** (ou simplesmente deixe sem conexão) para encerrar o fluxo silenciosamente. Não responda a estranhos — nem com uma mensagem de erro, para não confirmar que o bot existe e está ativo.
- **true** → segue para o parser.

### Node 4 — Set (contexto para o LLM)

- Tipo: **Edit Fields (Set)**
- Adicione os campos:
  - `data_hoje` = `{{ $now.setZone('America/Sao_Paulo').toFormat('yyyy-MM-dd') }}`
  - `texto_usuario` = `{{ $json.message.text }}`
  - `chat_id` = `{{ $json.message.chat.id }}`
  - `message_id` = `{{ $json.message.message_id }}`

### Node 5 — Information Extractor (parser LLM)

- Tipo: **Information Extractor** (node da categoria LangChain/AI do n8n)
- Conecte como **Chat Model** sub-node o **Google Gemini Chat Model**, usando a credencial da Parte D, modelo `gemini-2.5-flash`.
- **Text a extrair**: `{{ $json.texto_usuario }}`
- **System Prompt / instruções** (cole no campo de instrução do node):

```
Você é um extrator de dados de agenda. A mensagem do usuário é sempre sobre criar,
editar ou cancelar um compromisso. Hoje é {{ $json.data_hoje }} (fuso America/Sao_Paulo).

Regras:
- Se a mensagem pedir para marcar algo novo → intencao = "criar".
- Se pedir para mudar horário/data de algo existente → intencao = "editar".
- Se pedir para cancelar/desmarcar algo → intencao = "cancelar".
- Extraia a data no formato YYYY-MM-DD. Se o ano não for mencionado, use o ano atual
  com base em "data_hoje" (a normalização de virada de ano é feita depois, não se
  preocupe em decidir isso).
- Se a duração não for mencionada, deixe duracao_min vazio (será preenchido com
  padrão depois).
- Em "referencia_evento", coloque uma descrição curta do compromisso (ex.: "consulta
  do dentista") — usado para localizar o evento em editar/cancelar.
- Se não conseguir identificar data ou título com segurança, marque confianca = "baixa".
```

- **Schema de saída** (defina no node, modo JSON Schema):

```json
{
  "type": "object",
  "properties": {
    "intencao": { "type": "string", "enum": ["criar", "editar", "cancelar"] },
    "titulo": { "type": "string" },
    "data": { "type": "string", "description": "formato YYYY-MM-DD" },
    "hora_inicio": { "type": "string", "description": "formato HH:MM" },
    "duracao_min": { "type": ["integer", "null"] },
    "local": { "type": ["string", "null"] },
    "referencia_evento": { "type": ["string", "null"] },
    "confianca": { "type": "string", "enum": ["alta", "media", "baixa"] }
  },
  "required": ["intencao", "confianca"]
}
```

### Node 6 — Code (normalização determinística)

Não confie no LLM para decidir virada de ano ou aplicar o default de duração — isso é lógica determinística e deve ser feita em código, não em prompt.

- Tipo: **Code** (JavaScript)

```javascript
const DateTime = require('luxon').DateTime;
const out = $input.first().json;

const hoje = DateTime.fromISO($('Set').first().json.data_hoje, { zone: 'America/Sao_Paulo' });
let data = DateTime.fromISO(out.data, { zone: 'America/Sao_Paulo' });

// Regra: se a data resultante já passou, assume o próximo ano
if (data < hoje) {
  data = data.plus({ years: 1 });
}

const duracao = out.duracao_min || 60; // default 1h

return [{
  json: {
    ...out,
    data: data.toFormat('yyyy-MM-dd'),
    duracao_min: duracao
  }
}];
```

*(ajuste o nome `'Set'` para o nome real que você deu ao node 4 no seu workflow)*

### Node 7 — Postgres (INSERT pending_event)

- Tipo: **Postgres → Execute Query**
- Query:

```sql
INSERT INTO pending_events
  (telegram_chat_id, telegram_message_id, intencao, titulo, data_evento,
   hora_inicio, duracao_min, local, referencia_evento, confianca)
VALUES
  ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
ON CONFLICT (telegram_message_id) DO NOTHING
RETURNING id;
```

- Parâmetros (na ordem): `{{ $json.chat_id }}`, `{{ $json.message_id }}`, `{{ $json.intencao }}`, `{{ $json.titulo }}`, `{{ $json.data }}`, `{{ $json.hora_inicio }}`, `{{ $json.duracao_min }}`, `{{ $json.local }}`, `{{ $json.referencia_evento }}`, `{{ $json.confianca }}`.

### Node 8 — IF: inserção ocorreu?

- Condição: `{{ $json.id !== undefined }}` (se o `ON CONFLICT DO NOTHING` bloqueou, não vem `id` de volta).
- **false** → encerra (mensagem duplicada, já tratada antes).
- **true** → segue para enviar a confirmação.

### Node 9 — Telegram (enviar resumo + botões)

- Tipo: **Telegram → Send Message**
- Chat ID: `{{ $('Set').first().json.chat_id }}`
- Texto (monte de acordo com a intenção — pode usar uma expressão condicional ou um node Set antes formatando o texto):

```
Entendi:
📌 {{ $json.titulo || $json.referencia_evento }}
📅 {{ $json.data_evento }} às {{ $json.hora_inicio }}
⏱️ {{ $json.duracao_min }} min
{{ $json.local ? '📍 ' + $json.local : '' }}
Ação: {{ $json.intencao }}

Confirma?
```

- **Reply Markup → Inline Keyboard**, dois botões na mesma linha:
  - Texto: `✅ Confirmar` | `callback_data`: `confirmar:{{ $json.id }}`
  - Texto: `❌ Cancelar` | `callback_data`: `cancelar:{{ $json.id }}`

(o `id` aqui é o UUID retornado pelo INSERT no Node 7 — o `callback_data` do Telegram tem limite de ~64 caracteres, por isso passamos só o UUID, não o payload inteiro; o payload completo já está salvo na tabela).

---

## RAMO B — Clique em botão (callback_query)

### Node 10 — Code (parse do callback_data)

```javascript
const data = $input.first().json.callback_query.data; // ex: "confirmar:uuid..." 
const [acao, pendingId] = data.split(':');
return [{
  json: {
    acao,               // 'confirmar' ou 'cancelar'
    pending_id: pendingId,
    chat_id: $input.first().json.callback_query.message.chat.id,
    callback_query_id: $input.first().json.callback_query.id
  }
}];
```

### Node 11 — Postgres (buscar pending_event)

```sql
SELECT * FROM pending_events WHERE id = $1 AND status = 'pending';
```
Parâmetro: `{{ $json.pending_id }}`

### Node 12 — IF: encontrado?

- **false** → Telegram: responder "Esse pedido já foi tratado ou expirou." Fim.
- **true** → segue.

### Node 13 — Switch (ação do botão)

- `confirmar` → Ramo confirmação
- `cancelar` → Postgres UPDATE `status = 'cancelado'` → Telegram: "Ok, não fiz nada." → Fim.

### Ramo confirmação → Node 14 — Switch (por intenção)

**Caso `criar`:**

- **Google Calendar → Create Event**
  - Calendar: seu calendário pessoal (primary)
  - Start: `{{ $json.data_evento }}T{{ $json.hora_inicio }}:00` (timezone: `America/Sao_Paulo`)
  - End: calcular somando `duracao_min` (pode usar um Code node antes, com Luxon, ou a expressão `{{ DateTime.fromISO(...).plus({minutes: $json.duracao_min}) }}`)
  - Summary: `{{ $json.titulo }}`
  - Location: `{{ $json.local }}`
  - **Use Default Reminders**: conforme sua preferência.

**Caso `editar` ou `cancelar`:**

- **Google Calendar → Get Many (Search)**
  - Calendar: primary
  - Query (`q`): `{{ $json.referencia_evento }}`
  - Time Min: `now`
  - Isso retorna eventos futuros cujo título/descrição bate com o texto de busca do Google (busca textual simples, não semântica).
- **IF**: quantidade de resultados
  - **0 resultados** → Telegram: "Não achei nenhum evento com essa descrição. Pode me dar mais detalhes (ex.: a data)?" → Fim.
  - **>1 resultado** → Telegram: lista os eventos encontrados (título + data) e pede para o usuário reenviar especificando melhor. → Fim.
  - **exatamente 1** → segue:
    - Se `editar`: **Google Calendar → Update Event**, usando o `id` do evento encontrado, sobrescrevendo `start`/`end`/`summary`/`location` com os novos valores extraídos.
    - Se `cancelar`: **Google Calendar → Delete Event**, usando o `id` do evento encontrado.

### Node 15 — Postgres (UPDATE status = 'confirmado')

```sql
UPDATE pending_events SET status = 'confirmado' WHERE id = $1;
```

### Node 16 — Telegram (mensagem final)

- Texto de sucesso adequado à ação (ex.: "✅ Evento criado!", "✏️ Evento atualizado!", "🗑️ Evento cancelado!").

### Node 17 — HTTP Request (responder ao callback do Telegram)

Isso remove o "relógio de carregando" do botão no app do Telegram — sem ele, o botão fica "girando" indefinidamente do lado do usuário.

- Método: `POST`
- URL: `https://api.telegram.org/bot<SEU_TOKEN>/answerCallbackQuery`
- Body (JSON): `{ "callback_query_id": "{{ $('Code').first().json.callback_query_id }}" }`

---

## 8. Testes recomendados antes de considerar "pronto"

1. **Mensagem de estranho**: peça para alguém (ou use outro chat_id de teste) mandar mensagem pro bot — confirme que nada acontece e nenhuma resposta é enviada.
2. **Criação simples**: "Dentista 21/08 às 08h30" — confirme resumo, confirme, verifique se o evento aparece certo no Google Calendar (data, hora, timezone, duração padrão de 1h).
3. **Data já passada no ano atual**: teste com uma data tipo "05/01" quando já estiver depois disso no ano — confirme que ele assume o ano seguinte.
4. **Duração explícita**: "Reunião 15/09 das 14h às 15h30" — confirme que a duração calculada bate.
5. **Reenvio de mensagem (idempotência)**: force um reenvio (ex.: reenviando a mesma mensagem do Telegram rapidamente) e confirme que não gera duas perguntas de confirmação.
6. **Cancelar pelo botão**: clique em ❌ e confirme que nada é criado.
7. **Editar**: crie um evento de teste, depois mande algo como "Muda o horário da consulta do dentista pra 10h" — confirme que ele encontra o evento certo (e testa o caso de encontrar 0 ou mais de 1, digitando uma referência vaga de propósito).
8. **Cancelar existente**: "Cancela a consulta do dentista" — confirme que o evento certo some da agenda.
9. **Timeout de confirmação** (opcional, fase 2): hoje um `pending_event` nunca expira sozinho — se quiser, dá pra adicionar um Cron que marca como `expirado` tudo que ficou `pending` há mais de 1h.

---

## 9. Resumo de custo esperado

| Item | Custo |
|---|---|
| Telegram Bot API | gratuito, sem limites relevantes para uso pessoal |
| Google Calendar API | gratuito dentro das cotas padrão (muito acima do necessário aqui) |
| Google Gemini API (free tier) | gratuito, cota diária muito acima do volume esperado de um bot pessoal |
| Railway (n8n + Postgres) | trial de US$5/30 dias, depois ~US$5/mês (Hobby) |

O único ponto realmente fora do seu controle de "custo zero" é a hospedagem no Railway — o resto (Telegram, Google Calendar, LLM) fica dentro dos free tiers com folga confortável para uso pessoal.

---

## 10. Próximos passos (fase 2, não implementar agora)

- Expiração automática de `pending_events` antigos (Cron + UPDATE).
- Roteamento por múltiplos calendários (ex.: pessoal vs. trabalho), se um dia precisar.
- Ajuste de confiança: pular a confirmação quando `confianca = "alta"` e a ação for só `criar` (mantendo confirmação obrigatória para `editar`/`cancelar`, que são mais arriscados por natureza).
