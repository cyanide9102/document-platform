from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.domain.documents.entities import Document
from document_platform.domain.documents.repositories import DocumentRepository
from document_platform.infrastructure.persistence.mappers.document_mapper import (
    to_domain,
    to_model,
)
from document_platform.infrastructure.persistence.models.document import DocumentModel


class SqlAlchemyDocumentRepository(DocumentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, document: Document) -> None:
        model = to_model(document)

        self.session.add(model)

    async def get_by_id(self, document_id: UUID) -> Document | None:
        statement = select(DocumentModel).where(DocumentModel.id == document_id)
        result = await self.session.execute(statement)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return to_domain(model)

    async def list(self) -> list[Document]:
        statement = select(DocumentModel).order_by(DocumentModel.created_at.desc())
        result = await self.session.execute(statement)
        models = result.scalars().all()

        return [to_domain(model) for model in models]
