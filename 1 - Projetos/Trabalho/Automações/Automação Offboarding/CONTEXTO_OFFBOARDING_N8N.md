---
tags:
- tipo/trabalho/projeto/automaes
- API
- AWS
- Azure
- n8n
- Python
- SQL
---
# Contexto: Automação de Offboarding Mosten (Playbook 030/25) via n8n

> Documento de continuidade — gerado para retomar o projeto em outra conversa sem perder decisões já tomadas. Reflete o estado da conversa até a implementação parcial confirmada pelos JSONs dos Workflows 1, 2, 3 e parte do 4.

---
## 1. Objetivo do projeto

Automatizar o Playbook 030/25 (Bloqueio de Acessos e Devolução de Equipamentos — Offboarding) da Mosten Tecnologia via n8n, disparado a partir de um webhook da Convenia quando um desligamento é finalizado. A automação deve revogar/desativar o acesso do colaborador em 8 sistemas, fazer backup de dados M365, e reportar o resultado para a TI.

**Regra de negócio central:** bloqueio de acesso deve ocorrer na data de saída oficial (`access_removal_date` vindo da Convenia) **às 18h fixo**, sem tolerância de atraso — mas com um gate de aprovação manual antes da execução (fase de teste).

---
## 2. Sistemas envolvidos e status de integração

| Sistema | Ação | Viabilidade de API | Status de decisão |
|---|---|---|---|
| Microsoft 365 | Bloquear login + revogar sessões + backup (caixa compartilhada + delegação OneDrive) | Graph API — App Registration **já existe**, escopos confirmados incluindo `Mail.ReadWrite` | ✅ Fechado (Ramo A completo; Ramo B em revisão — ver seção 6) |
| pfSense | Excluir usuário VPN local | Sem API nativa — via SSH + `pfSsh.php` | ✅ Fechado (com validação anti-colisão de username) |
| InControl (Intelbras) | Excluir usuário controle de acesso físico | API existe mas documentação pública indisponível; hospedado on-premises (VM "Network Gateway", mesma rede do n8n) | ⏸️ Pendente — endpoints reais não confirmados, fallback manual |
| Azure DevOps | Remover da organização inteira | REST API confirmada (`Member Entitlement Management`) | ✅ Fechado |
| OnFly | Remover colaborador | API confirmada (`docs.api.onfly.com.br`), token expira em 1 ano | ✅ Fechado |
| Qulture Rocks | Desativar usuário | Sem API pública confirmada | ❌ 100% manual (fallback), sem tentativa de HTTP |
| PontoMais (SuperAppVR) | Desativar usuário | API existe mas é add-on pago no Marketplace, **não contratado pela Mosten** | ❌ 100% manual (fallback) |
| PSOffice | Desativar usuário | Nenhuma API identificada | ❌ 100% manual (fallback) |

**Fora do escopo desta fase:** GLPI (registro/encerramento de chamado), comunicação ao cliente.

---
## 3. Arquitetura geral — 5 workflows

```
1. [Offboarding] Ingestão   — Webhook Convenia → valida → grava em Postgres (status: agendado)
2. [Offboarding] Agendador  — Schedule Trigger (15 min) → busca vencidos → dispara Aprovação
3. [Offboarding] Aprovação  — Send and Wait (e-mail) → aprovado/rejeitado → dispara Execução
4. [Offboarding] Execução   — 7 ramos paralelos (M365, pfSense, InControl, Azure DevOps, OnFly, Qulture/PontoMais/PSOffice manual)
5. [Offboarding] Relatório  — (NÃO IMPLEMENTADO AINDA) verifica conclusão de todos os ramos + envia relatório final
```

Cada workflow é encadeado via **Execute Workflow / Execute Sub-workflow**, não por um único workflow monolítico — decisão tomada porque o intervalo entre "início do desligamento" e "data de saída" pode ser de semanas (aviso prévio), tornando arriscado segurar isso com um node `Wait`.

