Week 1 Report – Project Understanding & Planning
Title:
Chanakya Navigator 
Abstract
This project focuses on developing a agent that helps students, faculty, and visitors navigate Chanakya University campus. The system will model the campus as a graph of locations, provide pathfinding and campus guidance using AI search algorithms, and answer basic FAQs about buildings. The goal is to reduce confusion for new campus members, and better access to important facilities.
Introduction
University campuses often confuse new students and visitors, leading to lost time and frustration. Traditional signage or digital maps don’t offer personalized step-by-step navigation or contextual campus information. This AI agent addresses these gaps using search algorithms and query processing to act as a smart digital companion for campus movement and information needs.
Problem Statement
It is sometimes challenging to navigate a big university campus, especially for guests and newcomers. Due to limited time, students frequently have difficulty locating classrooms, administrative offices, or facilities. Existing solutions lack customisation and interactivity or are manual (maps, directions). An automated, intelligent system that can direct users, recommend the best routes, and respond to frequently asked campus-related questions using actual infrastructure data is therefore required.
Objectives
1.	Model the actual Chanakya University campus as graph.
2.	Implement core pathfinding using BFS, DFS, UCS, and A* search algorithms.
3.	Design a user-friendly interface for navigation and queries.
4.	Provide information about buildings (open hours, facilities).
5.	Demonstrate route comparisons and real-time path suggestions.
6.	Compare algorithm performances
Scope
•	The solution will serve students, faculty, and visitors within the boundaries of Chanakya University.
•	It will include a minimum of 12 major buildings/locations and model all significant paths between them.
•	Primary features: navigation, building info, basic amenities queries.
Requirements
Functional Requirements
•	Allow user to select source and destination from campus locations.
•	Support selection of search algorithm (BFS, DFS, UCS, A*).
•	Provide path and distance.
•	Display basic facts about selected buildings (e.g., services, timings).
•	Offer interface as a command-line tool, GUI, or web app.
Non-Functional Requirements
•	System should be responsive and easy to use.
•	Campus graph must be based on real and justified campus layout.
•	Implementation should allow extensions (visual output, chatbot, database integration).
Data Requirements
•	Accurate campus layout (buildings, walking paths).
•	Information of each building (services, schedules, descriptions).
Technology Requirements
•	Programming language: Python (for agent, algorithms, and backend).
•	Possible frontend tech: PySimpleGUI / Tkinter (optional GUI), Flask (for web).
•	Source code management: GitHub.
•	Tools for documentation: Word doc, Powerpoint.
Literature 
Prior art includes mobile navigation apps using GPS, campus-specific navigation tools integrating with Google Maps, and FAQ/chatbot systems for college information. Many focus on mapping, algorithm efficiency, and ease-of-use, but lack an integrated intelligent agent for both pathfinding and campus queries. BotBrain will bridge this gap by using AI search strategies and a smart interface tailored to the real layout of Chanakya University.
Tools & Technology List
•	Python: Core logic and algorithms.
•	Tkinter /PySimpleGUI /Flask: Possible GUI/web interface options.
•	PowerPoint: Map and diagram creation.
•	GitHub: Version control and code collaboration.
•	Google Maps API :For satellite views or real-world path overlays.


