import tkinter as tk
from tkinter import ttk, messagebox
import math
from collections import deque
from queue import PriorityQueue
import re

class NavigatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chanakya Navigator")
        self.root.geometry("1100x700")  # Increased width to accommodate map
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
        
        # Building positions for the map (scaled for better visualization)
        self.building_positions = {
            "Main Entrance": (50, 50),
            "Admin Block": (50, 150),
            "Academic Block A": (200, 50),
            "Library": (150, 200),
            "Auditorium": (170, 220),
            "Cafeteria": (250, 100),
            "Academic Block C": (400, 250),
            "Academic Block B": (420, 270),
            "Food Court": (500, 300),
            "Hostel": (550, 350),
            "Mini Mart": (570, 380),
            "Cricket Ground": (700, 400),
            "Gym": (520, 310),
        }
        
        # Colors for the map
        self.building_color = "#3498db"
        self.path_color = "#e74c3c"
        self.connection_color = "#95a5a6"
        self.bg_color = "#ecf0f1"
        self.text_color = "#2c3e50"

        self.locations = list(self.campus_graph.keys())
        self.selected_algorithm = None
        self.current_path = []  # To store the current path for map drawing
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#D4B94D', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Welcome to Chanakya Navigator", 
                              font=('Arial', 20, 'bold'), fg='#2c3e50', bg='#D4B94D')
        title_label.pack(expand=True)

        # Main content frame - using PanedWindow for resizable split
        main_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg='#D4D3D3')
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for controls and information
        left_frame = tk.Frame(main_pane, bg='#D4D3D3')
        main_pane.add(left_frame, width=400)
        
        # Add chatbot frame to the left frame
        self.create_chatbot_interface(left_frame)
        
        # Right frame for the map
        right_frame = tk.Frame(main_pane, bg='white', relief=tk.SUNKEN, borderwidth=2)
        main_pane.add(right_frame, width=600)
        
        # Create the map canvas
        self.map_canvas = tk.Canvas(right_frame, bg=self.bg_color, width=600, height=600)
        self.map_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_chatbot_interface(self, parent_frame):
        """Create the chatbot interface within the given parent frame"""
        chatbot_frame = tk.Frame(parent_frame, bg='#f0f0f0', relief=tk.RAISED, borderwidth=2)
        chatbot_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Chatbot header
        chatbot_header = tk.Label(chatbot_frame, text="Chanakya Assistant", 
                                 font=('Arial', 14, 'bold'), bg='#3498db', fg='white', 
                                 padx=10, pady=5)
        chatbot_header.pack(fill=tk.X)
        
        # Chat display area
        self.chat_display = tk.Text(chatbot_frame, width=15, height=5, bg='white', 
                                   font=('Arial', 10), state='disabled', wrap=tk.WORD)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar for chat display
        chat_scrollbar = tk.Scrollbar(self.chat_display)
        chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.config(yscrollcommand=chat_scrollbar.set)
        chat_scrollbar.config(command=self.chat_display.yview)
        
        # User input area
        input_frame = tk.Frame(chatbot_frame, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.user_input = tk.Entry(input_frame, width=30, font=('Arial', 10))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.user_input.bind("<Return>", self.process_user_input)
        
        send_button = tk.Button(input_frame, text="Send", bg='#2ecc71', fg='white',
                               command=self.process_user_input)
        send_button.pack(side=tk.RIGHT)
        
        # Welcome message
        self.add_bot_message("Hello! I'm your Chanakya Navigator Assistant. How can I help you today? You can ask me about locations, directions, or information about campus buildings.")
        
    def add_user_message(self, message):
        """Add a user message to the chat display"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "You: " + message + "\n", "user_msg")
        self.chat_display.tag_configure("user_msg", foreground="#2c3e50", font=('Arial', 10, 'bold'))
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
    def add_bot_message(self, message):
        """Add a bot message to the chat display"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "Assistant: " + message + "\n", "bot_msg")
        self.chat_display.tag_configure("bot_msg", foreground="#3498db", font=('Arial', 10))
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
    def process_user_input(self, event=None):
        """Process user input and generate a response"""
        user_message = self.user_input.get().strip()
        if not user_message:
            return
            
        # Add user message to chat
        self.add_user_message(user_message)
        self.user_input.delete(0, tk.END)
        
        # Process the message and generate a response
        response = self.generate_response(user_message)
        self.add_bot_message(response)
        
    def generate_response(self, user_message):
        """Generate a response based on the user's message using enhanced NLP"""
        user_message = user_message.lower()
        
        # Extract keywords from user message
        keywords = self.extract_keywords(user_message)
        
        # Check for greetings
        if any(greeting in keywords for greeting in ["hello", "hi", "hey", "greetings", "morning", "afternoon", "evening"]):
            return "Hello! How can I help you navigate around Chanakya University today?"
            
        # Check for thank you messages
        if any(word in keywords for word in ["thanks", "thank", "appreciate", "grateful"]):
            return "You're welcome! Is there anything else I can help you with?"
            
        # Check for location information requests
        if any(word in keywords for word in ["what", "tell", "info", "about", "describe", "details", "information"]):
            for location in self.locations:
                if location.lower() in user_message:
                    return f"Information about {location}: {self.building_info.get(location, 'No information available.')}"
            
            # If no specific location was mentioned but user asked for information
            return "I can provide information about various locations on campus. Which location would you like to know about?"
        
        # Check for navigation requests
        if any(word in keywords for word in ["go", "navigate", "path", "route", "way", "get", "directions", "find", "shortest", "fastest", "walk", "reach"]):
            # Try to identify source and destination
            source = None
            destination = None
            
            # First check for explicit from/to format
            if "from" in user_message and "to" in user_message:
                from_index = user_message.find("from")
                to_index = user_message.find("to")
                
                if from_index < to_index:  # Normal order: "from X to Y"
                    from_part = user_message[from_index+4:to_index].strip()
                    to_part = user_message[to_index+2:].strip()
                else:  # Reverse order: "to Y from X"
                    to_part = user_message[to_index+2:from_index].strip()
                    from_part = user_message[from_index+4:].strip()
                
                # Find best matching locations
                source = self.find_best_location_match(from_part)
                destination = self.find_best_location_match(to_part)
            else:
                # Try to identify locations mentioned in the message
                mentioned_locations = []
                
                # First check for exact matches
                for location in self.locations:
                    if location.lower() in user_message.lower():
                        mentioned_locations.append(location)
                
                # If no exact matches, try to find the best match
                if not mentioned_locations:
                    # Extract potential location words (nouns)
                    words = user_message.split()
                    for word in words:
                        if len(word) > 3:  # Only consider words with more than 3 characters
                            match = self.find_best_location_match(word)
                            if match and match not in mentioned_locations:
                                mentioned_locations.append(match)
                
                # If we have direct "to [location]" pattern
                to_match = re.search(r'to\s+(\w+(?:\s+\w+)*)', user_message, re.IGNORECASE)
                if to_match:
                    potential_dest = to_match.group(1)
                    dest_match = self.find_best_location_match(potential_dest)
                    if dest_match and dest_match not in mentioned_locations:
                        mentioned_locations.append(dest_match)
                
                if len(mentioned_locations) >= 2:
                    # If multiple locations mentioned, assume first is source and second is destination
                    source = mentioned_locations[0]
                    destination = mentioned_locations[1]
                elif len(mentioned_locations) == 1:
                    # If only one location mentioned, assume it's the destination
                    destination = mentioned_locations[0]
                    
                    # Try to infer current location as source
                    if any(word in user_message for word in ["here", "current", "now", "present"]):
                        # For demo purposes, assume Main Entrance as current location
                        source = "Main Entrance"
                        return f"I'll assume you're at the Main Entrance. Is that correct? If not, please specify your starting point to {destination}."
            
            # If we have both source and destination, find the path
            if source and destination:
                if source == destination:
                    return f"You're already at {source}!"
                
                # Use A* algorithm for navigation
                success, path, cost = self.a_star_search(source, destination)
                if success:
                    self.current_path = path
                    self.draw_map()  # Update the map with the new path
                    
                    # Calculate the total distance
                    distance = self.calculate_path_distance(path)
                    
                    # Generate a more natural language response
                    if len(path) <= 3:
                        path_str = " → ".join(path)
                        return f"Path from {source} to {destination}: {path_str}\nTotal distance: {distance:.2f} meters"
                    else:
                        # For longer paths, provide step-by-step directions
                        response = f"Here's how to get from {source} to {destination} (total distance: {distance:.2f} meters):\n"
                        for i in range(len(path)-1):
                            segment_distance = 0
                            for neighbor, dist in self.campus_graph[path[i]]:
                                if neighbor == path[i+1]:
                                    segment_distance = dist
                                    break
                            response += f"{i+1}. Go from {path[i]} to {path[i+1]} ({segment_distance:.2f} meters)\n"
                        return response
                else:
                    return f"Sorry, I couldn't find a path from {source} to {destination}."
            elif destination:
                return f"I need to know where you're starting from. Please specify your starting point to {destination}."
            else:
                return "I need to know your destination. Please specify where you want to go."
        
        # Check for available locations request
        if any(word in keywords for word in ["locations", "places", "buildings", "where", "list", "available", "options", "show"]):
            locations_list = ", ".join(self.locations)
            return f"Available locations on campus: {locations_list}"
            
        # Check for facility-related queries
        if any(word in keywords for word in ["eat", "food", "hungry", "lunch", "dinner", "breakfast", "snack"]):
            food_places = ["Cafeteria", "Food Court", "Mini Mart"]
            food_places_str = ", ".join(food_places)
            return f"You can find food at these locations: {food_places_str}. Would you like directions to any of these places?"
            
        if any(word in keywords for word in ["study", "book", "read", "research", "quiet"]):
            return "The Library is the best place for studying. It's open from 8 AM to 10 PM and has study halls, computer labs, and reading rooms."
            
        if any(word in keywords for word in ["sport", "exercise", "fitness", "play", "game", "cricket"]):
            return "For sports and exercise, you can visit the Cricket Ground or the Gym. The Gym has indoor equipment while the Cricket Ground is used for outdoor sports and events."
            
        # Check for help request
        if any(word in keywords for word in ["help", "assist", "support", "guide", "how", "use"]):
            return ("I can help you with:\n"
                   "1. Finding directions between locations (e.g., 'How do I get from the Library to the Cafeteria?')\n"
                   "2. Information about campus buildings (e.g., 'Tell me about the Library')\n"
                   "3. Listing all available locations (e.g., 'Show me all buildings')\n"
                   "4. Finding specific facilities (e.g., 'Where can I get food?')")
        
        # Default response
        return "I'm not sure how to help with that. You can ask me about campus locations, get directions between buildings, or request information about specific places."
        
    def extract_keywords(self, text):
        """Extract important keywords from the user message"""
        # Simple keyword extraction by removing common words
        common_words = ["a", "an", "the", "is", "are", "was", "were", "be", "been", "being", 
                       "in", "on", "at", "by", "for", "with", "about", "against", "between",
                       "into", "through", "during", "before", "after", "above", "below", "to",
                       "from", "up", "down", "of", "off", "over", "under", "again", "further",
                       "then", "once", "here", "there", "when", "where", "why", "how", "all",
                       "any", "both", "each", "few", "more", "most", "other", "some", "such",
                       "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
                       "s", "t", "can", "will", "just", "don", "should", "now", "d", "ll", "m",
                       "o", "re", "ve", "y", "ain", "aren", "couldn", "didn", "doesn", "hadn",
                       "hasn", "haven", "isn", "ma", "mightn", "mustn", "needn", "shan", "shouldn",
                       "wasn", "weren", "won", "wouldn", "i", "me", "my", "myself", "we", "our", 
                       "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", 
                       "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", 
                       "its", "itself", "they", "them", "their", "theirs", "themselves", "what", 
                       "which", "who", "whom", "this", "that", "these", "those", "am", "have", 
                       "has", "had", "having", "do", "does", "did", "doing", "would", "should", 
                       "could", "ought", "i'm", "you're", "he's", "she's", "it's", "we're", 
                       "they're", "i've", "you've", "we've", "they've", "i'd", "you'd", "he'd", 
                       "she'd", "we'd", "they'd", "i'll", "you'll", "he'll", "she'll", "we'll", 
                       "they'll", "isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't", 
                       "hadn't", "doesn't", "don't", "didn't", "won't", "wouldn't", "shan't", 
                       "shouldn't", "can't", "cannot", "couldn't", "mustn't", "let's", "that's", 
                       "who's", "what's", "here's", "there's", "when's", "where's", "why's", 
                       "how's", "and", "but", "if", "or", "because", "as", "until", "while", "as"]
        
        words = text.lower().split()
        keywords = [word for word in words if word not in common_words]
        return keywords
        
    def find_best_location_match(self, text):
        """Find the best matching location from the text"""
        text = text.lower()
        
        # Direct match
        for location in self.locations:
            if location.lower() in text:
                return location
                
        # Partial match (for cases like "admin" instead of "Admin Block")
        for location in self.locations:
            location_parts = location.lower().split()
            for part in location_parts:
                if len(part) > 3 and part in text:  # Only match significant parts (>3 chars)
                    return location
        
        # Check for similar words (more flexible matching)
        for location in self.locations:
            location_words = location.lower().split()
            text_words = text.split()
            
            # Check if any word in the location matches any word in the input
            for loc_word in location_words:
                for text_word in text_words:
                    if loc_word == text_word or (len(loc_word) > 3 and loc_word in text_word) or (len(text_word) > 3 and text_word in loc_word):
                        return location
                    
        return None
        
        # Draw the initial map
        self.draw_map()
        
        # Input frame
        input_frame = tk.LabelFrame(left_frame, text="Navigation Input", 
                                   font=('Arial', 14, 'bold'), bg='#D4D3D3', 
                                   fg='#2c3e50', padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Source selection
        tk.Label(input_frame, text="Source:", font=('Arial', 12), bg='#D4D3D3').grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.source_var = tk.StringVar()
        self.source_combo = ttk.Combobox(input_frame, textvariable=self.source_var, 
                                        values=self.locations, state="readonly", width=20)
        self.source_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # Destination selection
        tk.Label(input_frame, text="Destination:", font=('Arial', 12), bg='#D4D3D3').grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.dest_var = tk.StringVar()
        self.dest_combo = ttk.Combobox(input_frame, textvariable=self.dest_var, 
                                      values=self.locations, state="readonly", width=20)
        self.dest_combo.grid(row=1, column=1, padx=10, pady=5)

        # Find Path button
        self.find_path_btn = tk.Button(input_frame, text="Find Path", font=('Arial', 10, 'bold'),
                                      bg='#3498db', fg='white', width=15, command=self.find_path)
        self.find_path_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Results frame
        results_frame = tk.LabelFrame(left_frame, text="Navigation Results", 
                                     font=('Arial', 12, 'bold'), bg='#D4D3D3', 
                                     fg='#2c3e50', padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Path details
        self.path_text = tk.Text(results_frame, height=6, width=40, font=('Arial', 10), wrap=tk.WORD)
        self.path_text.pack(fill=tk.X, pady=(0, 10))
        
        # Building information
        info_frame = tk.Frame(results_frame, bg='#D4D3D3')
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(info_frame, text="Building Information Along Route:",  
                font=('Arial', 10, 'bold'), bg='#D4D3D3').pack(anchor=tk.W, pady=(0, 5))
        
        self.info_text = tk.Text(info_frame, height=8, width=40, font=('Arial', 10), wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Show Building Info button
        self.show_info_btn = tk.Button(results_frame, text="Show Building Info", font=('Arial', 10),
                                      bg='#2ecc71', fg='white', command=self.show_building_info)
        self.show_info_btn.pack(pady=10)
    
    def draw_map(self, path=None):
        """Draw the campus map with buildings and connections"""
        self.map_canvas.delete("all")
        
        # Draw connections between buildings
        for building, connections in self.campus_graph.items():
            if building in self.building_positions:
                x1, y1 = self.building_positions[building]
                for connection, _ in connections:
                    if connection in self.building_positions:
                        x2, y2 = self.building_positions[connection]
                        self.map_canvas.create_line(x1, y1, x2, y2, 
                                                  fill=self.connection_color, 
                                                  width=1, dash=(4, 2))
        
        # Draw the path if provided
        if path:
            for i in range(len(path) - 1):
                if path[i] in self.building_positions and path[i+1] in self.building_positions:
                    x1, y1 = self.building_positions[path[i]]
                    x2, y2 = self.building_positions[path[i+1]]
                    self.map_canvas.create_line(x1, y1, x2, y2, 
                                              fill=self.path_color, 
                                              width=3, arrow=tk.LAST)
        
        # Draw buildings
        for building, (x, y) in self.building_positions.items():
            # Draw circle for building
            self.map_canvas.create_oval(x-15, y-15, x+15, y+15, 
                                      fill=self.building_color, 
                                      outline=self.text_color, width=2)
            
            # Draw building name
            self.map_canvas.create_text(x, y-25, text=building, 
                                      fill=self.text_color, 
                                      font=('Arial', 8, 'bold'))
            
        # Add title to the map
        self.map_canvas.create_text(300, 20, text="Campus Map", 
                                  fill=self.text_color, 
                                  font=('Arial', 16, 'bold'))
    
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
            
            # Store current path for map drawing
            self.current_path = best_path
            
            # Display results
            result_text = f"Path Found!\n\n"
            result_text += f"Algorithm: {best_algo}\n"
            result_text += f"Route: {' → '.join(best_path)}\n"
            result_text += f"Total Distance: {best_distance:.2f} meters\n"
            
            self.path_text.insert(tk.END, result_text)
            
            # Show building information along the route
            self.show_route_info(best_path)
            
            # Draw the path on the map
            self.draw_map(best_path)
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