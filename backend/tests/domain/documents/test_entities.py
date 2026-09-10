from datetime import UTC

import pytest

from document_platform.domain.documents.entities import Document
from document_platform.domain.documents.enums import DocumentStatus


def test_create_document() -> None:
    document = Document.create("invoice.xml")

    assert document.id is not None
    assert document.name == "invoice.xml"
    assert document.status == DocumentStatus.DRAFT
    assert document.created_at.tzinfo == UTC
    assert document.updated_at.tzinfo == UTC
    assert document.created_at == document.updated_at


def test_create_document_strips_name() -> None:
    document = Document.create(" invoice.xml ")

    assert document.name == "invoice.xml"


def test_create_document_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="Document name cannot be empty."):
        Document.create("")


def test_create_document_rejects_whitespace_name() -> None:
    with pytest.raises(ValueError, match="Document name cannot be empty."):
        Document.create("  ")
