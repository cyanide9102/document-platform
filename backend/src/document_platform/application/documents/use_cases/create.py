from typing import BinaryIO

from document_platform.application.documents.ports.document_storage import (
    DocumentStorage,
)
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.application.utils import validate_filename
from document_platform.domain.documents.entities import Document


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
        start = content.tell()
        content.seek(0, 2)
        size = content.tell()
        content.seek(start)

        normalized_name = validate_filename(name)

        document = Document.create(normalized_name, content_type, size)

        storage_key = await self._document_storage.save(
            document_id=document.id,
            filename=document.name,
            content=content,
        )

        try:
            document.attach_storage(storage_key)
            document.mark_uploaded()

            await self._unit_of_work.documents.add(document)
            await self._unit_of_work.commit()

            return document
        except Exception:
            await self._document_storage.delete(storage_key)
            raise
