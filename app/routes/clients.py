from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models, schemas
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("", response_model=List[schemas.ClientOut])
@router.get("/", response_model=List[schemas.ClientOut])
def list_clients(
    active_only: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(models.Client)
    if active_only is not None:
        q = q.filter(models.Client.is_active == active_only)
    if search:
        q = q.filter(
            models.Client.full_name.ilike("%" + search + "%") |
            models.Client.email.ilike("%" + search + "%") |
            models.Client.phone.ilike("%" + search + "%")
        )
    return q.offset(skip).limit(limit).all()


@router.post("", response_model=schemas.ClientOut, status_code=201)
@router.post("/", response_model=schemas.ClientOut, status_code=201)
def create_client(
    client_in: schemas.ClientCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    client = models.Client(**client_in.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("/{client_id}", response_model=schemas.ClientOut)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=schemas.ClientOut)
def update_client(
    client_id: int,
    client_in: schemas.ClientUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    for field, value in client_in.dict(exclude_unset=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client


@router.delete("/{client_id}", status_code=204)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    client.is_active = False
    db.commit()
