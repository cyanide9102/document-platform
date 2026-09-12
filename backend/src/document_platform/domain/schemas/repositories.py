from abc import ABC, abstractmethod
from uuid import UUID

from document_platform.domain.schemas.entities import XmlSchema


class XmlSchemaRepository(ABC):
    @abstractmethod
    async def add(self, schema: XmlSchema):
        pass

    @abstractmethod
    async def list(self) -> list[XmlSchema]:
        pass

    @abstractmethod
    async def get_by_id(self, schema_id: UUID) -> XmlSchema | None:
        pass

    @abstractmethod
    async def delete(self, schema_id: UUID):
        pass
