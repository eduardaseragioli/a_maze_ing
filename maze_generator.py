import random
from maze_config import MazeConfig

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

PATTERN_42: list[tuple[int, int]] = [

    (0, 0), (1, 0),
    (0, 1), (0, 2),
    (0, 3), (1, 3),

    (3, 0), (4, 0), (5, 0),
    (3, 1), (5, 1),
    (4, 2), (5, 2),
    (3, 3), (4, 3), (5, 3),
]

class MazeGenerator:
    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.width = config.width
        self.height = config.height
        self.grid: list[self.width: int, self.height: int] = []
        self.blocked_cells = set()
        self.solution_path: list = []

        random.seed(config.seed)
        self._init_grid()

    def __init__grid(self):
        for y in range(0, self.height -1):
            for x in range(0, self.width - 1):
                self.grid[y][x] = 1111

    def place_42_pattern(self) -> bool:
        center_x = self.width / 2 - 3
        center_y = self.height / 2 - 3

        for (dx, dy) in pattern_42:
            x = center_x + dx
            y = center_y + dy
            if (x < 0 or x >= self.width or y < 0 or y >= self.height):
                print("Warning: Maze too small for 42 pattern!")
                return False
            self.grid[y][x] = 1111
            self.blocked_cells.add((x, y))
        return True

    def remove_wall(self, x, y, direction) -> None:
        self.grid[y][x] = self.grid[y][x] and (not direction)

        (dy, dx) = DIRECTIONS[direction]
        nx = x + dx
        ny = y + dy

        if (0)