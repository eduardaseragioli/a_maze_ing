import random
import os
from maze_generator import MazeGenerator
from maze_config import MazeConfig
from renderer import Renderer


try:
    import sys
    sys.path.insert(0, 'lib/mlx-2.2-py3-ubuntu-any')
    from mlx.mlx import Mlx
except ImportError:
    print("Error: MLX library not found.")

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

DIRECTIONS = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
}

# Colors
COLOR_BG = 0x0B1020
COLOR_FLOOR = 0x151B2D
COLOR_WALL = 0x7C3AED
COLOR_PATH = 0xFACC15
COLOR_ENTRY = 0x22C55E
COLOR_EXIT = 0xEF4444
COLOR_42 = 0x2563EB

TILE_SIZE = 20


class MazeVisualizer(Renderer):

    def __init__(self, generator: MazeGenerator) -> None:

        if Mlx is None:
            raise ImportError("MLX library not available")

        self.gen = generator
        self.show_path = False
        self.wall_color = COLOR_WALL
        self.path_cells = self._build_path_cells()

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        self.tile_size = TILE_SIZE
        self.win_width = self.gen.width * self.tile_size
        self.win_height = self.gen.height * self.tile_size

        self.win = self.mlx.mlx_new_window(
            self.mlx_ptr, self.win_width, self.win_height, "A-Maze-ing"
        )

        self.img = self.mlx.mlx_new_image(
            self.mlx_ptr, self.win_width, self.win_height
        )

        addr_info = self.mlx.mlx_get_data_addr(self.img)
        self.img_data = addr_info[0]
        self.bpp = addr_info[1]
        self.line_size = addr_info[2]

    def _build_path_cells(self) -> set[tuple[int, int]]:
        cells: set[tuple[int, int]] = set()
        cx, cy = self.gen.config.entry

        for letter in self.gen.solution_path:
            if letter not in DIRECTIONS:
                continue
            dx, dy = DIRECTIONS[letter]
            cx += dx
            cy += dy
            cells.add((cx, cy))

        return cells

    def render(self) -> None:
        self._fill_rect(0, 0, self.win_width, self.win_height, COLOR_BG)

        for y in range(self.gen.height):
            for x in range(self.gen.width):
                self._draw_cell(x, y)

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win, self.img, 0, 0
        )

    def _draw_cell(self, x: int, y: int) -> None:

        cell_val = self.gen.grid[y][x]

        if (x, y) in self.gen.blocked_cells:
            interior_color = COLOR_42
        elif (x, y) == self.gen.config.entry:
            interior_color = COLOR_ENTRY
        elif (x, y) == self.gen.config.exit_coord:
            interior_color = COLOR_EXIT
        elif self.show_path and (x, y) in self.path_cells:
            interior_color = COLOR_PATH
        else:
            interior_color = COLOR_FLOOR

        interior_margin = 2
        self._fill_rect(
            x * self.tile_size + interior_margin,
            y * self.tile_size + interior_margin,
            self.tile_size - interior_margin * 2,
            self.tile_size - interior_margin * 2,
            interior_color,
        )

        wall_thickness = 1

        if cell_val & NORTH:
            self._fill_rect(
                x * self.tile_size,
                y * self.tile_size,
                self.tile_size,
                wall_thickness,
                self.wall_color,
            )

        if cell_val & SOUTH:
            self._fill_rect(
                x * self.tile_size,
                y * self.tile_size + self.tile_size - wall_thickness,
                self.tile_size,
                wall_thickness,
                self.wall_color,
            )

        if cell_val & WEST:
            self._fill_rect(
                x * self.tile_size,
                y * self.tile_size,
                wall_thickness,
                self.tile_size,
                self.wall_color,
            )

        if cell_val & EAST:
            self._fill_rect(
                x * self.tile_size + self.tile_size - wall_thickness,
                y * self.tile_size,
                wall_thickness,
                self.tile_size,
                self.wall_color,
            )

    def _on_key(self, keycode: int, param) -> int:
        if keycode == 65307:
            os._exit(0)
        elif keycode == 49:
            self._regenerate()
        elif keycode == 50:
            self.show_path = not self.show_path
            self.render()
        elif keycode == 51:
            self.wall_color = self._random_color()
            self.render()

        return 0

    def _on_close(self, param) -> int:
        os._exit(0)

    def _regenerate(self) -> None:
        old_config = self.gen.config
        new_config = MazeConfig(
            width=old_config.width,
            height=old_config.height,
            entry=old_config.entry,
            exit_coord=old_config.exit_coord,
            output_file=old_config.output_file,
            perfect=old_config.perfect,
            seed=random.randint(0, 2**32),
        )

        new_gen = MazeGenerator(new_config)
        new_gen.generate()
        new_gen.write_output()

        self.gen = new_gen
        self.path_cells = self._build_path_cells()
        self.show_path = False

        self.render()

    def run(self) -> None:
        self.render()

        self.mlx.mlx_key_hook(self.win, self._on_key, None)
        self.mlx.mlx_hook(self.win, 17, 0, self._on_close, None)

        self.mlx.mlx_loop(self.mlx_ptr)
