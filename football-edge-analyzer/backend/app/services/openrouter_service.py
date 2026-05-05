from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from app.core.config import Settings
from app.schemas.ai import AnalysisChatRequest, ValueBetNarrativeRequest


SYSTEM_PROMPT = """
Voce e um analista quantitativo de futebol integrado a um software de value betting.
Responda em portugues do Brasil, com linguagem objetiva, tecnica e prudente.
Nunca prometa lucro, green garantido ou certeza de resultado.
Sempre diferencie: probabilidade estimada, odd justa, odd oferecida, EV, risco e variancia.
Quando os dados forem insuficientes, diga que a oportunidade deve ser marcada como inconclusiva.
Nao exponha cadeia de pensamento. Entregue apenas conclusao, justificativa resumida e riscos.
""".strip()


@dataclass
class OpenRouterResult:
    text: str
    used_mock: bool = False


class OpenRouterService:
    """OpenRouter client used to turn model output into readable betting analysis.

    This service is intentionally optional. The mathematical analysis must work without AI.
    When OPENROUTER_API_KEY is not configured, it returns deterministic mock output so the
    product remains usable in local development and tests.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = settings.openrouter_base_url.rstrip("/")
        self.model = settings.openrouter_model
        self.timeout = settings.openrouter_timeout_seconds

    def enabled(self) -> bool:
        return bool(self.settings.openrouter_enabled and self.settings.openrouter_api_key)

    async def explain_value_bet(self, payload: ValueBetNarrativeRequest) -> OpenRouterResult:
        user_prompt = build_value_bet_prompt(payload)
        if not self.enabled():
            return OpenRouterResult(text=mock_value_bet_narrative(payload), used_mock=True)
        return await self._chat(user_prompt)

    async def answer_analysis_question(self, payload: AnalysisChatRequest) -> OpenRouterResult:
        user_prompt = build_chat_prompt(payload)
        if not self.enabled():
            return OpenRouterResult(text=mock_chat_answer(payload), used_mock=True)
        return await self._chat(user_prompt)

    async def _chat(self, user_prompt: str) -> OpenRouterResult:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.settings.openrouter_api_key}",
            "Content-Type": "application/json",
        }
        if self.settings.openrouter_site_url:
            headers["HTTP-Referer"] = self.settings.openrouter_site_url
        if self.settings.openrouter_app_title:
            headers["X-Title"] = self.settings.openrouter_app_title

        body: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()

        text = data["choices"][0]["message"].get("content", "").strip()
        if not text:
            text = "Nao foi possivel gerar uma explicacao confiavel para esta analise."
        return OpenRouterResult(text=text, used_mock=False)


def build_value_bet_prompt(payload: ValueBetNarrativeRequest) -> str:
    context = "\n".join(f"- {item}" for item in payload.contextual_factors) or "- Nenhum fator contextual informado."
    risks = "\n".join(f"- {item}" for item in payload.risk_factors) or "- Nenhum risco especifico informado."
    return f"""
Explique a oportunidade abaixo para um usuario do dashboard.

Jogo: {payload.match_name}
Mercado: {payload.market}
Selecao: {payload.selection}
Probabilidade estimada pelo modelo: {payload.model_probability:.2%}
Odd oferecida: {payload.offered_odd:.2f}
Odd justa: {payload.fair_odd:.2f}
Valor esperado: {payload.expected_value:.2%}
Edge percentual: {payload.edge_percentage:.2f}%
Confianca: {payload.confidence_score}/100

Fatores contextuais:
{context}

Riscos:
{risks}

Formato de resposta:
1. Diagnostico em uma frase.
2. Justificativa matematica curta.
3. Riscos principais.
4. Classificacao final: forte, moderada, fraca ou nao qualificada.
""".strip()


def build_chat_prompt(payload: AnalysisChatRequest) -> str:
    return f"""
Pergunta do usuario:
{payload.question}

Contexto estruturado disponivel:
{payload.context}

Responda somente com base no contexto informado e nas regras matematicas do produto.
Quando faltar dado, explique exatamente qual dado falta.
""".strip()


def mock_value_bet_narrative(payload: ValueBetNarrativeRequest) -> str:
    if payload.expected_value >= 0.15 and payload.confidence_score >= 60:
        classification = "forte"
    elif payload.expected_value >= 0.10 and payload.confidence_score >= 60:
        classification = "moderada"
    elif payload.expected_value > 0:
        classification = "fraca"
    else:
        classification = "nao qualificada"

    return (
        f"Diagnostico: {payload.match_name} apresenta uma oportunidade {classification} em {payload.market} "
        f"para {payload.selection}.\n"
        f"Justificativa: a probabilidade estimada e {payload.model_probability:.2%}, gerando odd justa "
        f"de {payload.fair_odd:.2f}; a odd oferecida de {payload.offered_odd:.2f} implica EV de "
        f"{payload.expected_value:.2%}.\n"
        "Riscos: a analise depende da qualidade dos dados, do tamanho da amostra, da variancia do futebol "
        "e de possiveis mudancas de escalao, lesoes ou odds.\n"
        f"Classificacao final: {classification}."
    )


def mock_chat_answer(payload: AnalysisChatRequest) -> str:
    return (
        "Modo local sem OpenRouter ativo. Com base no contexto enviado, valide sempre odd justa, "
        "EV, confianca e risco contextual antes de qualificar qualquer entrada. "
        "Configure OPENROUTER_API_KEY para respostas analiticas geradas pelo modelo."
    )
