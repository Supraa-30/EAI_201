from queue import PriorityQueue

def ucs(graph, start, target):
    """Uniform Cost Search algorithm implementation."""
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


if __name__ == "__main__":
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 10), ('D', 2), ('E', 5)],
        'C': [('A', 4), ('F', 3)],
        'D': [('B', 2)],
        'E': [('B', 5), ('F', 1)],
        'F': [('C', 3), ('E', 1)]
    }

    start_node = 'A'
    target_node = 'F'
    found, path = ucs(graph, start_node, target_node)
    print(f"Path from {start_node} to {target_node}: {'Found' if found else 'Not Found'}")
    print("Path followed:", " -> ".join(path) if found else "No path followed")
