import json
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.db_models import ImportedFile, Match, Odds, SyncLog, Team, ValueBet
from app.schemas.db import MatchCreate, MatchOut, OddsCreate, OddsOut, TeamCreate, TeamOut
from app.services.flashscore_transformer import normalize_flashscore_payload

router = APIRouter(tags=["entities"])


def normalize_team_name(name: str) -> str:
    return " ".join(name.strip().lower().split())


@router.post("/teams", response_model=TeamOut)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)):
    normalized = normalize_team_name(payload.name)
    existing = db.scalar(select(Team).where(Team.normalized_name == normalized))
    if existing:
        return existing
    team = Team(name=payload.name.strip(), normalized_name=normalized)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@router.get("/teams", response_model=list[TeamOut])
def list_teams(db: Session = Depends(get_db)):
    return db.scalars(select(Team).order_by(Team.id.desc())).all()


@router.post("/matches", response_model=MatchOut)
def create_match(payload: MatchCreate, db: Session = Depends(get_db)):
    match = Match(**payload.model_dump())
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


@router.get("/matches", response_model=list[MatchOut])
def list_matches(db: Session = Depends(get_db)):
    return db.scalars(select(Match).order_by(Match.id.desc())).all()


@router.get("/matches/{match_id}", response_model=MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.post("/odds", response_model=OddsOut)
def create_odds(payload: OddsCreate, db: Session = Depends(get_db)):
    odds = Odds(**payload.model_dump())
    db.add(odds)
    db.commit()
    db.refresh(odds)
    return odds


@router.get("/odds", response_model=list[OddsOut])
def list_odds(db: Session = Depends(get_db)):
    return db.scalars(select(Odds).order_by(Odds.id.desc())).all()


@router.get("/value-bets")
def list_value_bets(db: Session = Depends(get_db)):
    return db.scalars(select(ValueBet).order_by(ValueBet.id.desc())).all()


@router.post("/imports/flashscore-json")
async def import_flashscore_json(file: UploadFile = File(...), db: Session = Depends(get_db)):
    payload = json.loads((await file.read()).decode("utf-8"))
    matches = normalize_flashscore_payload(payload)

    imported = 0
    duplicated = 0
    for item in matches:
        home_norm = normalize_team_name(item.home.name)
        away_norm = normalize_team_name(item.away.name)
        home = db.scalar(select(Team).where(Team.normalized_name == home_norm)) or Team(name=item.home.name, normalized_name=home_norm)
        away = db.scalar(select(Team).where(Team.normalized_name == away_norm)) or Team(name=item.away.name, normalized_name=away_norm)
        db.add(home)
        db.add(away)
        db.flush()

        if item.external_id and db.scalar(select(Match).where(Match.external_id == item.external_id)):
            duplicated += 1
            continue

        db.add(Match(external_id=item.external_id, home_team_id=home.id, away_team_id=away.id, status=item.status or "unavailable", date=item.date))
        imported += 1

    report = {"imported": imported, "duplicated": duplicated, "total": len(matches)}
    db.add(ImportedFile(filename=file.filename or "upload.json", records_count=imported, report=json.dumps(report)))
    db.add(SyncLog(source="flashscore", status="ok", message=json.dumps(report)))
    db.commit()
    return report


@router.get("/imports")
def list_imports(db: Session = Depends(get_db)):
    return db.scalars(select(ImportedFile).order_by(ImportedFile.id.desc())).all()


@router.get("/sync-logs")
def list_sync_logs(db: Session = Depends(get_db)):
    return db.scalars(select(SyncLog).order_by(SyncLog.id.desc())).all()
