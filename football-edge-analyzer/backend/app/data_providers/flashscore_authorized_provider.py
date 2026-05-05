from __future__ import annotations

import asyncio
import httpx
from app.core.config import Settings
from app.data_providers.base_provider import BaseFootballDataProvider
from app.models.domain import FootballMatch, OddsQuote


class FlashscoreAuthorizedProvider(BaseFootballDataProvider):
    """Stub seguro para endpoint/feed/API autorizada do Flashscore.

    Este provider presume acesso documentado/autorizado. Não implementa evasão,
    bypass, rotação agressiva de proxy ou engenharia reversa.
    """

    def __init__(self, settings: Settings):
        if not settings.flashscore_base_url:
            raise ValueError("FLASHSCORE_BASE_URL is required.")
        self.settings = settings
        self._delay_seconds = 60 / max(settings.flashscore_rate_limit_per_minute, 1)
        self._last_request_at = 0.0

    async def _rate_limit(self) -> None:
        now = asyncio.get_event_loop().time()
        wait_for = self._delay_seconds - (now - self._last_request_at)
        if wait_for > 0:
            await asyncio.sleep(wait_for)
        self._last_request_at = asyncio.get_event_loop().time()

    async def _get(self, path: str, params: dict | None = None) -> dict:
        await self._rate_limit()
        headers = {}
        if self.settings.flashscore_api_key:
            headers["Authorization"] = f"Bearer {self.settings.flashscore_api_key}"
        async with httpx.AsyncClient(timeout=self.settings.flashscore_timeout_seconds) as client:
            response = await client.get(
                f"{self.settings.flashscore_base_url.rstrip('/')}/{path.lstrip('/')}",
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_fixtures(self, date: str, league: str | None = None) -> list[FootballMatch]:
        raise NotImplementedError("Mapeie aqui o formato real do endpoint autorizado de fixtures.")

    async def get_match_details(self, external_match_id: str) -> FootballMatch:
        raise NotImplementedError("Mapeie aqui o formato real do endpoint autorizado de detalhes.")

    async def get_odds(self, external_match_id: str, market: str | None = None) -> list[OddsQuote]:
        raise NotImplementedError("Mapeie aqui o formato real do endpoint autorizado de odds.")

    async def get_live_stats(self, external_match_id: str) -> dict:
        raise NotImplementedError("Mapeie aqui o formato real do endpoint autorizado de live stats.")
