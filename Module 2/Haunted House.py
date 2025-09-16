import heapq
import math

class Pathfinder:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start = None
        self.goal = None
        
        # Find start and goal positions
        for i in range(self.rows):
            for j in range(self.cols):
                if grid[i][j] == 'S':
                    self.start = (i, j)
                elif grid[i][j] == 'G':
                    self.goal = (i, j)
        
        if not self.start or not self.goal:
            raise ValueError("Start or goal not found in grid")

    def heuristic(self, pos, heuristic_type):
        i, j = pos
        gi, gj = self.goal
        
        if heuristic_type == "manhattan":
            return abs(i - gi) + abs(j - gj)
        elif heuristic_type == "euclidean":
            return math.sqrt((i - gi)**2 + (j - gj)**2)
        elif heuristic_type == "diagonal":
            dx = abs(i - gi)
            dy = abs(j - gj)
            return max(dx, dy)  # Diagonal distance for 4-direction movement
        else:
            raise ValueError("Invalid heuristic type")

    def get_neighbors(self, pos):
        i, j = pos
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.rows and 0 <= nj < self.cols and self.grid[ni][nj] != '1':
                neighbors.append((ni, nj))
                
        return neighbors

    def greedy_best_first(self, heuristic_type="manhattan"):
        open_set = []
        heapq.heappush(open_set, (0, self.start))
        came_from = {}
        visited = set()
        visited.add(self.start)
        nodes_explored = 0
        
        while open_set:
            _, current = heapq.heappop(open_set)
            nodes_explored += 1
            
            if current == self.goal:
                return self.reconstruct_path(came_from), nodes_explored
                
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    h = self.heuristic(neighbor, heuristic_type)
                    heapq.heappush(open_set, (h, neighbor))
                    
        return None, nodes_explored  # No path found

    def a_star(self, heuristic_type="manhattan"):
        open_set = []
        heapq.heappush(open_set, (0, self.start))
        came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start, heuristic_type)}
        nodes_explored = 0
        
        while open_set:
            _, current = heapq.heappop(open_set)
            nodes_explored += 1
            
            if current == self.goal:
                return self.reconstruct_path(came_from), nodes_explored
                
            for neighbor in self.get_neighbors(current):
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, heuristic_type)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    
        return None, nodes_explored  # No path found

    def reconstruct_path(self, came_from):
        current = self.goal
        path = [current]
        
        while current != self.start:
            current = came_from[current]
            path.append(current)
            
        path.reverse()
        return path

    def print_results(self, algorithm, heuristic_type, path, nodes_explored):
        path_length = len(path) - 1 if path else "N/A"
        print(f"{algorithm} with {heuristic_type} heuristic:")
        print(f"  Path length: {path_length}")
        print(f"  Nodes explored: {nodes_explored}")
        if path:
            print(f"  Path: {path}")
        else:
            print("  No path found")
        print()

# Example grid
grid = [
        ['S', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', '1', '1', 'O', '1', '1', '1', 'O'],
        ['O', '1', 'O', 'O', 'O', 'O', '1', 'O'],
        ['O', '1', 'O', '1', '1', 'O', '1', 'O'],
        ['O', 'O', 'O', '1', 'G', 'O', 'O', 'O'],
        ['O', '1', 'O', '1', '1', '1', '1', 'O'],
        ['O', '1', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', '1', '1', '1', '1', 'O']
    ]

# Create pathfinder instance
pf = Pathfinder(grid)

# Test all algorithms and heuristics
heuristics = ["manhattan", "euclidean", "diagonal"]

for h in heuristics:
    path, nodes = pf.greedy_best_first(h)
    pf.print_results("Greedy Best-First", h, path, nodes)
    
for h in heuristics:
    path, nodes = pf.a_star(h)
    pf.print_results("A*", h, path, nodes)