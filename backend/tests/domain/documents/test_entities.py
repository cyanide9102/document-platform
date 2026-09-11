from datetime import UTC

import pytest

from document_platform.domain.documents.entities import Document
from document_platform.domain.documents.enums import DocumentStatus


def test_create_document():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
    )

    assert document.id is not None
    assert document.name == "invoice.xml"
    assert document.storage_key is None
    assert document.content_type == "application/xml"
    assert document.size == 1024
    assert document.status == DocumentStatus.DRAFT
    assert document.created_at.tzinfo == UTC
    assert document.updated_at.tzinfo == UTC
    assert document.created_at == document.updated_at


def test_create_document_strips_name():
    document = Document.create(
        name=" invoice.xml ",
        content_type="application/xml",
        size=1024,
    )

    assert document.name == "invoice.xml"


def test_create_document_rejects_empty_name():
    with pytest.raises(ValueError, match="Document name cannot be empty."):
        Document.create(
            name="",
            content_type="application/xml",
            size=1024,
        )


def test_create_document_rejects_whitespace_name():
    with pytest.raises(ValueError, match="Document name cannot be empty."):
        Document.create(
            name="  ",
            content_type="application/xml",
            size=1024,
        )


def test_create_document_rejects_negative_size():
    with pytest.raises(ValueError, match="Document size cannot be negative."):
        Document.create(
            name="invoice.xml",
            content_type="application/xml",
            size=-1,
        )


def test_attach_storage():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
    )

    document.attach_storage("documents/123/invoice.xml")

    assert document.storage_key == "documents/123/invoice.xml"


def test_attach_storage_rejects_empty_storage_key():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
    )

    with pytest.raises(ValueError, match="Storage key cannot be empty."):
        document.attach_storage("")


def test_attach_storage_rejects_second_storage_key():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
    )

    document.attach_storage("documents/123/invoice.xml")

    with pytest.raises(ValueError, match="Document already has a storage key."):
        document.attach_storage("documents/123/other.xml")


def test_mark_uploaded():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
    )

    document.attach_storage("documents/123/invoice.xml")
    document.mark_uploaded()

    assert document.storage_key == "documents/123/invoice.xml"
    assert document.status == DocumentStatus.UPLOADED


def test_mark_uploaded_requires_storage():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
    )

    with pytest.raises(
        ValueError,
        match="Cannot mark document as uploaded without storage.",
    ):
        document.mark_uploaded()
