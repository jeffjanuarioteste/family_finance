# PRD – Sistema de Controle Financeiro Familiar

Versão 1.0 | Data: 21/11/2026 | Idioma: pt-BR | Origem: Documento de Análise v1.0

---

## 1. Resumo executivo

Aplicação web/PWA para uma família registrar e acompanhar gastos, ganhos, prioridades, metas e planos, com visão única e segmentada por membro. Responde cinco perguntas: **quanto tenho, quanto posso gastar, onde economizar, como ganhar mais, quando realizarei meus planos**.

## 2. Problema e oportunidade

Informações financeiras da família ficam dispersas (bancos, planilhas, anotações) e sem segmentação por pessoa. Não há visão consolidada de saldo livre, nem projeção de quando metas serão atingidas.

## 3. Objetivos e métricas de sucesso

| Objetivo | Métrica | Meta |
|---|---|---|
| Visão única do dinheiro | Contas e capital cadastrados | 100% das contas da família |
| Hábito de uso | Lançamentos por semana (ambos os cônjuges) | ≥ 10 por semana |
| Controle de orçamento | Categorias com orçamento definido | ≥ 80% dos gastos cobertos |
| Saber o saldo livre | Consulta ao dashboard "Quanto posso gastar" | ≥ 1x por semana |
| Planos concretos | Metas com aporte e data prevista | ≥ 3 ativas |
| Qualidade técnica | Lighthouse PWA; dashboards | ≥ 90; ≤ 3 s com 50 mil lançamentos |

**Não objetivos:** login individual por membro, pagamentos/transferências, emissão de NF ou IR, aconselhamento de investimento regulado, multi-família público, app nativo nas lojas (MVP).

## 4. Usuários e personas

| Persona | Perfil | Necessidades principais |
|---|---|---|
| Titular | Marido, iPhone, programador; dono do login | Configurar família, bancos, orçamentos; exportar relatórios; consultar saldo livre |
| Cônjuge | Esposa, Android, nail designer, renda variável | Lançar gastos/receitas, marcar contas pagas, acompanhar negócio extra |
| Membro filho(a) | Perfil sem login | Ter prioridades, necessidades e plano de faculdade atribuídos |
| Família | Pseudo-membro compartilhado | Registrar gastos comuns (mercado, aluguel, viagem) |

## 5. Premissas e restrições

- Uma conta (login único) = uma família (`familia_id`); sem login por membro.
- Backend FastAPI + MongoDB; frontend PWA mobile first.
- Valores em centavos (inteiro) + moeda; BRL como base; datas em UTC, fuso America/Sao_Paulo.
- Cotações de fonte pública gratuita (PTAX; cripto/ações a confirmar).
- Open Finance via agregador regulado (Pluggy/Belvo), custo a validar.
- Hospedagem em camada gratuita ou baixo custo.

## 6. Escopo

### 6.1 Dentro
21 módulos funcionais, 6 dashboards, entrada manual e Open Finance (leitura), multi-moeda, PWA (Android/iOS), notificações, offline básico, exportação PDF/Excel, segmentação por membro/Família.

### 6.2 Fora
Ver "Não objetivos" (seção 3).

## 7. Jornada principal

1. Titular cria conta e cadastra membros.
2. Cadastra contas/capital e moedas.
3. Conecta Open Finance (opcional) ou lança manualmente.
4. Define receitas, contas fixas e orçamentos.
5. Cadastra metas, planos e investimentos.
6. Sistema calcula saldo livre e aportes; exibe dashboards e alertas.
7. Ajusta via simulador; acompanha mensalmente e exporta relatórios.

## 8. Requisitos funcionais

Regras transversais (RN-TRV): todo registro tem `membro_id` ou "Família"; valores em centavos + moeda; exclusão lógica e auditoria; listagens paginadas com filtros por membro, período e status.

### 8.1 Épicos e módulos

