from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.ai import (
    AnalysisChatRequest,
    AnalysisChatResponse,
    ValueBetNarrativeRequest,
    ValueBetNarrativeResponse,
)
from app.services.openrouter_service import OpenRouterService

router = APIRouter(prefix="/ai", tags=["ai"])

RISK_NOTICE = "Analise informativa. Nao ha garantia de lucro; use gestao de banca, backtesting e controle de risco."


@router.post("/explain-value-bet", response_model=ValueBetNarrativeResponse)
async def explain_value_bet(payload: ValueBetNarrativeRequest) -> ValueBetNarrativeResponse:
    settings = get_settings()
    service = OpenRouterService(settings)
    result = await service.explain_value_bet(payload)
    return ValueBetNarrativeResponse(
        provider="openrouter",
        model=settings.openrouter_model,
        narrative=result.text,
        risk_notice=RISK_NOTICE,
        used_mock=result.used_mock,
    )


@router.post("/chat", response_model=AnalysisChatResponse)
async def analysis_chat(payload: AnalysisChatRequest) -> AnalysisChatResponse:
    settings = get_settings()
    service = OpenRouterService(settings)
    result = await service.answer_analysis_question(payload)
    return AnalysisChatResponse(
        provider="openrouter",
        model=settings.openrouter_model,
        answer=result.text,
        risk_notice=RISK_NOTICE,
        used_mock=result.used_mock,
    )
