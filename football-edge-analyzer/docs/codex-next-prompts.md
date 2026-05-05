# Prompts para continuar no Codex

## Prompt 1 - Persistência em banco

Implemente persistência real no backend usando SQLAlchemy e SQLite.
Crie tabelas para teams, matches, match_statistics, odds_quotes e value_bet_analyses.
Adicione migrations simples ou create_all no modo local.
Atualize o endpoint /import/flashscore-json para salvar os jogos normalizados no banco.

## Prompt 2 - Dashboard frontend

Conecte o frontend Next.js ao backend FastAPI.
Crie telas para:
- importar JSON
- listar partidas importadas
- calcular value bet
- visualizar ranking de oportunidades
- executar backtest usando JSON colado no formulário

Use componentes limpos com TypeScript e Tailwind.

## Prompt 3 - Modelo pre-jogo inicial

Crie um serviço de estimativa de probabilidade inicial baseado em médias históricas.
Use gols marcados, gols sofridos, casa/fora e últimos N jogos.
Implemente um Poisson simples para over/under 1.5 e 2.5.
Inclua testes unitários.

## Prompt 4 - Integração autorizada Flashscore

Complete o FlashscoreAuthorizedProvider com base na documentação real do endpoint autorizado.
Mapeie fixtures, match details, odds e live stats para os schemas internos.
Mantenha rate limit, timeout, retries e logs.
Não implemente bypass, proxy rotation, captcha solving ou evasão.


## Prompt 4 — OpenRouter AI narrative layer

Implement and refine the OpenRouter AI module.

Goals:
- Keep all betting math deterministic and independent from AI.
- Use OpenRouter only to explain structured outputs from the analysis engine.
- Default model: poolside/laguna-m.1:free.
- Add UI components that call `/ai/explain-value-bet` for a selected value bet.
- Do not expose chain-of-thought or reasoning traces.
- Ensure every AI response includes a risk notice and never promises profit.

Acceptance criteria:
- Backend tests pass.
- App works without OPENROUTER_API_KEY by using mock output.
- Live OpenRouter calls work when OPENROUTER_ENABLED=true and OPENROUTER_API_KEY is set.
