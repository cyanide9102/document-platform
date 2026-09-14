from dataclasses import dataclass

from document_platform.application.processing.models.validation_severity import (
    ValidationSeverity,
)


@dataclass(frozen=True)
class ValidationResult:
    severity: ValidationSeverity
    code: str
    message: str
    path: str | None = None
    line: int | None = None
    column: int | None = None
    rule_name: str | None = None
