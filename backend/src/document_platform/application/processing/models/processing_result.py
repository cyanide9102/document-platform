from dataclasses import dataclass

from document_platform.application.processing.models.extracted_value import (
    ExtractedValue,
)
from document_platform.application.processing.models.validation_result import (
    ValidationResult,
)


@dataclass(frozen=True)
class ProcessingResult:
    extracted_values: list[ExtractedValue]
    validation_results: list[ValidationResult]
