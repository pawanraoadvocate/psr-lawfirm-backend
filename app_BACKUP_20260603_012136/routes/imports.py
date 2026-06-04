from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ecourt_import import import_ecourt_json
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/ecourt")
def import_ecourt(payload: dict, db: Session = Depends(get_db), _=Depends(get_current_user)):
    raw_json = payload.get("data", payload)
    client_id = payload.get("client_id")
    result = import_ecourt_json(raw_json, client_id)
    return {"status": "ok", "inserted": result}
