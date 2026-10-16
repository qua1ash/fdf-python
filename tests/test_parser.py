from pathlib import Path

import pytest

from fdf.errors import MapFormatError
from fdf.parser import parse_map, parse_value

ROOT = Path(__file__).resolve().parents[1]


def test_parse_elem_map() -> None:
    height_map = parse_map(ROOT / "maps" / "elem.fdf")

    assert (height_map.width, height_map.height) == (5, 5)
    assert height_map.point_at(2, 2).z == 5
    assert height_map.point_at(3, 1).x == 3
    assert height_map.point_at(3, 1).y == 1


@pytest.mark.parametrize(
    ("token", "expected"),
    [
        ("7", (7, None)),
        ("-3", (-3, None)),
        ("2,0xFF8800", (2, "#FF8800")),
        ("1,0xff", (1, "#0000FF")),
    ],
)
def test_parse_value(token: str, expected: tuple[int, str | None]) -> None:
    assert parse_value(token) == expected


@pytest.mark.parametrize("name", ["empty", "not_integer", "ragged", "color"])
def test_bad_maps_raise_format_error(name: str) -> None:
    with pytest.raises(MapFormatError):
        parse_map(ROOT / "maps" / "bad" / f"{name}.fdf")


def test_short_color_is_normalized() -> None:
    height_map = parse_map(ROOT / "maps" / "peak.fdf")
    assert height_map.point_at(1, 0).color == "#0000FF"
    assert height_map.point_at(1, 1).color == "#FF0000"

