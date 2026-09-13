from dataclasses import dataclass

from document_platform.application.processing.models.extracted_value import (
    ExtractedValue,
)


@dataclass(frozen=True)
class ProcessingResult:
    extracted_values: list[ExtractedValue]
