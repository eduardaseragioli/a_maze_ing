"""Global constants for maze generation and visualization."""

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000


OPPOSITE: dict[int, int] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
}

DIRECTIONS: dict[int, tuple[int, int]] = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0)
}

DIRECTIONS_BY_LETTER: dict[str, tuple[int, int]] = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
}

DIR_LETTER = {
    NORTH: "N",
    EAST:  "E",
    SOUTH: "S",
    WEST:  "W"
}

PATTERN_42: list[tuple[int, int]] = [
    (0, 0), (0, 1), (0, 2),
    (1, 2),
    (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
    (4, 0), (5, 0), (6, 0),
    (6, 1), (6, 2),
    (5, 2), (4, 2),
    (4, 3), (4, 4), (5, 4), (6, 4),
]

COLOR_BG = 0x0B1020
COLOR_FLOOR = 0x151B2D
COLOR_WALL = 0x7C3AED
COLOR_PATH = 0xFACC15
COLOR_ENTRY = 0x22C55E
COLOR_EXIT = 0xEF4444
COLOR_42 = 0x2563EB

TILE_SIZE = 20
