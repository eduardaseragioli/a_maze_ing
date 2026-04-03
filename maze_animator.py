
from constants import COLOR_PATH, COLOR_BG
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maze_visualizer import MazeVisualizer



class MazeAnimator:
    """Handles path animation for the maze visualizer."""

    def __init__(self, visualizer: "MazeVisualizer") -> None:
        self.vis: "MazeVisualizer" = visualizer
        self.path_anim_index: int = 0
        self.path_animating: bool = False
        self.path_anim_frame: int = 0
        self.path_anim_speed: int = 3
        self.blink_state: bool = True
        self.blink_counter: int = 0
        self.blink_interval: int = 20

    def start(self) -> None:
        """Start the path animation from the beginning."""
        self.path_anim_index = 0
        self.path_anim_frame = 0
        self.path_animating = True

    def stop(self) -> None:
        """Stop and reset the animation."""
        self.path_animating = False
        self.path_anim_index = 0
        self.path_anim_frame = 0


    def step(self, param: object) -> int:
        """Advance animation by one step. Called every MLX loop tick."""
        # Atualiza o estado do piscar
        self.blink_counter += 1
        if self.blink_counter >= self.blink_interval:
            self.blink_counter = 0
            self.blink_state = not self.blink_state

        if not self.path_animating:
            # Mesmo parado, renderiza o piscar
            self._render_partial()
            return 0
        if self.path_anim_index >= len(self.vis.path_cells) - 1:
            self.path_animating = False
            self.vis.show_path = True
            return 0

        self.path_anim_frame += 1
        if self.path_anim_frame >= self.path_anim_speed:
            self.path_anim_frame = 0
            self.path_anim_index += 1
            self._render_partial()


        return 0


    def _render_partial(self) -> None:
        """Render maze with path drawn up to current animation index."""
        vis: "MazeVisualizer" = self.vis
        vis._fill_rect(0, 0, vis.win_width, vis.win_height, COLOR_BG)

        for y in range(vis.gen.height):
            for x in range(vis.gen.width):
                vis._draw_cell(x, y)

        # Piscar a entrada, saída e 42
        if self.blink_state:
            entry_x, entry_y = vis.gen.config.entry
            margin = 4
            vis._fill_rect(
                entry_x * vis.tile_size + margin,
                entry_y * vis.tile_size + margin,
                vis.tile_size - margin * 2,
                vis.tile_size - margin * 2,
                0x00460F
            )
            exit_x, exit_y = vis.gen.config.exit_coord
            vis._fill_rect(
                exit_x * vis.tile_size + margin,
                exit_y * vis.tile_size + margin,
                vis.tile_size - margin * 2,
                vis.tile_size - margin * 2,
                0x460000
            )


        self._draw_path_line_partial(self.path_anim_index)

        vis.mlx.mlx_put_image_to_window(
            vis.mlx_ptr, vis.win, vis.img, 0, 0
        )
        vis._draw_menu()

    def _draw_path_line_partial(self, up_to: int) -> None:
        """Draw path line only up to a given index."""
        vis: "MazeVisualizer" = self.vis
        line_thickness: int = max(2, vis.tile_size // 6)
        half: int = line_thickness // 2

        for i in range(min(up_to, len(vis.path_cells) - 1)):
            x1, y1 = vis.path_cells[i]
            x2, y2 = vis.path_cells[i + 1]

            cx1 = x1 * vis.tile_size + vis.tile_size // 2
            cy1 = y1 * vis.tile_size + vis.tile_size // 2
            cx2 = x2 * vis.tile_size + vis.tile_size // 2
            cy2 = y2 * vis.tile_size + vis.tile_size // 2

            if x1 == x2:
                vis._fill_rect(
                    cx1 - half,
                    min(cy1, cy2),
                    line_thickness,
                    abs(cy2 - cy1) + line_thickness,
                    COLOR_PATH
                )
            else:
                vis._fill_rect(
                    min(cx1, cx2),
                    cy1 - half,
                    abs(cx2 - cx1) + line_thickness,
                    line_thickness,
                    COLOR_PATH
                )
