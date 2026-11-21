# PAD – Plano de Ação e Desenvolvimento
Sistema de Controle Financeiro Familiar | Versão 1.0 | 21/11/2026 | pt-BR
Origem: Documento de Análise v1.0 e PRD v1.0

Hierarquia: **ÉPICO (EP) → ESTÓRIA (US) → TAREFA (T)**.
Prioridade: M = Must, S = Should, C = Could, W = Won't (MVP).
Critério geral de pronto (DoD): código revisado, testes automatizados, filtro por `familia_id` aplicado, textos/datas/valores em pt-BR, documentação OpenAPI atualizada.

## Visão geral

| Épico | Nome | Fase | Prior. |
|---|---|---|---|
| EP-00 | Fundação e infraestrutura | 0 | M |
| EP-01 | Autenticação, família e membros | 0 | M |
| EP-02 | PWA base, offline e notificações | 0/1 | M |
| EP-03 | Lançamentos e categorias | 1 | M |
| EP-04 | Contas e capital (mód. 9) | 1 | M |
| EP-05 | Controle mensal (mód. 16, 15, 19, 6, 7) | 1 | M |
| EP-06 | Receitas (mód. 10, 20) | 1 | M |
| EP-07 | Dashboards MVP (1, 2, 6) | 1 | M |
| EP-08 | Planejamento pessoal (mód. 1–5) | 2 | S |
| EP-09 | Metas e planos (mód. 8, 12, 13, 18) e multi-moeda | 2 | M/S |
| EP-10 | Patrimônio e renda extra (mód. 11, 17, 14) | 3 | S |
| EP-11 | Open Finance | 4 | S |
| EP-12 | Exportação de relatórios | 4 | S |
| EP-13 | Simulador de cenários (mód. 21) | 5 | C |
| EP-14 | Segurança, LGPD e qualidade (transversal) | 0–5 | M |
| EP-15 | Distribuição em lojas | 6 | W |

---

## EP-00 – Fundação e infraestrutura (Fase 0)

**US-00.01 – Como desenvolvedor, quero o projeto estruturado para entregar com padrão.**
- T-00.01.01 Definir provedor de hospedagem e orçamento (D-03).
- T-00.01.02 Criar repositórios (backend FastAPI, frontend PWA) e convenções de branch/commit.
- T-00.01.03 Configurar FastAPI + Pydantic + Beanie/Motor e conexão MongoDB Atlas.
- T-00.01.04 Configurar variáveis de ambiente e secrets (chave AES, JWT).
- T-00.01.05 Criar camada base: modelo com campos comuns (`familia_id`, `membro_id`, `criado_em`, `atualizado_em`, `deletado_em`, `observacao`), soft delete e versão otimista.
- T-00.01.06 Implementar paginação, filtros, ordenação e formato padrão de erros (seção 9.1).

**US-00.02 – Como equipe, quero CI/CD para publicar com segurança.**
- T-00.02.01 Pipeline de lint, testes e build (backend e frontend).
- T-00.02.02 Deploy automático em ambiente de homologação com HTTPS.
- T-00.02.03 Rotina de backup diário MongoDB (retenção 7 dias) e checklist de restauração.

**US-00.03 – Como desenvolvedor, quero o jobs agendados disponíveis.**
- T-00.03.01 Escolher e configurar scheduler (ex.: APScheduler) com execução às 00:05.
- T-00.03.02 Criar estrutura de jobs idempotentes com log.

---

## EP-01 – Autenticação, família e membros (Fase 0)

**US-01.01 – Como titular, quero criar conta e fazer login.**
- T-01.01.01 `POST /auth/registrar` com hash Argon2id e e-mail único.
- T-01.01.02 `POST /auth/login`, JWT de 15 min e refresh rotativo.
- T-01.01.03 Bloqueio após 5 falhas por 15 min.
- T-01.01.04 `POST /auth/refresh` e `POST /auth/logout`.
- T-01.01.05 Recuperação de senha por e-mail (RK-09).
- T-01.01.06 Telas de cadastro, login e recuperação.

**US-01.02 – Como titular, quero gerenciar sessões por dispositivo.**
- T-01.02.01 Coleção `sessoes` com TTL e limite de 5 sessões.
- T-01.02.02 `GET /auth/sessoes` e `DELETE /auth/sessoes/{id}`.
- T-01.02.03 Tela de sessões com revogação.

**US-01.03 – Como titular, quero PIN local opcional.**
- T-01.03.01 `POST /auth/pin` (hash).
- T-01.03.02 Tela de bloqueio após 1 min de inatividade (configurável).
- T-01.03.03 Suporte a WebAuthn quando disponível.

