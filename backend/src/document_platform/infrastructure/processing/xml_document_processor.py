from typing import BinaryIO

from lxml import etree

from document_platform.application.processing.ports import DocumentProcessor


class XmlDocumentProcessor(DocumentProcessor):
    async def process(self, document: BinaryIO, schema: BinaryIO):
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
