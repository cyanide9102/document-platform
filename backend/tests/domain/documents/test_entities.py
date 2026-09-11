from datetime import UTC

import pytest

from document_platform.domain.documents import Document, DocumentStatus

CONTENT_HASH = "a" * 64


def test_create_document():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
        content_hash=CONTENT_HASH,
    )

    assert document.id is not None
    assert document.name == "invoice.xml"
    assert document.original_name == "invoice.xml"
    assert document.content_type == "application/xml"
    assert document.size == 1024
    assert document.content_hash == CONTENT_HASH
    assert document.status == DocumentStatus.UPLOADED
    assert document.created_at.tzinfo == UTC
    assert document.updated_at.tzinfo == UTC
    assert document.created_at == document.updated_at


def test_create_document_strips_name():
    document = Document.create(
        name=" invoice.xml ",
        content_type="application/xml",
        size=1024,
        content_hash=CONTENT_HASH,
    )

    assert document.name == "invoice.xml"
    assert document.original_name == "invoice.xml"


def test_create_document_rejects_empty_name():
    with pytest.raises(ValueError, match="Document name cannot be empty."):
        Document.create(
            name="",
            content_type="application/xml",
            size=1024,
            content_hash=CONTENT_HASH,
        )


def test_create_document_rejects_whitespace_name():
    with pytest.raises(ValueError, match="Document name cannot be empty."):
        Document.create(
            name="  ",
            content_type="application/xml",
            size=1024,
            content_hash=CONTENT_HASH,
        )


def test_create_document_rejects_name_with_path():
    with pytest.raises(ValueError, match="Document name cannot contain a path."):
        Document.create(
            name="documents/invoice.xml",
            content_type="application/xml",
            size=1024,
            content_hash=CONTENT_HASH,
        )


def test_create_document_rejects_negative_size():
    with pytest.raises(ValueError, match="Document size cannot be negative."):
        Document.create(
            name="invoice.xml",
            content_type="application/xml",
            size=-1,
            content_hash=CONTENT_HASH,
        )


def test_create_document_rejects_invalid_content_hash_length():
    with pytest.raises(
        ValueError,
        match="Document content hash must be a SHA-256 hash.",
    ):
        Document.create(
            name="invoice.xml",
            content_type="application/xml",
            size=1024,
            content_hash="abc",
        )


def test_create_document_rejects_non_hex_content_hash():
    with pytest.raises(
        ValueError,
        match="Document content hash must be a hexadecimal string.",
    ):
        Document.create(
            name="invoice.xml",
            content_type="application/xml",
            size=1024,
            content_hash="g" * 64,
        )


def test_rename_document():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
        content_hash=CONTENT_HASH,
    )

    document.rename("March Invoice")

    assert document.name == "March Invoice"
    assert document.original_name == "invoice.xml"


def test_rename_document_rejects_empty_name():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
        content_hash=CONTENT_HASH,
    )

    with pytest.raises(ValueError, match="Document name cannot be empty."):
        document.rename("")


def test_start_processing():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
        content_hash=CONTENT_HASH,
    )

    document.start_processing()

    assert document.status == DocumentStatus.PROCESSING


def test_mark_processed():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
        content_hash=CONTENT_HASH,
    )

    document.start_processing()
    document.mark_processed()

    assert document.status == DocumentStatus.PROCESSED


def test_mark_failed():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
        content_hash=CONTENT_HASH,
    )

    document.start_processing()
    document.mark_failed()

    assert document.status == DocumentStatus.FAILED


def test_failed_document_can_be_reprocessed():
    document = Document.create(
        name="invoice.xml",
        content_type="application/xml",
        size=1024,
        content_hash=CONTENT_HASH,
    )

    document.start_processing()
    document.mark_failed()
    document.start_processing()

    assert document.status == DocumentStatus.PROCESSING
