from pydantic import BaseModel, Field
from typing import Any


class ValueBetNarrativeRequest(BaseModel):
    match_name: str = Field(..., examples=["Roma vs Vitoria"])
    market: str = Field(..., examples=["Over 2.5 gols"])
    selection: str = Field(..., examples=["Over 2.5"])
    model_probability: float = Field(..., ge=0, le=1)
    offered_odd: float = Field(..., gt=1)
    fair_odd: float = Field(..., gt=1)
    expected_value: float
    edge_percentage: float
    confidence_score: int = Field(..., ge=0, le=100)
    contextual_factors: list[str] = Field(default_factory=list)
    risk_factors: list[str] = Field(default_factory=list)


class ValueBetNarrativeResponse(BaseModel):
    provider: str
    model: str
    narrative: str
    risk_notice: str
    used_mock: bool = False


class AnalysisChatRequest(BaseModel):
    question: str
    context: dict[str, Any] = Field(default_factory=dict)


class AnalysisChatResponse(BaseModel):
    provider: str
    model: str
    answer: str
    risk_notice: str
    used_mock: bool = False
