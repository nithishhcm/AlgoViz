"""
algorithms/graph.py — Graph algorithm implementations.
BFS, DFS, Dijkstra's, Kruskal's, Prim's.
"""

import heapq
from collections import deque


def bfs(graph, start):
    """
    Breadth-First Search — O(V + E) time, O(V) space.
    Explores all neighbours at current depth before going deeper.
    Returns list of visited nodes in order.
    """
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in sorted(graph.get(node, [])):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return order


def dfs(graph, start, visited=None, order=None):
    """
    Depth-First Search — O(V + E) time, O(V) space.
    Explores as far as possible along each branch before backtracking.
    Returns list of visited nodes in order.
    """
    if visited is None:
        visited = set()
    if order is None:
        order = []
    visited.add(start)
    order.append(start)
    for neighbour in sorted(graph.get(start, [])):
        if neighbour not in visited:
            dfs(graph, neighbour, visited, order)
    return order


def dijkstra(graph, start):
    """
    Dijkstra's Shortest Path — O((V + E) log V) time, O(V) space.
    graph: dict of {node: [(neighbour, weight), ...]}
    Returns dict of shortest distances from start.
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        dist, node = heapq.heappop(heap)
        if dist > distances[node]:
            continue
        for neighbour, weight in graph.get(node, []):
            new_dist = dist + weight
            if new_dist < distances[neighbour]:
                distances[neighbour] = new_dist
                heapq.heappush(heap, (new_dist, neighbour))

    return distances


def kruskal(nodes, edges):
    """
    Kruskal's MST — O(E log E) time, O(V) space.
    edges: list of (weight, u, v)
    Returns list of edges in MST.
    """
    parent = {n: n for n in nodes}
    rank = {n: 0 for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return True

    mst = []
    for weight, u, v in sorted(edges):
        if union(u, v):
            mst.append((weight, u, v))
    return mst


def prim(graph, start):
    """
    Prim's MST — O((V + E) log V) time, O(V) space.
    graph: dict of {node: [(neighbour, weight), ...]}
    Returns list of edges in MST.
    """
    in_mst = set([start])
    edges = [(weight, start, neighbour)
             for neighbour, weight in graph.get(start, [])]
    heapq.heapify(edges)
    mst = []

    while edges:
        weight, u, v = heapq.heappop(edges)
        if v in in_mst:
            continue
        in_mst.add(v)
        mst.append((weight, u, v))
        for neighbour, w in graph.get(v, []):
            if neighbour not in in_mst:
                heapq.heappush(edges, (w, v, neighbour))

    return mst


if __name__ == "__main__":
    # Example undirected graph
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E'],
    }
    print("BFS from A:", bfs(graph, 'A'))
    print("DFS from A:", dfs(graph, 'A'))

    # Weighted graph for Dijkstra
    weighted = {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', 1), ('D', 5)],
        'C': [('B', 1), ('D', 8), ('E', 10)],
        'D': [('E', 2)],
        'E': [],
    }
    print("Dijkstra from A:", dijkstra(weighted, 'A'))
