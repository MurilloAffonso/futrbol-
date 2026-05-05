# Especificação do Produto - Football Edge Analyzer

## Objetivo

Criar uma ferramenta para análise de apostas de futebol baseada em dados, probabilidade e valor esperado.

O produto deve ajudar o usuário a responder:

> A odd oferecida está maior do que a odd justa estimada pelo modelo?

## Camadas do produto

### 1. Contexto pre-jogo

- Times
- Forma recente
- Casa/fora
- H2H
- Estatísticas históricas
- Escalações
- Desfalques
- Árbitro

### 2. Valor matemático

- Odd oferecida
- Probabilidade implícita
- Probabilidade estimada
- Odd justa
- EV
- Edge

### 3. Validação live

- Pressão
- Ataques perigosos
- APM
- Escanteios recentes
- Chutes no gol
- Cartões
- Momentum

A versão atual implementa a camada 2 e a normalização inicial da camada 1.

## MVP v0.1

- Backend FastAPI
- Fórmulas matemáticas testadas
- Upload de JSON do FlashscoreScraping
- Normalização de partidas
- Endpoint de value bet
- Endpoint de remoção de margem 1X2
- Endpoint de backtest flat stake
- Frontend inicial

## Critérios de classificação

| Condição | Status |
|---|---|
| EV <= 0 | no_value |
| 0 < EV < 10% | weak_value |
| 10% <= EV < 15% | moderate_value |
| EV >= 15% | strong_value |
| confiança baixa ou odd fora do filtro | insufficient_data |

## Aviso de risco

O sistema não garante resultado. Ele apenas classifica oportunidades segundo dados disponíveis, critérios configurados e hipóteses do modelo.
