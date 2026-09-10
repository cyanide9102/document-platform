from uuid import UUID

from pydantic import BaseModel, Field

from document_platform.domain.documents.enums import DocumentStatus


class CreateDocumentRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class DocumentResponse(BaseModel):
    id: UUID
    name: str
    status: DocumentStatus
