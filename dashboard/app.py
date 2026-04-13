from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import streamlit as st

_SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from ai_autonomous_navigation_system.environments.grid import GridConfig, GridEnvironment
from ai_autonomous_navigation_system.navigation import AStarResult, astar_shortest_path
from ai_autonomous_navigation_system.visualization import plot_grid


def _clamp_int(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, int(value)))


def _init_state(grid_size: int) -> None:
    if "config" not in st.session_state:
        st.session_state.config = GridConfig(width=int(grid_size), height=int(grid_size), start=(0, 0), goal=None)
    if "env" not in st.session_state:
        st.session_state.env = None
    if "result" not in st.session_state:
        st.session_state.result = None
    if "status" not in st.session_state:
        st.session_state.status = ""


def _generate_environment(*, width: int, height: int, density: float, seed: int) -> Tuple[GridConfig, GridEnvironment]:
    cfg = GridConfig(width=int(width), height=int(height), start=(0, 0), goal=None)
    env = GridEnvironment(cfg)

    total_cells = env.width * env.height
    obstacle_count = int(total_cells * float(density))
    env.add_random_obstacles(count=obstacle_count, seed=int(seed))
    return cfg, env


def _generate_environment_with_positions(
    *,
    grid_size: int,
    density: float,
    seed: int,
    start: Tuple[int, int],
    goal: Tuple[int, int],
) -> Tuple[GridConfig, GridEnvironment]:
    size = int(grid_size)
    sx = _clamp_int(start[0], 0, size - 1)
    sy = _clamp_int(start[1], 0, size - 1)
    gx = _clamp_int(goal[0], 0, size - 1)
    gy = _clamp_int(goal[1], 0, size - 1)

    # Ensure start != goal (keep it non-technical and predictable).
    if (sx, sy) == (gx, gy):
        gx = min(size - 1, gx + 1)

    cfg = GridConfig(width=size, height=size, start=(sx, sy), goal=(gx, gy))
    env = GridEnvironment(cfg)

    total_cells = env.width * env.height
    obstacle_count = int(total_cells * float(density))
    env.add_random_obstacles(count=obstacle_count, seed=int(seed), avoid=[cfg.start, cfg.goal])
    return cfg, env


def _run_navigation(env: GridEnvironment) -> AStarResult:
    return astar_shortest_path(env)


def _render_environment_map(*, env: Optional[GridEnvironment]) -> None:
    if env is None:
        st.info("Click **Generate Environment** to create a map.")
        return

    fig = plot_grid(
        env,
        path=None,
        title="Environment Map",
        show_grid_lines=True,
        show_legend=True,
    )
    st.pyplot(fig, clear_figure=True, use_container_width=True)
    plt.close(fig)


def _render_navigation_result(*, env: Optional[GridEnvironment], result: Optional[AStarResult]) -> None:
    if env is None:
        st.info("Generate an environment to see results.")
        return
    if result is None:
        st.info("Run navigation to see the path.")
        return

    fig = plot_grid(
        env,
        path=result.path,
        title="Navigation Result",
        show_grid_lines=True,
        show_legend=True,
    )
    st.pyplot(fig, clear_figure=True, use_container_width=True)
    plt.close(fig)


def _animate_path(*, env: GridEnvironment, result: AStarResult, delay_ms: int = 60) -> None:
    """
    Step-by-step animation using Streamlit updates.
    Keeps it simple: re-render the same figure with a moving agent marker.
    """
    if not result.path:
        st.warning("No path to animate.")
        return

    delay_s = max(0, int(delay_ms)) / 1000.0
    frame = st.empty()

    for i, agent_pos in enumerate(result.path):
        fig = plot_grid(
            env,
            path=result.path,
            agent_position=agent_pos,
            title="Simulation Running...",
            show_grid_lines=True,
            show_legend=True,
        )
        frame.pyplot(fig, clear_figure=True, use_container_width=True)
        plt.close(fig)
        time.sleep(delay_s)


