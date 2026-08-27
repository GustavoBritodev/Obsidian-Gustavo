---
tags:
- tipo/trabalho/projeto/automaes
- API
- Azure
- n8n
- SQL
---
# Runbook — Automação de Offboarding (Playbook 030/25)

> **Versão:** 0.4 — 20/08/2026 **Responsável:** Gustavo Martinho Santos de Brito — Analista de Negócios e Processos, Mosten **Status geral:** 🟡 Em validação — Ramo A implementado e revisado, ingestão em modo diagnóstico
> 
> Documento vivo. Atualizado a cada iteração. O changelog fica no fim.

---
## 1. Visão geral do fluxo

```
Convenia (webhook dismissal.finished)
        │
        ▼
[Offboarding] Ingestão ......... valida assinatura, enriquece, agenda
        │  grava em offboarding_processos (status = agendado)
        ▼
[Offboarding] Agendador ........ varre a cada 15 min
        │  quando scheduled_datetime <= agora → status = aguardando_aprovacao
        ▼
[Offboarding] Aprovação ........ e-mail com Aprovar/Reprovar (Send and Wait)
        │  aprovado → status = aprovado          rejeitado → status = rejeitado + e-mail GeP
        ▼
[Offboarding] Workflow Execução  status = em_execucao → 7 ramos paralelos
        │  cada ramo grava 1 linha em offboarding_acoes
        ▼
[Offboarding] Relatório ........ ⛔ NÃO IMPLEMENTADO
```

### Ramos do Workflow Execução

|Ramo|Sistema|Método|Status|
|---|---|---|---|
|A|Microsoft 365 — Bloqueio|Graph API|✅ Implementado e revisado|
|B|Microsoft 365 — Backup|VM PowerShell + Graph|🔶 Aguarda VM|
|C|pfSense (VPN)|SSH + `pfSsh.php`|⚠️ Implementado, comando não validado|
|D|InControl (acesso físico)|—|⏸️ Manual (sem API confirmada)|
|E|Azure DevOps|REST API|🔶 Aguarda PAT|
|F|OnFly|REST API|🔶 Aguarda token|
|G|Qulture / PontoMais / PSOffice|—|✅ Manual por decisão|

---
## 2. Passo a passo de execução

### 2.1 Preparação do banco (uma vez)

```sql
-- Log de diagnóstico do webhook
CREATE TABLE IF NOT EXISTS offboarding_webhook_log (
    id                  SERIAL PRIMARY KEY,
    recebido_em         TIMESTAMP NOT NULL DEFAULT NOW(),
    assinatura_valida   BOOLEAN,
    signature_recebida  TEXT,
    hash_calculado      TEXT,
    origem_body         TEXT,
    evento_tipo         TEXT,
    headers             JSONB,
    raw_body            TEXT,
    erro                TEXT
);
```

Conferir também o fuso do banco — impacta diretamente a regra das 18h:

```sql
SELECT current_setting('TIMEZONE');
```

Se retornar algo diferente de `America/Sao_Paulo`, aplicar o ajuste descrito na sticky note do Agendador.

### 2.2 Importação dos workflows

> 🔴 **Importe SEMPRE em um workflow NOVO e VAZIO.** Se você importar dentro de um workflow que já tem conteúdo, o n8n cola tudo por cima e renomeia os nodes com sufixo numérico (`PARAMETROS1`, `Verificar Assinatura1`...). O canvas vira duas cópias sobrepostas e as expressões `$('PARAMETROS')` passam a apontar para o node errado.
> 
> Se isso já aconteceu: `Ctrl+A` → `Delete` no workflow bagunçado, e importe de novo.

Ordem sugerida: **Execução → Aprovação → Agendador → Ingestão**. Importar Execução e Aprovação primeiro faz com que os IDs de sub-workflow já existam quando você abrir os nodes `Disparar Execução` e `Disparar Aprovação`.

Após importar cada um:

1. Selecionar a credencial Postgres (`Postgres account automacoes_app`) nos nodes que a exigem.
2. Selecionar a credencial Microsoft (`Microsoft account - Gustavo`) nos nodes Outlook.
3. Preencher o node `PARAMETROS` (ver seção 3).
4. Reabrir `Disparar Aprovação` e `Disparar Execução` e **reselecionar o workflow de destino** — os IDs mudam no import.
5. Conferir que os ramos desativados continuam desativados (ver 2.2.1).

### 2.2.1 Estado dos ramos no import (Workflow Execução)

Por padrão **somente o Ramo A vem ativo**. Todo o resto vem com `disabled: true` em todos os nodes do ramo.