| Épico | Módulo | Requisitos-chave | Prioridade |
|---|---|---|---|
| Fundação | Auth, família, membros, categorias | Login, sessões por dispositivo (máx. 5), PIN opcional, CRUD de membros | Must |
| Lançamentos | Lançamentos | CRUD, lote, idempotência, conversão de moeda, mesclagem | Must |
| Controle mensal | 16 Contas do mês | Recorrência automática, status atrasada, pagar gera lançamento, lembrete push | Must |
| Controle mensal | 15 Mercado | Registro diário, orçamento mensal, média diária, alerta 80%/100% | Must |
| Controle mensal | 19 Orçamento por categoria | Limite por categoria/membro/mês, consumo em tempo real, alertas, copiar mês anterior | Must |
| Controle mensal | 6 Posso gastar | Limites por categoria/membro, restante, alertas | Must |
| Controle mensal | 7 Todo mês | Checklist mensal automático, comprado gera lançamento | Must |
| Patrimônio | 9 Capital atual | Contas por membro, saldo manual/sincronizado, snapshot mensal, total por moeda | Must |
| Receita | 10 Profissão, 20 Outras receitas | Receita prevista mensal, renda variável (média 6 meses), previsto × realizado | Must |
| Dashboards MVP | 1 Fluxo de caixa, 2 Gastos, 6 Saldo livre | Filtros período/membro/moeda, ≤ 3 s | Must |
| Planejamento | 1 Prioridades, 2 Quero, 3 Preciso, 4 Consegui, 5 Economizar | CRUD, conversões entre módulos (desejo → plano, preciso → compra) | Should |
| Metas | 8 Planos, 12 Lazer, 13 Lugares, 18 Reserva | Aportes, aporte necessário, data prevista, progresso | Should |
| Patrimônio | 11 Investir, 17 Dívidas | Carteira, rentabilidade, cotação automática; parcelas e previsão de quitação | Should |
| Receita | 14 Negócio extra | Margem, lucro, ponto de equilíbrio, resultados por ciclo | Should |
| Dashboards | 3 Patrimônio, 4 Metas, 5 Ganhar mais | KPIs e alertas conforme análise | Should |
| Integração | Open Finance | Consentimento, sync a cada 6 h, deduplicação, categorização, revogação | Should |
| Exportação | Relatórios | Extrato, resumo mensal, orçamento × realizado, patrimônio, metas (PDF/Excel, ≤ 100 mil linhas) | Should |
| Análise | 21 Simulador | Cenários "e se", comparação base × cenário, aplicar com confirmação | Could |

Os campos, validações e requisitos detalhados (RF-MODxx-yy) de cada módulo estão no Documento de Análise, seção 4.

### 8.2 Regras de negócio essenciais

| ID | Regra |
|---|---|
| RN-001 | Saldo livre = receitas previstas − contas fixas − parcelas de dívidas − limites "posso gastar" − orçamento de mercado − itens todo mês − aportes de metas − aportes de investimento − reserva de lazer |
| RN-002 | Aporte necessário: sem juros `(alvo − acumulado)/meses`; com juros `PMT = (alvo − acumulado·(1+i)^n)·i/((1+i)^n − 1)` |
| RN-003 | Previsão de meta: `n = ceil(log((alvo·i+aporte)/(acumulado·i+aporte))/log(1+i))`; `i=0` → `ceil((alvo−acumulado)/aporte)` |
| RN-007 | Restante = limite − lançamentos da categoria no mês |
| RN-009 | Patrimônio líquido = contas + investimentos − dívidas (em BRL) |
| RN-012 | Meta da reserva = meta_meses × média de saídas dos últimos 3 meses |
| RN-014 | Alertas de orçamento uma vez por limite/mês |
| RN-015/016 | Job diário 00:05 gera recorrências sem duplicar; conta vencida pendente vira atrasada |
| RN-017 | Lançamentos gravam cotação na data; saldos/metas convertem pela cotação atual |
| RN-019 | Consolidado = membros + Família; visão do membro exclui Família salvo filtro |
| RN-021 | Sugestões de corte baseadas em dados (sem IA generativa no MVP) |

Demais regras (RN-004 a RN-022): ver Documento de Análise, seção 6.

