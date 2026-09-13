from abc import ABC, abstractmethod
from uuid import UUID

from document_platform.domain.schemas.entities.schema_xpath_rule import (
    XmlSchemaXPathRule,
)


class XmlSchemaXPathRuleRepository(ABC):
    @abstractmethod
    async def add(self, rule: XmlSchemaXPathRule):
        pass

    @abstractmethod
    async def list_by_schema_id(self, schema_id: UUID) -> list[XmlSchemaXPathRule]:
        pass

    @abstractmethod
    async def get_by_id(self, rule_id: UUID) -> XmlSchemaXPathRule | None:
        pass

    @abstractmethod
    async def delete(self, rule_id: UUID):
        pass
