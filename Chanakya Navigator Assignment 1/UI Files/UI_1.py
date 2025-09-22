import tkinter as tk
from tkinter import ttk, messagebox
import math
from collections import deque
from queue import PriorityQueue


class NavigatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chanakya Navigator")
        self.root.geometry("850x700")
        self.root.configure(bg='#D4D3D3')
        

        # Campus graph
        self.campus_graph = {
            "Main Entrance": [("Admin Block",79.26) ,("Academic Block A",104)],
            "Admin Block": [("Main Entrance",79.26),("Library",15.80),("Auditorium",16.72),("Academic Block A",33.84),("Cafeteria",54.50)],
            "Academic Block A": [("Main Entrance",104),("Cafeteria",26.60),("Library",45.05),("Auditorium",15),("Admin Block",33.84)],
            "Library": [("Admin Block",15.80), ("Academic Block A",45.05),("Cafeteria",62.71),("Auditorium",2.40),("Academic Block C",178.56),("Academic Block B",182.56)],
            "Auditorium":[("Admin Block",16.72),("Academic Block A",15),("Library",2.40),("Cafeteria",10)],
            "Cafeteria": [("Academic Block A",26.60),("Admin Block",54.50), ("Library",62.71),("Auditorium",10),("Academic Block C",175.68),("Academic Block B",171.71)],
            "Academic Block C": [("Library",178.56),("Cafeteria",175.68),("Food Court",286),("Academic Block B",60)],
            "Academic Block B": [("Library",182.56),("Cafeteria",171.71),("Food Court",282),("Academic Block C",60)],
            "Food Court": [("Academic Block C",286),( "Academic Block B",282),("Cricket Ground",722.50),( "Gym",15.10), ("Hostel",276)],
            "Hostel": [("Mini Mart",54.16),("Food Court",276)],
            "Mini Mart": [("Hostel",54.16)],
            "Cricket Ground": [("Food Court",722.50)],
            "Gym": [("Food Court",15.10)]
        }
        
        # Building information database
        self.building_info = {
            'Main Entrance': "Main entrance to Chanakya University. Security office located here.",
            'Admin Block': "Administrative offices: Registrar, Finance, Admissions.",
            'Academic Block A': "Classes for Engineering and Computer Science departments.",
            'Academic Block B': "Classes for Business and Management studies.",
            'Academic Block C': "Classes for Humanities and Social Sciences.",
            'Library': "Open 8 AM - 10 PM. Study halls, computer lab, and reading rooms available.",
            'Cafeteria': "Open 8 AM - 8 PM. Serves breakfast, lunch, and snacks.",
            'Food Court': "Multiple food vendors. Popular student hangout.",
            'Hostel': "Student residence with dining facilities.",
            'Mini Mart': "Small convenience store for daily needs.",
            'Cricket Ground': "Outdoor field used for cricket and events.",
            'Gym': "Indoor gym facility with equipment.",
            'Auditorium': "Venue for events, conferences, and ceremonies."
        }
        
        self.building_positions = {
            "Main Entrance": (0, 0),
            "Admin Block": (0, 80),
            "Academic Block A": (100, 0),
            "Library": (120, 100),
            "Auditorium": (130, 120),
            "Cafeteria": (200, 50),
            "Academic Block C": (300, 150),
            "Academic Block B": (320, 170),
            "Food Court": (400, 200),
            "Hostel": (450, 250),
            "Mini Mart": (470, 280),
            "Cricket Ground": (600, 300),
            "Gym": (420, 210),
        }

        
        self.locations = list(self.campus_graph.keys())
        self.selected_algorithm = None  # Default algorithm
        self.create_widgets()
        

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#D4B94D', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Welcome to Chanakya Navigator", font=('Arial', 30, 'bold'), fg='#2c3e50', bg='#D4B94D')
        title_label.pack(expand=True)

        # Main content frame
        main_frame = tk.Frame(self.root, bg='#D4D3D3')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        

        # Input frame
        input_frame = tk.LabelFrame(main_frame, text="Navigation Input", font=('Arial', 18, 'bold'),bg='#D4D3D3', fg='#2c3e50', padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=(20))

        # Source selection
        tk.Label(input_frame, text="Source:", font=('Arial', 14), bg='#D4D3D3').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.source_var = tk.StringVar()
        self.source_combo = ttk.Combobox(input_frame, textvariable=self.source_var, 
                                        values=self.locations, state="readonly", width=25)
        self.source_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # Destination selection
        tk.Label(input_frame, text="Destination:", font=('Arial', 14), bg='#D4D3D3').grid(row=0, column=4, sticky=tk.E, pady=5)
        self.dest_var = tk.StringVar()
        self.dest_combo = ttk.Combobox(input_frame, textvariable=self.dest_var, 
                                      values=self.locations, state="readonly", width=25)
        self.dest_combo.grid(row=0, column=5, padx=10, pady=5)


        # Find Path button
        self.find_path_btn = tk.Button(input_frame, text="Find Path", font=('Arial', 10, 'bold'),
                                      bg='#3498db', fg='white', width=20, command=self.find_path)
        self.find_path_btn.grid(row=3, column=3, padx=10, pady=5)

        # Results frame
        results_frame = tk.LabelFrame(main_frame, text="Navigation Results", font=('Arial', 12, 'bold'), bg='#D4D3D3', fg='#2c3e50', padx=10, pady=10)
        results_frame.pack(fill=tk.Y, expand=True)
        
        # Path details
        self.path_text = tk.Text(results_frame, height=6, width=80, font=('Arial', 10), wrap=tk.WORD)
        self.path_text.pack(fill=tk.Y, pady=(0, 10))
        
        # Building information
        info_frame = tk.Frame(results_frame, bg='#D4D3D3')
        info_frame.pack(fill=tk.X, expand=True)
        
        tk.Label(info_frame, text="Building Information Along Route:",  font=('Arial', 10, 'bold'), bg='#D4D3D3').pack(anchor=tk.W, pady=(0, 5))
        
        self.info_text = tk.Text(info_frame, height=10, width=80, font=('Arial', 10), wrap=tk.WORD)
        self.info_text.pack(fill=tk.X, expand=True)
        
        # Show Building Info button
        self.show_info_btn = tk.Button(results_frame, text="Show Building Info", font=('Arial', 10),
                                      bg='#2ecc71', fg='white', command=self.show_building_info)
        self.show_info_btn.pack(pady=20)


    
    def find_path(self):
        source = self.source_var.get()
        dest = self.dest_var.get()
        if not source or not dest:
            messagebox.showerror("Error", "Please select both source and destination locations.")
            return
            
        if source == dest:
            messagebox.showinfo("Info", "Source and destination are the same. No navigation needed.")
            return

        # Clear previous results
        self.path_text.delete(1.0, tk.END)
        self.info_text.delete(1.0, tk.END)

        results = []
        # Run the selected algorithm

        found1, path1, cost1= self.bfs(source, dest)
        if found1:
            bfs_distance = self.calculate_path_distance(path1)
            results.append(("BFS", path1, bfs_distance))
        
        found2, path2, cost2 = self.dfs(source, dest)
        if found2:
            dfs_distance = self.calculate_path_distance(path2)
            results.append(("DFS", path2, dfs_distance))
        
        found3, path3, cost3 = self.ucs(source, dest)
        if found3:
            results.append(("UCS", path3, cost3))
        
        found4, path4, cost4 = self.a_star_search(source, dest)
        if found4:
            results.append(("A*", path4, cost4))

        if results:
        # Pick the one with the smallest distance
            best_algo, best_path, best_distance = min(results, key=lambda x: x[2])        
            
            # Display results
            result_text = f"Path Found!\n\n"
            result_text += f"Route: {' → '.join(best_path)}\n"
            result_text += f"Total Distance: {best_distance} meters\n"
            
            self.path_text.insert(tk.END, result_text)
            
            # Show building information along the route
            self.show_route_info(best_path)
        else:
            self.path_text.insert(tk.END, f"No path found from {source} to {dest}.")

            
    def show_route_info(self, best_path):
        self.info_text.delete(1.0, tk.END)
        
        for building in best_path:
            info = self.building_info.get(building, "Information not available.")
            self.info_text.insert(tk.END, f"{building}: {info}\n\n")
            

    def show_building_info(self):
        # Get selected text from path or show all buildings
        try:
            selected_text = self.path_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text:
                # Try to find the building in the selected text
                for building in self.locations:
                    if building in selected_text:
                        info = self.building_info.get(building, "Information not available.")
                        messagebox.showinfo(f"Building Information: {building}", info)
                        return
        except:
            pass
            

