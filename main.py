"""Command-line entry point for the FdF application."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from fdf.app import App
from fdf.errors import FdfError
from fdf.parser import parse_map


def main(argv: Sequence[str] | None = None) -> int:
    """Validate the requested height-map file.

    The graphical window is added in the rendering feature. Keeping argument and
    file-error handling here lets every branch provide the final CLI contract.
    """
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) != 1:
        print("Использование: python main.py <файл.fdf>", file=sys.stderr)
        return 2

    try:
        height_map = parse_map(arguments[0])
    except (FdfError, OSError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    App(height_map).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
