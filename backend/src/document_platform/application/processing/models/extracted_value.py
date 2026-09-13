from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractedValue:
    name: str
    values: list[str]
