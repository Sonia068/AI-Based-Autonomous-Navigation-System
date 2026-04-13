from __future__ import annotations

from typing import Iterable, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D

from ai_autonomous_navigation_system.environments.grid import (
    FREE,
    GOAL,
    OBSTACLE,
    START,
    GridEnvironment,
    Point,
)


def plot_grid(
    env: GridEnvironment,
    *,
    path: Optional[Iterable[Point]] = None,
    agent_position: Optional[Point] = None,
    agent_color: str = "deepskyblue",
    title: Optional[str] = None,
    show_grid_lines: bool = True,
    cell_size: float = 0.7,
    show_legend: bool = True,
) -> Figure:
    """
    Create a Matplotlib figure visualizing the grid.

    Color requirements:
    - obstacles: black
    - start: green
    - goal: red
    - path: blue

    This function returns a Figure so it's easy to use in Streamlit:
        fig = plot_grid(env, path=path)
        st.pyplot(fig)
    """
    grid = env.as_array()
    overlay = _path_overlay(grid.shape, path=path)

    # Base layer: free/obstacle/start/goal.
    base_cmap = ListedColormap(
        [
            "white",  # FREE
            "black",  # OBSTACLE
            "green",  # START
            "red",  # GOAL
        ]
    )
    base_norm = plt.Normalize(vmin=0, vmax=3)

    fig_w = max(4.0, env.width * cell_size)
    fig_h = max(4.0, env.height * cell_size)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    ax.imshow(grid, cmap=base_cmap, norm=base_norm, interpolation="nearest")

    # Path layer: draw as semi-transparent blue squares on top.
    if overlay is not None:
        path_cmap = ListedColormap([(0, 0, 0, 0), (0.0, 0.2, 1.0, 0.75)])  # transparent, blue
        ax.imshow(overlay, cmap=path_cmap, vmin=0, vmax=1, interpolation="nearest")
        _plot_path_line(ax, path=list(path) if path is not None else [])

    # Make start/goal extra clear (on top of the image).
    sx, sy = env.start
    gx, gy = env.goal
    ax.scatter([sx], [sy], s=120, c="green", edgecolors="white", linewidths=1.5, zorder=5)
    ax.scatter([gx], [gy], s=120, c="red", edgecolors="white", linewidths=1.5, zorder=5)

    # Agent marker (for simple animations / step-by-step updates).
    if agent_position is not None:
        ax.scatter(
            [agent_position[0]],
            [agent_position[1]],
            s=90,
            c=agent_color,
            edgecolors="white",
            linewidths=1.5,
            zorder=6,
        )

    if title:
        ax.set_title(title)

    ax.set_xticks([])
    ax.set_yticks([])

    if show_grid_lines:
        ax.set_xticks(np.arange(-0.5, env.width, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, env.height, 1), minor=True)
        ax.grid(which="minor", color="#DDDDDD", linewidth=0.8)
        ax.tick_params(which="minor", bottom=False, left=False)

    ax.set_aspect("equal")

    if show_legend:
        handles = [
            Line2D([0], [0], marker="s", color="none", markerfacecolor="black", markersize=10, label="Obstacle"),
            Line2D([0], [0], marker="o", color="none", markerfacecolor="green", markeredgecolor="white", markersize=10, label="Start"),
            Line2D([0], [0], marker="o", color="none", markerfacecolor="red", markeredgecolor="white", markersize=10, label="Goal"),
            Line2D([0], [0], color=(0.0, 0.2, 1.0, 0.9), linewidth=3, label="Path"),
            Line2D(
                [0],
                [0],
                marker="o",
                color="none",
                markerfacecolor=agent_color,
                markeredgecolor="white",
                markersize=9,
                label="Agent",
            ),
        ]
        ax.legend(handles=handles, loc="upper right", frameon=True, framealpha=0.95)

    fig.tight_layout()
    return fig


def _path_overlay(shape: Tuple[int, int], *, path: Optional[Iterable[Point]]) -> Optional[np.ndarray]:
    """
    Build a 2D overlay array where 1 marks path cells.
    We intentionally do not overwrite start/goal markers.
    """
    if path is None:
        return None

    height, width = shape
    overlay = np.zeros((height, width), dtype=np.uint8)
    for x, y in path:
        if 0 <= x < width and 0 <= y < height:
            overlay[y, x] = 1
    return overlay


def _plot_path_line(ax: plt.Axes, *, path: List[Point]) -> None:
    """
    Overlay a line through the centers of path cells.
    This makes the route easier to see than squares alone.
    """
    if len(path) < 2:
        return

    xs = [p[0] for p in path]
    ys = [p[1] for p in path]
    ax.plot(xs, ys, color=(0.0, 0.2, 1.0, 0.9), linewidth=3, zorder=4)