**Sem Merge final no Workflow 4:** os 7 ramos não convergem para um node comum — cada um termina gravando seu próprio resultado em `offboarding_acoes`. O Workflow 5 (ainda não construído) deve fazer polling nessa tabela para saber quando todos os sistemas de um processo já foram registrados, e então disparar o relatório.

---
## 4. Modelo de dados (Postgres) — já criado via Workflow 0 (Setup)

```sql
CREATE TABLE IF NOT EXISTS offboarding_processos (
    id                      SERIAL PRIMARY KEY,
    convenia_employee_id    TEXT NOT NULL,
    nome                    TEXT NOT NULL,
    email                   TEXT NOT NULL,
    access_removal_date     DATE NOT NULL,
    scheduled_datetime      TIMESTAMP NOT NULL,
    status                  TEXT NOT NULL DEFAULT 'agendado',
        -- agendado | aguardando_aprovacao | aprovado | rejeitado | em_execucao | concluido | concluido_com_pendencias
    aprovado_por            TEXT,
    aprovado_em             TIMESTAMP,
    convenia_raw_payload    JSONB,
    created_at              TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_offboarding_processos_employee ON offboarding_processos (convenia_employee_id);
CREATE INDEX IF NOT EXISTS ix_offboarding_processos_status_data ON offboarding_processos (status, scheduled_datetime);

CREATE TABLE IF NOT EXISTS offboarding_acoes (
    id              SERIAL PRIMARY KEY,
    processo_id     INTEGER NOT NULL REFERENCES offboarding_processos(id),
    sistema         TEXT NOT NULL,
        -- m365_bloqueio | m365_backup | pfsense | incontrol | azure_devops | qulture_rocks | pontomais | psoffice | onfly
    status          TEXT NOT NULL,
        -- sucesso | falha | pendente_manual
    detalhe         TEXT,
    executado_em    TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_offboarding_acoes_processo ON offboarding_acoes (processo_id);
```

Credencial Postgres já cadastrada no n8n: **"Postgres account automacoes_app"** (id `Vd5PY1QcwrdtuV1o`), reaproveitada em todos os workflows.

**Padrão obrigatório em todo Insert em `offboarding_acoes`:** nunca enviar o campo `id` (é `SERIAL`, autoincremento — mapear na coluna causa erro ou comportamento indesejado).

---
## 5. Workflow 1 — Ingestão (✅ implementado e validado contra o JSON real)

Webhook (`POST /webhook/offboarding/convenia`, raw body habilitado) → `Code` valida HMAC-SHA256 do header `Signature` contra `CONVENIA_WEBHOOK_SECRET` (padrão `spatie/laravel-webhook-client`: hex, sem prefixo) → `IF` assinatura válida → `IF` `body.type == "dismissal.finished"` → `HTTP Request` busca colaborador na Convenia (`GET /api/v3/employees/{id}`, header `token`) → `Set` normaliza dados (calcula `scheduled_datetime = access_removal_date + 18:00:00`) → `IF` e-mail e data presentes → `Postgres Insert` em `offboarding_processos` (`status: agendado`) → `Respond to Webhook` 200.

**🐛 Bug do typo `acess_removal_date` → CORRIGIDO** (confirmado no JSON): o node `Normalizar Dados` agora grava corretamente `access_removal_date`, batendo com o que o node de Insert lê.

**Pendências não resolvidas:**
- Confirmar se o payload real do webhook já traz e-mail corporativo (tornaria o HTTP Request de busca desnecessário).
- Confirmar nomes reais dos campos de resposta da Convenia (`data.name`, `data.corporate_email` são suposições).

---
## 6. Workflow 2 — Agendador (✅ implementado)

`Schedule Trigger` (15 min) → `Postgres` seleciona `WHERE status='agendado' AND scheduled_datetime <= NOW()` → `Split In Batches` (1 por vez) → `Postgres Update` (`status: aguardando_aprovacao`) → `Execute Workflow` chama `[Offboarding] Aprovação` (id `lcIxYFHhLVQq3DsB`), passando `processo_id`, `nome`, `email` → retorna ao loop.

Sem alterações pendentes conhecidas.

---
## 7. Workflow 3 — Aprovação (✅ implementado e validado contra o JSON real)

