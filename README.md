# Chanakya Navigator
 A campus navigation system using AI search algorithms to help students, faculty, and visitors navigate Chanakya University campus.

# Project Structure

├── Algorithm Files
│   ├── BFS.py                # Breadth-First Search implementation
│   ├── DFS.py                # Depth-First Search implementation 
│   ├── UCS.py                # Uniform Cost Search implementation
│   └── combination of BFS DFS UCS.py # Combined algorithms demo which has command line interface
├── UI Files
│   ├── UI_prototype.py       # Basic UI prototype with buttons
│   ├── UI_1.py              # Full UI with algorithm comparison
│   ├── UI_2.py              # UI with algorithm selection
│   └── Chatbot.py           # Chatbot interface implementation
├── Data Files
│   └── Buildings.py         # Campus graph and building data
│   ├── Week1 Report.md      # Project planning document
│   └── README.md            # Project documentation
└├── Campus Location.png  # Campus map
 └── Campus_graph.png     # Graph visualization

Features
Multiple pathfinding algorithms (BFS, DFS, UCS, A*)
Interactive GUI interfaces
Chatbot for natural language interaction
Building information database
Real campus layout and distances
Algorithm performance comparison
Visual route display
Search Algorithms
BFS: Finds shortest path in terms of steps
DFS: Depth-first exploration of paths
UCS: Finds least-cost path using actual distances
A*: Optimal pathfinding using distance heuristic

Usage
Run any of the UI files:

# Basic prototype
python UI_prototype.py

# Full comparison UI
python UI_1.py 

# Algorithm selection UI
python UI_2.py

# Chatbot interface
python Chatbot.py

Data Model
The campus is modeled as a weighted graph with:

13 key locations/buildings
Actual walking distances between points
Building information (services, timings, etc.)
Geographical coordinates for visualization
Dependencies
Python 3.x
tkinter
Standard libraries (collections, queue, math)
Documentation
Week 1 Report: Project planning and requirements
Campus maps and visualizations in image files
