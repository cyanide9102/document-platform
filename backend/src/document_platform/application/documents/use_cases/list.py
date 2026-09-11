from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.documents import Document


class ListDocumentsUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def execute(self) -> list[Document]:
        async with self._unit_of_work:
            return await self._unit_of_work.documents.list()