`Execute Workflow Trigger` (nomeado **`Quando Chamado pelo Workflow 2`** — campos: `processo_id` number, `nome`, `email`) → `Microsoft Outlook` node, operação **Send and Wait** (`sendAndWait`), credencial **"Microsoft account - Gustavo"** (OAuth2 delegado, ambiente de teste usando a conta pessoal do Gustavo como aprovador — `APPROVER_EMAIL = gustavo.brito@mosten.com`) → `IF` `{{ $json.data.approved }}` → aprovado: `Postgres Update status=aprovado` (`aprovado_por = {{ $env.APPROVER_EMAIL }}`) + `Execute Workflow` chama `[Offboarding] Workflow Execução` (id `NTV6xYJWdxv8I93U`) / rejeitado: `Postgres Update status=rejeitado` + `Microsoft Outlook` notifica GeP (`toRecipients = {{ $env.GEP_NOTIFICATION_EMAIL }}`).
**Pendências não resolvidas:**
- Sem timeout/expiração de aprovação implementado (decisão consciente do usuário: não trabalhar esse cenário agora, mas manter sinalizado).
- Quem é o aprovador em produção (hoje é só o Gustavo, em teste).

---
## 8. Workflow 4 — Execução (🔶 parcialmente implementado)

`Execute Workflow Trigger` → `Postgres Update status=em_execucao` → ramifica em paralelo para 7 ramos.

### Ramo A — M365 Bloqueio: ✅ **totalmente implementado e correto**
`HTTP Request POST /revokeSignInSessions` (OAuth2 API) → `HTTP Request PATCH accountEnabled:false` (OAuth2 API) → `IF` ambos sem erro → `Postgres Insert` log sucesso/falha (`sistema: m365_bloqueio`).

### Ramo B — M365 Backup: 🔶 **em revisão — decisão de arquitetura recém-fechada**
**Decisão final (após múltiplas rodadas de alternativas):** usar **Opção 1 — VM dedicada separada** (fora da VM que roda o n8n) para resolver a conversão de caixa compartilhada (`Set-Mailbox -Type Shared`), que **não tem equivalente no Graph API** (confirmado, sem alternativa até 2026 — só via Exchange Online PowerShell).

**Por que essa opção:** reaproveita um padrão que o usuário já tem em produção pessoal (VM Oracle Cloud Always Free + Cloudflare Tunnel, usada no bot Telegram/Google Calendar) — nenhum vínculo com Azure/AWS, controle total, familiaridade com o padrão.

**Desenho ainda não detalhado node a node** — próximo passo da conversa. Estrutura esperada:
- Uma VM separada (não a do n8n) com `pwsh` (PowerShell 7, multiplataforma) + módulo `ExchangeOnlineManagement` instalados, expondo um endpoint HTTP simples que recebe o e-mail e executa `Connect-ExchangeOnline` + `Set-Mailbox -Type Shared` + `Disconnect-ExchangeOnline`.
- O node no n8n vira um `HTTP Request` comum (não SSH, não Execute Command) apontando para essa VM — mantendo o mesmo padrão de todos os outros ramos.
- ✅ **Confirmado no JSON mais recente do Workflow 4:** o node SSH órfão `Converter Caixa Compartilhada` já não existe mais — foi removido do workflow, coerente com a troca de abordagem.
- Node `Conceder Acesso Delegado OneDrive` (Graph API puro, `POST /users/{email}/drive/root/invite`) **não muda**, nunca dependeu dessa decisão.

**Pendências:**
- Detalhar node a node o Ramo B completo com a Opção 1 (não feito ainda nesta conversa).
- Confirmar permissão RBAC do Exchange Online para o mecanismo de autenticação que a VM dedicada vai usar (`Exchange.ManageAsApp` + role assignment — mesma exigência independente de onde o PowerShell rodar).
- Definir e provisionar a VM dedicada (quem faz, onde hospedar, tamanho).
- Confirmar `BACKUP_DELEGATE_EMAIL` de produção (em teste é `gustavo.brito@mosten.com`).

