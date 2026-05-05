import pytest

from app.core.config import Settings
from app.schemas.ai import ValueBetNarrativeRequest, AnalysisChatRequest
from app.services.openrouter_service import OpenRouterService, build_value_bet_prompt


@pytest.mark.asyncio
async def test_openrouter_service_uses_mock_without_key():
    settings = Settings(openrouter_enabled=False, openrouter_api_key=None)
    service = OpenRouterService(settings)
    payload = ValueBetNarrativeRequest(
        match_name="Roma vs Vitoria",
        market="Over 2.5 gols",
        selection="Over 2.5",
        model_probability=0.57,
        offered_odd=2.22,
        fair_odd=1.75,
        expected_value=0.2654,
        edge_percentage=26.54,
        confidence_score=72,
    )
    result = await service.explain_value_bet(payload)
    assert result.used_mock is True
    assert "EV" in result.text
    assert "Classificacao final" in result.text


def test_value_bet_prompt_contains_core_metrics():
    payload = ValueBetNarrativeRequest(
        match_name="A vs B",
        market="1X2",
        selection="Casa",
        model_probability=0.60,
        offered_odd=2.00,
        fair_odd=1.67,
        expected_value=0.20,
        edge_percentage=19.76,
        confidence_score=80,
    )
    prompt = build_value_bet_prompt(payload)
    assert "Probabilidade estimada" in prompt
    assert "Odd oferecida" in prompt
    assert "Valor esperado" in prompt


@pytest.mark.asyncio
async def test_analysis_chat_uses_mock_without_key():
    settings = Settings(openrouter_enabled=False, openrouter_api_key=None)
    service = OpenRouterService(settings)
    result = await service.answer_analysis_question(
        AnalysisChatRequest(question="Por que essa odd tem valor?", context={"ev": 0.18})
    )
    assert result.used_mock is True
    assert "OPENROUTER_API_KEY" in result.text
