from abc import ABC, abstractmethod
from app.models.domain import FootballMatch, OddsQuote


class BaseFootballDataProvider(ABC):
    @abstractmethod
    async def get_fixtures(self, date: str, league: str | None = None) -> list[FootballMatch]:
        raise NotImplementedError

    @abstractmethod
    async def get_match_details(self, external_match_id: str) -> FootballMatch:
        raise NotImplementedError

    @abstractmethod
    async def get_odds(self, external_match_id: str, market: str | None = None) -> list[OddsQuote]:
        raise NotImplementedError

    @abstractmethod
    async def get_live_stats(self, external_match_id: str) -> dict:
        raise NotImplementedError
