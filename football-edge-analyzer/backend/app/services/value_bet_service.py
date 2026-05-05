from app.core.config import get_settings
from app.models.domain import BetValueStatus, ValueBetResult
from app.services.probability_service import (
    edge_percentage,
    expected_value,
    fair_odd,
    implied_probability,
)


def classify_value_bet(ev: float, confidence_score: int, offered_odd: float) -> BetValueStatus:
    settings = get_settings()

    if confidence_score < settings.min_confidence_score:
        return BetValueStatus.INSUFFICIENT_DATA
    if offered_odd < settings.min_odd or offered_odd > settings.max_odd:
        return BetValueStatus.INSUFFICIENT_DATA
    if ev <= 0:
        return BetValueStatus.NO_VALUE
    if ev < settings.min_ev:
        return BetValueStatus.WEAK_VALUE
    if ev < settings.strong_ev:
        return BetValueStatus.MODERATE_VALUE
    return BetValueStatus.STRONG_VALUE


def explain_status(status: BetValueStatus, ev: float) -> str:
    ev_pct = ev * 100
    if status == BetValueStatus.INSUFFICIENT_DATA:
        return "Oportunidade não qualificada por baixa confiança, faixa de odd fora do filtro ou dados insuficientes."
    if status == BetValueStatus.NO_VALUE:
        return f"Sem valor esperado positivo segundo o modelo. EV estimado: {ev_pct:.2f}%."
    if status == BetValueStatus.WEAK_VALUE:
        return f"EV positivo, mas abaixo do filtro principal. EV estimado: {ev_pct:.2f}%."
    if status == BetValueStatus.MODERATE_VALUE:
        return f"EV positivo em zona moderada. EV estimado: {ev_pct:.2f}%."
    return f"EV forte segundo o filtro inicial. EV estimado: {ev_pct:.2f}%."


def analyze_value_bet(
    market: str,
    selection: str,
    offered_odd: float,
    model_probability: float,
    confidence_score: int,
) -> ValueBetResult:
    implied = implied_probability(offered_odd)
    fair = fair_odd(model_probability)
    ev = expected_value(model_probability, offered_odd)
    edge = edge_percentage(offered_odd, fair)
    status = classify_value_bet(ev, confidence_score, offered_odd)

    return ValueBetResult(
        market=market,
        selection=selection,
        offered_odd=offered_odd,
        model_probability=model_probability,
        implied_probability=implied,
        fair_odd=fair,
        expected_value=ev,
        edge_percentage=edge,
        confidence_score=confidence_score,
        status=status,
        explanation=explain_status(status, ev),
    )
