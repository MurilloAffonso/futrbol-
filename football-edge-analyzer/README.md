# Football Edge Analyzer

Software de análise de apostas esportivas de futebol focado em **probabilidade, odd justa, valor esperado, normalização de dados e backtesting**.

Este projeto foi criado para começar o MVP agora, usando:

- dados autorizados do Flashscore ou exportações geradas pelo scraper enviado;
- upload/ingestão de JSON e CSV;
- cálculo matemático de probabilidade implícita, odd justa, EV e edge;
- classificação de oportunidades por valor esperado;
- backend FastAPI;
- frontend Next.js preparado para dashboard.

> O sistema não promete lucro. Ele classifica oportunidades segundo o modelo, com risco, variância e limitação de dados.

## Arquitetura

```text
football-edge-analyzer/
  backend/
    app/
      main.py
      core/
      data_providers/
      models/
      routers/
      schemas/
      services/
    tests/
  frontend/
    app/
    components/
    lib/
  data/
    samples/
  docs/
  integrations/
```

## Rodar backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse:

```text
http://127.0.0.1:8000/docs
```

## Rodar testes

```bash
cd backend
pytest
```

## Rodar frontend

```bash
cd frontend
npm install
npm run dev
```

## Fluxo recomendado do MVP

1. Gerar dados com o coletor autorizado ou usar `data/samples/flashscore_sample.json`.
2. Enviar o JSON para `POST /import/flashscore-json`.
3. Calcular oportunidade em `POST /analysis/value-bet`.
4. Rodar simulação em `POST /analysis/backtest`.
5. Evoluir para sincronização automática.

## Fórmulas

```text
probabilidade_implicita = 1 / odd
odd_justa = 1 / probabilidade_modelo
valor_esperado = (probabilidade_modelo * odd_oferecida) - 1
edge_percentual = ((odd_oferecida / odd_justa) - 1) * 100
```

## Integração Flashscore autorizada

O projeto não implementa evasão, bypass, rotação agressiva de proxy ou engenharia reversa. A integração fica isolada atrás da interface `BaseFootballDataProvider`.

Existem dois caminhos iniciais:

1. `FlashscoreScrapingJsonProvider`: lê arquivos JSON exportados pelo scraper Node/Playwright enviado.
2. `FlashscoreAuthorizedProvider`: stub para endpoint/feed/API autorizada com credenciais.


## OpenRouter / AI assistant

The backend includes an optional AI narrative layer using OpenRouter. By default it uses mock output for local development. To activate live model calls, configure the variables in `backend/.env.example` and set `OPENROUTER_ENABLED=true`.

Default model:

```text
poolside/laguna-m.1:free
```

Relevant endpoints:

- `POST /ai/explain-value-bet`
- `POST /ai/chat`

See `docs/openrouter-integration.md` for details and guardrails.

## Endpoints MVP
- GET /health
- POST/GET /teams
- POST/GET /matches
- GET /matches/{id}
- POST/GET /odds
- POST /analysis/value-bet
- POST /analysis/batch-value-bets
- GET /value-bets
- POST /imports/flashscore-json
- GET /imports
- GET /sync-logs
- POST /ai/explain-value-bet
- POST /ai/chat
