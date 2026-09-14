from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.domain.schemas import (
    XmlSchemaSchematron,
    XmlSchemaSchematronRepository,
)
from document_platform.infrastructure.persistence.mappers import (
    XmlSchemaSchematronMapper,
)
from document_platform.infrastructure.persistence.models import XmlSchemaSchematronModel


class SqlAlchemyXmlSchemaSchematronRepository(XmlSchemaSchematronRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, schematron: XmlSchemaSchematron):
        model = XmlSchemaSchematronMapper.to_model(schematron)
        self._session.add(model)

    async def get_by_schema_id(self, schema_id: UUID) -> XmlSchemaSchematron | None:
        statement = select(XmlSchemaSchematronModel).where(
            XmlSchemaSchematronModel.schema_id == schema_id
        )

        result = await self._session.execute(statement)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return XmlSchemaSchematronMapper.to_domain(model)

    async def delete_by_schema_id(self, schema_id: UUID):
        statement = delete(XmlSchemaSchematronModel).where(
            XmlSchemaSchematronModel.schema_id == schema_id,
        )

        await self._session.execute(statement)
