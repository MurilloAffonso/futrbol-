from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str


class TeamOut(BaseModel):
    id: int
    name: str
    normalized_name: str

    model_config = {"from_attributes": True}


class MatchCreate(BaseModel):
    home_team_id: int
    away_team_id: int
    status: str | None = None
    date: str | None = None
    external_id: str | None = None


class MatchOut(BaseModel):
    id: int
    home_team_id: int
    away_team_id: int
    status: str | None = None
    date: str | None = None
    external_id: str | None = None

    model_config = {"from_attributes": True}


class OddsCreate(BaseModel):
    match_id: int
    bookmaker: str
    market: str
    selection: str
    odd: float


class OddsOut(OddsCreate):
    id: int

    model_config = {"from_attributes": True}