**US-01.04 – Como titular, quero cadastrar membros e a família.**
- T-01.04.01 `GET/PATCH /familia` (moeda base, configurações).
- T-01.04.02 CRUD `/membros` (nome, papel, cor, profissão embutida).
- T-01.04.03 Pseudo-membro "Família" e seletor global de membro (individual/Família/consolidado – RN-019).
- T-01.04.04 Telas de membros e onboarding.

**US-01.05 – Como titular, quero que dados de outra família sejam inacessíveis.**
- T-01.05.01 Extrair `familia_id` do token em todas as consultas (middleware/dependência).
- T-01.05.02 Teste automatizado de acesso cruzado (RNF-007).

---

## EP-02 – PWA base, offline e notificações (Fases 0/1)

**US-02.01 – Como usuário, quero instalar o app no iPhone e Android.**
- T-02.01.01 `manifest.webmanifest` e ícones (192, 512, maskable, apple-touch-icon 180).
- T-02.01.02 Metatags iOS e `viewport-fit=cover` com safe areas.
- T-02.01.03 Layout mobile first, alvos ≥ 44 px, contraste AA.
- T-02.01.04 Tela de ajuda com passo a passo de instalação (iPhone/Android).

**US-02.02 – Como usuário, quero usar o app offline.**
- T-02.02.01 Service worker: cache do shell e leitura de dados recentes.
- T-02.02.02 Fila offline de lançamentos com UUID de cliente e `Idempotency-Key`.
- T-02.02.03 `POST /sync/lote` no backend.
- T-02.02.04 Indicador de pendências de sincronização.
- T-02.02.05 Aviso "nova versão disponível" e atualização do SW.

**US-02.03 – Como usuário, quero ver mudanças feitas em outro aparelho.**
- T-02.03.01 Atualização ao voltar o foco e polling de 60 s.
- T-02.03.02 Tratamento de conflito por versão com aviso.

**US-02.04 – Como usuário, quero receber alertas.**
- T-02.04.01 Coleções `notificacoes` e `dispositivos_push`.
- T-02.04.02 `POST /push/assinaturas`, envio Web Push (VAPID).
- T-02.04.03 Central de notificações no app, `PATCH /notificacoes/{id}/lida`.
- T-02.04.04 Fallback por e-mail e alertas dentro do app (iOS).

---

## EP-03 – Lançamentos e categorias (Fase 1)

**US-03.01 – Como usuário, quero gerenciar categorias.**
- T-03.01.01 Definir categorias padrão (D-05).
- T-03.01.02 CRUD `/categorias` com hierarquia e seed inicial.
- T-03.01.03 Tela de categorias.

**US-03.02 – Como usuário, quero registrar entradas e saídas.**
- T-03.02.01 Modelo `lancamentos` e índices (seção 5.3).
- T-03.02.02 CRUD `/lancamentos` com `Idempotency-Key`.
- T-03.02.03 `POST /lancamentos/lote`.
- T-03.02.04 Formulário rápido de lançamento (valor, categoria, membro, conta, data).
- T-03.02.05 Listagem com filtros por membro, período, categoria, conta e status.

**US-03.03 – Como usuário, quero lançamentos em outra moeda.**
- T-03.03.01 Serviço de cotações: PTAX diária e coleção `cotacoes`.
- T-03.03.02 Gravar `cotacao_na_data` e `valor_base_centavos` (RN-017).
- T-03.03.03 Fallback para última cotação com aviso.

**US-03.04 – Como usuário, quero mesclar lançamentos duplicados.**
- T-03.04.01 `POST /lancamentos/{id}/mesclar`.
- T-03.04.02 Tela de sugestão de mesclagem (conta, valor igual, data ±2 dias).

**US-03.05 – Como titular, quero trilha de auditoria.**
- T-03.05.01 Registrar criação/edição/exclusão em `auditoria` (antes/depois, dispositivo).
- T-03.05.02 Retenção de 12 meses.

---

## EP-04 – Contas e capital (Módulo 9, Fase 1)

**US-04.01 – Como titular, quero cadastrar contas por membro.**
- T-04.01.01 CRUD `/contas` (tipo, moeda, instituição, origem de dados).
- T-04.01.02 Tela de contas com total por moeda e convertido em BRL.

**US-04.02 – Como usuário, quero atualizar saldos.**
- T-04.02.01 `POST /contas/{id}/saldo` (manual).
- T-04.02.02 Snapshot mensal em `saldos_historico`.
- T-04.02.03 `GET /contas/patrimonio`.

---