## 9. Dashboards

| # | Dashboard | Foco | Fase |
|---|---|---|---|
| 1 | Saldo e fluxo de caixa | Entradas, saídas, saldo projetado, vencimentos | MVP |
| 2 | Gastos | Por categoria/membro, orçado × realizado | MVP |
| 6 | Quanto posso gastar | Saldo livre, cascata, sugestões de corte | MVP |
| 4 | Metas e planos | Progresso, aporte, meta em risco | Fase 2 |
| 3 | Capital e patrimônio | Evolução, carteira, dívidas | Fase 3 |
| 5 | Ganhar mais | Receitas, negócios, ponto de equilíbrio | Fase 3 |

## 10. Requisitos de plataforma e mobile

- PWA instalável em Android (Chrome) e iPhone (Safari ≥ 16.4): manifest, ícones (incl. maskable e apple-touch-icon), standalone, safe areas.
- Service worker: cache do shell e de leitura, fila offline de lançamentos (idempotente), aviso de nova versão.
- Push de vencimento e orçamento; fallback para notificações no app e e-mail.
- Sessões simultâneas (até 5), listáveis e revogáveis; controle otimista de versão; polling de 60 s.
- PIN local opcional, bloqueio após 1 min inativo; WebAuthn quando disponível.
- Tela de ajuda com passo a passo de instalação para iPhone e Android.
- Dados definitivos sempre no servidor.

## 11. Requisitos não funcionais

| Área | Requisito |
|---|---|
| Segurança | Argon2id; JWT 15 min com refresh rotativo; bloqueio após 5 falhas por 15 min; HTTPS/TLS 1.2+ e HSTS; rate limit 100 req/min/IP; CORS restrito; OWASP Top 10 |
| Privacidade | LGPD: consentimento, exportação e exclusão de dados; tokens Open Finance e campos sensíveis em AES-256 |
| Isolamento | Toda consulta filtrada por `familia_id` do token; teste automatizado de acesso cruzado |
| Auditoria | Log de criação/edição/exclusão retido por 12 meses |
| Desempenho | Listagens P95 ≤ 500 ms; dashboards ≤ 3 s com 50 mil lançamentos; carga inicial ≤ 3 s em 4G |
| Disponibilidade | 99% mensal; backup diário, retenção 7 dias, RPO 24 h, RTO 4 h |
| Acessibilidade/i18n | Contraste AA, alvos ≥ 44 px, pt-BR, `R$ 1.234,56`, `dd/mm/aaaa` |
| Qualidade PWA | Lighthouse PWA ≥ 90 |

## 12. Arquitetura e dados (resumo)

- **Backend:** FastAPI (async, Pydantic, OpenAPI), Beanie/Motor, MongoDB.
- **API:** REST `/api/v1`, JWT Bearer, paginação `page/page_size` (máx. 100), erros padronizados, `Idempotency-Key` em lançamentos, `POST /sync/lote` para fila offline.
- **Coleções principais:** familias, membros, contas, lancamentos, categorias, orcamentos, contas_mes, itens_planejamento, economias, itens_mensais, metas, investimentos, dividas, receitas_extras, negocios_extra, cenarios, conexoes_open_finance, cotacoes, notificacoes, dispositivos_push, sessoes, auditoria.
- **Modelagem:** embutir listas pequenas (aportes, checklist, resultados); referenciar entidades ilimitadas (lançamentos).
- **Índices-chave:** `lancamentos {familia_id, data:-1}`, único `{familia_id, id_externo}` esparso, único em orçamentos por categoria/membro/competência, TTL em sessões.

Detalhamento: Documento de Análise, seções 5 e 9.

## 13. Integrações

| Integração | Definição |
|---|---|
| Open Finance | Agregador regulado; sem armazenar credenciais bancárias; consentimento de 12 meses; sync a cada 6 h (primeira: 90 dias); deduplicação por `id_externo`; mesclagem manual confirmada; retentativa exponencial (3x); alertas de renovação 15 e 3 dias antes |
| Cotações | PTAX (fiat, diária); cripto/ações a cada 15 min com cache; última cotação válida em caso de falha |
| Exportação | PDF/Excel gerados sob demanda, não persistidos |

