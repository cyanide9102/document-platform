from temporalio import activity

from document_platform.application.documents.use_cases.process import (
    ProcessDocumentUseCase,
)
from document_platform.config.settings import settings
from document_platform.infrastructure.persistence.database import session_factory
from document_platform.infrastructure.persistence.unit_of_work import (
    SqlAlchemyUnitOfWork,
)
from document_platform.infrastructure.processing.xml_document_processor import (
    XmlDocumentProcessor,
)
from document_platform.infrastructure.storage.local_file_storage import LocalFileStorage
from document_platform.infrastructure.temporal.contracts import DocumentWorkflowInput


class DocumentActivities:
    @activity.defn(name="process_document")
    async def process_document(self, input: DocumentWorkflowInput):
        async with session_factory() as session:
            unit_of_work = SqlAlchemyUnitOfWork(session)

            process_document_use_case = ProcessDocumentUseCase(
                unit_of_work=unit_of_work,
                schema_storage=LocalFileStorage(settings.storage_path / "schemas"),
                document_storage=LocalFileStorage(settings.storage_path / "documents"),
                document_processor=XmlDocumentProcessor(),
            )

            await process_document_use_case.execute(input.document_id)
