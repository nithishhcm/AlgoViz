"""
app.py — AlgoViz Flask application.
Serves the frontend and provides REST API for code execution and algorithm metadata.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from sandbox import run_code

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# ─── Algorithm Metadata ───────────────────────────────────────────────────────

ALGORITHMS = [
    # Sorting
    {
        "id": "bubble_sort",
        "name": "Bubble Sort",
        "category": "sorting",
        "time_best": "O(n)",
        "time_avg": "O(n²)",
        "time_worst": "O(n²)",
        "space": "O(1)",
        "stable": True,
        "description": "Repeatedly compares adjacent elements and swaps them if they are in the wrong order. Smaller elements 'bubble' to the top.",
    },
    {
        "id": "selection_sort",
        "name": "Selection Sort",
        "category": "sorting",
        "time_best": "O(n²)",
        "time_avg": "O(n²)",
        "time_worst": "O(n²)",
        "space": "O(1)",
        "stable": False,
        "description": "Finds the minimum element from the unsorted portion and places it at the beginning. Repeats until sorted.",
    },
    {
        "id": "insertion_sort",
        "name": "Insertion Sort",
        "category": "sorting",
        "time_best": "O(n)",
        "time_avg": "O(n²)",
        "time_worst": "O(n²)",
        "space": "O(1)",
        "stable": True,
        "description": "Builds the sorted array one element at a time by inserting each element into its correct position.",
    },
    {
        "id": "merge_sort",
        "name": "Merge Sort",
        "category": "sorting",
        "time_best": "O(n log n)",
        "time_avg": "O(n log n)",
        "time_worst": "O(n log n)",
        "space": "O(n)",
        "stable": True,
        "description": "Divide-and-conquer algorithm that splits the array in half, recursively sorts each half, then merges them.",
    },
    {
        "id": "quick_sort",
        "name": "Quick Sort",
        "category": "sorting",
        "time_best": "O(n log n)",
        "time_avg": "O(n log n)",
        "time_worst": "O(n²)",
        "space": "O(log n)",
        "stable": False,
        "description": "Picks a pivot element and partitions the array around it. Recursively sorts the sub-arrays.",
    },
    {
        "id": "heap_sort",
        "name": "Heap Sort",
        "category": "sorting",
        "time_best": "O(n log n)",
        "time_avg": "O(n log n)",
        "time_worst": "O(n log n)",
        "space": "O(1)",
        "stable": False,
        "description": "Builds a max-heap from the array, then repeatedly extracts the maximum to build the sorted array.",
    },
    # Searching
    {
        "id": "linear_search",
        "name": "Linear Search",
        "category": "searching",
        "time_best": "O(1)",
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(1)",
        "stable": True,
        "description": "Sequentially checks every element until the target is found or the list ends.",
    },
    {
        "id": "binary_search",
        "name": "Binary Search",
        "category": "searching",
        "time_best": "O(1)",
        "time_avg": "O(log n)",
        "time_worst": "O(log n)",
        "space": "O(1)",
        "stable": True,
        "description": "Requires sorted array. Repeatedly halves the search space by comparing the target to the middle element.",
    },
    # Graph
    {
        "id": "bfs",
        "name": "Breadth-First Search",
        "category": "graph",
        "time_best": "O(V + E)",
        "time_avg": "O(V + E)",
        "time_worst": "O(V + E)",
        "space": "O(V)",
        "stable": True,
        "description": "Explores all neighbours at the current depth before moving deeper. Uses a queue. Finds shortest path in unweighted graphs.",
    },
    {
        "id": "dfs",
        "name": "Depth-First Search",
        "category": "graph",
        "time_best": "O(V + E)",
        "time_avg": "O(V + E)",
        "time_worst": "O(V + E)",
        "space": "O(V)",
        "stable": True,
        "description": "Explores as far as possible along each branch before backtracking. Uses a stack (or recursion).",
    },
    {
        "id": "dijkstra",
        "name": "Dijkstra's Algorithm",
        "category": "graph",
        "time_best": "O((V + E) log V)",
        "time_avg": "O((V + E) log V)",
        "time_worst": "O((V + E) log V)",
        "space": "O(V)",
        "stable": True,
        "description": "Finds shortest paths from a source node to all others in a weighted graph with non-negative edges. Uses a min-heap.",
    },
    {
        "id": "kruskal",
        "name": "Kruskal's Algorithm",
        "category": "graph",
        "time_best": "O(E log E)",
        "time_avg": "O(E log E)",
        "time_worst": "O(E log E)",
        "space": "O(V)",
        "stable": True,
        "description": "Finds the Minimum Spanning Tree by greedily adding the cheapest edge that doesn't form a cycle. Uses Union-Find.",
    },
    {
        "id": "prim",
        "name": "Prim's Algorithm",
        "category": "graph",
        "time_best": "O((V + E) log V)",
        "time_avg": "O((V + E) log V)",
        "time_worst": "O((V + E) log V)",
        "space": "O(V)",
        "stable": True,
        "description": "Finds the Minimum Spanning Tree by growing it one edge at a time, always choosing the cheapest edge to an unvisited node.",
    },
    # Trees
    {
        "id": "inorder",
        "name": "Inorder Traversal",
        "category": "tree",
        "time_best": "O(n)",
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(h)",
        "stable": True,
        "description": "Visits nodes in Left → Root → Right order. For a BST, this visits nodes in sorted ascending order.",
    },
    {
        "id": "preorder",
        "name": "Preorder Traversal",
        "category": "tree",
        "time_best": "O(n)",
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(h)",
        "stable": True,
        "description": "Visits nodes in Root → Left → Right order. Useful for copying or serialising a tree.",
    },
    {
        "id": "postorder",
        "name": "Postorder Traversal",
        "category": "tree",
        "time_best": "O(n)",
        "time_avg": "O(n)",
        "time_worst": "O(n)",
        "space": "O(h)",
        "stable": True,
        "description": "Visits nodes in Left → Right → Root order. Useful for deleting a tree or evaluating expression trees.",
    },
]

# Python code templates for each algorithm (shown in sandbox)
CODE_TEMPLATES = {
    "bubble_sort": """\
