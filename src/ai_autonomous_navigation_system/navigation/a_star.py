from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np

from ai_autonomous_navigation_system.environments.grid import OBSTACLE, GridEnvironment, Point


@dataclass(frozen=True)
class AStarResult:
    """
    Result returned by A*.

    - path: list of (x, y) points including start and goal; empty if no path exists
    - cost: number of moves in the path (0 if path is empty or start==goal)
    """

    path: List[Point]
    cost: int


def manhattan(a: Point, b: Point) -> int:
    """Manhattan distance on a grid: |x1-x2| + |y1-y2|."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_shortest_path(env: GridEnvironment) -> AStarResult:
    """
    Find the shortest path from env.start to env.goal using A*.

    - Works on 4-connected grids (up, right, down, left).
    - Avoids obstacles (cells with value OBSTACLE).
    - Uses Manhattan distance as the heuristic.

    Returns:
        AStarResult with path (possibly empty) and its move cost.
    """
    grid = env.grid  # shape: (height, width)
    start = env.start
    goal = env.goal

    if start == goal:
        return AStarResult(path=[start], cost=0)

    if _is_blocked(grid, start) or _is_blocked(grid, goal):
        return AStarResult(path=[], cost=0)

    # Priority queue entries are (f_score, tie_breaker, point).
    # tie_breaker makes the ordering deterministic when f_scores tie.
    open_heap: List[Tuple[int, int, Point]] = []
    tie = 0

    g_score: Dict[Point, int] = {start: 0}
    came_from: Dict[Point, Point] = {}

    heapq.heappush(open_heap, (manhattan(start, goal), tie, start))

    while open_heap:
        _, _, current = heapq.heappop(open_heap)

        if current == goal:
            path = _reconstruct_path(came_from, current)
            return AStarResult(path=path, cost=len(path) - 1)

        for neighbor in _neighbors_4(current, width=env.width, height=env.height):
            if _is_blocked(grid, neighbor):
                continue

            tentative_g = g_score[current] + 1  # each move has cost 1
            if tentative_g < g_score.get(neighbor, 1_000_000_000):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f = tentative_g + manhattan(neighbor, goal)
                tie += 1
                heapq.heappush(open_heap, (f, tie, neighbor))

    # No path found.
    return AStarResult(path=[], cost=0)


def _is_blocked(grid: np.ndarray, p: Point) -> bool:
    x, y = p
    return int(grid[y, x]) == OBSTACLE


def _neighbors_4(p: Point, *, width: int, height: int) -> List[Point]:
    x, y = p
    candidates = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
    in_bounds: List[Point] = []
    for nx, ny in candidates:
        if 0 <= nx < width and 0 <= ny < height:
            in_bounds.append((nx, ny))
    return in_bounds


def _reconstruct_path(came_from: Dict[Point, Point], current: Point) -> List[Point]:
    # Walk backwards from goal to start, then reverse.
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

