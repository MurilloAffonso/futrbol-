from __future__ import annotations

import json
from pathlib import Path
from app.data_providers.base_provider import BaseFootballDataProvider
from app.models.domain import FootballMatch, OddsQuote
from app.services.flashscore_transformer import normalize_flashscore_payload


class FlashscoreScrapingJsonProvider(BaseFootballDataProvider):
    """Provider para ler arquivos JSON gerados pelo scraper Node/Playwright enviado.

    Use quando o coletor autorizado salvar arquivos em disco e o backend analítico
    precisar apenas normalizar e consumir os dados.
    """

    def __init__(self, json_path: str | Path):
        self.json_path = Path(json_path)
        if not self.json_path.exists():
            raise FileNotFoundError(f"File not found: {self.json_path}")

    def _load_matches(self) -> list[FootballMatch]:
        payload = json.loads(self.json_path.read_text(encoding="utf-8"))
        return normalize_flashscore_payload(payload)

    async def get_fixtures(self, date: str, league: str | None = None) -> list[FootballMatch]:
        matches = self._load_matches()
        # MVP: filtro simples por substring de data. Evoluir para parser de data/timezone.
        return [match for match in matches if match.date and date in match.date]

    async def get_match_details(self, external_match_id: str) -> FootballMatch:
        for match in self._load_matches():
            if match.external_id == external_match_id:
                return match
        raise KeyError(f"Match not found: {external_match_id}")

    async def get_odds(self, external_match_id: str, market: str | None = None) -> list[OddsQuote]:
        # O scraper atual enviado coleta resultados/estatísticas, não odds.
        return []

    async def get_live_stats(self, external_match_id: str) -> dict:
        # O scraper atual é adequado para histórico/resultados. Live fica para integração futura.
        return {"external_match_id": external_match_id, "available": False}
