from typing import BinaryIO

from lxml import etree

from document_platform.application.processing.models import (
    ExtractedValue,
    ProcessingConfiguration,
    ProcessingResult,
)
from document_platform.application.processing.ports import DocumentProcessor


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
            xml_schema.assertValid(xml_document)
        except etree.XMLSchemaParseError as exception:
            raise ValueError("Invalid XML schema.") from exception
        except etree.DocumentInvalid as exception:
            raise ValueError(
                "Document does not conform to the XML schema.",
            ) from exception

        extracted_values = []
        for rule in configuration.xpath_rules:
            values = xml_document.xpath(rule.expression, namespaces=rule.namespaces)

            extracted_values.append(
                ExtractedValue(
                    name=rule.name,
                    values=[
                        etree.tostring(value, encoding="unicode")
                        if isinstance(value, etree._Element)
                        else str(value)
                        for value in values
                    ],
                ),
            )

        return ProcessingResult(extracted_values)
