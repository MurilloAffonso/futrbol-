from enum import Enum
from pydantic import BaseModel, Field


class BetValueStatus(str, Enum):
    NO_VALUE = "no_value"
    WEAK_VALUE = "weak_value"
    MODERATE_VALUE = "moderate_value"
    STRONG_VALUE = "strong_value"
    INSUFFICIENT_DATA = "insufficient_data"


class Team(BaseModel):
    name: str
    image_url: str | None = None


class MatchResult(BaseModel):
    home: int | None = None
    away: int | None = None
    regulation_time: str | None = None
    penalties: str | None = None


class MatchInformationItem(BaseModel):
    category: str
    value: str | None = None


class MatchStatisticItem(BaseModel):
    category: str
    home_value: str | float | int | None = None
    away_value: str | float | int | None = None


class FootballMatch(BaseModel):
    external_id: str | None = None
    stage: str | None = None
    date: str | None = None
    status: str | None = None
    home: Team
    away: Team
    result: MatchResult | None = None
    information: list[MatchInformationItem] = Field(default_factory=list)
    statistics: list[MatchStatisticItem] = Field(default_factory=list)


class OddsQuote(BaseModel):
    match_external_id: str | None = None
    bookmaker: str
    market: str
    selection: str
    odd: float


class ValueBetResult(BaseModel):
    market: str
    selection: str
    offered_odd: float
    model_probability: float
    implied_probability: float
    fair_odd: float
    expected_value: float
    edge_percentage: float
    confidence_score: int
    status: BetValueStatus
    explanation: str
