from collections import deque
from queue import PriorityQueue
import math


# ---------------- BFS ----------------
def bfs(graph, start, target):
    visited = set()
    queue = deque([start])
    path_nodes = []

    while queue:
        node = queue.popleft()
        path_nodes.append(node)

        if node == target:
            return True, path_nodes

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)

    return False, path_nodes


# ---------------- DFS ----------------
def dfs(graph, start, target):
    visited = set()
    stack = [start]
    path_nodes = []

    while stack:
        node = stack.pop()
        path_nodes.append(node)

        if node == target:
            return True, path_nodes

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    stack.append(neighbor)

    return False, path_nodes


# ---------------- UCS ----------------
def ucs(graph, start, target):
    visited = set()
    priority_queue = PriorityQueue()
    priority_queue.put((0, start, []))

    while not priority_queue.empty():
        cost, node, path = priority_queue.get()
        path = path + [node]

        if node == target:
            return True, path, cost

        if node not in visited:
            visited.add(node)
            for neighbor, edge_cost in graph.get(node, []):
                if neighbor not in visited:
                    priority_queue.put((cost + edge_cost, neighbor, path))

    return False, [], 0

def heuristic(n1, n2):
        (x1, y1) = Positions[n1]
        (x2, y2) = Positions[n2]
        return math.hypot(x2 - x1, y2 - y1)


# ---------------- A* Search ----------------
def a_star(graph, start, target, heuristic):
    visited = set()
    priority_queue = PriorityQueue()
    priority_queue.put((0, start, 0, []))  


    while not priority_queue.empty():
        f, node, g, path = priority_queue.get()
        path = path + [node]

        if node == target:
            return True, path, g

        if node not in visited:
            visited.add(node)
            for neighbor, edge_cost in graph.get(node, []):
                if neighbor not in visited:
                    h = heuristic(neighbor, target)
                    priority_queue.put((g + edge_cost + h, neighbor, g + edge_cost, path))

    return False, []


# ---------------- MAIN ----------------
if __name__ == "__main__":
    # Graph for BFS & DFS (unweighted)
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    # Graph for UCS (weighted)
    graph_weighted = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 10), ('D', 2), ('E', 5)],
        'C': [('A', 4), ('F', 3)],
        'D': [('B', 2)],
        'E': [('B', 5), ('F', 1)],
        'F': [('C', 3), ('E', 1)]
    }

    Positions = {
        'A': (0, 0),
        'B': (2, 0),
        'C': (0, 3),
        'D': (2, 1),
        'E': (1, 3),
        'F': (3, 2)
    }


    S = 'A'
    G = 'F'

    # BFS: Terry always checks all nearby pipes before moving deeper.
    found, path = bfs(graph, S, G)
    print("\nTerry always checks all nearby pipes before moving deeper")
    print(f" Path from {S} to {G}: {'Found' if found else 'Not Found'}")
    print("Path followed:", " -> ".join(path) if found else "No path followed")

    # DFS: Terry always tries to go deeper into unexplored pipes before checking others.
    found, path = dfs(graph, S, G)
    print("\nTerry always tries to go deeper into unexplored pipes before checking others")
    print(f" Path from {S} to {G}: {'Found' if found else 'Not Found'}")
    print("Path followed:", " -> ".join(path) if found else "No path followed")

    # UCS: Path with the lowest total travel cost.
    found, path, cost = ucs(graph_weighted, S, G)
    print("\nPath with the lowest total travel cost")
    print(f" Path from {S} to {G}: {'Found' if found else 'Not Found'}")
    print("Path followed:", " -> ".join(path) if found else "No path followed")
    print(f"Total cost: {cost}")

    # A*: Straight-line distance from each junction to the cheese as a guide.
    found, path, cost = a_star(graph_weighted, S, G, heuristic)
    print("\nStraight-line distance from each junction to the cheese as a guide")
    print(f"\n Path from {S} to {G}: {'Found' if found else 'Not Found'}")
    print("Path followed:", " -> ".join(path) if found else "No path followed")
    print(f"Total cost: {cost}")