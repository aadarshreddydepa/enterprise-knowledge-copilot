import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
# from app.db.session import get_db
from app.db.session import AsyncSessionLocal
from app.db.session import get_db
from app.ingestion.schemas import (
    DocumentIngestRequest,
    DocumentIngestResponse,
)
from app.ingestion.service import ingest_document

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/document", response_model=DocumentIngestResponse)
async def ingest_document_api(
    payload: DocumentIngestRequest = Depends(),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    file_path = f"/tmp/{uuid.uuid4()}.pdf"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    document_id, chunks = await ingest_document(
        db=db,
        file_path=file_path,
        title=payload.title,
        department=payload.department,
        version=payload.version,
        allowed_roles=payload.allowed_roles,
        user_id=current_user.id,
    )

    return DocumentIngestResponse(
        document_id=str(document_id),
        version=payload.version,
        chunks_created=chunks,
    )
