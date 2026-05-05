from app.services.probability_service import (
    edge_percentage,
    expected_value,
    fair_odd,
    implied_probability,
    remove_margin_1x2,
)
from app.services.value_bet_service import analyze_value_bet


def test_implied_probability():
    assert round(implied_probability(2.0), 4) == 0.5


def test_fair_odd():
    assert round(fair_odd(0.57), 2) == 1.75


def test_expected_value():
    assert round(expected_value(0.57, 2.22), 4) == 0.2654


def test_edge_percentage():
    assert round(edge_percentage(2.22, 1.7543859649), 2) == 26.54


def test_remove_margin_1x2():
    result = remove_margin_1x2(2.0, 3.5, 4.0)
    assert round(result["home"] + result["draw"] + result["away"], 4) == 1.0
    assert result["bookmaker_margin"] > 0


def test_value_bet_result():
    result = analyze_value_bet(
        market="Goal Kicks",
        selection="Over 8.5",
        offered_odd=2.22,
        model_probability=0.57,
        confidence_score=72,
    )
    assert result.status == "strong_value"
    assert round(result.expected_value, 4) == 0.2654
