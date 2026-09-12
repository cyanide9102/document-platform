from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.schemas import XmlSchema


class ListXmlSchemasUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def execute(self) -> list[XmlSchema]:
        async with self._unit_of_work:
            return await self._unit_of_work.schemas.list()
