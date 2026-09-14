from datetime import UTC, datetime
from uuid import UUID, uuid4

from document_platform.domain.schemas.entities.schema_xpath_rule_type import (
    XmlSchemaXPathRuleType,
)


class XmlSchemaXPathRule:
    def __init__(
        self,
        id: UUID,
        schema_id: UUID,
        name: str,
        expression: str,
        namespaces: dict[str, str],
        rule_type: XmlSchemaXPathRuleType,
        created_at: datetime,
    ):
        self.id = id
        self.schema_id = schema_id
        self.name = name
        self.expression = expression
        self.namespaces = namespaces
        self.rule_type = rule_type
        self.created_at = created_at

    @classmethod
    def create(
        cls,
        schema_id: UUID,
        name: str,
        expression: str,
        namespaces: dict[str, str] | None = None,
        rule_type: XmlSchemaXPathRuleType = XmlSchemaXPathRuleType.EXTRACT,
    ) -> "XmlSchemaXPathRule":
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("XPath rule name cannot be empty.")

        normalized_expression = expression.strip()
        if not normalized_expression:
            raise ValueError("XPath expression cannot be empty.")

        normalized_namespaces = {
            prefix.strip(): uri.strip() for prefix, uri in (namespaces or {}).items()
        }

        if any(not prefix for prefix in normalized_namespaces):
            raise ValueError("XPath namespace prefix cannot be empty.")

        if any(not uri for uri in normalized_namespaces.values()):
            raise ValueError("XPath namespace URI cannot be empty.")

        return cls(
            id=uuid4(),
            schema_id=schema_id,
            name=normalized_name,
            expression=normalized_expression,
            namespaces=normalized_namespaces,
            rule_type=rule_type,
            created_at=datetime.now(UTC),
        )
