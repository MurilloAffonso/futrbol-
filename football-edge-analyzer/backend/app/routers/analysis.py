from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.analysis import BacktestRequest, RemoveMargin1x2Request, ValueBetRequest
from app.db import get_db
from app.models.db_models import ValueBet
from app.services.backtest_service import run_flat_stake_backtest
from app.services.probability_service import remove_margin_1x2
from app.services.value_bet_service import analyze_value_bet

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/value-bet")
def value_bet(request: ValueBetRequest):
    return analyze_value_bet(**request.model_dump())


@router.post("/batch-value-bets")
def batch_value_bets(requests: list[ValueBetRequest], db: Session = Depends(get_db)):
    results = []
    for request in requests:
        result = analyze_value_bet(**request.model_dump())
        db.add(
            ValueBet(
                market=result.market,
                selection=result.selection,
                offered_odd=result.offered_odd,
                model_probability=result.model_probability,
                expected_value=result.expected_value,
                edge_percentage=result.edge_percentage,
                status=result.status,
            )
        )
        results.append(result)
    db.commit()
    return results


@router.post("/remove-margin-1x2")
def remove_margin(request: RemoveMargin1x2Request):
    return remove_margin_1x2(**request.model_dump())


@router.post("/backtest")
def backtest(request: BacktestRequest):
    return run_flat_stake_backtest(
        bets=request.bets,
        min_ev=request.min_ev,
        min_confidence_score=request.min_confidence_score,
    )
