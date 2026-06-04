from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import random, string
from app.database import get_db
from app import models, schemas
from app.utils.auth import get_current_user

router = APIRouter()


def generate_case_number(case_type: str = "", reg_no: str = "", reg_year: str = "") -> str:
    if case_type and reg_no and reg_year:
        return f"{case_type}-{reg_no}-{reg_year}"
    if case_type and reg_no:
        return f"{case_type}-{reg_no}"
    year = datetime.now().year
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"PSR-{year}-{suffix}"


@router.get("", response_model=List[schemas.CaseOut])
@router.get("/", response_model=List[schemas.CaseOut])
def list_cases(
    client_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(models.Case)
    if client_id:
        q = q.filter(models.Case.client_id == client_id)
    if status:
        q = q.filter(models.Case.status == status)
    return q.order_by(models.Case.id.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=schemas.CaseOut, status_code=201)
@router.post("/", response_model=schemas.CaseOut, status_code=201)
def create_case(
    case_in: schemas.CaseCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    client = db.query(models.Client).filter(models.Client.id == case_in.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    data = case_in.dict()
    data["case_number"] = generate_case_number(
        data.get("case_type", ""),
        data.get("registration_number", ""),
        data.get("registration_year", ""),
    )
    case = models.Case(**data)
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


@router.get("/{case_id}", response_model=schemas.CaseOut)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.put("/{case_id}", response_model=schemas.CaseOut)
def update_case(
    case_id: int,
    case_in: schemas.CaseUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    for field, value in case_in.dict(exclude_unset=True).items():
        setattr(case, field, value)
    db.commit()
    db.refresh(case)
    return case


@router.delete("/{case_id}", status_code=204)
def delete_case(
    case_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    db.delete(case)
    db.commit()
