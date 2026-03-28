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
        self.grid: list[list[int]] = []
        self.blocked_cells = set()
        self.solution_path: list = []

        random.seed(config.seed)
        self._init_grid()

    def _init_grid(self) -> None:
        for _ in range(self.height):
            row: list = []
            for _ in range(self.width):
                row.append(0b1111)
            self.grid.append(row)

    def place_42_pattern(self) -> bool:
        center_x = self.width // 2 - 3
        center_y = self.height // 2 - 3

        for (dx, dy) in PATTERN_42:
            x = center_x + dx
            y = center_y + dy
            if (x < 0 or x >= self.width or y < 0 or y >= self.height):
                print("Warning: Maze too small for 42 pattern!")
                return False
            self.grid[y][x] = 0b1111
            self.blocked_cells.add((x, y))
        return True

    def remove_wall(self, x, y, direction) -> None:

        if (x < 0 or x >= self.width or y < 0 or y >= self.height):
            return
        
        if not direction in DIRECTIONS:
            return
        
        if (x, y) in self.blocked_cells:
            return 

        self.grid[y][x] = self.grid[y][x] and (not direction)

        (dx, dy) = DIRECTIONS[direction]
        nx = x + dx
        ny = y + dy

        if (0 <= nx < self.width and 0 <= ny < self.height):
            if not (nx, ny) in self.blocked_cells:
                opposite = OPPOSITE[direction]
                self.grid[ny][nx] = self.grid[ny][nx] and (not opposite)

        def generate(self) -> None:
            
