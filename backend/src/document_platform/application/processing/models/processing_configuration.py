from dataclasses import dataclass

from document_platform.application.processing.models.xpath_rule import XPathRule


@dataclass(frozen=True)
class ProcessingConfiguration:
    xpath_rules: list[XPathRule]
    schematron: bytes | None = None
