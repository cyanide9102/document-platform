from abc import ABC, abstractmethod
from uuid import UUID

from document_platform.domain.schemas.entities.schema_schematron import (
    XmlSchemaSchematron,
)


class XmlSchemaSchematronRepository(ABC):
    @abstractmethod
    async def add(self, schematron: XmlSchemaSchematron):
        pass

    @abstractmethod
    async def get_by_schema_id(self, schema_id: UUID) -> XmlSchemaSchematron | None:
        pass

    @abstractmethod
    async def delete_by_schema_id(self, schema_id: UUID):
        pass
