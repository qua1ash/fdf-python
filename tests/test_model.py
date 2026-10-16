from fdf.model import Map, Point


def test_map_supports_length_and_iteration() -> None:
    points = tuple(Point(x, y, 0) for y in range(2) for x in range(2))
    height_map = Map(points, width=2, height=2)

    assert len(height_map) == 4
    assert list(height_map) == list(points)


def test_corner_has_two_neighbors() -> None:
    points = tuple(Point(x, y, 0) for y in range(2) for x in range(2))
    height_map = Map(points, width=2, height=2)

    assert height_map.neighbors(height_map.point_at(0, 0)) == (
        height_map.point_at(1, 0),
        height_map.point_at(0, 1),
    )
