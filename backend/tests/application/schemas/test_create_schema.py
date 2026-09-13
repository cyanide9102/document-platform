from io import BytesIO

import pytest

from document_platform.application.schemas.use_cases import CreateXmlSchemaUseCase
from document_platform.application.storage.ports import FileStorage
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.schemas import XmlSchema, XmlSchemaRepository

VALID_XSD = b"""<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="invoice">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="number" type="xs:string"/>
                <xs:element name="amount" type="xs:decimal"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>
"""


INVALID_XSD = b"""<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="invoice" type="xs:thisTypeDoesNotExist"/>
</xs:schema>
"""


class FakeXmlSchemaRepository(XmlSchemaRepository):
    def __init__(self):
        self.schemas: list[XmlSchema] = []

    async def add(self, schema: XmlSchema) -> None:
        self.schemas.append(schema)

    async def get_by_id(self, schema_id) -> XmlSchema | None:
        for schema in self.schemas:
            if schema.id == schema_id:
                return schema

        return None

    async def delete(self, schema_id) -> None:
        self.schemas = [schema for schema in self.schemas if schema.id != schema_id]

    async def list(self) -> list[XmlSchema]:
        return self.schemas


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
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


class FakeSchemaStorage(FileStorage):
    def __init__(self):
        self.saved_schemas: dict[str, bytes] = {}
        self.deleted_schemas: list[str] = []

    async def save(self, file_id, content):
        self.saved_schemas[str(file_id)] = content.read()

    async def get(self, file_id):
        content = self.saved_schemas[str(file_id)]
        return BytesIO(content)

    async def delete(self, file_id):
        file_id = str(file_id)
        self.deleted_schemas.append(file_id)
        self.saved_schemas.pop(file_id, None)


@pytest.mark.asyncio
async def test_create_schema():
    unit_of_work = FakeUnitOfWork()
    schema_storage = FakeSchemaStorage()

    use_case = CreateXmlSchemaUseCase(
        unit_of_work,
        schema_storage,
    )

    content = BytesIO(VALID_XSD)

    schema = await use_case.execute(
        name="Invoice",
        content=content,
    )

    assert schema.id is not None
    assert schema.name == "Invoice"
    assert schema.size == len(VALID_XSD)
    assert len(schema.content_hash) == 64

    assert len(unit_of_work.schemas.schemas) == 1
    assert unit_of_work.schemas.schemas[0] is schema
    assert unit_of_work.committed is True

    schema_id = str(schema.id)

    assert schema_id in schema_storage.saved_schemas
    assert schema_storage.saved_schemas[schema_id] == VALID_XSD


@pytest.mark.asyncio
async def test_create_schema_rejects_invalid_xsd():
    unit_of_work = FakeUnitOfWork()
    schema_storage = FakeSchemaStorage()

    use_case = CreateXmlSchemaUseCase(
        unit_of_work,
        schema_storage,
    )

    content = BytesIO(INVALID_XSD)

    with pytest.raises(
        ValueError,
        match="Invalid XML schema.",
    ):
        await use_case.execute(
            name="Invalid Invoice",
            content=content,
        )

    assert len(unit_of_work.schemas.schemas) == 0
    assert len(schema_storage.saved_schemas) == 0
    assert unit_of_work.committed is False


@pytest.mark.asyncio
async def test_create_schema_deletes_storage_when_commit_fails():
    unit_of_work = FailingUnitOfWork()
    schema_storage = FakeSchemaStorage()

    use_case = CreateXmlSchemaUseCase(
        unit_of_work,
        schema_storage,
    )

    content = BytesIO(VALID_XSD)

    with pytest.raises(
        RuntimeError,
        match="Database failure",
    ):
        await use_case.execute(
            name="Invoice",
            content=content,
        )

    assert len(schema_storage.saved_schemas) == 0
    assert len(schema_storage.deleted_schemas) == 1
