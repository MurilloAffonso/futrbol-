from __future__ import annotations

import csv
import io
from typing import Any
from app.models.domain import (
    FootballMatch,
    MatchInformationItem,
    MatchResult,
    MatchStatisticItem,
    Team,
)


def _parse_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(str(value).strip())
    except ValueError:
        return None


def normalize_flashscore_match(external_id: str, raw: dict[str, Any]) -> FootballMatch:
    home = raw.get("home") or {}
    away = raw.get("away") or {}
    result = raw.get("result") or {}

    information = [
        MatchInformationItem(category=str(item.get("category", "")).strip(), value=item.get("value"))
        for item in raw.get("information", [])
        if item.get("category")
    ]

    statistics = [
        MatchStatisticItem(
            category=str(item.get("category", "")).strip(),
            home_value=item.get("homeValue") or item.get("home_value"),
            away_value=item.get("awayValue") or item.get("away_value"),
        )
        for item in raw.get("statistics", [])
        if item.get("category")
    ]

    return FootballMatch(
        external_id=raw.get("matchId") or external_id,
        stage=raw.get("stage"),
        date=raw.get("date"),
        status=raw.get("status"),
        home=Team(name=home.get("name") or "Unknown Home", image_url=home.get("image")),
        away=Team(name=away.get("name") or "Unknown Away", image_url=away.get("image")),
        result=MatchResult(
            home=_parse_int(result.get("home")),
            away=_parse_int(result.get("away")),
            regulation_time=result.get("regulationTime") or result.get("regulation_time"),
            penalties=result.get("penalties"),
        ),
        information=information,
        statistics=statistics,
    )


def normalize_flashscore_payload(payload: dict[str, Any] | list[dict[str, Any]]) -> list[FootballMatch]:
    if isinstance(payload, list):
        return [normalize_flashscore_match(str(item.get("matchId", idx)), item) for idx, item in enumerate(payload)]

    matches: list[FootballMatch] = []
    for external_id, raw in payload.items():
        if isinstance(raw, dict):
            matches.append(normalize_flashscore_match(external_id, raw))
    return matches


def normalize_flashscore_csv(csv_content: str) -> list[FootballMatch]:
    reader = csv.DictReader(io.StringIO(csv_content))
    matches: list[FootballMatch] = []

    for idx, row in enumerate(reader):
        external_id = row.get("match_id") or row.get("matchId") or str(idx)
        raw_match = {
            "matchId": external_id,
            "stage": row.get("stage"),
            "date": row.get("date"),
            "status": row.get("status"),
            "home": {"name": row.get("home_name"), "image": row.get("home_image")},
            "away": {"name": row.get("away_name"), "image": row.get("away_image")},
            "result": {
                "home": row.get("home_goals"),
                "away": row.get("away_goals"),
                "regulationTime": row.get("regulation_time"),
                "penalties": row.get("penalties"),
            },
        }
        matches.append(normalize_flashscore_match(str(external_id), raw_match))

    return matches
