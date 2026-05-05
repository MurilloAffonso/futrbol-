import json
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.flashscore_transformer import normalize_flashscore_csv, normalize_flashscore_payload

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/flashscore-json")
async def import_flashscore_json(file: UploadFile = File(...)):
    raw = await file.read()
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON payload.") from exc

    matches = normalize_flashscore_payload(payload)
    return {
        "imported_matches": len(matches),
        "preview": [match.model_dump() for match in matches[:5]],
    }


@router.post("/flashscore-csv")
async def import_flashscore_csv(file: UploadFile = File(...)):
    try:
        raw = await file.read()
        csv_content = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded.") from exc

    try:
        matches = normalize_flashscore_csv(csv_content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not matches:
        raise HTTPException(status_code=400, detail="CSV file has no valid rows.")

    return {
        "imported_matches": len(matches),
        "preview": [match.model_dump() for match in matches[:5]],
    }
