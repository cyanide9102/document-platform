from document_platform.domain.schemas.entities.schema_xpath_rule import (
    XmlSchemaXPathRule,
)
from document_platform.infrastructure.persistence.models.schema_xpath_rule import (
    XmlSchemaXPathRuleModel,
)


class XmlSchemaXPathRuleMapper:
    @staticmethod
    def to_model(rule: XmlSchemaXPathRule) -> XmlSchemaXPathRuleModel:
        return XmlSchemaXPathRuleModel(
            id=rule.id,
            schema_id=rule.schema_id,
            name=rule.name,
            expression=rule.expression,
            namespaces=rule.namespaces,
            created_at=rule.created_at,
        )

    @staticmethod
    def to_domain(model: XmlSchemaXPathRuleModel) -> XmlSchemaXPathRule:
        return XmlSchemaXPathRule(
            id=model.id,
            schema_id=model.schema_id,
            name=model.name,
            expression=model.expression,
            namespaces=model.namespaces,
            created_at=model.created_at,
        )
