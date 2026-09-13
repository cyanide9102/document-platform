from document_platform.domain.documents import Document, DocumentStatus
from document_platform.infrastructure.persistence.models import DocumentModel


class DocumentMapper:
    @staticmethod
    def to_model(document: Document) -> DocumentModel:
        return DocumentModel(
            id=document.id,
            name=document.name,
            original_name=document.original_name,
            content_type=document.content_type,
            size=document.size,
            content_hash=document.content_hash,
            schema_id=document.schema_id,
            status=document.status.value,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )

    @staticmethod
    def to_domain(model: DocumentModel) -> Document:
        return Document(
            id=model.id,
            name=model.name,
            original_name=model.original_name,
            content_type=model.content_type,
            size=model.size,
            content_hash=model.content_hash,
            schema_id=model.schema_id,
            status=DocumentStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
