*This project has been created as part of the 42 curriculum by stagma, moguenia.*

# A-Maze-ing

## Description
A-Maze-ing is a Python project that creates random mazes from a config file:
- generate a maze
- save it in the required hex format
- find the shortest path
- show the maze in the terminal

The project follows the 42 subject rules (Python 3.10+, flake8, mypy, error handling, reusable class).

## Instructions

### Requirements
- Python 3.10+
- pip

### Install
```bash
make install
```

### Run
```bash
make run
```
Or:
```bash
python3 a_maze_ing.py config.txt
```

### Debug
```bash
make debug
```

### Lint
```bash
make lint
```

### Strict lint (optional)
```bash
make lint-strict
```

### Clean caches
```bash
make clean
```

## Config File Format
Use one `KEY=VALUE` per line.
Lines starting with `#` are comments.

Mandatory keys:
- `WIDTH` 
- `HEIGHT` 
- `ENTRY`
- `EXIT`
- `OUTPUT_FILE`
- `PERFECT`

Optional key:
- `SEED` (example: `SEED=42`)

Example config:
```ini
WIDTH=42
HEIGHT=42
ENTRY=0,0
EXIT=42,42
OUTPUT_FILE=output.txt
PERFECT=1
SEED=42
```

## Maze Rules (Mandatory)
- Entry and exit must be valid and different.
- Maze walls must be coherent between neighbor cells.
- Maze must stay connected (no isolated cells).
- No open 3x3 area is allowed.
- If `PERFECT=1`, there is exactly one path from entry to exit.
- The maze tries to include a visible `42` pattern with closed cells.
- If maze is too small, `42` may be skipped with a warning message.

## Output File Format
Each cell is written as one hex character.
Bits for walls:
- bit 0: North
- bit 1: East
- bit 2: South
- bit 3: West

After maze rows, the file contains:
1. empty line
2. entry coordinates
3. exit coordinates
4. shortest path as letters `N E S W`

## Visual Mode
The terminal view shows:
- walls
- entry/exit
- optional shortest path
- highlighted `42` cells

Controls:
- `1` or `R`: generate a new maze (new seed)
- `2` or `V`: show/hide shortest path
- `3` or `T`: change colors/theme
- `4` or `Q`: quit
- `P`: play button

## Bonus Part


## Reusable Code
Reusable part: `MazeGenerator` class in `maze_generator.py`.

Basic use:
```python
from maze_generator import MazeGenerator

config = {
    "WIDTH": 10,
    "HEIGHT": 10,
    "ENTRY": (0, 0),
    "EXIT": (9, 9),
    "OUTPUT_FILE": "maze.txt",
    "PERFECT": 1,
    "SEED": 42,
}

maze = MazeGenerator(config)
maze_data = generated.generate()
```

## Team and Project Management
### Roles
- `moguenia`: parsing and error handling, maze display and rendering, bonus play button, menu display
- `stagma`: maze generation algorithm, pathfinding, perfect and non-perfect maze modes

### Planning (expected vs real)
- Start: parser + generator + file output
- Then: pathfinding + visual mode
- End: polish, lint/mypy fixes, README

### What worked well
- clear split between main script and reusable module
- deterministic generation with seed
- simple controls for interactive mode

### What can be improved
- add more generation algorithms and animations

### Tools used
- Python 3.10+
- flake8
- mypy
- Makefile
- git

## Resources
- 42 subject PDF/text for A-Maze-ing
- Python docs: https://docs.python.org/3/
- flake8 docs: https://flake8.pycqa.org/
- mypy docs: https://mypy.readthedocs.io/
- Maze generation overview: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- BFS overview: https://en.wikipedia.org/wiki/Breadth-first_search

## AI Usage
AI was used for:
- checking explanation clarity
- drafting documentation text
- getting info about the project