def main() -> None:
    st.set_page_config(page_title="AI-Based Autonomous Navigation System", layout="wide")
    # Minimal styling: spacing + larger plot area feel.
    st.markdown(
        """
        <style>
          .block-container { padding-top: 1.1rem; padding-bottom: 1.4rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- Sidebar (ALL controls live here) ---
    st.sidebar.header("Controls")
    grid_size = st.sidebar.slider("Grid size", min_value=8, max_value=60, value=int(st.session_state.get("grid_size", 20)), step=1)
    density = st.sidebar.slider("Obstacle density", min_value=0.0, max_value=0.45, value=float(st.session_state.get("density", 0.15)), step=0.01)

    st.sidebar.subheader("Start")
    start_x = st.sidebar.number_input("Start X", min_value=0, max_value=int(grid_size) - 1, value=int(st.session_state.get("start_x", 0)), step=1)
    start_y = st.sidebar.number_input("Start Y", min_value=0, max_value=int(grid_size) - 1, value=int(st.session_state.get("start_y", 0)), step=1)

    st.sidebar.subheader("Goal")
    goal_x = st.sidebar.number_input("Goal X", min_value=0, max_value=int(grid_size) - 1, value=int(st.session_state.get("goal_x", int(grid_size) - 1)), step=1)
    goal_y = st.sidebar.number_input("Goal Y", min_value=0, max_value=int(grid_size) - 1, value=int(st.session_state.get("goal_y", int(grid_size) - 1)), step=1)

    seed = st.sidebar.number_input("Seed", min_value=0, max_value=999999, value=int(st.session_state.get("seed", 7)), step=1)
    speed_ms = st.sidebar.slider("Simulation speed", min_value=10, max_value=250, value=int(st.session_state.get("speed_ms", 60)), step=10)

    st.sidebar.divider()
    generate = st.sidebar.button("Generate Environment", use_container_width=True)
    run = st.sidebar.button("Run Navigation", use_container_width=True, type="primary")
    simulate = st.sidebar.button("Start Simulation", use_container_width=True)

    # Persist sidebar inputs
    st.session_state.grid_size = int(grid_size)
    st.session_state.density = float(density)
    st.session_state.start_x = int(start_x)
    st.session_state.start_y = int(start_y)
    st.session_state.goal_x = int(goal_x)
    st.session_state.goal_y = int(goal_y)
    st.session_state.seed = int(seed)
    st.session_state.speed_ms = int(speed_ms)

    _init_state(grid_size=int(grid_size))

    # --- Main screen (ONLY title, description, graph, status) ---
    st.title("AI-Based Autonomous Navigation System")
    st.write("Create a grid map, find a route, and watch the agent move to the goal in real time.")
    st.divider()

    # Actions (driven by sidebar buttons)
    if generate:
        cfg, env = _generate_environment_with_positions(
            grid_size=int(grid_size),
            density=float(density),
            seed=int(seed),
            start=(int(start_x), int(start_y)),
            goal=(int(goal_x), int(goal_y)),
        )
        st.session_state.config = cfg
        st.session_state.env = env
        st.session_state.result = None
        st.session_state.status = "Environment Generated"

    if run:
        env = st.session_state.env
        if env is None:
            st.session_state.status = "Environment Generated" if st.session_state.env is not None else "Environment not generated yet."
        else:
            res = _run_navigation(env)
            st.session_state.result = res
            st.session_state.status = "Path Found" if bool(res.path) else "No Path Found"

    # Status (simple language)
    status = st.session_state.get("status", "")
    if status == "Environment Generated":
        st.success("Environment Generated")
    elif status == "Path Found":
        st.success("Path Found")
    elif status == "No Path Found":
        st.error("No Path Found")
    elif status == "Simulation Running":
        st.info("Simulation Running")
    elif status:
        st.info(status)
    else:
        st.info("Ready.")

    # Big, centered graph area
    plot_area = st.container()
    with plot_area:
        env = st.session_state.env
        res = st.session_state.result

        placeholder = st.empty()

        # Animation takes over this placeholder when requested.
        if simulate:
            if env is None:
                st.session_state.status = "Environment not generated yet."
            elif res is None:
                st.session_state.status = "Please run navigation first."
            elif not res.path:
                st.session_state.status = "No Path Found"
            else:
                st.session_state.status = "Simulation Running"
                for i, pos in enumerate(res.path):
                    fig = plot_grid(
                        env,
                        path=res.path,
                        agent_position=pos,
                        agent_color="gold",
                        title="Simulation Running",
                        show_grid_lines=True,
                        show_legend=True,
                        cell_size=0.9,
                    )
                    placeholder.pyplot(fig, clear_figure=True, use_container_width=True)
                    plt.close(fig)
                    time.sleep(max(0, int(speed_ms)) / 1000.0)
                st.session_state.status = "Path Found"
        else:
            # Static view: show env + (optional) path.
            if env is None:
                st.info("Use the sidebar to generate an environment.")
            else:
                fig = plot_grid(
                    env,
                    path=(res.path if res is not None else None),
                    agent_position=None,
                    title=("Navigation Result" if res is not None else "Environment Map"),
                    show_grid_lines=True,
                    show_legend=True,
                    cell_size=0.9,
                )
                placeholder.pyplot(fig, clear_figure=True, use_container_width=True)
                plt.close(fig)


if __name__ == "__main__":
    main()

