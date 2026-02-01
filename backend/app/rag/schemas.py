from pydantic import BaseModel, Field
from typing import List


class RAGQueryRequest(BaseModel):
    question: str = Field(min_length=5, max_length=500)


class Citation(BaseModel):
    document_id: str
    document_version: int
    page: int | None
    snippet: str


class RAGQueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
