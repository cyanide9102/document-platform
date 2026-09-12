from uuid import UUID

from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.schemas import XmlSchema


class GetXmlSchemaUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def execute(self, schema_id: UUID) -> XmlSchema | None:
        async with self._unit_of_work:
            return await self._unit_of_work.schemas.get_by_id(schema_id)
