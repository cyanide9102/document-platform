from document_platform.domain.schemas import XmlSchemaSchematron
from document_platform.infrastructure.persistence.models import (
    XmlSchemaSchematronModel,
)


class XmlSchemaSchematronMapper:
    @staticmethod
    def to_model(schematron: XmlSchemaSchematron) -> XmlSchemaSchematronModel:
        return XmlSchemaSchematronModel(
            id=schematron.id,
            schema_id=schematron.schema_id,
            name=schematron.name,
            size=schematron.size,
            content_hash=schematron.content_hash,
            created_at=schematron.created_at,
        )

    @staticmethod
    def to_domain(model: XmlSchemaSchematronModel) -> XmlSchemaSchematron:
        return XmlSchemaSchematron(
            id=model.id,
            schema_id=model.schema_id,
            name=model.name,
            size=model.size,
            content_hash=model.content_hash,
            created_at=model.created_at,
        )