def bubble_sort(arr):
    n = len(arr)
    arr = arr[:]
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

arr = [64, 34, 25, 12, 22, 11, 90]
print("Sorted:", bubble_sort(arr))
""",
    "selection_sort": """\
def selection_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

arr = [64, 25, 12, 22, 11]
print("Sorted:", selection_sort(arr))
""",
    "insertion_sort": """\
def insertion_sort(arr):
    arr = arr[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

arr = [12, 11, 13, 5, 6]
print("Sorted:", insertion_sort(arr))
""",
    "merge_sort": """\
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

arr = [38, 27, 43, 3, 9, 82, 10]
print("Sorted:", merge_sort(arr))
""",
    "quick_sort": """\
def quick_sort(arr, low=0, high=None):
    if high is None:
        arr = arr[:]
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

arr = [10, 7, 8, 9, 1, 5]
print("Sorted:", quick_sort(arr))
""",
    "heap_sort": """\
def heapify(arr, n, i):
    largest, l, r = i, 2*i+1, 2*i+2
    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr

arr = [12, 11, 13, 5, 6, 7]
print("Sorted:", heap_sort(arr))
""",
    "linear_search": """\
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

arr = [10, 20, 30, 40, 50]
target = 30
idx = linear_search(arr, target)
print(f"Found {target} at index: {idx}")
""",
    "binary_search": """\
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23
idx = binary_search(arr, target)
print(f"Found {target} at index: {idx}")
""",
    "bfs": """\
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return order

graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 5],
    3: [1],
    4: [1, 5],
    5: [2, 4],
}
print("BFS order:", bfs(graph, 0))
""",
    "dfs": """\
def dfs(graph, start, visited=None, order=None):
    if visited is None:
        visited, order = set(), []
    visited.add(start)
    order.append(start)
    for neighbour in graph.get(start, []):
        if neighbour not in visited:
            dfs(graph, neighbour, visited, order)
    return order

graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 5],
    3: [1],
    4: [1, 5],
    5: [2, 4],
}
print("DFS order:", dfs(graph, 0))
""",
    "dijkstra": """\
import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue
        for v, w in graph.get(u, []):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist

graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 1), ('D', 5)],
    'C': [('B', 1), ('D', 8), ('E', 10)],
    'D': [('E', 2)],
    'E': [],
}
print("Distances from A:", dijkstra(graph, 'A'))
""",
    "kruskal": """\
def kruskal(nodes, edges):
    parent = {n: n for n in nodes}
    rank = {n: 0 for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry: return False
        if rank[rx] < rank[ry]: rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]: rank[rx] += 1
        return True

    mst = []
    for weight, u, v in sorted(edges):
        if union(u, v):
            mst.append((weight, u, v))
    return mst

nodes = ['A', 'B', 'C', 'D', 'E']
edges = [(2,'A','B'),(3,'A','C'),(1,'B','C'),(4,'B','D'),(5,'C','D'),(6,'D','E')]
print("MST edges:", kruskal(nodes, edges))
""",
    "prim": """\
import heapq

def prim(graph, start):
    in_mst = set([start])
    edges = [(w, start, v) for v, w in graph.get(start, [])]
    heapq.heapify(edges)
    mst = []
    while edges:
        w, u, v = heapq.heappop(edges)
        if v in in_mst: continue
        in_mst.add(v)
        mst.append((w, u, v))
        for nb, nw in graph.get(v, []):
            if nb not in in_mst:
                heapq.heappush(edges, (nw, v, nb))
    return mst

graph = {
    'A': [('B', 2), ('C', 3)],
    'B': [('A', 2), ('C', 1), ('D', 4)],
    'C': [('A', 3), ('B', 1), ('D', 5)],
    'D': [('B', 4), ('C', 5), ('E', 6)],
    'E': [('D', 6)],
}
print("MST:", prim(graph, 'A'))
""",
    "inorder": """\
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None

def insert(root, val):
    if not root: return TreeNode(val)
    if val < root.val: root.left = insert(root.left, val)
    else: root.right = insert(root.right, val)
    return root

def inorder(root, result=None):
    if result is None: result = []
    if root:
        inorder(root.left, result)
        result.append(root.val)
        inorder(root.right, result)
    return result

root = None
for v in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, v)

print("Inorder (sorted):", inorder(root))
""",
    "preorder": """\
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None

def insert(root, val):
    if not root: return TreeNode(val)
    if val < root.val: root.left = insert(root.left, val)
    else: root.right = insert(root.right, val)
    return root

def preorder(root, result=None):
    if result is None: result = []
    if root:
        result.append(root.val)
        preorder(root.left, result)
        preorder(root.right, result)
    return result

root = None
for v in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, v)

print("Preorder:", preorder(root))
""",
    "postorder": """\
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None

def insert(root, val):
    if not root: return TreeNode(val)
    if val < root.val: root.left = insert(root.left, val)
    else: root.right = insert(root.right, val)
    return root

def postorder(root, result=None):
    if result is None: result = []
    if root:
        postorder(root.left, result)
        postorder(root.right, result)
        result.append(root.val)
    return result

root = None
for v in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, v)

print("Postorder:", postorder(root))
""",
}


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/algorithms")
def get_algorithms():
    return jsonify(ALGORITHMS)


@app.route("/api/algorithms/<algo_id>/code")
def get_code(algo_id):
    code = CODE_TEMPLATES.get(algo_id, "# No template available for this algorithm.\nprint('Hello, AlgoViz!')")
    return jsonify({"code": code})


@app.route("/api/run-code", methods=["POST"])
def run_code_route():
    data = request.get_json(force=True)
    code = data.get("code", "")
    timeout = min(int(data.get("timeout", 5)), 10)  # cap at 10s

    if not code.strip():
        return jsonify({"stdout": "", "stderr": "No code provided.", "exit_code": 1})

    result = run_code(code, timeout=timeout)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
