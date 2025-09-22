from collections import deque

def dfs(graph, start, goal):
    """Depth-First Search algorithm implementation."""
    visited = set()
    stack = [start]
    path_nodes = []

    while stack:
        node = stack.pop()
        path_nodes.append(node)

        if node == goal:
            return True, path_nodes

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    stack.append(neighbor)

    return False, path_nodes


if __name__ == "__main__":
     campus_graph = {
    "Main Entrance": ["Admin Block A", "Academic Block A"],
    "Admin Block A": ["Main Entrance","Library","Auditorium","Academic Block A"],
    "Academic Block A": ["Main Entrance","Cafeteria","Auditorium","Admin Block A"],
    "Library": ["Admin Block A", "Academic Block A","Cafeteria","Auditorium","Academic Block C", "Academic Block B"],
    "Cafeteria": ["Academic Block A","Admin Block A", "Library","Auditorium","Academic Block C", "Academic Block B"],
    "Academic Block C": ["Library","Cafeteria","Food Court","Academic Block B"],
    "Academic Block B": ["Library","Cafeteria","Food Court","Academic Block C"],
    "Food Court": ["Academic Block C", "Academic Block B","Cricket Ground", "Gym", "Hostel"],
    "Hostel": ["Mini Mart"],
    "Mini Mart": ["Hostel"],
    "Cricket Ground": ["Food Court"],
    "Gym": ["Food Court"]
    }
     
     start_node = 'Library'
     target_node = 'Cafeteria'

     found, path = dfs(campus_graph, start_node, target_node)
     print(f"Path from {start_node} to {target_node}: {'Found' if found else 'Not Found'}")
     print("Path followed:", " -> ".join(path) if found else "No path followed")
     