|Ramo|Estado|Para reativar, antes é preciso|
|---|---|---|
|A — M365 Bloqueio|✅ **ATIVO**|—|
|B — M365 Backup|🚫 Desativado|VM provisionada + `ps_vm_url` / `ps_vm_api_key`|
|C — pfSense|🚫 Desativado|Comandos `pfSsh.php` testados manualmente + credencial SSH|
|D — InControl|🚫 Desativado|Definir caixa da TI (ou decidir por RPA)|
|E — Azure DevOps|🚫 Desativado|PAT + `azdo_org`|
|F — OnFly|🚫 Desativado|Token OnFly|
|G — Sistemas manuais|🚫 Desativado|Só um teste — não é destrutivo, é o mais fácil de liberar|

**Como reativar um ramo:** selecione **todos** os nodes do ramo e tecle `D`. Reativar só o primeiro node não adianta — no n8n, um node desativado repassa os dados adiante, então um ramo meio ativo executa pela metade.

**Trava da Ingestão:** não usa `disabled`. A trava é o `modo_diagnostico` no `PARAMETROS`, que interrompe o fluxo no IF `Modo Diagnóstico?` antes de qualquer gravação.

### 2.3 Teste da ingestão em modo diagnóstico

Pré-requisito: `modo_diagnostico = true` no `PARAMETROS` da Ingestão, `convenia_webhook_secret` preenchido, workflow **ativo**.

Simulação local antes do evento real:

```bash
BODY='{"type":"dismissal.finished","employee":{"id":"55fe5c64-84c5-426d-9903-0768fcc8732d"},"status_name":"finished","access_removal_date":"2026-08-20","dismissal_date":"2026-08-20"}'
SECRET='<valor do convenia_webhook_secret>'
SIG=$(echo -n "$BODY" | openssl dgst -sha256 -hmac "$SECRET" | sed 's/^.* //')

curl -i -X POST 'https://<sua-instancia-n8n>/webhook/offboarding/convenia' \
  -H 'Content-Type: application/json' \
  -H "Signature: $SIG" \
  -d "$BODY"
```

Verificação:

```sql
SELECT id, recebido_em, evento_tipo, assinatura_valida, origem_body, erro
FROM offboarding_webhook_log ORDER BY id DESC LIMIT 5;
```

|Resultado|Leitura|
|---|---|
|Nenhuma linha|Não chegou — URL, workflow inativo ou firewall|
|`assinatura_valida = true`|Entrega e HMAC corretos|
|`assinatura_valida = false`, `erro` nulo|Chegou; formato da assinatura difere do assumido|
|`origem_body` com "fallback"|Raw body binário não veio — ver premissa P2|

### 2.4 Saída do modo diagnóstico

`PARAMETROS` → `modo_diagnostico` = **false**. O fluxo volta a gravar em `offboarding_processos`.

### 2.5 Reprocessar um evento capturado em diagnóstico

Eventos recebidos com `modo_diagnostico = true` **não geram processo**. Para injetar manualmente a partir do log (exige que o e-mail corporativo seja conhecido):

```sql
INSERT INTO offboarding_processos
  (convenia_employee_id, nome, email, access_removal_date, scheduled_datetime, status, convenia_raw_payload)
SELECT
  raw_body::jsonb -> 'employee' ->> 'id',
  '<NOME COMPLETO>',
  '<email.corporativo@mosten.com>',
  (raw_body::jsonb ->> 'access_removal_date')::date,
  ((raw_body::jsonb ->> 'access_removal_date') || ' 18:00:00')::timestamp,
  'agendado',
  raw_body::jsonb
FROM offboarding_webhook_log
WHERE id = <ID_DO_LOG>
ON CONFLICT (convenia_employee_id) DO UPDATE
  SET status = 'agendado', updated_at = NOW();
```

### 2.6 Teste isolado do Workflow Execução

```sql
INSERT INTO offboarding_processos
  (convenia_employee_id, nome, email, access_removal_date, scheduled_datetime, status)
VALUES ('TESTE-001','Colaborador Teste','conta.descartavel@mosten.com', CURRENT_DATE, NOW(), 'aprovado')
RETURNING id;
```

Executar o workflow manualmente informando `processo_id`, `nome`, `email`.

> ⚠️ Usar **conta M365 descartável**. O teste bloqueia o login e revoga as sessões de verdade.

Limpeza:

```sql
DELETE FROM offboarding_acoes     WHERE processo_id = <id>;
DELETE FROM offboarding_processos WHERE id = <id>;
```

### 2.7 Consultas de acompanhamento

