from app.schemas.analysis import BacktestBet
from app.services.value_bet_service import analyze_value_bet


def run_flat_stake_backtest(
    bets: list[BacktestBet],
    min_ev: float = 0.10,
    min_confidence_score: int = 60,
) -> dict:
    selected = []
    profit = 0.0
    total_staked = 0.0
    wins = 0

    for bet in bets:
        analysis = analyze_value_bet(
            market=bet.market,
            selection=bet.selection,
            offered_odd=bet.offered_odd,
            model_probability=bet.model_probability,
            confidence_score=bet.confidence_score,
        )
        if analysis.expected_value >= min_ev and bet.confidence_score >= min_confidence_score:
            total_staked += bet.stake
            pnl = bet.stake * (bet.offered_odd - 1) if bet.won else -bet.stake
            profit += pnl
            wins += int(bet.won)
            selected.append({"bet": bet.model_dump(), "analysis": analysis.model_dump(), "pnl": pnl})

    count = len(selected)
    roi = profit / total_staked if total_staked else 0.0
    hit_rate = wins / count if count else 0.0

    return {
        "total_candidates": len(bets),
        "selected_bets": count,
        "wins": wins,
        "losses": count - wins,
        "total_staked": round(total_staked, 4),
        "profit": round(profit, 4),
        "roi": round(roi, 4),
        "hit_rate": round(hit_rate, 4),
        "details": selected,
    }
