from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


Point = Tuple[int, int]


@dataclass
class StepResult:
    observation: np.ndarray
    reward: float
    terminated: bool
    info: dict


class GridWorld:
    """
    Minimal grid environment placeholder.
    0 = free, 1 = obstacle.
    """

    def __init__(self, width: int = 10, height: int = 10) -> None:
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self.agent: Point = (0, 0)
        self.goal: Point = (width - 1, height - 1)

    def reset(self) -> np.ndarray:
        self.agent = (0, 0)
        return self._obs()

    def step(self, action: int) -> StepResult:
        # 0 up, 1 right, 2 down, 3 left
        x, y = self.agent
        if action == 0:
            y -= 1
        elif action == 1:
            x += 1
        elif action == 2:
            y += 1
        elif action == 3:
            x -= 1

        x = int(np.clip(x, 0, self.width - 1))
        y = int(np.clip(y, 0, self.height - 1))
        self.agent = (x, y)

        terminated = self.agent == self.goal
        reward = 1.0 if terminated else -0.01
        return StepResult(observation=self._obs(), reward=reward, terminated=terminated, info={})

    def _obs(self) -> np.ndarray:
        obs = self.grid.copy()
        ax, ay = self.agent
        gx, gy = self.goal
        obs[ay, ax] = 2
        obs[gy, gx] = 3
        return obs