#-------------------------- Search Algorithms -----------------------------------

# ---------------- BFS ----------------
    def bfs(self, start, target):
        if start not in self.campus_graph or target not in self.campus_graph:
            return False, [], "Invalid locations"

        visited = set()
        queue = deque([(start,[start],0)])   #This now has node, path, and total path cost

        while queue:
            node, current_path ,cost_till_now = queue.popleft()

            if node == target:
               return True, current_path, cost_till_now

            if node not in visited:
                visited.add(node)
                for neighbor, path_cost in self.campus_graph.get(node, []):
                    if neighbor not in visited:
                        Cost = cost_till_now + path_cost
                        N_path = current_path + [neighbor] 
                        queue.append((neighbor, N_path, Cost))

        return False, [], 0


# ---------------- DFS ----------------
    def dfs(self, start, target):
        if start not in self.campus_graph or target not in self.campus_graph:
                return False, [], "Invalid locations"

        visited = set()
        stack = [(start, [start],0)] # since graph is in list in tuple form

        while stack:
            node, current_path, cost_till_now = stack.pop()

            if node == target:
                return True, current_path, cost_till_now

            if node not in visited:
                visited.add(node)
                for neighbor, path_cost in self.campus_graph.get(node, []):
                    if neighbor not in visited:
                        Cost = cost_till_now + path_cost
                        N_path = current_path + [neighbor]
                        stack.append((neighbor, N_path, Cost))

        return False, [], 0


