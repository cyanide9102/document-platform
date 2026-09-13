from document_platform.domain.schemas import XmlSchema
from document_platform.infrastructure.persistence.models import XmlSchemaModel


class XmlSchemaMapper:
    @staticmethod
    def to_model(schema: XmlSchema) -> XmlSchemaModel:
        return XmlSchemaModel(
            id=schema.id,
            name=schema.name,
            size=schema.size,
            content_hash=schema.content_hash,
            created_at=schema.created_at,
        )

    @staticmethod
    def to_domain(model: XmlSchemaModel) -> XmlSchema:
        return XmlSchema(
            id=model.id,
            name=model.name,
            size=model.size,
            content_hash=model.content_hash,
            created_at=model.created_at,
        )
