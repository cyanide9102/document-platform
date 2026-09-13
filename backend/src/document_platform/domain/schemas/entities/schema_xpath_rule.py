from datetime import UTC, datetime
from uuid import UUID, uuid4


class XmlSchemaXPathRule:
    def __init__(
        self,
        id: UUID,
        schema_id: UUID,
        name: str,
        expression: str,
        namespaces: dict[str, str],
        created_at: datetime,
    ):
        self.id = id
        self.schema_id = schema_id
        self.name = name
        self.expression = expression
        self.namespaces = namespaces
        self.created_at = created_at

    @classmethod
    def create(
        cls,
        schema_id: UUID,
        name: str,
        expression: str,
        namespaces: dict[str, str] | None = None,
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
            created_at=datetime.now(UTC),
        )
