from pathlib import PurePath


def validate_filename(name: str) -> str:
    normalized_name = name.strip()
    if not normalized_name:
        raise ValueError("Filename cannot be empty.")

    if PurePath(normalized_name).name != normalized_name:
        raise ValueError("Filename cannot contain a path.")

    return normalized_name
