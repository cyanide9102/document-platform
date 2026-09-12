from uuid import UUID

from document_platform.application.storage.ports.file_storage import FileStorage
from document_platform.application.unit_of_work import UnitOfWork


class DeleteXmlSchemaUseCase:
    def __init__(self, unit_of_work: UnitOfWork, schema_storage: FileStorage):
        self._unit_of_work = unit_of_work
        self._schema_storage = schema_storage

    async def execute(self, schema_id: UUID):
        async with self._unit_of_work:
            schema = await self._unit_of_work.schemas.get_by_id(schema_id)
            if schema is None:
                return

            document_count = await self._unit_of_work.documents.count_by_schema_id(
                schema.id
            )

            if document_count > 0:
                raise ValueError(
                    f"Cannot delete schema '{schema.id}' because "
                    f"documents reference it."
                )

            await self._unit_of_work.schemas.delete(schema.id)
            await self._unit_of_work.commit()

        await self._schema_storage.delete(schema.id)
