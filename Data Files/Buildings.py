campus_graph = {
    "Main Entrance": [("Admin Block A",79.26) ,("Academic Block A",104)],
    "Admin Block A": [("Main Entrance",79.26),("Library",15.80),("Auditorium",16.72),("Academic Block A",33.84),("Cafeteria",54.5)],
    "Academic Block A": [("Main Entrance",104),("Cafeteria",26.6),("Library",45.05),("Auditorium",15),("Admin Block A",33.84)],
    "Library": [("Admin Block A",15.80), ("Academic Block A",45.05),("Cafeteria",62.71),("Auditorium",2.4),("Academic Block C",178.56),("Academic Block B",182.56)],
    "Auditorium":[("Admin Block A",16.72),("Academic Block A",15),("Library",2.4),("Cafeteria",10)],
    "Cafeteria": [("Academic Block A",26.6),("Admin Block A",54.5), ("Library",62.71),("Auditorium",10),("Academic Block C",175.68),("Academic Block B",171.71)],
    "Academic Block C": [("Library",178.56),("Cafeteria",175.68),("Food Court",286),("Academic Block B",60)],
    "Academic Block B": [("Library",182.56),("Cafeteria",171.71),("Food Court",282),("Academic Block C",60)],
    "Food Court": [("Academic Block C",286),( "Academic Block B",282),("Cricket Ground",722.5),( "Gym",15.1), ("Hostel",276)],
    "Hostel": [("Mini Mart",54.16),("Food Court",276)],
    "Mini Mart": [("Hostel",54.16)],
    "Cricket Ground": [("Food Court",722.5)],
    "Gym": [("Food Court",15.1)]
    }


    #"Main Entrance": "Entrance to the campus"
    #"Admin Block A": "Has register office, Finance department, Travel desk, Reception."
    #"Academic Block A": "Has classes for Degree students"
    #"Library": "Has Books and sitting facilities. Timings (8 am to 9 pm) "
    #"Auditorium":"Has a capacity of 260 seats which allows to host events"
    #"Cafeteria":"Has sitting space for breakfast, lunch and snacks and a Caterer"
    #"Academic Block C":"Has classes for Science related students"
    #"Academic Block B": "Has classes for Engineering students"
    #"Food Court":"Mess for hostellers "
    #"Hostel":"Rooms for hostellers"
    #"Mini Mart":"To buy things for students"
    #"Cricket Ground":"Ground for stuendts to play"
    #"Gym":"To keep students fit"

building_positions = {
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