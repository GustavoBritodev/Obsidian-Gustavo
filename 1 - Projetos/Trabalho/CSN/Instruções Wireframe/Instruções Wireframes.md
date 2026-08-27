---
tags:
  - tipo/trabalho/projeto/csn
---
| Etapa                    | Requisitos cobertos                    |
| ------------------------ | -------------------------------------- |
| 1 — Pesquisa por BL      | ENT-04, ENT-05, ENT-10                 |
| 2 — Dados da Carga       | ENT-06, ENT-07, ENT-08, ENT-09, ENT-10 |
| 3 — Transporte + SILOG   | ENT-11, ENT-12, GEN-02                 |
| 4 — Janela + Finalização | ENT-13, ENT-14, GEN-04                 |

**Comportamentos validados via mock:**

- `BL-VALIDO-01` / `BL-VALIDO-02` → sucesso com 2 itens e saldo dinâmico (nunca abaixo de zero — ENT-07)
- Qualquer outro BL → toast de erro vermelho
- Placa `ABC-1234` → erro bloqueante SILOG (ENT-12)
- Placa `ERR-0000` → falha técnica de comunicação (GEN-02)
- Botão "Confirmar Agendamento" desabilitado imediatamente (GEN-04), spinner de 2s e overlay de sucesso com Ticket ID aleatório