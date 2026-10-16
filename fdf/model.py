"""Data model for a rectangular grid of height-map points."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point:
    """One point of the height map."""

    x: int
    y: int
    z: int
    color: str | None = None


@dataclass(frozen=True, slots=True)
class Map:
    """A rectangular collection of points addressed by their map coordinates."""

    points: tuple[Point, ...]
    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Map dimensions must be positive")
        if len(self.points) != self.width * self.height:
            raise ValueError("Point count does not match map dimensions")

    def __len__(self) -> int:
        """Return the total number of points."""
        return len(self.points)

    def __iter__(self) -> Iterator[Point]:
        """Iterate over points in row-major order."""
        return iter(self.points)

    def point_at(self, x: int, y: int) -> Point:
        """Return a point by its map coordinates."""
        if not 0 <= x < self.width or not 0 <= y < self.height:
            raise IndexError("Point coordinates are outside the map")
        return self.points[y * self.width + x]

    def neighbors(self, point: Point) -> tuple[Point, ...]:
        """Return orthogonal neighbours of *point* that belong to this map."""
        if self.point_at(point.x, point.y) != point:
            raise ValueError("Point does not belong to this map")

        result: list[Point] = []
        for x, y in (
            (point.x - 1, point.y),
            (point.x + 1, point.y),
            (point.x, point.y - 1),
            (point.x, point.y + 1),
        ):
            if 0 <= x < self.width and 0 <= y < self.height:
                result.append(self.point_at(x, y))
        return tuple(result)

