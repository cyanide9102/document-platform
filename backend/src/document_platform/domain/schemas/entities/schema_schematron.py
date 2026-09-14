from datetime import UTC, datetime
from uuid import UUID, uuid4


class XmlSchemaSchematron:
    def __init__(
        self,
        id: UUID,
        schema_id: UUID,
        name: str,
        size: int,
        content_hash: str,
        created_at: datetime,
    ):
        self.id = id
        self.schema_id = schema_id
        self.name = name
        self.size = size
        self.content_hash = content_hash
        self.created_at = created_at

    @classmethod
    def create(
        cls,
        schema_id: UUID,
        name: str,
        size: int,
        content_hash: str,
    ) -> "XmlSchemaSchematron":
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Schematron name cannot be empty.")

        if "/" in normalized_name or "\\" in normalized_name:
            raise ValueError("Schematron name cannot contain a path.")

        if size < 0:
            raise ValueError("Schematron size cannot be negative.")

        normalized_content_hash = content_hash.strip()

        if len(normalized_content_hash) != 64:
            raise ValueError("Schematron content hash must be a SHA-256 hash.")

        if any(
            character not in "0123456789abcdefABCDEF"
            for character in normalized_content_hash
        ):
            raise ValueError("Schematron content hash must be a hexadecimal string.")

        return cls(
            id=uuid4(),
            schema_id=schema_id,
            name=normalized_name,
            size=size,
            content_hash=normalized_content_hash,
            created_at=datetime.now(UTC),
        )
