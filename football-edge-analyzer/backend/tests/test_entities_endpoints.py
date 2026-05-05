from fastapi.testclient import TestClient

from app.main import app
from app.db import Base, engine


def setup_module():
    Base.metadata.create_all(bind=engine)


def test_team_normalization_and_deduplication():
    with TestClient(app) as client:
        response1 = client.post("/teams", json={"name": " Real Madrid "})
        response2 = client.post("/teams", json={"name": "real   madrid"})
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["id"] == response2.json()["id"]


def test_import_avoids_duplicates():
    payload = {
        "1": {"matchId": "m-1", "home": {"name": "A"}, "away": {"name": "B"}, "status": "FT", "date": "2026-01-01"},
        "2": {"matchId": "m-1", "home": {"name": "A"}, "away": {"name": "B"}, "status": "FT", "date": "2026-01-01"},
    }
    files = {"file": ("matches.json", str(payload).replace("'", '"'), "application/json")}
    with TestClient(app) as client:
        response = client.post("/imports/flashscore-json", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["imported"] >= 1
    assert data["duplicated"] >= 1
