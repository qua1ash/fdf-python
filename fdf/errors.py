"""Exceptions used by the FdF application."""


class FdfError(Exception):
    """Base exception for expected FdF errors."""


class MapFormatError(FdfError):
    """Raised when a height-map file does not follow the FdF format."""

    def __init__(self, line: int, column: int, token: str, reason: str) -> None:
        self.line = line
        self.column = column
        self.token = token
        self.reason = reason
        super().__init__(f"строка {line}, колонка {column}: {token!r} — {reason}")

