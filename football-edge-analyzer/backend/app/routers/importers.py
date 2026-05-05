import json
from fastapi import APIRouter, File, UploadFile
from app.services.flashscore_transformer import normalize_flashscore_payload

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/flashscore-json")
async def import_flashscore_json(file: UploadFile = File(...)):
    raw = await file.read()
    payload = json.loads(raw.decode("utf-8"))
    matches = normalize_flashscore_payload(payload)
    return {
        "imported_matches": len(matches),
        "preview": [match.model_dump() for match in matches[:5]],
    }
