*This project has been created as part of the 42 curriculum by [stagma], [moguenia]*

## Description

A-Maze-ing is a maze generator that creates random mazes from a configuration file. It supports perfect mazes (exactly one path between any two points) and includes visual rendering with interactive features. The maze generation logic is packaged as a reusable module that can be installed and used in other projects.

## Instructions

### Installation

Clone the repository and install dependencies:

```bash
make install
```

### Usage

Run the program with a configuration file:

```bash
make run
```

Or manually:

```bash
python3 a_maze_ing.py config.txt
```

### Interactive Controls

During visual display:
- Press `1` - Generate new maze
- Press `2` - Show/hide shortest path
- Press `3` - Change wall colors
- Press `4` - Quit

### Makefile Commands

- `make install` - Install dependencies
- `make run` - Execute the program
- `make debug` - Run with Python debugger
- `make clean` - Remove temporary files
- `make lint` - Run flake8 and mypy checks

## Configuration File Format

The configuration file uses `KEY=VALUE` format. Comments start with `#`.

| Key | Description | Example |
|-----|-------------|---------|
| WIDTH | Maze width (number of cells) | WIDTH=20 |
| HEIGHT | Maze height | HEIGHT=15 |
| ENTRY | Entry coordinates (x,y) | ENTRY=0,0 |
| EXIT | Exit coordinates (x,y) | EXIT=19,14 |
| OUTPUT_FILE | Output filename | OUTPUT_FILE=maze.txt |
| PERFECT | Is the maze perfect? | PERFECT=True |

Optional keys:
- `SEED` - Random seed for reproducibility (e.g., SEED=42)

### Example config.txt

```ini
# Maze configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Maze Generation Algorithm

I chose the **Recursive Backtracker** algorithm because:
- It guarantees perfect mazes (one unique path between any two points)
- Implementation is straightforward and efficient
- Produces mazes with long corridors and good branching
- Maps directly to spanning tree concepts in graph theory

The algorithm works by:
1. Starting from a random cell
2. Choosing a random unvisited neighbor
3. Removing the wall between them
4. Recursively continuing from the new cell
5. Backtracking when no unvisited neighbors remain

## Reusable Module

The maze generation logic is contained in `src/maze_generator.py` as a `MazeGenerator` class.

### Installation as a Package

The module is distributed as `mazegen-1.0.0-py3-none-any.whl` and `mazegen-1.0.0.tar.gz` at the root of the repository.

Install the package:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic Usage

```python
from maze_generator import MazeGenerator

# Create generator with dimensions
generator = MazeGenerator(width=20, height=15, seed=42)

# Generate maze
generator.generate(perfect=True)

# Access maze data
walls = generator.get_cell_walls(x, y)

# Find shortest path
path = generator.find_path(entry=(0,0), exit=(19,14))

# Save to file
generator.save_to_file("output.txt", entry=(0,0), exit=(19,14))
```

### Available Methods

- `__init__(width, height, seed)` - Initialize generator
- `generate(perfect)` - Generate the maze
- `get_cell_walls(x, y)` - Return hex value for cell walls
- `find_path(entry, exit)` - Return shortest path as list of directions
- `save_to_file(filename, entry, exit)` - Save maze in required format

## Resources

### Technical References
- [Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Flake8 Coding Standards](https://flake8.pycqa.org/)

### AI Usage

AI was used for:
- **Initial code structure** - Generating class skeletons and method signatures
- **Documentation** - Formatting README and docstrings
- **Debugging** - Identifying edge cases in maze validity checks
- **Algorithm explanation** - Understanding recursive backtracker implementation

All AI-generated code was reviewed, tested, and modified to ensure full understanding and compliance with project requirements.

## Team Management

### Roles
- **[Your Name]** - Maze generation algorithm, reusable module, configuration parser

*(If working in a team, list each member's role)*

### Planning
- Week 1: Implement MazeGenerator class and basic generation
- Week 2: Add configuration parsing and output file format
- Week 3: Implement visual rendering and interactive features
- Week 4: Testing, documentation, and package building

### What Worked Well
- Recursive backtracker produced clean perfect mazes reliably
- Type hints caught many bugs early
- Unit tests validated maze consistency

### What Could Be Improved
- Add multiple algorithm options
- Implement animation during generation
- Add more color customization options

### Tools Used
- Python 3.10
- Flake8 for linting
- Mypy for type checking
- Make for automation
- Build package for distribution
```

This covers all the mandatory sections from Chapter VII of the subject. Adjust the login(s), algorithm details, and team information to match your actual implementation.