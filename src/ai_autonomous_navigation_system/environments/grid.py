from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np

# Cell values stored in the grid array.
FREE: int = 0
OBSTACLE: int = 1
START: int = 2
GOAL: int = 3

Point = Tuple[int, int]  # (x, y)


@dataclass
class GridConfig:
    width: int = 10
    height: int = 10
    start: Point = (0, 0)
    goal: Optional[Point] = None  # defaults to (width-1, height-1)


class GridEnvironment:
    """
    Beginner-friendly grid environment.

    - The grid is stored as a 2D NumPy array with shape (height, width).
    - Coordinates are (x, y) where x is column, y is row.

    Cell values:
    - 0: free
    - 1: obstacle
    - 2: start
    - 3: goal
    """

    def __init__(self, config: GridConfig) -> None:
        self.width = int(config.width)
        self.height = int(config.height)
        if self.width <= 0 or self.height <= 0:
            raise ValueError("width and height must be positive integers")

        goal = config.goal if config.goal is not None else (self.width - 1, self.height - 1)
        self.start: Point = tuple(config.start)  # type: ignore[assignment]
        self.goal: Point = tuple(goal)  # type: ignore[assignment]

        self.grid: np.ndarray = np.zeros((self.height, self.width), dtype=np.uint8)
        self.reset(clear_obstacles=True)

    def reset(self, *, clear_obstacles: bool = False) -> np.ndarray:
        """
        Reset the grid markings for start/goal.

        If clear_obstacles=True, obstacles are removed too.
        Returns a copy of the current grid.
        """
        if clear_obstacles:
            self.grid.fill(FREE)
        else:
            # Keep obstacles, clear any old START/GOAL markings.
            self.grid[self.grid == START] = FREE
            self.grid[self.grid == GOAL] = FREE

        self._validate_point(self.start, name="start")
        self._validate_point(self.goal, name="goal")
        if self.start == self.goal:
            raise ValueError("start and goal must be different points")

        self._mark_start_goal()
        return self.grid.copy()

    def set_start_goal(self, *, start: Point, goal: Point) -> None:
        """Update start and goal positions, then re-mark the grid."""
        self.start = tuple(start)  # type: ignore[assignment]
        self.goal = tuple(goal)  # type: ignore[assignment]
        self.reset(clear_obstacles=False)

    def add_obstacle(self, point: Point) -> bool:
        """
        Add an obstacle at a single point.
        Returns True if placed, False if skipped (out of bounds or start/goal).
        """
        if not self._in_bounds(point):
            return False
        if point == self.start or point == self.goal:
            return False
        x, y = point
        self.grid[y, x] = OBSTACLE
        self._mark_start_goal()
        return True

    def add_obstacles(self, points: Iterable[Point]) -> int:
        """Add multiple obstacles. Returns the number successfully placed."""
        placed = 0
        for p in points:
            if self.add_obstacle(p):
                placed += 1
        return placed

    def add_random_obstacles(
        self,
        *,
        count: int,
        seed: Optional[int] = None,
        avoid: Sequence[Point] = (),
    ) -> List[Point]:
        """
        Randomly place obstacles on free cells.

        - count: desired number of obstacles to add
        - seed: optional RNG seed for reproducibility
        - avoid: additional points to avoid (besides start/goal)

        Returns the list of placed obstacle points.
        """
        count = int(count)
        if count < 0:
            raise ValueError("count must be >= 0")

        rng = np.random.default_rng(seed)
        avoid_set = {tuple(p) for p in avoid} | {self.start, self.goal}

        free_cells: List[Point] = []
        for y in range(self.height):
            for x in range(self.width):
                p = (x, y)
                if p in avoid_set:
                    continue
                if self.grid[y, x] == FREE:
                    free_cells.append(p)

        if not free_cells or count == 0:
            return []

        count = min(count, len(free_cells))
        idx = rng.choice(len(free_cells), size=count, replace=False)

        placed: List[Point] = []
        for i in idx:
            p = free_cells[int(i)]
            if self.add_obstacle(p):
                placed.append(p)
        return placed

    def as_array(self) -> np.ndarray:
        """Return a copy of the underlying 2D grid array."""
        return self.grid.copy()

    def _mark_start_goal(self) -> None:
        sx, sy = self.start
        gx, gy = self.goal
        # Re-apply these markers (obstacles should never override them).
        self.grid[sy, sx] = START
        self.grid[gy, gx] = GOAL

    def _validate_point(self, p: Point, *, name: str) -> None:
        if not self._in_bounds(p):
            raise ValueError(f"{name} must be within grid bounds, got {p}")

    def _in_bounds(self, p: Point) -> bool:
        x, y = p
        return 0 <= x < self.width and 0 <= y < self.height