## 14. Distribuição

MVP: PWA em Android e iPhone (custo zero). Futuro: Google Play via TWA (US$ 25 único) se desejado; App Store (US$ 99/ano) apenas com necessidade nativa comprovada.

## 15. Roadmap

| Fase | Escopo | Prioridade |
|---|---|---|
| 0 Fundação | Auth, família, membros, categorias, PWA base, CI | Must |
| 1 MVP núcleo | Lançamentos, módulos 9, 16, 15, 19, 6, 7, 10, 20; dashboards 1, 2, 6; alertas/push; offline básico | Must |
| 2 Metas | Módulos 1–5, 8, 12, 13, 18; dashboard 4; multi-moeda e cotações | Must/Should |
| 3 Patrimônio e renda | Módulos 11, 17, 14; dashboards 3 e 5 | Should |
| 4 Integrações | Open Finance, exportação | Should |
| 5 Inteligência | Simulador, sugestões avançadas | Could |
| 6 Distribuição | Play Store, App Store | Won't (MVP) |

Open Finance pode subir para o MVP se o custo for aceito (D-01).

## 16. Critérios de aceite do MVP

- Titular cria conta, cadastra membros e acessa os mesmos dados em iPhone e Android.
- Filtros por membro e consolidado funcionam em todas as listagens e dashboards.
- PWA instala em Safari e Chrome e abre em tela cheia.
- Lançamentos offline sincronizam sem duplicidade.
- Contas e itens mensais gerados automaticamente; status atrasada correto.
- Alertas de vencimento e orçamento (80% e 100%) disparados.
- Saldo livre, aporte necessário e data prevista conferem com RN-001 a RN-003 em casos de teste.
- Multi-moeda grava cotação no lançamento.
- Dashboards 1, 2 e 6 em ≤ 3 s.
- Nenhum acesso entre famílias (teste automatizado).
- Sessões por dispositivo listadas e revogáveis.
- RNF-MOB atendidos e Lighthouse PWA ≥ 90; textos, datas e valores em pt-BR.

## 17. Riscos

| ID | Risco | Mitigação |
|---|---|---|
| RK-01 | Limitações do PWA no iOS | Dados no servidor; alertas no app; guia de instalação |
| RK-03 | Custo do agregador Open Finance | Opcional; manual é o fluxo principal |
| RK-04 | LGPD e dados sensíveis | Minimização, criptografia, consentimento, exclusão |
| RK-05 | Limites de hospedagem gratuita | Monitorar; migrar para plano pago pequeno |
| RK-06 | Cotações gratuitas instáveis | Cache e última cotação válida |
| RK-07 | Escopo de 21 módulos | Entrega faseada; coleções genéricas |
| RK-08 | Sem privacidade entre membros | PIN por membro (sugestão futura) |
| RK-09 | Perda de conta do titular | Recuperação por e-mail e exportação de backup |

## 18. Questões em aberto

| ID | Questão | Responsável / prazo |
|---|---|---|
| D-01 | Agregador Open Finance, custo aceito e obrigatoriedade no MVP | A definir antes da Fase 4 |
| D-02 | Fonte definitiva de cotações de cripto/ações | A definir antes da Fase 2 |
| D-03 | Provedor de hospedagem e orçamento de infraestrutura | A definir antes da Fase 0 |
| D-04 | Tratamento LGPD para dados de menores | A definir antes do MVP |
| D-05 | Categorias padrão iniciais | A definir antes da Fase 1 |

## 19. Ideias futuras (fora do escopo)

Leitura de QR Code de nota fiscal; PIN individual por membro; metas compartilhadas com divisão de aportes; resumo mensal por e-mail.

## 20. Referências

Documento de Análise – Sistema de Controle Financeiro Familiar v1.0 (módulos, modelo de dados, regras, API, RNFs e rastreabilidade completos).