## EP-05 – Controle mensal (Fase 1)

**US-05.01 – Contas do mês (módulo 16).**
- T-05.01.01 CRUD `/contas-mes` com recorrência e lembrete (padrão 3 dias).
- T-05.01.02 Job de geração mensal sem duplicar (`recorrencia_id + competencia`, RN-015).
- T-05.01.03 Job que marca `atrasada` (RN-016).
- T-05.01.04 `POST /contas-mes/{id}/pagar` gerando lançamento de saída.
- T-05.01.05 `GET /contas-mes/a-vencer` e push de lembrete.
- T-05.01.06 Telas: lista do mês, pagar, criar recorrência.

**US-05.02 – Mercado (módulo 15).**
- T-05.02.01 Configuração de orçamento mensal de mercado.
- T-05.02.02 Registro diário rápido (gera lançamento categoria "Mercado").
- T-05.02.03 `GET /mercado/resumo` (total, restante, média diária, comparativo).
- T-05.02.04 Tela de mercado e alertas 80%/100%.

**US-05.03 – Orçamento por categoria (módulo 19).**
- T-05.03.01 CRUD `/orcamentos` com índice único categoria/membro/competência.
- T-05.03.02 Cálculo de consumido/restante em tempo real (RN-007).
- T-05.03.03 Serviço de alertas por `alerta_pcts`, uma vez por limite/mês (RN-014).
- T-05.03.04 `POST /orcamentos/copiar` e `GET /orcamentos/status`.
- T-05.03.05 Telas de orçamento.

**US-05.04 – Posso gastar (módulo 6).**
- T-05.04.01 CRUD `/limites-gasto` e vínculo de lançamentos.
- T-05.04.02 `GET /limites-gasto/resumo?competencia=`.
- T-05.04.03 Alertas 80%/100% e telas.

**US-05.05 – Todo mês (módulo 7).**
- T-05.05.01 CRUD `/itens-mensais` com checklist embutido.
- T-05.05.02 Job de geração do checklist no dia 1º.
- T-05.05.03 `PATCH /itens-mensais/{id}/checklist/{competencia}` gerando lançamento.
- T-05.05.04 Tela de checklist (estimado × real).

---

## EP-06 – Receitas (Fase 1)

**US-06.01 – Profissão (módulo 10).**
- T-06.01.01 CRUD `/profissoes` por membro (renda fixa/variável).
- T-06.01.02 Geração de receita prevista mensal.
- T-06.01.03 `POST /profissoes/{id}/renda-realizada` e média de 6 meses.
- T-06.01.04 Telas.

**US-06.02 – Outras receitas (módulo 20).**
- T-06.02.01 CRUD `/receitas-extras`.
- T-06.02.02 `POST /receitas-extras/{id}/receber` gerando lançamento de entrada.
- T-06.02.03 Comparativo previsto × realizado e telas.

---

## EP-07 – Dashboards MVP (Fase 1)

**US-07.01 – Filtros comuns.**
- T-07.01.01 Componente de filtro: período, membro, moeda de exibição.
- T-07.01.02 Agregações MongoDB com índices e cache; teste de carga com 50 mil lançamentos (≤ 3 s).

**US-07.02 – Dashboard 1: Saldo e fluxo de caixa.**
- T-07.02.01 `GET /dashboards/fluxo-caixa` (entradas, saídas, saldo, projetado RN-013, vencimentos).
- T-07.02.02 Gráficos e alertas (saldo projetado negativo, conta atrasada).

**US-07.03 – Dashboard 2: Gastos.**
- T-07.03.01 `GET /dashboards/gastos` (categoria, membro, média diária, orçado × realizado).
- T-07.03.02 Gráficos (rosca, barras, linha) e alertas.

**US-07.04 – Dashboard 6: Quanto posso gastar.**
- T-07.04.01 Cálculo do saldo livre (RN-001) e por dia restante.
- T-07.04.02 Sugestões de corte baseadas em dados (RN-021).
- T-07.04.03 `GET /dashboards/saldo-livre`, cascata e alerta de saldo ≤ 0.
- T-07.04.04 Testes com casos de referência.

---

## EP-08 – Planejamento pessoal (Módulos 1–5, Fase 2)

**US-08.01 – Prioridades (1).**
- T-08.01.01 CRUD `/prioridades` (nível, prazo, recorrência) em `itens_planejamento`.
- T-08.01.02 Ordenação e destaque de atrasadas; telas.

**US-08.02 – Coisas que quero (2).**
- T-08.02.01 CRUD `/desejos` e total por membro.
- T-08.02.02 `POST /desejos/{id}/converter` (RN-020).

