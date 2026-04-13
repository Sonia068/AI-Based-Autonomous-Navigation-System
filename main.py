from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

import matplotlib

# Allow running from repo root without installing the package.
_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from ai_autonomous_navigation_system.environments.grid import GridConfig, GridEnvironment
from ai_autonomous_navigation_system.navigation import astar_shortest_path
from ai_autonomous_navigation_system.visualization import plot_grid


def run_demo() -> None:
    # Use a non-interactive backend so this runs cleanly in terminals/CI.
    matplotlib.use("Agg")

    env = GridEnvironment(
        GridConfig(
            width=20,
            height=12,
            start=(1, 1),
            goal=(18, 10),
        )
    )

    # Manual obstacles (a simple wall with a gap).
    wall_y = 6
    wall = [(x, wall_y) for x in range(2, 19) if x != 10]
    env.add_obstacles(wall)

    # Random obstacles for a slightly harder test case.
    env.add_random_obstacles(count=25, seed=7)

    result = astar_shortest_path(env)

    print("A* demo")
    print(f"- Grid size: {env.width} x {env.height}")
    print(f"- Start: {env.start}")
    print(f"- Goal:  {env.goal}")
    print(f"- Path found: {bool(result.path)}")
    print(f"- Path cost: {result.cost}")
    if result.path:
        print(f"- Path length (cells): {len(result.path)}")
        print(f"- First/last: {result.path[0]} -> {result.path[-1]}")
    else:
        print("- No path exists (try changing obstacles/seed).")

    fig = plot_grid(env, path=result.path, title="Grid + A* shortest path")

    outputs_dir = Path("outputs")
    outputs_dir.mkdir(parents=True, exist_ok=True)
    out_path = outputs_dir / f"astar_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    fig.savefig(out_path, dpi=160)
    print(f"- Saved figure: {out_path}")


if __name__ == "__main__":
    run_demo()

