from document_platform.application.processing.models import XPathRule
from document_platform.domain.schemas import XmlSchemaXPathRule


class XPathRuleMapper:
    @staticmethod
    def to_application(rule: XmlSchemaXPathRule) -> XPathRule:
        return XPathRule(
            name=rule.name,
            expression=rule.expression,
            namespaces=rule.namespaces,
            rule_type=rule.rule_type,
        )
