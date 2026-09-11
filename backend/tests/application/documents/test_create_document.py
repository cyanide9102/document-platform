from io import BytesIO

import pytest

from document_platform.application.documents.ports.document_storage import (
    DocumentStorage,
)
from document_platform.application.documents.use_cases import CreateDocumentUseCase
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.documents.entities import Document
from document_platform.domain.documents.enums import DocumentStatus
from document_platform.domain.documents.repositories import DocumentRepository


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


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.documents = FakeDocumentRepository()
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


class FakeDocumentStorage(DocumentStorage):
    def __init__(self):
        self.saved_documents: dict[str, bytes] = {}
        self.deleted_keys: list[str] = []

    async def save(
        self,
        document_id,
        filename,
        content,
    ) -> str:
        storage_key = f"documents/{document_id}/{filename}"

        self.saved_documents[storage_key] = content.read()

        return storage_key

    async def get(self, storage_key):
        content = self.saved_documents[storage_key]
        return BytesIO(content)

    async def delete(self, storage_key):
        self.deleted_keys.append(storage_key)
        self.saved_documents.pop(storage_key, None)


@pytest.mark.asyncio
async def test_create_document():
    unit_of_work = FakeUnitOfWork()
    document_storage = FakeDocumentStorage()
    use_case = CreateDocumentUseCase(unit_of_work, document_storage)

    content = BytesIO(b"<invoice>test</invoice>")

    document = await use_case.execute(
        name="invoice.xml",
        content=content,
        content_type="application/xml",
    )

    assert document.name == "invoice.xml"
    assert document.id is not None
    assert document.content_type == "application/xml"
    assert document.size == len(b"<invoice>test</invoice>")
    assert document.storage_key == (f"documents/{document.id}/invoice.xml")
    assert document.status == DocumentStatus.UPLOADED

    assert len(unit_of_work.documents.documents) == 1
    assert unit_of_work.documents.documents[0] is document
    assert unit_of_work.committed is True

    assert document.storage_key in document_storage.saved_documents
    assert (
        document_storage.saved_documents[document.storage_key]
        == b"<invoice>test</invoice>"
    )


@pytest.mark.asyncio
async def test_create_document_deletes_storage_when_commit_fails():
    unit_of_work = FailingUnitOfWork()
    document_storage = FakeDocumentStorage()

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
        )

    assert len(document_storage.saved_documents) == 0
    assert len(document_storage.deleted_keys) == 1
