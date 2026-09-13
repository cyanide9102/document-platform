from datetime import UTC

import pytest

from document_platform.domain.schemas import XmlSchema

VALID_HASH = "a" * 64


def test_create_schema():
    schema = XmlSchema.create(
        name="Invoice",
        size=1024,
        content_hash=VALID_HASH,
    )

    assert schema.id is not None
    assert schema.name == "Invoice"
    assert schema.size == 1024
    assert schema.content_hash == VALID_HASH
    assert schema.created_at.tzinfo == UTC


def test_create_schema_trims_name():
    schema = XmlSchema.create(
        name="  Invoice  ",
        size=1024,
        content_hash=VALID_HASH,
    )

    assert schema.name == "Invoice"


def test_create_schema_rejects_empty_name():
    with pytest.raises(
        ValueError,
        match="Schema name cannot be empty.",
    ):
        XmlSchema.create(
            name="   ",
            size=1024,
            content_hash=VALID_HASH,
        )


@pytest.mark.parametrize(
    "name",
    [
        "schemas/invoice.xsd",
        r"schemas\invoice.xsd",
    ],
)
def test_create_schema_rejects_path_in_name(name):
    with pytest.raises(
        ValueError,
        match="Schema name cannot contain a path.",
    ):
        XmlSchema.create(
            name=name,
            size=1024,
            content_hash=VALID_HASH,
        )


def test_create_schema_rejects_negative_size():
    with pytest.raises(
        ValueError,
        match="Schema size cannot be negative.",
    ):
        XmlSchema.create(
            name="Invoice",
            size=-1,
            content_hash=VALID_HASH,
        )


@pytest.mark.parametrize(
    "content_hash",
    [
        "",
        "a" * 63,
        "a" * 65,
    ],
)
def test_create_schema_rejects_invalid_hash_length(content_hash):
    with pytest.raises(
        ValueError,
        match="Schema content hash must be a SHA-256 hash.",
    ):
        XmlSchema.create(
            name="Invoice",
            size=1024,
            content_hash=content_hash,
        )


def test_create_schema_rejects_non_hex_hash():
    invalid_hash = "g" * 64

    with pytest.raises(
        ValueError,
        match="Schema content hash must be a hexadecimal string.",
    ):
        XmlSchema.create(
            name="Invoice",
            size=1024,
            content_hash=invalid_hash,
        )


def test_create_schema_accepts_uppercase_hex_hash():
    content_hash = "A" * 64

    schema = XmlSchema.create(
        name="Invoice",
        size=1024,
        content_hash=content_hash,
    )

    assert schema.content_hash == content_hash


def test_create_schema_accepts_zero_size():
    schema = XmlSchema.create(
        name="Empty",
        size=0,
        content_hash=VALID_HASH,
    )

    assert schema.size == 0
