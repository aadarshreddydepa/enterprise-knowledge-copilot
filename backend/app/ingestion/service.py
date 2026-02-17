import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document import Document
from app.db.models.document_version import DocumentVersion
from app.db.models.audit_log import AuditLog
from app.ingestion.utils import extract_pdf_pages, chunk_text
from app.core.embedding import embed_text
from app.core.vector import vector_client


async def ingest_document(
    *,
    db: AsyncSession,
    file_path: str,
    title: str,
    department: str,
    version: int,
    allowed_roles: list[str],
    user_id: uuid.UUID,
):
    # 1️⃣ Create document
    document = Document(
        title=title,
        department=department,
        created_by=user_id,
    )
    db.add(document)
    await db.flush()

    # 2️⃣ Create document version
    doc_version = DocumentVersion(
        document_id=document.id,
        version=version,
        source_path=file_path,
        checksum="todo",
    )
    db.add(doc_version)
    await db.flush()

    # 3️⃣ Extract pages
    pages = extract_pdf_pages(file_path)

    chunk_count = 0

    for page_number, page_text in enumerate(pages, start=1):
        chunks = chunk_text(page_text)

        for chunk in chunks:
            embedding = embed_text(chunk)

            vector_client.upsert(
                vectors=[
                    {
                        "id": str(uuid.uuid4()),
                        "values": embedding,
                        "metadata": {
                            "document_id": str(document.id),
                            "document_version": version,
                            "page": page_number,
                            "roles": allowed_roles,
                            "text": chunk,
                        },
                    }
                ]
            )
            chunk_count += 1

    # 4️⃣ Audit log
    audit = AuditLog(
        user_id=user_id,
        action="DOCUMENT_INGEST",
        roles_applied=allowed_roles,
        retrieved_doc_ids=[str(document.id)],
        outcome="SUCCESS",
    )
    db.add(audit)

    await db.commit()

    return document.id, chunk_count
