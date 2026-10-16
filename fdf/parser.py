"""Parsing and validation for .fdf height-map files."""

from __future__ import annotations

import re
from pathlib import Path

from .errors import MapFormatError
from .model import Map, Point

_COLOR_PATTERN = re.compile(r"0x[0-9a-fA-F]{1,6}\Z")


def parse_value(token: str, line: int = 1, column: int = 1) -> tuple[int, str | None]:
    """Parse one ``height[,0xRRGGBB]`` value from an FdF map."""
    parts = token.split(",")
    if len(parts) > 2:
        raise MapFormatError(line, column, token, "некорректное значение точки")

    try:
        height = int(parts[0])
    except ValueError as exc:
        raise MapFormatError(line, column, token, "не целое число") from exc

    if len(parts) == 1:
        return height, None

    color_text = parts[1]
    if not _COLOR_PATTERN.fullmatch(color_text):
        raise MapFormatError(line, column, token, "некорректный цвет")
    return height, f"#{int(color_text, 0):06X}"


def parse_map(path: str | Path) -> Map:
    """Read *path* and return its validated rectangular height map.

    ``OSError`` is intentionally allowed to reach the caller so the command-line
    layer can decide how to present file-system errors to the user.
    """
    source = Path(path)
    lines = source.read_text(encoding="utf-8").splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        raise MapFormatError(1, 1, "", "пустой файл")

    rows: list[list[Point]] = []
    expected_width: int | None = None
    for line_number, text in enumerate(lines, start=1):
        tokens = text.split()
        if not tokens:
            raise MapFormatError(line_number, 1, "", "пустая строка внутри карты")
        if expected_width is None:
            expected_width = len(tokens)
        elif len(tokens) != expected_width:
            raise MapFormatError(
                line_number,
                len(tokens) + 1,
                "",
                "строки имеют разную длину",
            )

        row: list[Point] = []
        for column_number, token in enumerate(tokens, start=1):
            height, color = parse_value(token, line_number, column_number)
            row.append(Point(column_number - 1, line_number - 1, height, color))
        rows.append(row)

    width = expected_width
    assert width is not None
    return Map(tuple(point for row in rows for point in row), width, len(rows))

