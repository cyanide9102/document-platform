from document_platform.domain.documents.entities import Document
from document_platform.domain.documents.enums import DocumentStatus
from document_platform.infrastructure.persistence.models.document import DocumentModel


def to_model(document: Document) -> DocumentModel:
    return DocumentModel(
        id=document.id,
        name=document.name,
        status=document.status.value,
        created_at=document.created_at,
        updated_at=document.updated_at,
    )


def to_domain(model: DocumentModel) -> Document:
    return Document(
        id=model.id,
        name=model.name,
        status=DocumentStatus(model.status),
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