**US-08.03 – Coisas que preciso (3).**
- T-08.03.01 CRUD `/necessidades` ordenado por urgência.
- T-08.03.02 `POST /necessidades/{id}/comprar` com confirmação gerando lançamento.

**US-08.04 – Coisas que já consegui (4).**
- T-08.04.01 CRUD `/conquistas` e linha do tempo por membro.
- T-08.04.02 Sugestão automática ao concluir prioridade, desejo, plano ou dívida.

**US-08.05 – Economizar (5).**
- T-08.05.01 CRUD `/economias` e cálculo (RN-008).
- T-08.05.02 `GET /economias/{id}/historico` e telas.

---

## EP-09 – Metas, planos e multi-moeda (Fase 2)

**US-09.01 – Planos futuros (8).**
- T-09.01.01 Modelo `metas` com `tipo` e `aportes[]`.
- T-09.01.02 Funções RN-002, RN-003 e RN-004 com testes unitários.
- T-09.01.03 CRUD `/metas`, `POST /metas/{id}/aportes`, `GET /metas/{id}/projecao`.
- T-09.01.04 Telas (cartões, progresso, projeção) e sugestão de "Consegui" ao 100%.

**US-09.02 – Lugares (13).**
- T-09.02.01 Metas tipo `viagem` com participantes e moeda estrangeira.
- T-09.02.02 Telas.

**US-09.03 – Reserva de emergência (18).**
- T-09.03.01 Meta em meses, média de saídas 3 meses (RN-012), cobertura.
- T-09.03.02 Vínculo de contas/investimentos e telas.

**US-09.04 – Lazer (12).**
- T-09.04.01 CRUD `/lazer`, reserva mensal (RN-018) e avanço de ciclo.
- T-09.04.02 Telas.

**US-09.05 – Cotações multi-moeda.**
- T-09.05.01 Definir fonte de cripto/ações (D-02).
- T-09.05.02 Job de cotações (15 min com cache) e `GET /cotacoes`.
- T-09.05.03 Conversão de saldos e metas pela cotação atual.

**US-09.06 – Dashboard 4: Metas e planos.**
- T-09.06.01 `GET /dashboards/metas` e alerta de meta em risco.
- T-09.06.02 Telas.

---

## EP-10 – Patrimônio e renda extra (Fase 3)

**US-10.01 – Investir (11).**
- T-10.01.01 CRUD `/investimentos` com aportes e `GET /investimentos/carteira`.
- T-10.01.02 Rentabilidade (RN-010) e atualização por cotação.
- T-10.01.03 Meta mensal × realizado e telas.

**US-10.02 – Dívidas (17).**
- T-10.02.01 CRUD `/dividas`, previsão de quitação (RN-011).
- T-10.02.02 `POST /dividas/{id}/pagar-parcela` gerando conta do mês.
- T-10.02.03 Registro de conquista ao quitar e telas.

**US-10.03 – Negócio extra (14).**
- T-10.03.01 CRUD `/negocios-extra`, margem e ponto de equilíbrio (RN-005/006).
- T-10.03.02 `POST /negocios-extra/{id}/resultados` e `GET /negocios-extra/{id}/analise`.

**US-10.04 – Dashboards 3 e 5.**
- T-10.04.01 Patrimônio líquido (RN-009), snapshots e evolução; alertas de saldo desatualizado.
- T-10.04.02 Ganhar mais (receitas, negócios, previsto × realizado).

---

## EP-11 – Open Finance (Fase 4)

**US-11.01 – Como titular, quero conectar bancos.**
- T-11.01.01 Decidir agregador e custo (D-01); POC.
- T-11.01.02 `POST /open-finance/conexoes` (consentimento) e retorno.
- T-11.01.03 Armazenar tokens criptografados (AES-256).
- T-11.01.04 Vincular contas importadas ao membro.
- T-11.01.05 `DELETE /conexoes/{id}` (revogação).

**US-11.02 – Como usuário, quero importar sem duplicar.**
- T-11.02.01 Job de sincronização a cada 6 h e `POST /conexoes/{id}/sincronizar`.
- T-11.02.02 Idempotência por `id_externo` (RN-022).
- T-11.02.03 Sugestão de mesclagem com lançamentos manuais.
- T-11.02.04 Webhook `/open-finance/webhook`.

**US-11.03 – Como usuário, quero categorização automática.**
- T-11.03.01 Regras por palavra-chave e aprendizado por correção.

**US-11.04 – Como titular, quero tratamento de falhas e renovação.**
- T-11.04.01 Retentativa exponencial (3x) e status `erro`.
- T-11.04.02 Alertas 15 e 3 dias antes da expiração.

