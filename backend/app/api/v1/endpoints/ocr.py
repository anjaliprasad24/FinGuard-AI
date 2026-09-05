"""OCR Receipt Upload Endpoint."""

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.services.ocr_engine import OCREngine

router = APIRouter()


@router.post("/upload")
async def upload_ocr_receipt(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Ingest receipt/invoice image or PDF file and extract line items and clean merchant."""
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    extracted = OCREngine.process_image(contents, filename=file.filename or "")
    return {
        "filename": file.filename,
        "extracted_data": extracted
    }
