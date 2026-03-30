import random
import os
from maze_generator import MazeGenerator
from maze_config import MazeConfig
from renderer import Renderer
from constants import (
    NORTH, EAST, SOUTH, WEST,
    COLOR_BG, COLOR_FLOOR, COLOR_WALL, COLOR_PATH,
    COLOR_ENTRY, COLOR_EXIT, COLOR_42, TILE_SIZE,
    DIRECTIONS_BY_LETTER
)

try:
    import sys
    sys.path.insert(0, 'lib/mlx-2.2-py3-ubuntu-any')
    from mlx.mlx import Mlx
except ImportError:
    print("Error: MLX library not found.")
    Mlx = None


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
        MENU_HEIGHT = 40
        self.tile_size = TILE_SIZE
        self.win_width = self.gen.width * self.tile_size

        self.win_height = self.gen.height * self.tile_size + MENU_HEIGHT

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
            if letter not in DIRECTIONS_BY_LETTER:
                continue
            dx, dy = DIRECTIONS_BY_LETTER[letter]
            cx += dx
            cy += dy
            cells.add((cx, cy))

        return cells

    def _draw_menu(self):
        if hasattr(self.mlx, "mlx_string_put"):
            y_pos = self.win_height - 30
            self.mlx.mlx_string_put(
                self.mlx_ptr, self.win, 10, y_pos, 0xFFFFFF,
                "1:new maze  2:show path  3:random colour  ESC:exit"
            )

    def render(self) -> None:
        self._fill_rect(0, 0, self.win_width, self.win_height, COLOR_BG)

        for y in range(self.gen.height):
            for x in range(self.gen.width):
                self._draw_cell(x, y)

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win, self.img, 0, 0
        )
        self._draw_menu()

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
