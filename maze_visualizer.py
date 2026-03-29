from maze_generator import MazeGenerator
from maze_config import MazeConfig
import ctypes

try:
    import sys
    sys.path.insert(0, 'lib/mlx-2.2-py3-ubuntu-any')
    from mlx.mlx import Mlx
except ImportError:
    print("Error: MLX library not found.")

CELL_SIZE = 20
WALL_THICK = 2
MENU_HEIGHT = 20

COLOUR_BKG = 0x330033  
COLOUR_WALL_PRESETS = [0xFFFFFF, 0xFF6B9D, 0xC44569, 0xF8B739, 0x00D9FF]
COLOUR_PATH = 0x00FF00  
COLOUR_ENTRY = 0x0000FF  
COLOUR_EXIT = 0xFF0000  
COLOUR_42 = 0xFFFF00  
COLOUR_TEXT = 0xFFFFFF  

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

DIR_MAP = {
    'N': (0, -1),
    'E': (1,  0),
    'S': (0,  1),
    'W': (-1, 0),
}


class MazeVisualizer:
    
    def __init__(self, generator: MazeGenerator):
        self.generator = generator
        self.show_path = False
        self.colour_index = 0
        self.wall_colour = 0xFFFFFF
        self.window_width = (generator.width * CELL_SIZE + WALL_THICK)
        self.window_height = (generator.height * CELL_SIZE + WALL_THICK + MENU_HEIGHT)
        
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.window_width, self.window_height, "A_Maze_ing")
        self.img_ptr = self.mlx.mlx_new_image(
            self.mlx_ptr, self.window_width, self.window_height)
        
        self.mlx.mlx_func.mlx_get_data_addr.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint),
            ctypes.POINTER(ctypes.c_uint),
            ctypes.POINTER(ctypes.c_uint)
        ]
        self.mlx.mlx_func.mlx_get_data_addr.restype = ctypes.POINTER(
            ctypes.c_char)

        bpp = ctypes.c_uint()
        line_size = ctypes.c_uint()
        endian = ctypes.c_uint()
        data_ptr = self.mlx.mlx_func.mlx_get_data_addr(
            self.img_ptr, ctypes.byref(bpp), ctypes.byref(line_size),
            ctypes.byref(endian))

        self.bpp = bpp.value
        self.line_size = line_size.value
        self.endian = endian.value

        total_bytes = self.line_size * self.window_height
        self.buffer = (ctypes.c_char * total_bytes).from_address(
            ctypes.addressof(data_ptr.contents))
        
        self.path_cells: set[tuple[int, int]] = self._build_path_cells()
        
    def run(self):
        self._draw_all()
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self._on_loop, None)
        self.mlx.mlx_key_hook(self.win_ptr, self._on_key, None)
        self.mlx.mlx_hook(self.win_ptr, 17, 0, self._on_close, None)
        self.mlx.mlx_loop(self.mlx_ptr)

    def _on_loop(self, param) -> int:
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)
        return 0

    def _on_key(self, keycode, param):
        KEY_1 = 49
        KEY_2 = 50
        KEY_3 = 51
        KEY_4 = 52
        KEY_ESC = 65307
        KEY_Q = 113
        
        if keycode == KEY_1:
            self._regenerate()
            
        elif keycode == KEY_2:
            self.colour_index = (self.colour_index + 1) % len(COLOUR_WALL_PRESETS)
            self.wall_colour = COLOUR_WALL_PRESETS[self.colour_index]
            self._draw_all()
            
        elif keycode == KEY_3:
            self.show_path = not self.show_path
            self._draw_all()

        elif keycode in (KEY_4, KEY_ESC, KEY_Q):
            self.mlx.mlx_loop_exit(self.mlx_ptr)

        return 0

    def _on_close(self, param):
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0
        
    def _build_path_cells(self) -> set[tuple[int,int]]:
        cells: set[tuple[int, int]] = set()
        
        cx, cy = self.generator.config.entry
        for letter in self.generator.solution_path:
            dx, dy = DIR_MAP[letter]
            cx += dx
            cy += dy
            cells.add((cx, cy))
        return cells
    
    def _draw_all(self) -> None:
        self._fill_rect(
            0, 0, self.window_width, self.window_height, COLOUR_BKG)

        for y in range(self.generator.height):
            for x in range(self.generator.width):
                self._draw_cell(x, y)

        self._draw_menu()

    def _draw_cell(self, x, y):
        wx = x * CELL_SIZE
        wy = y * CELL_SIZE + MENU_HEIGHT
        
        px = wx + WALL_THICK
        py = wy + WALL_THICK
        inner = CELL_SIZE - WALL_THICK * 2
        
        if (x, y) in self.generator.blocked_cells:
            colour = COLOUR_42
        elif (x, y) == self.generator.config.entry:
            colour = COLOUR_ENTRY
        elif (x, y) == self.generator.config.exit_coord:
            colour = COLOUR_EXIT
        elif self.show_path and (x, y) in self.path_cells:
            colour = COLOUR_PATH
        else:
            colour = COLOUR_BKG
        
        self._fill_rect(px, py, inner, inner, colour)

        cell_value = self.generator.grid[y][x]
        
        if cell_value & NORTH:
            self._fill_rect(
                wx, wy, CELL_SIZE, WALL_THICK, self.wall_colour)
        
        if cell_value & SOUTH:
            self._fill_rect(
                wx, wy + CELL_SIZE - WALL_THICK, CELL_SIZE,
                WALL_THICK, self.wall_colour)

        if cell_value & WEST:
            self._fill_rect(
                wx, wy, WALL_THICK, CELL_SIZE, self.wall_colour)

        if cell_value & EAST:
            self._fill_rect(
                wx + CELL_SIZE - WALL_THICK, wy, WALL_THICK,
                CELL_SIZE, self.wall_colour)

    def _put_pixel(self, x, y, colour) -> None:
        if x < 0 or x >= self.window_width:
            return
        if y < 0 or y >= self.window_height:
            return
        bytes_per_pixel = self.bpp // 8
        offset = y * self.line_size + x * bytes_per_pixel

        r = (colour >> 16) & 0xFF
        g = (colour >> 8) & 0xFF
        b = colour & 0xFF

        self.buffer[offset] = bytes([b])[0:1]
        self.buffer[offset + 1] = bytes([g])[0:1]
        self.buffer[offset + 2] = bytes([r])[0:1]
            
    def _fill_rect(self, px, py, width, height, colour) -> None:
        """Desenha um retângulo preenchido de forma otimizada"""
        bytes_per_pixel = self.bpp // 8
        r = (colour >> 16) & 0xFF
        g = (colour >> 8) & 0xFF
        b = colour & 0xFF

        b_byte = bytes([b])[0:1]
        g_byte = bytes([g])[0:1]
        r_byte = bytes([r])[0:1]

        for y in range(py, py + height):
            if y < 0 or y >= self.window_height:
                continue
            for x in range(px, px + width):
                if x < 0 or x >= self.window_width:
                    continue
                offset = y * self.line_size + x * bytes_per_pixel
                if offset + 2 < len(self.buffer):
                    self.buffer[offset] = b_byte
                    self.buffer[offset + 1] = g_byte
                    self.buffer[offset + 2] = r_byte

                
    def _draw_menu(self) -> None:
        self.mlx.mlx_string_put(
            self.mlx_ptr, self.win_ptr,
            4, 4,
            COLOUR_TEXT,
            "1:Regen | 2:Colour | 3:Path | ESC:Quit"
        )
        
    def _regenerate(self) -> None:
        import random
        old = self.generator.config
        new_config = MazeConfig(
            width = old.width,
            height = old.height,
            entry = old.entry,
            exit_coord = old.exit_coord,
            output_file = old.output_file,
            perfect = old.perfect,
            seed = random.randint(0, 2**32)
        )
        new_gen = MazeGenerator(new_config)
        new_gen.generate()
        new_gen.write_output()
        self.generator  = new_gen
        self.path_cells = self._build_path_cells()
        self._draw_all()