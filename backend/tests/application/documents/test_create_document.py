from io import BytesIO
from uuid import UUID

import pytest

from document_platform.application.documents.use_cases import CreateDocumentUseCase
from document_platform.application.storage.ports import FileStorage
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.documents import Document, DocumentStatus
from document_platform.domain.documents.repositories import DocumentRepository
from document_platform.domain.schemas import XmlSchema
from document_platform.domain.schemas.repositories import XmlSchemaRepository

SCHEMA_ID = UUID("11111111-1111-1111-1111-111111111111")


class FakeDocumentRepository(DocumentRepository):
    def __init__(self):
        self.documents: list[Document] = []

    async def add(self, document):
        self.documents.append(document)

    async def get_by_id(self, document_id) -> Document | None:
        for document in self.documents:
            if document.id == document_id:
                return document

        return None

    async def list(self) -> list[Document]:
        return self.documents


class FakeXmlSchemaRepository(XmlSchemaRepository):
    def __init__(self):
        self.schemas: list[XmlSchema] = []

    async def add(self, schema):
        self.schemas.append(schema)

    async def get_by_id(self, schema_id) -> XmlSchema | None:
        for schema in self.schemas:
            if schema.id == schema_id:
                return schema

        return None

    async def list(self) -> list[XmlSchema]:
        return self.schemas

    async def delete(self, schema_id):
        self.schemas = [schema for schema in self.schemas if schema.id != schema_id]


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.documents = FakeDocumentRepository()
        self.schemas = FakeXmlSchemaRepository()
        self.committed = False

    async def __aenter__(self) -> "FakeUnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object | None,
    ):
        pass

    async def commit(self):
        self.committed = True

    async def rollback(self):
        pass


class FailingUnitOfWork(FakeUnitOfWork):
    async def commit(self):
        raise RuntimeError("Database failure")


class FakeDocumentStorage(FileStorage):
    def __init__(self):
        self.saved_documents: dict[str, bytes] = {}
        self.deleted_documents: list[str] = []

    async def save(self, document_id, content):
        self.saved_documents[str(document_id)] = content.read()

    async def get(self, document_id):
        content = self.saved_documents[str(document_id)]
        return BytesIO(content)

    async def delete(self, document_id):
        document_id = str(document_id)

        self.deleted_documents.append(document_id)
        self.saved_documents.pop(document_id, None)


def create_schema() -> XmlSchema:
    schema = XmlSchema.create(
        name="Invoice",
        size=1024,
        content_hash="a" * 64,
    )

    schema.id = SCHEMA_ID

    return schema


@pytest.mark.asyncio
async def test_create_document():
    unit_of_work = FakeUnitOfWork()
    document_storage = FakeDocumentStorage()

    schema = create_schema()
    unit_of_work.schemas.schemas.append(schema)

    use_case = CreateDocumentUseCase(
        unit_of_work,
        document_storage,
    )

    content = BytesIO(b"<invoice>test</invoice>")

    document = await use_case.execute(
        name="invoice.xml",
        content=content,
        content_type="application/xml",
        schema_id=SCHEMA_ID,
    )

    assert document.name == "invoice.xml"
    assert document.original_name == "invoice.xml"
    assert document.id is not None
    assert document.content_type == "application/xml"
    assert document.size == len(b"<invoice>test</invoice>")
    assert len(document.content_hash) == 64
    assert document.schema_id == SCHEMA_ID
    assert document.status == DocumentStatus.UPLOADED

    assert len(unit_of_work.documents.documents) == 1
    assert unit_of_work.documents.documents[0] is document
    assert unit_of_work.committed is True

    document_id = str(document.id)

    assert document_id in document_storage.saved_documents
    assert document_storage.saved_documents[document_id] == b"<invoice>test</invoice>"


@pytest.mark.asyncio
async def test_create_document_rejects_nonexistent_schema():
    unit_of_work = FakeUnitOfWork()
    document_storage = FakeDocumentStorage()

    use_case = CreateDocumentUseCase(
        unit_of_work,
        document_storage,
    )

    content = BytesIO(b"<invoice>test</invoice>")

    with pytest.raises(
        ValueError,
        match=f"Schema not found: {SCHEMA_ID}",
    ):
        await use_case.execute(
            name="invoice.xml",
            content=content,
            content_type="application/xml",
            schema_id=SCHEMA_ID,
        )

    assert len(unit_of_work.documents.documents) == 0
    assert len(document_storage.saved_documents) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_create_document_deletes_storage_when_commit_fails():
    unit_of_work = FailingUnitOfWork()
    document_storage = FakeDocumentStorage()

    schema = create_schema()
    unit_of_work.schemas.schemas.append(schema)

    use_case = CreateDocumentUseCase(
        unit_of_work,
        document_storage,
    )

    content = BytesIO(b"<invoice>test</invoice>")

    with pytest.raises(RuntimeError, match="Database failure"):
        await use_case.execute(
            name="invoice.xml",
            content=content,
            content_type="application/xml",
            schema_id=SCHEMA_ID,
        )

    assert len(document_storage.saved_documents) == 0
    assert len(document_storage.deleted_documents) == 1
