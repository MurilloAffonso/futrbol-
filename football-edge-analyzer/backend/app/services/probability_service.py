from __future__ import annotations


def implied_probability(odd: float) -> float:
    if odd <= 1:
        raise ValueError("Odd must be greater than 1.")
    return 1 / odd


def fair_odd(model_probability: float) -> float:
    if not 0 < model_probability < 1:
        raise ValueError("Model probability must be between 0 and 1.")
    return 1 / model_probability


def expected_value(model_probability: float, offered_odd: float) -> float:
    if offered_odd <= 1:
        raise ValueError("Offered odd must be greater than 1.")
    if not 0 < model_probability < 1:
        raise ValueError("Model probability must be between 0 and 1.")
    return (model_probability * offered_odd) - 1


def edge_percentage(offered_odd: float, calculated_fair_odd: float) -> float:
    if offered_odd <= 1 or calculated_fair_odd <= 1:
        raise ValueError("Odds must be greater than 1.")
    return ((offered_odd / calculated_fair_odd) - 1) * 100


def remove_margin_1x2(home_odd: float, draw_odd: float, away_odd: float) -> dict[str, float]:
    raw_home = implied_probability(home_odd)
    raw_draw = implied_probability(draw_odd)
    raw_away = implied_probability(away_odd)
    overround = raw_home + raw_draw + raw_away
    if overround <= 0:
        raise ValueError("Invalid overround.")
    return {
        "home": raw_home / overround,
        "draw": raw_draw / overround,
        "away": raw_away / overround,
        "overround": overround,
        "bookmaker_margin": overround - 1,
    }