**Histórico de decisão (para não repetir avaliação):** já foram descartadas as opções SSH+Python (dependia de um script `.py` de automação de RH cuja infraestrutura de hospedagem é desconhecida — usuário decidiu desconsiderar essa automação por completo), Execute Command local na VM do n8n (usuário pediu para não adicionar configuração na VM do n8n), Azure Function e Azure Automation (usuário pediu alternativas sem vínculo Azure).

### Ramo C — pfSense: ✅ desenhado (não confirmado se já implementado no n8n)
`SSH` lista usuários locais (`pfSsh.php`) → `Code` gera username (regra: `primeironome.ultimosobrenome`; se colidir com outra pessoa, usa `primeironome.nomedomeio`) e valida contra a lista real → `IF` exatamente 1 match → `SSH` exclui (`local_user_del`) → log sucesso/falha ou fallback manual (`Postgres` + `Send Email` para `TI_NOTIFICATION_EMAIL`).

### Ramo D — InControl: ⏸️ desenhado com placeholders, endpoints reais pendentes
`HTTP Request` login → busca por nome completo (**não e-mail** — sistemas de controle físico normalmente não usam e-mail como chave) → `IF` exatamente 1 resultado → exclui ou cai em fallback manual. URLs/portas ainda são placeholder (`INCONTROL_HOST`, `INCONTROL_PORT`).

### Ramo E — Azure DevOps: ✅ desenhado
`GET .../userentitlements?$filter=name eq '{email}'` (Basic Auth, senha=PAT) → `DELETE .../userentitlements/{id}` → log sucesso/falha ou fallback manual.

### Ramo F — OnFly: ✅ desenhado
`GET https://api.onfly.com.br/employees?email=...` (Header Auth Bearer) → `DELETE .../employees/{id}` → log sucesso/falha ou fallback manual.

### Ramo G — Qulture Rocks / PontoMais / PSOffice: ✅ desenhado (100% manual, sem tentativa de API)
`Code` gera 3 itens (um por sistema, com motivo) → `Postgres Insert` (`status: pendente_manual`) para cada um → `Aggregate` → `Send Email` único para `GEP_NOTIFICATION_EMAIL` listando os 3.

**Status real no JSON mais recente:** só o Ramo A está com nodes configurados de verdade (validado, sem bugs). Restam nodes `HTTP Request` vazios como placeholders para os demais ramos — nenhum dos ramos C a G tem parâmetros preenchidos ainda no n8n, e o Ramo B está zerado (órfão removido), aguardando o detalhamento node a node da Opção 1.

---
## 9. Workflow 5 — Verificador + Relatório Final: ❌ **NÃO INICIADO**

Desenho conceitual (não detalhado node a node ainda): `Schedule Trigger` faz polling em `offboarding_acoes` contando quantos sistemas já foram registrados por `processo_id`; quando atingir o total esperado (9 registros: m365_bloqueio, m365_backup, pfsense, incontrol, azure_devops, qulture_rocks, pontomais, psoffice, onfly), monta e envia relatório final por e-mail para TI, e atualiza `offboarding_processos.status` para `concluido` ou `concluido_com_pendencias` (se algum `pendente_manual`/`falha` existir).

---
## 10. Variáveis de ambiente — checklist consolidado

| Variável | Usada em | Status |
|---|---|---|
| `CONVENIA_WEBHOOK_SECRET` | Workflow 1 | Pendente de cadastro real no webhook da Convenia |
| `CONVENIA_API_TOKEN` | Workflow 1 | Pendente de geração na Convenia |
| `APPROVER_EMAIL` | Workflow 3 | Teste: `gustavo.brito@mosten.com` |
| `GEP_NOTIFICATION_EMAIL` | Workflow 3, Ramo G | A definir |
| `TI_NOTIFICATION_EMAIL` | Ramos C, D | A definir |
| `BACKUP_DELEGATE_EMAIL` | Ramo B | Teste: `gustavo.brito@mosten.com` |
| `INCONTROL_HOST`, `INCONTROL_PORT`, `INCONTROL_USER`, `INCONTROL_PASSWORD` | Ramo D | Pendente — API não documentada |
| `AZDO_ORG`, `AZDO_PAT` | Ramo E | PAT ainda não gerado |
| `ONFLY_API_TOKEN` | Ramo F | A gerar (expira em 1 ano) |
| (variável da VM dedicada do Ramo B, nome ainda não definido) | Ramo B | A definir junto do detalhamento pendente |

