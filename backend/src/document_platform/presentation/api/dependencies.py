from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.application.documents.use_cases import (
    CreateDocumentUseCase,
    GetDocumentContentUseCase,
    GetDocumentUseCase,
    ListDocumentsUseCase,
)
from document_platform.application.schemas.use_cases import (
    CreateXmlSchemaUseCase,
    DeleteXmlSchemaUseCase,
    GetXmlSchemaUseCase,
    ListXmlSchemasUseCase,
)
from document_platform.application.storage.ports import FileStorage
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.config.settings import settings
from document_platform.infrastructure.persistence.database import session_factory
from document_platform.infrastructure.persistence.unit_of_work import (
    SqlAlchemyUnitOfWork,
)
from document_platform.infrastructure.storage.local_file_storage import (
    LocalFileStorage,
)


def get_schema_storage() -> FileStorage:
    return LocalFileStorage(settings.storage_path / "schemas")


def get_document_storage() -> FileStorage:
    return LocalFileStorage(settings.storage_path / "documents")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


async def get_unit_of_work(
    session: AsyncSession = Depends(get_session),
) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session)


async def get_create_xml_schema_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    schema_storage: FileStorage = Depends(get_schema_storage),
) -> CreateXmlSchemaUseCase:
    return CreateXmlSchemaUseCase(unit_of_work, schema_storage)


async def get_delete_xml_schema_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    schema_storage: FileStorage = Depends(get_schema_storage),
) -> DeleteXmlSchemaUseCase:
    return DeleteXmlSchemaUseCase(unit_of_work, schema_storage)


async def get_xml_schema_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> GetXmlSchemaUseCase:
    return GetXmlSchemaUseCase(unit_of_work)


async def get_list_xml_schemas_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> ListXmlSchemasUseCase:
    return ListXmlSchemasUseCase(unit_of_work)


async def get_create_document_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    document_storage: FileStorage = Depends(get_document_storage),
) -> CreateDocumentUseCase:
    return CreateDocumentUseCase(unit_of_work, document_storage)


async def get_document_content_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    document_storage: FileStorage = Depends(get_document_storage),
) -> GetDocumentContentUseCase:
    return GetDocumentContentUseCase(unit_of_work, document_storage)


async def get_document_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> GetDocumentUseCase:
    return GetDocumentUseCase(unit_of_work)


async def get_list_documents_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> ListDocumentsUseCase:
    return ListDocumentsUseCase(unit_of_work)
