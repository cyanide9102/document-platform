import pytest

from document_platform.application.documents.use_cases import CreateDocumentUseCase
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.documents.entities import Document
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


@pytest.mark.asyncio
async def test_create_document():
    unit_of_work = FakeUnitOfWork()
    use_case = CreateDocumentUseCase(unit_of_work)

    document = await use_case.execute("invoice.xml")

    assert document.name == "invoice.xml"
    assert document.id is not None
    assert len(unit_of_work.documents.documents) == 1
    assert unit_of_work.documents.documents[0] is document
    assert unit_of_work.committed is True
