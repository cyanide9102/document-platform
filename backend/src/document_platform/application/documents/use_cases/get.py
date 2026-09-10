from uuid import UUID

from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.documents.entities import Document


class GetDocumentUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def execute(self, document_id: UUID) -> Document | None:
        async with self._unit_of_work:
            return await self._unit_of_work.documents.get_by_id(document_id)
