"""Isometric projection and viewport fitting for FdF maps."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, radians, sin

from .model import Map, Point


@dataclass(slots=True)
class Camera:
    """Projection parameters that place a map in a two-dimensional viewport."""

    angle: float = 30.0
    z_scale: float = 1.0
    scale: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0

    def project(self, point: Point) -> tuple[float, float]:
        """Return the screen coordinates of a height-map point."""
        x, y = self._project_unscaled(point)
        return x * self.scale + self.offset_x, y * self.scale + self.offset_y

    def fit(self, height_map: Map, width: int, height: int) -> None:
        """Scale and centre *height_map* inside a viewport of ``width × height``."""
        if width <= 0 or height <= 0:
            raise ValueError("Viewport dimensions must be positive")

        projected = [self._project_unscaled(point) for point in height_map]
        min_x = min(x for x, _ in projected)
        max_x = max(x for x, _ in projected)
        min_y = min(y for _, y in projected)
        max_y = max(y for _, y in projected)

        map_width = max_x - min_x
        map_height = max_y - min_y
        candidates: list[float] = []
        if map_width > 0:
            candidates.append(width / map_width)
        if map_height > 0:
            candidates.append(height / map_height)
        self.scale = min(candidates) * 0.9 if candidates else 1.0

        self.offset_x = width / 2 - (min_x + max_x) / 2 * self.scale
        self.offset_y = height / 2 - (min_y + max_y) / 2 * self.scale

    def _project_unscaled(self, point: Point) -> tuple[float, float]:
        angle = radians(self.angle)
        x = (point.x - point.y) * cos(angle)
        y = (point.x + point.y) * sin(angle) - point.z * self.z_scale
        return x, y
