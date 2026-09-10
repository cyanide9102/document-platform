from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.documents.entities import Document


class CreateDocument:
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def execute(self, name: str) -> Document:
        document = Document.create(name)

        async with self._unit_of_work:
            await self._unit_of_work.documents.add(document)
            await self._unit_of_work.commit()

        return document
