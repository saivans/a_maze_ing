import random
import sys
from typing import List, Tuple, Set
from collections import deque

N, E, S, W = 1, 2, 4, 8
DIRECTIONS = [
    (0, -1, N, S, "N"),
    (1, 0, E, W, "E"),
    (0, 1, S, N, "S"),
    (-1, 0, W, E, "W")
]


class MazeGenerator:
    def __init__(self, width: int, height: int, perfect: bool = True,
                 seed: int | None = None):
        self.width = width
        self.height = height
        self.perfect = perfect
        if seed is not None:
            random.seed(seed)
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]

    def _reserve_42_pattern(self) -> None:
        if self.width < 7 or self.height < 5:
            return
        cx, cy = self.width // 2 - 3, self.height // 2 - 2
        pattern_42 = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1),
            (2, 0), (2, 3), (2, 4),
            (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2),
            (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)
        ]
        for dx, dy in pattern_42:
            x, y = cx + dx, cy + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.visited[y][x] = True

    def _make_imperfect(self) -> None:
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] != 15 and random.random() < 0.35:
                    dx, dy, wall, opp_wall, _ = random.choice(DIRECTIONS)
                    nx, ny = x + dx, y + dy
                    if ((0 <= nx < self.width) and (0 <= ny < self.height) and
                            (self.grid[ny][nx] != 15)):
                        self.grid[y][x] &= ~wall
                        self.grid[ny][nx] &= ~opp_wall

    def generate(self, start_x: int, start_y: int) -> None:
        self._reserve_42_pattern()
        if self.visited[start_y][start_x]:
            self.visited[start_y][start_x] = False

        stack: List[Tuple[int, int]] = [(start_x, start_y)]
        self.visited[start_y][start_x] = True

        while stack:
            cx, cy = stack[-1]
            unvisited_neighbors = []

            for dx, dy, wall, opp_wall, _ in DIRECTIONS:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not self.visited[ny][nx]:
                        unvisited_neighbors.append((nx, ny, wall, opp_wall))

            if unvisited_neighbors:
                nx, ny, wall, opp_wall = random.choice(unvisited_neighbors)
                self.grid[cy][cx] &= ~wall
                self.grid[ny][nx] &= ~opp_wall

                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

        if not self.perfect:
            self._make_imperfect()

    def solve_bfs(self, start: Tuple[int, int],
                  exit_pos: Tuple[int, int]) -> str:
        sx, sy = start
        ex, ey = exit_pos

        queue = deque([(sx, sy, "")])
        visited_bfs: Set[Tuple[int, int]] = {(sx, sy)}

        while queue:
            cx, cy, path = queue.popleft()

            if cx == ex and cy == ey:
                return path

            cell = self.grid[cy][cx]

            for dx, dy, wall, _, letter in DIRECTIONS:
                nx, ny = cx + dx, cy + dy
                if (not (cell & wall) and
                    0 <= nx < self.width and
                        0 <= ny < self.height):
                    if (nx, ny) not in visited_bfs:
                        visited_bfs.add((nx, ny))
                        queue.append((nx, ny, path + letter))
        return ""

    def save_to_file(self, filename: str, start: Tuple[int, int],
                     exit_pos: Tuple[int, int], path: str) -> None:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for row in self.grid:
                    hex_line = "".join([hex(cell)[2:].upper() for cell in row])
                    f.write(hex_line + "\n")
                f.write("\n")
                f.write(f"{start[0]},{start[1]}\n")
                f.write(f"{exit_pos[0]},{exit_pos[1]}\n")
                f.write(path + "\n")
        except IOError as e:
            print(f"File Error: {e}", file=sys.stderr)
            sys.exit(1)
