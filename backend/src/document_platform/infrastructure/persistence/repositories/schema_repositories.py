from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.domain.schemas import XmlSchema
from document_platform.domain.schemas.repositories import XmlSchemaRepository
from document_platform.infrastructure.persistence.mappers.schema_mapper import (
    to_domain,
    to_model,
)
from document_platform.infrastructure.persistence.models import XmlSchemaModel


class SqlAlchemyXmlSchemaRepository(XmlSchemaRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, schema: XmlSchema):
        model = to_model(schema)

        self._session.add(model)

    async def list(self) -> list[XmlSchema]:
        statement = select(XmlSchemaModel).order_by(XmlSchemaModel.created_at.desc())

        result = await self._session.execute(statement)
        models = result.scalars().all()

        return [to_domain(model) for model in models]

    async def get_by_id(self, schema_id: UUID) -> XmlSchema | None:
        statement = select(XmlSchemaModel).where(XmlSchemaModel.id == schema_id)

        result = await self._session.execute(statement)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return to_domain(model)

    async def delete(self, schema_id):
        statement = delete(XmlSchemaModel).where(XmlSchemaModel.id == schema_id)
        await self._session.execute(statement)
