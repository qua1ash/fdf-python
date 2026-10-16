"""Tkinter user interface for rendering an FdF height map."""

from __future__ import annotations

import tkinter as tk

from .model import Map, Point
from .projection import Camera


class App:
    """Display a wireframe map in a resizable window."""

    def __init__(self, height_map: Map, width: int = 1000, height: int = 700) -> None:
        self.height_map = height_map
        self.camera = Camera()
        self.root = tk.Tk()
        self.root.title("FdF")
        self.root.minsize(320, 240)
        self.canvas = tk.Canvas(self.root, bg="#111827", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.root.bind("<Escape>", self._close)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas.bind("<Configure>", self._on_resize)
        self.root.geometry(f"{width}x{height}")

    def run(self) -> None:
        """Start the graphical event loop."""
        self.root.mainloop()

    def close(self) -> None:
        """Close the application window."""
        self.root.destroy()

    def draw(self, width: int, height: int) -> None:
        """Fit the map and draw every horizontal and vertical edge once."""
        self.camera.fit(self.height_map, width, height)
        self.canvas.delete("all")
        for point in self.height_map:
            for neighbor in self._forward_neighbors(point):
                x1, y1 = self.camera.project(point)
                x2, y2 = self.camera.project(neighbor)
                self.canvas.create_line(x1, y1, x2, y2, fill="#60A5FA", width=2)

    def _forward_neighbors(self, point: Point) -> tuple[Point, ...]:
        """Return only right and lower neighbours so an edge is never duplicated."""
        result: list[Point] = []
        if point.x + 1 < self.height_map.width:
            result.append(self.height_map.point_at(point.x + 1, point.y))
        if point.y + 1 < self.height_map.height:
            result.append(self.height_map.point_at(point.x, point.y + 1))
        return tuple(result)

    def _on_resize(self, event: tk.Event[tk.Misc]) -> None:
        if event.width > 0 and event.height > 0:
            self.draw(event.width, event.height)

    def _close(self, _event: tk.Event[tk.Misc]) -> None:
        self.close()
