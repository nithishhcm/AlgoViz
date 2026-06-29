![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black)
![HTML5/Canvas](https://img.shields.io/badge/HTML5-Canvas-orange)
![Algorithms](https://img.shields.io/badge/Algorithms-Data_Structures-green)
![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)
# 📊 AlgoViz: Interactive Algorithm & Data Structure Sandbox

An immersive, full-stack visualization and safe code execution engine built using **Python Flask**, **HTML5 Canvas/JavaScript**, and an isolated sandboxed processing container. 

**AlgoViz** bridges the gap between theoretical algorithmic complexity and concrete execution. It serves a responsive web dashboard packed with comprehensive algorithmic tracking (Sorting, Searching, Graphs, and Trees), an interactive canvas playground where users can dynamically append vertices or edges to live graphs, a built-in multiple-choice quiz engine to test structural comprehension, and an integrated terminal sandbox for executing custom Python logic in real-time.

---

## 🚀 Key Features

### 💻 1. Isolated Python Code Sandbox
* **Real-Time API Transpiler Pipeline:** Features a `/api/run-code` endpoint backed by isolated execution wrappers (`sandbox.py`) to run custom algorithm modifications safely.
* **Smart Performance Enforcement:** Integrates automated runtime timeout caps (ranging from 5s up to a hard 10s ceiling) to actively intercept infinite loops and secure local resource thresholds.
* **Pre-Loaded Structural Boilerplates:** Instantly pulls syntax-highlighted code implementations for complex graph metrics and tree traversals straight into the editor panel.

### 🗺️ 2. Dynamic Data Graph & Node Manipulation
* **Interactive Topology Generation:** Modify graph payloads directly inside your browser window. You can explicitly click to create new vertices or drag connections to link custom edges with personalized edge weights on the fly.
* **Visual Execution Path Tracer:** Watch algorithms step forward frame-by-frame. The interface highlights active queues for Breadth-First Search (BFS), backtracks along Depth-First Search (DFS) stack layers, and changes edge states dynamically to mirror Dijkstra’s, Prim’s, or Kruskal’s logic.

### 🧠 3. Interactive Assessment Learning Center
* **Toggled Quiz Suite:** Features a built-in, modular quiz platform designed to test data structure and complexity concepts.
* **Instant Evaluation Engine:** Provides immediate validation feedback on algorithmic behavior, big-O metrics, and state transitions, helping students analyze operational bottlenecks directly from the web panel.



* <img width="1917" height="1025" alt="image" src="https://github.com/user-attachments/assets/28e50189-fb15-428d-bd6d-a9ee1c56831d" /> <img width="1906" height="977" alt="image" src="https://github.com/user-attachments/assets/9af167ce-6ea2-40da-a7f5-398504543d10" /><img width="1918" height="963" alt="image" src="https://github.com/user-attachments/assets/c6b69711-556d-437d-97b5-d642a419c087" />




---

## 🏗️ Project Architecture & Component Blueprint

The application uses an decoupled architectural design, separating metadata configurations and execution modules from client-side interface files:

```text




AlgoViz/
│
├── app.py                      # Primary Flask App Controller & Core API Routing
├── sandbox.py                  # Sandboxed Isolated Code Execution Controller
├── requirements.txt            # System Library Dependencies Manifest
├── README.md                   # Repository Documentation Homepage
│
└── static/                     # Frontend Static Web Layouts
    ├── index.html              # Core Visualization Interface
    ├── css/
    │   └── styles.css          # Dark-Themed Dashboard Token Sheet
    └── js/
        ├── main.js             # API Integration, Engine Toggles & App Logic
        ├── canvas.js           # Nodes, Edges, and Tree Graph Animation Engine

        └── quiz.js             # Data Assessment & Conceptual Quiz Tracker