## 11. Credenciais n8n — checklist consolidado

| Credencial | Tipo | Status |
|---|---|---|
| Postgres account automacoes_app | Postgres | ✅ já criada (id `Vd5PY1QcwrdtuV1o`) |
| Microsoft account - Gustavo | OAuth2 (Outlook) | ✅ já criada (id `VFUb495HoR35JAwE`), usada em Send and Wait |
| OAuth2 App Registration M365 (Graph) | OAuth2 API | Já existe (reaproveitado do Faturas SaaS), escopos confirmados incluindo `Mail.ReadWrite` |
| SSH — pfSense | SSH | A criar, usuário com permissão restrita (não admin geral) |
| (credencial/endpoint da VM dedicada do Ramo B) | HTTP/a definir | A criar junto do detalhamento pendente |

---
## 12. Riscos e premissas ainda vigentes (não resolvidos)

1. **pfSense via SSH** é o node de maior risco operacional do workflow inteiro (acesso a firewall de produção) — usar usuário SSH com permissão mínima necessária.
2. **InControl usa nome completo como identificador**, não e-mail — risco de homônimos; desenho já mitiga exigindo match exato de 1 resultado, senão cai em fallback manual.
3. **Regra de derivação de username pfSense** (`primeironome.ultimosobrenome`, desempate por nome do meio em caso de sobrenome duplicado) foi confirmada pelo usuário, mas a validação real é feita comparando contra a lista de usuários existentes no pfSense (não apenas gerando e assumindo).
4. **Sem sandbox em nenhum sistema** — plano de teste definido: conta de teste descartável + flag de dry-run + teste isolado por sistema antes do ponta a ponta + rollout gradual (M365 → Azure DevOps/OnFly → pfSense/InControl → sistemas manuais).
5. **Sem timeout de aprovação implementado** — sinalizado, não resolvido, usuário decidiu não tratar agora.
6. **PontoMais**: API é add-on pago não contratado — decisão de negócio necessária caso queiram automatizar no futuro.
7. Campos de retorno reais de vários nodes (SSH `exitCode`/`stdout`, Aggregate, resposta da Convenia) foram **assumidos com base em padrões comuns do n8n**, não confirmados em teste real — todos sinalizados com ⚠️ nas respostas originais, precisam validação empírica.
8. Workflow "Infra - Notificar Erro" (já existente, reaproveitado do projeto Faturas SaaS) — **campos de entrada esperados por ele nunca foram confirmados** nesta conversa; necessário abrir esse workflow e verificar antes de conectar os fallbacks de erro do Workflow 4 a ele.

---
## 13. Estilo de trabalho combinado nesta conversa (para manter consistência)

- Construção **um workflow por vez**, avançando só depois que o anterior é implementado/testado pelo usuário.
- Para cada node: **Tipo**, **Por que esse tipo**, **Configuração campo a campo**, **O que ele faz**, e ⚠️ pendências/premissas explícitas — nunca preencher lacunas com suposição não sinalizada.
- Regra inegociável do usuário, repetida várias vezes: **não presumir, inventar ou alucinar** — inclusive sobre o conteúdo de arquivos já lidos anteriormente na conversa (esse documento já corrigiu 2 alucinações anteriores sobre o conteúdo do script `.py` de RH, que foi descartado como referência de implementação).
- Ao propor uma solução técnica nova (ex.: Ramo B), apresentar **alternativas comparadas** antes de implementar, e só detalhar node a node depois que o usuário escolhe explicitamente.

---
## 14. Próximo passo imediato

Detalhar o Ramo B do Workflow 4 (M365 Backup) node a node, já usando a **Opção 1 (VM dedicada separada)** confirmada pelo usuário — este é o item que estava em aberto quando este documento foi gerado.