# ---------------- UCS ----------------
    def ucs(self, start, target):
        if start not in self.campus_graph or target not in self.campus_graph:
                return False, [], "Invalid locations"

        visited = set()
        priority_queue = PriorityQueue()
        priority_queue.put((0, start,[start]))   # (cost, node)


        while not priority_queue.empty():
            cost, node, path = priority_queue.get()


            if node == target:
                return True, path, cost

            if node not in visited:
                visited.add(node)
                for neighbor, path_cost in self.campus_graph.get(node, []):
                    if neighbor not in visited:
                        new_cost = cost + path_cost
                        N_path = path + [neighbor]
                        priority_queue.put((new_cost, neighbor, N_path))

        return False, path, 0


# ---------------- Heuristic----------------
    def heuristic(self, node, goal):
        x1, y1 = self.building_positions[node]
        x2, y2 = self.building_positions[goal]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# ---------------- A* ----------------
    def a_star_search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            _, current = frontier.get()

            if current == goal:
                # Reconstruct path
                path = []
                node = goal
                while node is not None:
                    path.append(node)
                    node = came_from.get(node)
                path.reverse()
                return True, path, cost_so_far[goal] 

            for neighbor, edge_cost in self.campus_graph.get(current, []):
                new_cost = cost_so_far[current] + edge_cost
                if neighbor not in cost_so_far or new_cost <= cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    frontier.put((priority, neighbor))
                    came_from[neighbor] = current

        return False, [], 0     


    def calculate_path_distance(self, path):
        total_distance = 0
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]

            for neighbor, dist in self.campus_graph.get(current, []):
                if neighbor == next_node:
                    total_distance += dist
                    break

        return total_distance


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = NavigatorGUI(root)
    root.mainloop()