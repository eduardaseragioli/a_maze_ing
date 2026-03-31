import sys
from config_parser import parse_config
from maze_generator import MazeGenerator
from maze_visualizer import MazeVisualizer


def main() -> None:
    args = sys.argv
    if len(args) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        config = parse_config(file_path)
        generator = MazeGenerator(config)
        generator.generate()
        generator.write_output()

        visualizer = MazeVisualizer(generator)
        visualizer.run()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