---

## EP-12 – Exportação de relatórios (Fase 4)

**US-12.01 – Como titular, quero exportar relatórios.**
- T-12.01.01 `GET /relatorios/{tipo}?formato=` com limite de 100 mil linhas.
- T-12.01.02 Extrato (Excel/PDF).
- T-12.01.03 Resumo mensal (PDF).
- T-12.01.04 Orçamento × realizado (Excel/PDF).
- T-12.01.05 Patrimônio (PDF) e Metas e planos (PDF/Excel).
- T-12.01.06 Tela de exportação.

---

## EP-13 – Simulador de cenários (Fase 5)

**US-13.01 – Como usuário, quero simular "e se".**
- T-13.01.01 CRUD `/cenarios` com ajustes e horizonte 1–120 meses.
- T-13.01.02 `POST /cenarios/{id}/simular` sem alterar dados reais.
- T-13.01.03 Comparativo base × cenário (saldo livre, datas das metas).

**US-13.02 – Como usuário, quero aplicar um cenário.**
- T-13.02.01 `POST /cenarios/{id}/aplicar` com confirmação.
- T-13.02.02 Telas do simulador.

**US-13.03 – Sugestões de corte avançadas.**
- T-13.03.01 Evoluir RN-021 com novas heurísticas.

---

## EP-14 – Segurança, LGPD e qualidade (transversal)

**US-14.01 – Segurança da aplicação.**
- T-14.01.01 HTTPS/TLS 1.2+, HSTS e cabeçalhos de segurança.
- T-14.01.02 Rate limit 100 req/min/IP e CORS restrito.
- T-14.01.03 Revisão OWASP Top 10 por fase.
- T-14.01.04 Criptografia de campos sensíveis.

**US-14.02 – LGPD.**
- T-14.02.01 Política de privacidade e registro de consentimento.
- T-14.02.02 Exportação e exclusão de dados da família.
- T-14.02.03 Definir tratamento de dados de menores (D-04).

**US-14.03 – Qualidade e desempenho.**
- T-14.03.01 Testes de carga (listagens P95 ≤ 500 ms; dashboards ≤ 3 s).
- T-14.03.02 Lighthouse PWA ≥ 90 e carga inicial ≤ 3 s em 4G.
- T-14.03.03 Testes em Safari/iOS ≥ 16.4 e Chrome/Android.
- T-14.03.04 Monitoramento, alertas e meta de 99% de disponibilidade.
- T-14.03.05 Teste de restauração de backup trimestral.

---

## EP-15 – Distribuição em lojas (Fase 6, fora do MVP)

**US-15.01 – Google Play via TWA.**
- T-15.01.01 Gerar AAB (Bubblewrap/PWABuilder) e `assetlinks.json`.
- T-15.01.02 Conta Play (US$ 25), ficha, Data Safety e teste fechado.

**US-15.02 – App Store (somente com necessidade nativa).**
- T-15.02.01 Empacotar com Capacitor e recursos nativos (push/biometria).
- T-15.02.02 Conta Apple (US$ 99/ano) e submissão.

---

## Marcos de entrega

| Marco | Épicos | Critério de saída |
|---|---|---|
| M0 – Fundação | EP-00, EP-01, EP-02 (base), EP-14 (base) | Login, membros, PWA instalável, CI |
| M1 – MVP | EP-03 a EP-07 | Critérios de aceite do MVP (PRD seção 16) |
| M2 – Metas | EP-08, EP-09 | Metas com aporte/data prevista; multi-moeda |
| M3 – Patrimônio | EP-10 | Dashboards 3 e 5 |
| M4 – Integrações | EP-11, EP-12 | Open Finance idempotente; relatórios |
| M5 – Inteligência | EP-13 | Simulador funcional |

## Dependências principais
- EP-03 depende de EP-00/EP-01; EP-04 a EP-07 dependem de EP-03.
- EP-09 depende de EP-03 e do serviço de cotações (US-03.03).
- EP-10 depende de EP-04 e EP-09; EP-13 depende de EP-05 a EP-10.
- EP-11 depende de EP-03 e EP-04.

## Decisões pendentes que bloqueiam tarefas
| ID | Decisão | Bloqueia |
|---|---|---|
| D-01 | Agregador Open Finance e custo | T-11.01.01 |
| D-02 | Fonte de cripto/ações | T-09.05.01 |
| D-03 | Hospedagem e orçamento | T-00.01.01 |
| D-04 | LGPD de menores | T-14.02.03 |
| D-05 | Categorias padrão | T-03.01.01 |
