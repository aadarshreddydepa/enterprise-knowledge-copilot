from pydantic import BaseModel, Field
from typing import List


class DocumentIngestRequest(BaseModel):
    title: str
    department: str
    allowed_roles: List[str]
    version: int = Field(ge=1)


class DocumentIngestResponse(BaseModel):
    document_id: str
    version: int
    chunks_created: int
