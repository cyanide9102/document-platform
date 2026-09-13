from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.domain.documents.entities import Document
from document_platform.domain.documents.repositories import DocumentRepository
from document_platform.infrastructure.persistence.mappers.document_mapper import (
    to_domain,
    to_model,
)
from document_platform.infrastructure.persistence.models.document import DocumentModel


class SqlAlchemyDocumentRepository(DocumentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, document: Document):
        model = to_model(document)

        self.session.add(model)

    async def update(self, document):
        model = await self.session.get(DocumentModel, document.id)
        if model is None:
            return

        model.name = document.name
        model.status = document.status
        model.updated_at = document.updated_at

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

    async def count_by_schema_id(self, schema_id: UUID) -> int:
        statement = (
            select(func.count())
            .select_from(DocumentModel)
            .where(DocumentModel.schema_id == schema_id)
        )

        result = await self.session.execute(statement)
        return result.scalar_one()
