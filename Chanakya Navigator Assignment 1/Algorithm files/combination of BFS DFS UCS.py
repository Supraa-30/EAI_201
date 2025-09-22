from collections import deque
from queue import PriorityQueue


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
    priority_queue.put((0, start))   # (cost, node)
    path_nodes = []

    while not priority_queue.empty():
        cost, node = priority_queue.get()
        path_nodes.append(node)

        if node == target:
            return True, path_nodes

        if node not in visited:
            visited.add(node)
            for neighbor, edge_cost in graph.get(node, []):
                if neighbor not in visited:
                    priority_queue.put((cost + edge_cost, neighbor))

    return False, path_nodes


# ---------------- MAIN ----------------
if __name__ == "__main__":
    # Graph for BFS & DFS (unweighted)
    graph_unweighted = {
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

    start_node = 'A'
    target_node = 'F'

    # Run BFS
    found, path = bfs(graph_unweighted, start_node, target_node)
    print(f"\nBFS: Path from {start_node} to {target_node}: {'Found' if found else 'Not Found'}")
    print("Path followed:", " -> ".join(path) if found else "No path followed")

    # Run DFS
    found, path = dfs(graph_unweighted, start_node, target_node)
    print(f"\nDFS: Path from {start_node} to {target_node}: {'Found' if found else 'Not Found'}")
    print("Path followed:", " -> ".join(path) if found else "No path followed")

    # Run UCS
    found, path = ucs(graph_weighted, start_node, target_node)
    print(f"\nUCS: Path from {start_node} to {target_node}: {'Found' if found else 'Not Found'}")
    print("Path followed:", " -> ".join(path) if found else "No path followed")
