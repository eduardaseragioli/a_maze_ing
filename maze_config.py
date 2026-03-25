from dataclasses import dataclass


@dataclass
class MazeConfig:
    width: int
    height: int
    entry: tuple[int, int]
    exit_coord: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int
