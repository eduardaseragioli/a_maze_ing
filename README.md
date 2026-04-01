*This project has been created as part of the 42 curriculum by dseragio, eseragio.*

# A-Maze-ing

## Description

A-Maze-ing is a Python maze generator project.
Its goal is to read a configuration file, generate a coherent random maze, optionally enforce perfect-maze behavior, and export the result in a hexadecimal wall format.

This project also includes a visual representation of the maze and a reusable generation module intended to be packaged and reused in future projects.

Core goals from the subject:

- Parse and validate configuration safely.
- Generate coherent mazes with reproducibility via seed.
- Respect wall consistency between neighboring cells.
- Support entry/exit and shortest-path extraction.
- Write output in the required file format.
- Provide visual rendering and basic interactions.

## Instructions

### Requirements

- Python 3.10+
- flake8
- mypy

### Run

The program must be executed as:

```bash
python3 a_maze_ing.py config.txt
```

### Makefile targets

The project provides these targets:

- install: install dependencies.
- run: run the main script.
- debug: run with Python debugger.
- clean: remove temporary/cache files.
- lint: run flake8 and mypy with required flags.
- lint-strict (optional): run flake8 and mypy --strict.

Expected lint command behavior:

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

Optional strict lint:

```bash
flake8 .
mypy . --strict
```

### Error handling policy

The program must never crash unexpectedly.
It must report clear errors for cases such as:

- missing file,
- invalid config syntax,
- invalid values,
- impossible maze parameters.

## Configuration File Format

The configuration file uses one KEY=VALUE per line.

- Lines starting with # are comments and must be ignored.
- Empty lines are ignored.

Mandatory keys:

- WIDTH: maze width in cells.
- HEIGHT: maze height in cells.
- ENTRY: entry coordinates in x,y.
- EXIT: exit coordinates in x,y.
- OUTPUT_FILE: output filename.
- PERFECT: True or False.

Optional keys (example):

- SEED: integer for reproducibility.

Example full config:

```ini
# Default project config
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

Validation rules:

- ENTRY and EXIT must be different and in bounds.
- Width and height must be positive.
- PERFECT must be boolean-like (True/False).

## Maze Generation Algorithm

Chosen algorithm: randomized depth-first search (recursive backtracker behavior with an explicit stack).

### Why this algorithm

- Simple and reliable to implement.
- Naturally produces coherent corridors.
- Easy to enforce perfect maze mode (single connected spanning-tree behavior).
- Works well with deterministic randomness using a seed.

### Coherence guarantees

Each cell uses a 4-bit wall mask:

- bit 0: North
- bit 1: East
- bit 2: South
- bit 3: West

When opening a wall between cell A and cell B, the opposite wall is also opened in B.
This guarantees neighbor consistency and avoids impossible wall states.

### Subject constraints handled

- Random generation with seed reproducibility.
- Entry and exit inside bounds.
- No isolated cells (except allowed "42" fully closed pattern cells).
- External border coherence.
- Perfect mode: exactly one path between entry and exit.
- "42" pattern insertion when maze size allows it; warning printed otherwise.

## Output File Format

The maze is written row by row, one hexadecimal digit per cell.

- Each hex digit encodes closed walls from the 4-bit mask.
- One row per line.
- All lines end with \n.

After one empty line, the file includes three lines:

1. Entry coordinates
2. Exit coordinates
3. Shortest valid path from entry to exit using letters N, E, S, W

Example bit interpretation:

- 3 (binary 0011): North and East walls closed.
- A (binary 1010): East and West walls closed.

## Visual Representation

The project provides terminal ASCII rendering.

Displayed elements:

- walls,
- entry,
- exit,
- optional shortest path overlay.

User interactions supported:

- regenerate maze,
- show/hide shortest path,
- change wall colors,
- optional custom color for "42" pattern.

## Reusable Module

Maze generation logic is implemented as a unique class in a standalone module: MazeGenerator.

Reusable features:

- instantiate generator with custom parameters,
- set seed,
- generate maze structure,
- access generated structure,
- access at least one valid solution path.

Basic usage example:

```python
from maze_generator import MazeGenerator
from maze_config import MazeConfig

config = MazeConfig(
	width=20,
	height=15,
	entry=(0, 0),
	exit_coord=(19, 14),
	output_file="maze.txt",
	perfect=True,
	seed=42,
)

generator = MazeGenerator(config)
generator.generate()
print(generator.grid)
print(generator.solution_path)
generator.write_output()
```

### Packaging requirement

The reusable module must be buildable as a package at repository root with name format mazegen-*.

Allowed built artifacts:

- .whl
- .tar.gz

Example:

- mazegen-1.0.0-py3-none-any.whl

All sources and build metadata required to rebuild the package must be present in the repository.

## Team and Project Management

### Team roles

This repository is currently maintained by two contributor:

- dseragio: parser, generation logic, validation, output format, README, packaging preparation.

- eseragio: parser, generation logic, validation, output format, README, packaging preparation.

### Planning (initial vs actual)

Initial plan:

1. Config parser and error handling.
2. Core generator and wall coherence.
3. Perfect mode and shortest path.
4. Output format and rendering.
5. Packaging and documentation.

Actual evolution:

1. Parser and validation were implemented first.
2. Grid and wall operations were iterated and corrected.
3. "42" pattern integration was added early for constraint compliance.
4. Remaining focus moved to complete generation flow, path extraction, and packaging checks.

### What worked well

- Clear separation between config parsing and generation.
- Bitmask wall model is compact and consistent.
- Seeded randomness improves reproducibility and debugging.

### What can be improved

- Expand automated tests for edge cases and tiny mazes.
- Add stricter static typing coverage across all modules.
- Improve visualization options and user interaction ergonomics.

### Tools used

- Python 3.10+
- flake8
- mypy
- Makefile
- Git/GitHub
- AI assistant (for explanation drafting, refactoring suggestions, and documentation polishing)

## AI Usage (Required Transparency)

AI was used for:

- organizing the project workflow by splitting tasks across days,
- checking whether variable names were clear and correctly used,
- improving understanding of how MLX could be used in the project.

AI was not used as blind copy-paste.
All generated suggestions were reviewed, adapted, and validated manually.

## Additional Guidelines Followed

- .gitignore includes Python artifacts and cache folders.
- Context managers are used for file operations.
- Small test programs are used locally for behavior checks (not graded artifacts).

## Resources

Classic references:

- Python documentation: https://docs.python.org/3/
- PEP 8: https://peps.python.org/pep-0008/
- PEP 257: https://peps.python.org/pep-0257/
- typing module: https://docs.python.org/3/library/typing.html
- mypy docs: https://mypy.readthedocs.io/
- flake8 docs: https://flake8.pycqa.org/
- Maze generation overview: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Depth-first search: https://en.wikipedia.org/wiki/Depth-first_search

## Submission and Evaluation Readiness

- All mandatory files are kept inside the repository.
- The project is prepared for peer-evaluation and quick live modifications.
- The implementation choices can be explained and justified during defense.
