import hashlib
from typing import BinaryIO

from document_platform.application.documents.ports import DocumentStorage
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.documents import Document


class CreateDocumentUseCase:
    def __init__(self, unit_of_work: UnitOfWork, document_storage: DocumentStorage):
        self._unit_of_work = unit_of_work
        self._document_storage = document_storage

    async def execute(
        self,
        name: str,
        content: BinaryIO,
        content_type: str | None,
    ) -> Document:
        size, content_hash = self._process_content(content)
        document = Document.create(name, content_type, size, content_hash)

        try:
            await self._document_storage.save(document.id, content)

            await self._unit_of_work.documents.add(document)
            await self._unit_of_work.commit()

            return document
        except Exception:
            await self._document_storage.delete(document.id)
            raise

    def _process_content(self, content: BinaryIO) -> tuple[int, str]:
        content.seek(0)

        hasher = hashlib.sha256()

        size = 0
        while chunk := content.read(1024 * 1024):
            hasher.update(chunk)
            size += len(chunk)

        content_hash = hasher.hexdigest()

        content.seek(0)

        return size, content_hash