```sql
-- Situação atual dos processos
SELECT id, nome, email, status, scheduled_datetime, aprovado_por, aprovado_em
FROM offboarding_processos ORDER BY id DESC LIMIT 20;

-- Ações de um processo (esperado: 9 linhas quando todos os ramos estiverem ativos)
SELECT sistema, status, executado_em, LEFT(detalhe, 120)
FROM offboarding_acoes WHERE processo_id = <id> ORDER BY sistema;

-- Pendências manuais em aberto
SELECT p.nome, a.sistema, a.executado_em, a.detalhe
FROM offboarding_acoes a JOIN offboarding_processos p ON p.id = a.processo_id
WHERE a.status = 'pendente_manual' ORDER BY a.executado_em DESC;
```

---
## 3. Configuração — nodes `PARAMETROS`

Não há `$env` nesta instância do n8n. Toda configuração vive em nodes Set chamados `PARAMETROS`, logo após o trigger, referenciados por `{{ $('PARAMETROS').first().json.campo }}`.

|Workflow|Campo|Valor atual|Pendência|
|---|---|---|---|
|Ingestão|`modo_diagnostico`|`true`|Virar `false` após validar|
|Ingestão|`convenia_webhook_secret`|`PREENCHER_`|Copiar da Convenia|
|Ingestão|`convenia_api_token`|`PREENCHER_`|Gerar na Convenia|
|Aprovação|`approver_email`|gustavo.brito@mosten.com|Definir aprovador de produção|
|Aprovação|`gep_notification_email`|gustavo.brito@mosten.com|Definir caixa do GeP|
|Execução|`ti_notification_email`|gustavo.brito@mosten.com|Definir caixa da TI|
|Execução|`gep_notification_email`|gustavo.brito@mosten.com|Definir caixa do GeP|
|Execução|`backup_delegate_email`|gustavo.brito@mosten.com|Definir política de backup|
|Execução|`ps_vm_url` / `ps_vm_api_key`|`PREENCHER_`|Provisionar VM|
|Execução|`azdo_org` / `azdo_pat`|`PREENCHER_`|Gerar PAT|
|Execução|`onfly_api_token`|`PREENCHER_`|Gerar token (expira em 1 ano)|

> 🔴 **Risco aceito e documentado:** segredos ficam em texto claro no JSON e **viajam em todo export**. Decisão consciente por indisponibilidade de acesso à infraestrutura do n8n. Interage com ISO/IEC 27001:2022 A.5.17 e A.8.24. Mitigações: não compartilhar exports fora da Mosten; rotacionar segredo se um export vazar; migrar para `$env` ou cofre quando houver acesso.

---
## 4. Premissas

Cada premissa é algo assumido que **ainda não foi confirmado empiricamente**. Enquanto não confirmada, o fluxo pode falhar silenciosamente.

|#|Premissa|Impacto se falsa|Como confirmar|
|---|---|---|---|
|P1|Assinatura da Convenia é HMAC-SHA256 hex, sem prefixo, no header `Signature`|Todo webhook rejeitado com 401|`offboarding_webhook_log.assinatura_valida`|
|P2|`$('Webhook Convenia').first().binary` expõe o raw body|HMAC calculado sobre bytes reserializados, pode divergir|`origem_body` no log|
|P3|`data.approved` é o caminho da resposta do Send and Wait|**Toda aprovação vira rejeição**|Output real do node `Solicitar Aprovação`|
|P4|`GET /employees/{id}` retorna `data.name` e `data.corporate_email`|`nome`/`email` vazios → 422|Chamada real à API|
|P5|`queryReplacement` aceita array via expressão|INSERT falha na ingestão|Primeiro webhook fora do diagnóstico|
|P6|`base64Encode()` existe nas expressões do n8n|Ramo E falha com 401|Teste do Ramo E|
|P7|Resposta da OnFly tem forma `{ data: [...] }`|Ramo F sempre cai em pendência manual|Doc + teste|
|P8|Node SSH retorna `exitCode` (ou `code`)|Ramo C loga falha mesmo com sucesso|Teste do Ramo C|
|P9|Erro com `onError: continue` chega em `$json.error`|IFs de sucesso/falha invertidos|Teste com e-mail inexistente|

### Confirmado pelo payload real (20/08/2026)

- `type` = `dismissal.finished` ✅ bate com o IF
- `employee.id` = UUID string ✅ compatível com `convenia_employee_id TEXT`
- `access_removal_date` no formato `AAAA-MM-DD` → **data pura, sem hora** ✅ `DateTime.fromISO` funciona
- O payload **não traz nome nem e-mail** → a chamada à API da Convenia é obrigatória, não opcional
- Campos extras disponíveis e ainda não usados: `dismissal_type`, `termination_notice`, `new_supervisor_id`, `motive`, `remove_benefit`

