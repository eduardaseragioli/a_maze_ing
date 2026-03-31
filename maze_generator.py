import random
from collections import deque
from maze_config import MazeConfig
from constants import (
    EAST, SOUTH,
    OPPOSITE, DIRECTIONS, DIR_LETTER, PATTERN_42
)


class MazeGenerator:
    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.width = config.width
        self.height = config.height
        self.grid: list[list[int]] = []
        self.blocked_cells: set = set()
        self.solution_path: list = []
        self.visited: set[tuple[int, int]] = set()

        random.seed(config.seed)
        self._init_grid()

    def _init_grid(self) -> None:
        for _ in range(self.height):
            row: list = []
            for _ in range(self.width):
                row.append(0b1111)
            self.grid.append(row)

    def _place_42_pattern(self) -> bool:
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

        if direction not in DIRECTIONS:
            return

        if (x, y) in self.blocked_cells:
            return

        self.grid[y][x] = self.grid[y][x] & ~direction

        (dx, dy) = DIRECTIONS[direction]
        nx = x + dx
        ny = y + dy

        if (0 <= nx < self.width and 0 <= ny < self.height):
            if not (nx, ny) in self.blocked_cells:
                opposite = OPPOSITE[direction]
                self.grid[ny][nx] = self.grid[ny][nx] & ~opposite

    def generate(self) -> None:

        self._place_42_pattern()

        visited: set = set()
        stack: list = [self.config.entry]

        visited.add(self.config.entry)

        while stack:
            cx, cy = stack[-1]
            random_directions: list = list(DIRECTIONS.keys())
            random.shuffle(random_directions)

            find = False

            for direction in random_directions:
                (dx, dy) = DIRECTIONS[direction]
                nx = cx + dx
                ny = cy + dy

                if ((nx, ny) not in visited and
                        (nx, ny) not in self.blocked_cells
                        and 0 <= nx < self.width and 0 <= ny < self.height):

                    if self._is_valid_open(cx, cy, nx, ny, visited):
                        self.remove_wall(cx, cy, direction)
                        visited.add((nx, ny))
                        stack.append((nx, ny))
                        find = True
                        break

            if not find:
                stack.pop()

        self.visited = visited
        if not self.config.perfect:
            self._open_extra_walls()

    def _is_valid_open(self, cx, cy, nx, ny, visited) -> bool:

        open_neighbors = 0

        for direction, (dx, dy) in DIRECTIONS.items():
            around_nx = nx + dx
            around_ny = ny + dy

            if 0 <= around_nx < self.width and 0 <= around_ny < self.height:
                if ((around_nx, around_ny) in visited
                        and (around_nx, around_ny) != (cx, cy)):
                    open_neighbors += 1

        return open_neighbors < 2

    def _open_extra_walls(self) -> None:

        walls_to_open = (self.width * self.height) // 10

        candidates: list = []

        for cy in range(self.height - 1):
            for cx in range(self.width - 1):
                if (cx, cy) in self.blocked_cells:
                    continue

                for direction in [EAST, SOUTH]:
                    (dx, dy) = DIRECTIONS[direction]
                    nx = cx + dx
                    ny = cy + dy

                    if nx >= self.width or ny >= self.height:
                        continue
                    if (nx, ny) in self.blocked_cells:
                        continue

                    if self.grid[cy][cx] & direction:
                        candidates.append((cx, cy, direction))

        random.shuffle(candidates)

        opened = 0
        for (cx, cy, direction) in candidates:

            if opened >= walls_to_open:
                break

            (dx, dy) = DIRECTIONS[direction]
            nx = cx + dx
            ny = cy + dy

            if self._is_valid_open(cx, cy, nx, ny, self.visited):
                self.remove_wall(cx, cy, direction)
                opened += 1

    def _bfs_shortest_path(self) -> list[str]:

        queue = deque([(self.config.entry, [])])
        visited = {self.config.entry}

        while queue:
            (cx, cy), path = queue.popleft()

            if (cx, cy) == self.config.exit_coord:
                return path

            for direction, (dx, dy) in DIRECTIONS.items():
                nx = cx + dx
                ny = cy + dy

                if nx < 0 or nx >= self.width:
                    continue
                if ny < 0 or ny >= self.height:
                    continue
                if (nx, ny) in visited:
                    continue

                if self.grid[cy][cx] & direction:
                    continue

                visited.add((nx, ny))
                queue.append(((nx, ny), path + [DIR_LETTER[direction]]))

        return []

    def write_output(self) -> None:

        self.solution_path = self._bfs_shortest_path()
        path_str = "".join(self.solution_path)

        with open(self.config.output_file, 'w') as file:

            for y in range(self.height):
                for x in range(self.width):
                    file.write(hex(self.grid[y][x])[2:].upper())
                file.write("\n")
            file.write("\n")

            file.write(f"{self.config.entry[0]},{self.config.entry[1]}\n")
            file.write(
                f"{self.config.exit_coord[0]},{self.config.exit_coord[1]}\n")
            file.write(f"{path_str}\n")

    def display(self) -> None:

        from maze_visualizer import MazeVisualizer
        visualizer = MazeVisualizer(self)
        visualizer.run()
