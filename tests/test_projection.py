from pytest import approx

from fdf.model import Map, Point
from fdf.projection import Camera


def test_origin_projects_to_origin() -> None:
    assert Camera().project(Point(0, 0, 0)) == (0.0, 0.0)


def test_positive_height_moves_point_up() -> None:
    _, y = Camera().project(Point(0, 0, 1))
    assert y < 0


def test_flat_map_is_symmetric_about_vertical_axis() -> None:
    camera = Camera()
    left, _ = camera.project(Point(0, 1, 0))
    right, _ = camera.project(Point(1, 0, 0))

    assert left == approx(-right)


def test_fit_keeps_every_point_inside_viewport() -> None:
    points = tuple(
        Point(x, y, z)
        for y, row in enumerate(((0, 0, 0), (0, 5, 0), (0, 0, 0)))
        for x, z in enumerate(row)
    )
    height_map = Map(points, width=3, height=3)
    camera = Camera()
    camera.fit(height_map, width=800, height=600)

    for point in height_map:
        x, y = camera.project(point)
        assert 0 <= x <= 800
        assert 0 <= y <= 600


def test_fit_centres_a_single_point() -> None:
    height_map = Map((Point(0, 0, 0),), width=1, height=1)
    camera = Camera()
    camera.fit(height_map, width=800, height=600)

    assert camera.project(height_map.point_at(0, 0)) == (400.0, 300.0)
