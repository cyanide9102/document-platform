from typing import BinaryIO
from uuid import UUID

from document_platform.application.documents.ports import DocumentStorage
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.documents import Document


class GetDocumentContentUseCase:
    def __init__(self, unit_of_work: UnitOfWork, document_storage: DocumentStorage):
        self._unit_of_work = unit_of_work
        self._document_storage = document_storage

    async def execute(self, document_id: UUID) -> tuple[Document, BinaryIO]:
        document = await self._unit_of_work.documents.get_by_id(document_id)
        if document is None:
            raise ValueError("Document not found.")

        content = await self._document_storage.get(document.storage_key)

        return document, content
