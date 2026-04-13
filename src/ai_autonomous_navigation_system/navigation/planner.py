from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple


Point = Tuple[int, int]


@dataclass(frozen=True)
class Plan:
    path: Tuple[Point, ...]


def plan_straight_line(start: Point, goal: Point) -> Plan:
    """
    Minimal placeholder planner.
    Replace with A*, RRT, MPC, or learned planners later.
    """
    if start == goal:
        return Plan(path=(start,))
    return Plan(path=(start, goal))

