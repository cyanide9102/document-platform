import hashlib
from typing import BinaryIO
from uuid import UUID

from document_platform.application.processing.ports import DocumentWorkflowStarter
from document_platform.application.storage.ports import FileStorage
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.documents import Document


class CreateDocumentUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        document_storage: FileStorage,
        workflow_starter: DocumentWorkflowStarter,
    ):
        self._unit_of_work = unit_of_work
        self._document_storage = document_storage
        self._workflow_starter = workflow_starter

    async def execute(
        self,
        name: str,
        content: BinaryIO,
        content_type: str | None,
        schema_id: UUID,
    ) -> Document:
        async with self._unit_of_work:
            schema = await self._unit_of_work.schemas.get_by_id(schema_id)
            if schema is None:
                raise ValueError(f"Schema not found: {schema_id}")

            size, content_hash = self._process_content(content)
            document = Document.create(
                name=name,
                content_type=content_type,
                size=size,
                content_hash=content_hash,
                schema_id=schema.id,
            )

            try:
                await self._document_storage.save(document.id, content)

                await self._unit_of_work.documents.add(document)
                await self._unit_of_work.commit()
            except Exception:
                await self._document_storage.delete(document.id)
                raise

        await self._workflow_starter.start(document.id)
        return document

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
