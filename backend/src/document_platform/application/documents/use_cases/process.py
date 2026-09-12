from uuid import UUID

from document_platform.application.processing.ports import DocumentProcessor
from document_platform.application.storage.ports import FileStorage
from document_platform.application.unit_of_work import UnitOfWork


class ProcessDocumentUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        schema_storage: FileStorage,
        document_storage: FileStorage,
        document_processor: DocumentProcessor,
    ):
        self._unit_of_work = unit_of_work
        self._schema_storage = schema_storage
        self._document_storage = document_storage
        self._document_processor = document_processor

    async def execute(self, document_id: UUID):
        async with self._unit_of_work:
            document = await self._unit_of_work.documents.get_by_id(document_id)
            if document is None:
                return

            schema = await self._unit_of_work.schemas.get_by_id(document.schema_id)
            if schema is None:
                raise ValueError(f"Schema not found: {document.schema_id}")

            document.start_processing()
            await self._unit_of_work.commit()

            try:
                document_content = await self._document_storage.get(document.id)
                schema_content = await self._schema_storage.get(schema.id)

                await self._document_processor.process(document_content, schema_content)

                document.mark_processed()
            except Exception:
                document.mark_failed()

            await self._unit_of_work.commit()
