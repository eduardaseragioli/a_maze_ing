import os
import random
from maze_config import MazeConfig
from constants import PATTERN_42


def _get_blocked_cells(width: int, height: int) -> set[tuple[int, int]]:
    """Calculate which cells are blocked by the 42 pattern."""
    center_x = width // 2 - 3
    center_y = height // 2 - 3
    blocked: set[tuple[int, int]] = set()

    for (dx, dy) in PATTERN_42:
        x = center_x + dx
        y = center_y + dy
        if 0 <= x < width and 0 <= y < height:
            blocked.add((x, y))

    return blocked


def parse_config(filepath: str) -> MazeConfig:
    if not os.path.isfile(filepath):
        raise FileNotFoundError("File path not found!")

    raw: dict[str, str] = {}

    with open(filepath, 'r') as config:
        for line in config:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                raise ValueError("Invalid syntax")

            key, value = line.split('=', 1)
            key = key.strip().upper()
            value = value.strip()
            raw[key] = value

    keys: list = ["WIDTH", "HEIGHT", "ENTRY",
                  "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in keys:
        if key not in raw:
            raise ValueError(f"Missing required key: {key}")
    try:
        width = int(raw["WIDTH"])
    except ValueError:
        raise ValueError(f"WIDTH must be an integer, got: {raw['WIDTH']}")
    if width <= 0:
        raise ValueError(
            "The width must be a interger and positive number")

    try:
        height = int(raw["HEIGHT"])
    except ValueError:
        raise ValueError(
            f"HEIGHT must be an integer, got: {raw['HEIGHT']}")
    if height <= 0:
        raise ValueError(
            "The height must be a integer and positive number")

    entry_raw = raw["ENTRY"]
    if "," not in entry_raw:
        raise ValueError("Entry must be in format x,y")
    x, y = entry_raw.split(",")
    try:
        entry = (int(x), int(y))
    except ValueError:
        raise ValueError(f"ENTRY must be an integer, got: {entry_raw}")
    if entry[0] >= width or entry[1] >= height or entry[0] < 0 or entry[1] < 0:
        raise ValueError("Entry out of bounds")

    # Validate that ENTRY is not in blocked cells (42 pattern)
    blocked_cells = _get_blocked_cells(width, height)
    if entry in blocked_cells:
        raise ValueError(
            f"ENTRY coordinate {entry} cannot be inside the 42 pattern"
        )

    exit_raw = raw["EXIT"]
    if "," not in exit_raw:
        raise ValueError("Exit must be in format x,y")
    x, y = exit_raw.split(",")
    try:
        exit_key = (int(x), int(y))
    except ValueError:
        raise ValueError(f"EXIT must be an integer, got: {exit_raw}")
    if (exit_key[0] >= width or exit_key[1] >= height or
            exit_key[0] < 0 or exit_key[1] < 0):
        raise ValueError("Exit out of bounds")

    if entry == exit_key:
        raise ValueError("Entry and Exit must be different values")

    # Validate that EXIT is not in blocked cells (42 pattern)
    blocked_cells = _get_blocked_cells(width, height)
    if exit_key in blocked_cells:
        raise ValueError(
            f"EXIT coordinate {exit_key} cannot be inside the 42 pattern"
        )

    output_file = raw["OUTPUT_FILE"]

    perfect_str = raw["PERFECT"].capitalize()
    if perfect_str not in ("True", "False"):
        raise ValueError("Perfect must be True or False")
    perfect = perfect_str == "True"

    if "SEED" in raw:
        try:
            seed = int(raw["SEED"])
        except ValueError:
            raise ValueError(f"SEED must be an integer, got: {raw['SEED']}")
    else:
        seed = random.randint(0, 2**32)

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit_coord=exit_key,
        output_file=output_file,
        perfect=perfect,
        seed=seed
    )