---
## 5. Restrições

|#|Restrição|Origem|
|---|---|---|
|R1|Sem `$env` e sem acesso para configurar|Infraestrutura|
|R2|Sem variáveis nativas do n8n (`$vars`)|Recurso Enterprise|
|R3|Conversão de caixa em compartilhada não existe no Graph|Limitação Microsoft — exige Exchange Online PowerShell|
|R4|InControl sem documentação pública de API|Fornecedor|
|R5|Qulture Rocks sem API pública|Fornecedor|
|R6|API do PontoMais é add-on pago não contratado|Decisão comercial pendente|
|R7|PSOffice sem API identificada|Fornecedor|
|R8|Bloqueio às 18h da data oficial, sem tolerância|Regra de negócio|
|R9|Exclusão só com match exato de 1 usuário|Segurança — proteção contra homônimo|
|R10|Aprovação humana obrigatória antes de qualquer revogação|Regra de negócio|

---
## 6. Dependências

### 6.1 Bloqueiam qualquer execução

- [ ] Credencial **OAuth2 (Graph)** selecionada em `Revogar Sessões M365`, `Bloquear Login M365`, `Conceder Acesso Delegado OneDrive`
- [ ] Credencial **Postgres** e **Microsoft Outlook** selecionadas em todos os nodes
- [ ] `convenia_webhook_secret` preenchido
- [ ] IDs de sub-workflow reselecionados após o import

### 6.2 Bloqueiam ramos específicos

|Ramo|Dependência|Responsável|
|---|---|---|
|B|VM com `pwsh` + `ExchangeOnlineManagement`, endpoint `POST /converter-caixa-compartilhada`|TI / Infra|
|B|RBAC `Exchange.ManageAsApp` + role assignment no App Registration|TI / M365|
|C|Validação manual dos comandos `pfSsh.php`|Gustavo|
|C|Credencial SSH com permissão mínima (não admin)|TI / Redes|
|D|Documentação da API InControl (ou decisão por RPA)|Fornecedor / TI|
|E|PAT do Azure DevOps + nome da organização|TI|
|F|Token OnFly|Administrador OnFly|

### 6.3 Decisões de negócio pendentes

- [ ] Aprovador oficial de produção (hoje: e-mail de teste)
- [ ] Caixa oficial do Gente & Performance
- [ ] Caixa oficial da TI
- [ ] Política de destinatário do backup de OneDrive/caixa
- [ ] Contratação (ou não) do add-on de API do PontoMais
- [ ] Política de expiração da aprovação (hoje: sem timeout — fica suspenso indefinidamente)

---
## 7. Pontos de atenção operacional

**Modo diagnóstico não registra processo.** Enquanto `modo_diagnostico = true`, o evento é logado mas o desligamento **não é agendado**. Se um desligamento real chegar nesse período, usar o reprocessamento da seção 2.5.

**O webhook chega antes da data de bloqueio.** `dismissal.finished` dispara quando o desligamento é concluído na Convenia; `access_removal_date` pode ser futuro. Receber o webhook hoje não significa bloquear hoje.

**Nada leva o status a `concluido`.** O processo fica em `em_execucao` até o Workflow Relatório existir.

**Sem timeout de aprovação.** Um e-mail não respondido deixa a execução suspensa para sempre.

**Ramos rodam em sequência interna.** Todo node de ação tem `onError: continue`. Ao criar ramos novos, manter a regra — sem ela, uma falha derruba os ramos seguintes.

**`Excluir Usuário pfSense` é destrutivo e não validado.** Recomendação: manter desabilitado (tecla `D`) até validar os comandos manualmente.

---
## 8. Changelog

|Versão|Data|Alterações|
|---|---|---|
|0.4|20/08/2026|Layout em espinha horizontal contínua; Ramos B–G desativados por padrão; alerta de import em workflow vazio|
|0.3|20/08/2026|Reorganização do canvas (zero sobreposições); confirmação do formato do payload real; runbook criado|
|0.2|20/08/2026|Trava de diagnóstico na Ingestão + tabela `offboarding_webhook_log`; `Verificar Assinatura` deixa de lançar exceção|
|0.1|20/08/2026|Eliminação de `$env` via nodes `PARAMETROS`; correção de 3 bugs P0; implementação dos Ramos B a G; sticky notes por bloco|
