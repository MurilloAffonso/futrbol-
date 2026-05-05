from fastapi import APIRouter
from app.schemas.analysis import BacktestRequest, RemoveMargin1x2Request, ValueBetRequest
from app.services.backtest_service import run_flat_stake_backtest
from app.services.probability_service import remove_margin_1x2
from app.services.value_bet_service import analyze_value_bet

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/value-bet")
def value_bet(request: ValueBetRequest):
    return analyze_value_bet(**request.model_dump())


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
