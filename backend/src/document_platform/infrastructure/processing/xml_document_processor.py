from typing import BinaryIO

from lxml import etree

from document_platform.application.processing.models import (
    ExtractedValue,
    ProcessingConfiguration,
    ProcessingResult,
    ValidationResult,
    ValidationSeverity,
)
from document_platform.application.processing.ports import DocumentProcessor
from document_platform.domain.schemas.entities.schema_xpath_rule_type import (
    XmlSchemaXPathRuleType,
)


class XmlDocumentProcessor(DocumentProcessor):
    async def process(
        self,
        document: BinaryIO,
        schema: BinaryIO,
        configuration: ProcessingConfiguration,
    ) -> ProcessingResult:
        document.seek(0)

        try:
            xml_document = etree.parse(document)
        except etree.XMLSyntaxError as exception:
            raise ValueError("Document contains invalid XML.") from exception

        schema.seek(0)

        try:
            schema_document = etree.parse(schema)
            xml_schema = etree.XMLSchema(schema_document)
        except (etree.XMLSyntaxError, etree.XMLSchemaParseError) as exception:
            raise ValueError("Invalid XML schema.") from exception

        validation_results = []
        if not xml_schema.validate(xml_document):
            validation_results.extend(
                ValidationResult(
                    severity=ValidationSeverity.ERROR,
                    code="XSD_VALIDATION_ERROR",
                    message=error.message,
                    line=error.line,
                    column=error.column,
                )
                for error in xml_schema.error_log
            )

        extracted_values = []
        for rule in configuration.xpath_rules:
            result = xml_document.xpath(rule.expression, namespaces=rule.namespaces)

            if rule.rule_type == XmlSchemaXPathRuleType.EXTRACT:
                extracted_values.append(
                    ExtractedValue(
                        name=rule.name,
                        values=[
                            etree.tostring(value, encoding="unicode")
                            if isinstance(value, etree._Element)
                            else str(value)
                            for value in result
                        ],
                    ),
                )

            elif rule.rule_type == XmlSchemaXPathRuleType.VALIDATE:
                if not isinstance(result, bool):
                    raise ValueError(
                        f"XPath validation rule '{rule.name}' must return a boolean."
                    )

                if not result:
                    validation_results.append(
                        ValidationResult(
                            severity=ValidationSeverity.ERROR,
                            code="XPATH_VALIDATION_ERROR",
                            message=f"XPath validation rule '{rule.name}' failed.",
                            rule_name=rule.name,
                        ),
                    )

        return ProcessingResult(
            extracted_values=extracted_values,
            validation_results=validation_results,
        )
