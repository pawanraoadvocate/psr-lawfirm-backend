from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import boto3, uuid
from app.database import get_db
from app import models, schemas
from app.utils.auth import get_current_user
from app.config import settings

router = APIRouter()

s3_client = boto3.client("s3", region_name=settings.AWS_REGION)


def upload_to_s3(file_bytes: bytes, filename: str, client_id: int) -> str:
    key = f"clients/{client_id}/documents/{uuid.uuid4()}_{filename}"
    s3_client.put_object(
        Bucket=settings.AWS_BUCKET_NAME,
        Key=key,
        Body=file_bytes,
        ContentDisposition=f'attachment; filename="{filename}"',
    )
    return key


def get_presigned_url(s3_key: str, expires: int = 3600) -> str:
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": s3_key},
        ExpiresIn=expires,
    )


@router.get("/", response_model=List[schemas.DocumentOut])
def list_documents(
    client_id: Optional[int] = None,
    case_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    q = db.query(models.Document)
    if client_id:
        q = q.filter(models.Document.client_id == client_id)
    if case_id:
        q = q.filter(models.Document.case_id == case_id)
    return q.all()


@router.post("/upload", response_model=schemas.DocumentOut, status_code=201)
async def upload_document(
    client_id: int = Form(...),
    case_id: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    content = await file.read()
    s3_key = upload_to_s3(content, file.filename, client_id)
    doc = models.Document(
        client_id=client_id,
        case_id=case_id,
        filename=file.filename,
        s3_key=s3_key,
        file_size=len(content),
        file_type=file.content_type,
        description=description,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.get("/{doc_id}/download")
def download_document(
    doc_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    url = get_presigned_url(doc.s3_key)
    return {"download_url": url, "filename": doc.filename, "expires_in": "1 hour"}
