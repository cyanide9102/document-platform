import hashlib

from lxml import etree

from document_platform.application.storage.ports import FileStorage
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.schemas import XmlSchema


class CreateXmlSchemaUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        schema_storage: FileStorage,
    ):
        self._unit_of_work = unit_of_work
        self._schema_storage = schema_storage

    async def execute(self, name: str, content: bytes) -> XmlSchema:
        size = len(content)
        content_hash = hashlib.sha256(content).hexdigest()

        self._validate_schema(content)

        schema = XmlSchema.create(name=name, size=size, content_hash=content_hash)

        try:
            await self._schema_storage.save(schema.id, content)

            async with self._unit_of_work:
                await self._unit_of_work.schemas.add(schema)
                await self._unit_of_work.commit()

            return schema
        except Exception:
            await self._schema_storage.delete(schema.id)
            raise

    @staticmethod
    def _validate_schema(content: bytes):
        try:
            schema_document = etree.fromstring(content)
            etree.XMLSchema(schema_document)
        except (etree.XMLSyntaxError, etree.XMLSchemaParseError) as exception:
            raise ValueError("Invalid XML schema.") from exception
