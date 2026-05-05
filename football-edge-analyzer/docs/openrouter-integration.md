# OpenRouter / Laguna M.1 Integration

This project includes an optional AI narrative layer powered by OpenRouter.

## Purpose

The mathematical engine is the source of truth. The AI layer only turns structured analysis into a readable explanation for the dashboard.

Use cases:

- explain why a value bet was classified as strong, moderate, weak, or not qualified;
- summarize risks in plain Portuguese;
- answer contextual questions using already-calculated match data;
- generate analyst-style commentary for a report.

The AI layer must never place bets, promise profit, or override the quantitative engine.

## Default model

The default model is:

```text
poolside/laguna-m.1:free
```

The PDFs supplied for the project show Laguna M.1 as a free OpenRouter model with a large context window and software-engineering orientation. They also show OpenRouter quickstart examples using the model id `poolside/laguna-m.1:free`.

## Environment variables

```env
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=
OPENROUTER_MODEL=poolside/laguna-m.1:free
OPENROUTER_ENABLED=false
OPENROUTER_TIMEOUT_SECONDS=30
OPENROUTER_SITE_URL=http://localhost:3000
OPENROUTER_APP_TITLE=Football Edge Analyzer
```

Set `OPENROUTER_ENABLED=true` and provide `OPENROUTER_API_KEY` to activate live calls.

Without an API key, the backend returns deterministic local mock output. This is intentional for tests and local development.

## Endpoints

### POST `/ai/explain-value-bet`

Generates a narrative for a structured value-bet analysis.

Example request:

```json
{
  "match_name": "Roma vs Vitoria",
  "market": "Over 2.5 gols",
  "selection": "Over 2.5",
  "model_probability": 0.57,
  "offered_odd": 2.22,
  "fair_odd": 1.75,
  "expected_value": 0.2654,
  "edge_percentage": 26.54,
  "confidence_score": 72,
  "contextual_factors": ["Pressao ofensiva acima da media", "Mandante com bom volume de finalizacoes"],
  "risk_factors": ["Amostra limitada", "Possivel rotacao de elenco"]
}
```

### POST `/ai/chat`

Answers a question using the structured context passed by the frontend.

## Guardrails

The system prompt requires the model to:

- answer in Brazilian Portuguese;
- avoid promises of profit;
- distinguish probability, fair odd, offered odd, EV, risk, and variance;
- state when data is insufficient;
- avoid exposing chain-of-thought or hidden reasoning;
- provide conclusion, concise justification, and risks only.

## Architecture

```text
Quantitative engine
        ↓
Structured analysis JSON
        ↓
OpenRouterService
        ↓
AI narrative
        ↓
Dashboard / report
```

Keep `OpenRouterService` optional and isolated. No core calculation should depend on AI availability.
