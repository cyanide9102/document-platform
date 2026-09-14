import hashlib
from uuid import UUID

from lxml import etree

from document_platform.application.storage.ports import FileStorage
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.schemas import XmlSchemaSchematron


class CreateXmlSchemaSchematronUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        schematron_storage: FileStorage,
    ):
        self._unit_of_work = unit_of_work
        self._schematron_storage = schematron_storage

    async def execute(
        self,
        schema_id: UUID,
        name: str,
        content: bytes,
    ) -> XmlSchemaSchematron:
        async with self._unit_of_work:
            schema = await self._unit_of_work.schemas.get_by_id(schema_id)
            if schema is None:
                raise ValueError(f"Schema not found: {schema_id}")

            existing = await self._unit_of_work.schema_schematrons.get_by_schema_id(
                schema_id
            )

            if existing is not None:
                raise ValueError(f"Schematron already exists for schema: {schema_id}")

            size = len(content)
            content_hash = hashlib.sha256(content).hexdigest()

            self._validate_schematron_definition(content)

            schematron = XmlSchemaSchematron.create(
                schema_id=schema_id,
                name=name,
                size=size,
                content_hash=content_hash,
            )

            try:
                await self._schematron_storage.save(schematron.id, content)

                await self._unit_of_work.schema_schematrons.add(schematron)
                await self._unit_of_work.commit()

                return schematron
            except Exception:
                await self._schematron_storage.delete(schematron.id)
                raise

    @staticmethod
    def _validate_schematron_definition(schematron: bytes):
        try:
            schematron_document = etree.fromstring(schematron)
            etree.Schematron(schematron_document)
        except (etree.XMLSyntaxError, etree.SchematronParseError) as exception:
            raise ValueError("Invalid Schematron definition.") from exception
