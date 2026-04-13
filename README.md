# AI-Based Autonomous Navigation System 🤖🧭

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Status](https://img.shields.io/badge/Status-Active-success)
![Simulation](https://img.shields.io/badge/Hardware-Not%20Required-lightgrey)

A simulation-based AI project that shows how an autonomous agent can navigate from a **start** point to a **goal** while avoiding **obstacles**.
It’s built to be easy to demo, easy to explain, and strong enough to include in a portfolio.

---

## Project Overview ✨

This project creates a simple grid “world”, places obstacles, and then uses **A\*** path planning (with **Manhattan distance**) to find the shortest route to the goal.
You can run everything in a clean Streamlit dashboard that visualizes the environment, the planned path, and a live step-by-step animation of the agent moving.

---

## Problem Statement 🎯

Autonomous navigation is hard to understand when it’s hidden inside code.
Recruiters and non-technical viewers also need something they can **see** and **interact with**.

This project focuses on a clear, visual explanation of navigation:
“Here is the map. Here are the obstacles. Here is the path. Here is the agent moving.”

---

## Solution ✅

This system:

- Builds a **grid-based environment**
- Adds **manual + random obstacles**
- Runs **A\*** to compute the **shortest path**
- Visualizes the result in a **matplotlib graph**
- Provides a **Streamlit dashboard** with a **live simulation animation**

---

## Industry Relevance 🌍

The same core ideas behind this project show up in:

- **Warehouse robots** navigating aisles
- **Self-driving systems** planning safe routes (at a much larger scale)
- **Drones** planning paths in mapped spaces
- **Game AI** (NPC navigation, pathfinding on maps)
- **Delivery robots** moving through indoor environments

---

## Tech Stack 🧰

| Category      | Tool/Library | Why it’s used                            |
| ------------- | ------------ | ---------------------------------------- |
| Language      | Python       | Simple, readable, fast to iterate        |
| Dashboard     | Streamlit    | Clean UI for demos and portfolio         |
| Planning      | A\* (custom) | Shortest path on a grid                  |
| Math / Arrays | NumPy        | 2D grid storage and operations           |
| Visualization | Matplotlib   | Clear graph rendering + animation frames |

---

## Folder Structure (project layout) 📁

Below is a **clean high-level view** (easy to understand at a glance):

```text
AI-Autonomous-Navigation-System/
│
├── src/                         # Main source code (importable package)
│   └── ai_autonomous_navigation_system/
│       ├── environments/
│       │   └── grid.py          # Grid environment (2D array + obstacles + start/goal)
│       ├── navigation/
│       │   └── a_star.py        # A* shortest path planner (Manhattan distance)
│       ├── visualization/
│       │   └── grid_plot.py     # Matplotlib grid + path + agent animation marker
│       └── utils/               # Small helpers (paths, etc.)
│
├── dashboard/
│   └── app.py                   # Streamlit dashboard (controls + visualization + animation)
│
├── outputs/                     # Saved images/results from runs
├── assets/                      # Images for README/screenshots
├── main.py                      # Simple demo runner (prints + saves a plot)
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

> Note: If you want a `data/` folder for datasets later, you can add it anytime. This project doesn’t require one right now.

---

## How It Works (workflow) 🔁

1. **Generate Environment**
   - Choose grid size and obstacle density
   - Set start and goal coordinates
   - Create a random obstacle map (start/goal are kept clear)
2. **Run Navigation**
   - A\* explores the grid and avoids obstacles
   - The shortest path is returned (if one exists)
3. **Visualize**
   - Obstacles, start, goal, and path are displayed on a clean map
4. **Start Simulation**
   - The agent moves along the planned path
   - The dashboard updates frame-by-frame so the motion is easy to follow

---

## Features ⭐

- **Configurable grid** (size, start/goal positions)
- **Obstacle placement** (random + manual support in the environment module)
- **A\* shortest path planning** (Manhattan distance heuristic)
- **Obstacle avoidance**
- **Streamlit dashboard** (professional layout, simple controls)
- **Live animation** of the agent moving step-by-step

---

## Installation Steps (Windows) 🪟

From the project root:

```powershell
cd "d:\AI-Autonomous-Navigation-System"
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## How to Run ▶️

### Option A: Run the simple demo script

This runs a test case and saves an output image in `outputs/`.

```powershell
python main.py
```

### Option B: Run the Streamlit dashboard (recommended)

```powershell
streamlit run dashboard\app.py
```

---

## Output / Results 🧾

When you run the dashboard, you’ll see:

- A **large grid map** with obstacles (black), start (green), goal (red)
- A **blue path** when navigation succeeds
- A **live simulation** where the agent moves step-by-step (highlighted during animation)
- Simple status messages like:
  - **Environment Generated**
  - **Path Found**
  - **No Path Found**
  - **Simulation Running**

---

## Screenshots 🖼️

Add your screenshots to `assets/images/` and link them here:

- Environment Map (placeholder)
  - `assets/images/environment_map.png`
- Navigation Result (placeholder)
  - `assets/images/navigation_result.png`
- Live Simulation (placeholder)
  - `assets/images/live_simulation.gif`

---

## Demo Video 🎥


[![Watch Demo](https://img.youtube.com/vi/y_jPy78wlos/0.jpg)](https://youtu.be/y_jPy78wlos)

👉 Click the image to watch the full demo
---

## Key Learnings 📚

- How A\* uses a heuristic to efficiently search for a shortest path
- How to model environments as **2D grids**
- How to turn algorithms into something **visual and explainable**
- How to build a clean demo UI with Streamlit for portfolio projects

---

## Future Improvements 🚀

- Add diagonal movement and weighted costs
- Add multiple environment types (maze maps, narrow corridors, random rooms)
- Add additional planners (Dijkstra, BFS, RRT)
- Add metrics (time to plan, nodes explored, path length charts)
- Add export tools (save run configs + results in `outputs/`)

---

## Author 👤

Built by **[Your Name Here]**

- GitHub: `https://github.com/Sonia068`
- LinkedIn: `https://www.linkedin.com/in/sonia-thakur-6ab93b349/`

---

## License 📄

MIT License (recommended for portfolio projects).  
If you plan to publish publicly, add a `LICENSE` file at the repository root.
