from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.rag.schemas import RAGQueryRequest, RAGQueryResponse, Citation
from app.rag.service import (
    retrieve_authorized_chunks,
    similarity_gate,
    build_context,
)

# Replace these with your real implementations
from app.core.embedding import embed_text
from app.core.llm import generate_answer
from app.core.vector import vector_client

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/query", response_model=RAGQueryResponse)
async def rag_query(
    payload: RAGQueryRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Secure RAG endpoint with:
    - JWT auth
    - RBAC
    - Similarity gating
    """

    # 1️⃣ Extract roles
    user_roles = [role.name for role in current_user.roles]

    # 2️⃣ Embed question
    query_embedding = embed_text(payload.question)

    # 3️⃣ Retrieve authorized chunks
    chunks = await retrieve_authorized_chunks(
        vector_client=vector_client,
        query_embedding=query_embedding,
        allowed_roles=user_roles,
    )

    # 4️⃣ Similarity gate
    try:
        similarity_gate(chunks)
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No authorized information found",
        )

    # 5️⃣ Build context
    context = build_context(chunks)

    # 6️⃣ Generate answer
    answer = generate_answer(
        question=payload.question,
        context=context,
    )

    # 7️⃣ Build citations
    citations = [
        Citation(
            document_id=chunk["document_id"],
            document_version=chunk["document_version"],
            page=chunk.get("page"),
            snippet=chunk["text"][:300],  # safe excerpt
        )
        for chunk in chunks
    ]

    return RAGQueryResponse(
        answer=answer,
        citations=citations,
    )
