from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models, schemas
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[schemas.HearingOut])
def list_hearings(
    case_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(models.Hearing)

    if case_id:
        q = q.filter(models.Hearing.case_id == case_id)

    return q.order_by(models.Hearing.hearing_date.desc()).all()


@router.post("/", response_model=schemas.HearingOut, status_code=201)
def create_hearing(
    hearing_in: schemas.HearingCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    case = db.query(models.Case).filter(
        models.Case.id == hearing_in.case_id
    ).first()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    hearing = models.Hearing(**hearing_in.dict())

    db.add(hearing)
    db.commit()
    db.refresh(hearing)

    return hearing


@router.get("/{hearing_id}", response_model=schemas.HearingOut)
def get_hearing(
    hearing_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    hearing = db.query(models.Hearing).filter(
        models.Hearing.id == hearing_id
    ).first()

    if not hearing:
        raise HTTPException(status_code=404, detail="Hearing not found")

    return hearing


@router.put("/{hearing_id}", response_model=schemas.HearingOut)
def update_hearing(
    hearing_id: int,
    hearing_in: schemas.HearingUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    hearing = db.query(models.Hearing).filter(
        models.Hearing.id == hearing_id
    ).first()

    if not hearing:
        raise HTTPException(status_code=404, detail="Hearing not found")

    for field, value in hearing_in.dict(exclude_unset=True).items():
        setattr(hearing, field, value)

    db.commit()
    db.refresh(hearing)

    return hearing
