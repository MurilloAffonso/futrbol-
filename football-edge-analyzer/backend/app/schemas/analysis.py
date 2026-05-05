from pydantic import BaseModel, Field


class ValueBetRequest(BaseModel):
    market: str = Field(examples=["Over 2.5 Goals"])
    selection: str = Field(examples=["Over 2.5"])
    offered_odd: float = Field(gt=1.0, examples=[2.22])
    model_probability: float = Field(gt=0.0, lt=1.0, examples=[0.57])
    confidence_score: int = Field(default=70, ge=0, le=100)


class RemoveMargin1x2Request(BaseModel):
    home_odd: float = Field(gt=1.0)
    draw_odd: float = Field(gt=1.0)
    away_odd: float = Field(gt=1.0)


class BacktestBet(BaseModel):
    market: str
    selection: str
    offered_odd: float = Field(gt=1.0)
    model_probability: float = Field(gt=0.0, lt=1.0)
    confidence_score: int = Field(default=70, ge=0, le=100)
    won: bool
    stake: float = Field(default=1.0, gt=0.0)


class BacktestRequest(BaseModel):
    bets: list[BacktestBet]
    min_ev: float = 0.10
    min_confidence_score: int = 60
