import sys
from typing import Set, Dict, Tuple
from dataclasses import dataclass
from maze_generator import MazeGenerator


@dataclass
class MazeConfig:
    """Stores the strictly mandatory configuration for the maze."""
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def parse_config(file_path: str) -> MazeConfig:
    """Parses and validates the mandatory keys from the config file."""
    raw_config: Dict[str, str] = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split('#')[0].strip()
                if not line:
                    continue

                if '=' not in line:
                    raise ValueError(f"Invalid format (missing '='): '{line}'")

                key, value = line.split('=', 1)
                raw_config[key.strip().upper()] = value.strip()

        mandatory_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
                          'OUTPUT_FILE', 'PERFECT']
        for key in mandatory_keys:
            if key not in raw_config:
                raise KeyError(f"Missing mandatory key: {key}")

        width = int(raw_config['WIDTH'])
        height = int(raw_config['HEIGHT'])

        if width <= 0 or height <= 0:
            raise ValueError("WIDTH and HEIGHT must be strictly positive.")

        if width < 7 or height < 5:
            print("Error: The maze size does not allow the '42' pattern.",
                  file=sys.stderr)

        def parse_coords(coord_str: str, max_w: int, max_h: int
                         ) -> Tuple[int, int]:
            parts = coord_str.split(',')
            if len(parts) != 2:
                raise ValueError(f"Invalid coordinates format: '{coord_str}'")
            x, y = int(parts[0].strip()), int(parts[1].strip())
            if not (0 <= x < max_w) or not (0 <= y < max_h):
                raise ValueError(f"Coordinates ({x},{y}) out of bounds.")
            return x, y

        entry = parse_coords(raw_config['ENTRY'], width, height)
        maze_exit = parse_coords(raw_config['EXIT'], width, height)

        if entry == maze_exit:
            raise ValueError("ENTRY and EXIT cannot be the same.")

        perfect_str = raw_config['PERFECT'].lower()
        if perfect_str in ('true', '1', 'yes'):
            perfect = True
        elif perfect_str in ('false', '0', 'no'):
            perfect = False
        else:
            raise ValueError(
                f"Invalid value for PERFECT: '{raw_config['PERFECT']}'")

        output_file = raw_config['OUTPUT_FILE']
        if not output_file:
            raise ValueError("OUTPUT_FILE cannot be empty.")

        seed_val = None
        if 'SEED' in raw_config:
            try:
                seed_val = int(raw_config['SEED'])
            except ValueError:
                raise ValueError(
                    f"Invalid value for SEED: '{raw_config['SEED']}'. "
                    f"Must be an integer.")

        return MazeConfig(width, height, entry, maze_exit, output_file,
                          perfect, seed_val)

    except (FileNotFoundError, ValueError, KeyError, Exception) as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)


class MazeVisualizer:
    def __init__(self, config: MazeConfig, generator: MazeGenerator,
                 path_str: str, seed: int | None = None):
        self.config = config
        self.generator = generator
        self.seed = seed
        self.path_str = path_str
        self.show_path = False

        self.wall_colors = [
            '\033[97m',       # White
            '\033[94m',       # Blue
            '\033[38;5;208m',  # Orange
            '\033[95m',       # Magenta
            '\033[93m'        # Yellow
        ]
        self.current_color_idx = 0
        self.reset_color = '\033[0m'

        self.path_coords: Set[Tuple[int, int]] = set()
        self.path_connections: Set[Tuple[int, int]] = set()
        self._calculate_path_coords()

    def _calculate_path_coords(self) -> None:
        cx, cy = self.config.entry
        self.path_coords.add((cx, cy))
        for move in self.path_str:
            px, py = cx, cy
            if move == 'N':
                cy -= 1
                self.path_connections.add((cx * 2 + 1, py * 2))
            elif move == 'S':
                cy += 1
                self.path_connections.add((cx * 2 + 1, py * 2 + 2))
            elif move == 'E':
                cx += 1
                self.path_connections.add((px * 2 + 2, py * 2 + 1))
            elif move == 'W':
                cx -= 1
                self.path_connections.add((px * 2, py * 2 + 1))
            self.path_coords.add((cx, cy))

    def regenerate_maze(self) -> None:
        self.generator = MazeGenerator(
            self.config.width, self.config.height,
            self.config.perfect, self.seed)
        self.generator.generate(self.config.entry[0], self.config.entry[1])
        self.path_str = self.generator.solve_bfs(
            self.config.entry, self.config.exit)
        self.generator.save_to_file(
            self.config.output_file, self.config.entry,
            self.config.exit, self.path_str)
        self.path_coords.clear()
        self.path_connections.clear()
        self._calculate_path_coords()

    def draw_maze(self) -> None:
        print("\033[H\033[J", end="")
        color = self.wall_colors[self.current_color_idx]
        reset = self.reset_color

        wall_block = f"{color}██{reset}"
        path_block = "  "

        term_h = self.config.height * 2 + 1
        term_w = self.config.width * 2 + 1
        canvas = [[wall_block for _ in range(term_w)] for _ in range(term_h)]

        for y in range(self.config.height):
            for x in range(self.config.width):
                cell = self.generator.grid[y][x]

                cx, cy = x * 2 + 1, y * 2 + 1

                if cell != 15:
                    canvas[cy][cx] = path_block
                    if not (cell & 2):
                        canvas[cy][cx + 1] = path_block
                    if not (cell & 4):
                        canvas[cy + 1][cx] = path_block
                else:
                    canvas[cy][cx] = f"\033[92m██{reset}"

        if self.show_path:
            for (px, py) in self.path_coords:
                canvas[py * 2 + 1][px * 2 + 1] = f"\033[91m••{reset}"
            for (cx, cy) in self.path_connections:
                canvas[cy][cx] = f"\033[91m••{reset}"

        ex, ey = self.config.entry
        canvas[ey * 2 + 1][ex * 2 + 1] = "\033[91mEN\033[0m"

        ox, oy = self.config.exit
        canvas[oy * 2 + 1][ox * 2 + 1] = "\033[91mEX\033[0m"

        print(f"{color}=== A-Maze-ing [{self.config.width}x"
              f"{self.config.height}] ==={reset}\n")
        for row in canvas:
            print("".join(row))

        print(f"\nEntry: {self.config.entry} | Exit: {self.config.exit}")
        print(f"Path visible: {'Yes' if self.show_path else 'No'}")

    def interactive_loop(self) -> None:
        while True:
            self.draw_maze()
            print("\n=== Menu ===")
            print("1. Generate new maze")
            print("2. on/off --> path")
            print("3. Change maze wall colors")
            print("4. Quit")

            choice = input("\nChoice (1-4): ").strip()

            if choice == '1':
                self.regenerate_maze()
            elif choice == '2':
                self.show_path = not self.show_path
            elif choice == '3':
                self.current_color_idx = (
                    self.current_color_idx + 1) % len(self.wall_colors)
            elif choice == '4':
                print("Exiting A-Maze-ing...")
                sys.exit(0)
            else:
                input("Invalid choice! Press Enter to try again...")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config.txt>", file=sys.stderr)
        sys.exit(1)

    config = parse_config(sys.argv[1])

    maze = MazeGenerator(
        config.width, config.height, config.perfect, config.seed)
    maze.generate(config.entry[0], config.entry[1])

    shortest_path = maze.solve_bfs(config.entry, config.exit)

    maze.save_to_file(
        config.output_file, config.entry, config.exit, shortest_path)

    visualizer = MazeVisualizer(config, maze, shortest_path, config.seed)
    visualizer.interactive_loop()


if __name__ == "__main__":
    main()
