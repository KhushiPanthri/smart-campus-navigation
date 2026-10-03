# Smart Campus Navigation

## About the Project

Smart Campus Navigation is a graph-based campus navigation and resource finder system that helps students and visitors find campus locations and calculate the shortest route between them.

The campus is represented as a weighted graph, where locations are represented as vertices (nodes), connections between locations are represented as edges, and the distance between connected locations is represented as the edge weight.

The system uses Dijkstra's Shortest Path Algorithm to find the shortest route between two campus locations. It also implements Breadth-First Search (BFS) and Depth-First Search (DFS) for graph traversal.

The user interface is developed using Streamlit and the core algorithms are implemented in Python.

## Objectives

- Represent campus locations using a graph data structure.
- Find the shortest route between two campus locations.
- Implement Dijkstra's shortest-path algorithm.
- Implement BFS and DFS graph traversal.
- Provide a location search facility.
- Display information about campus locations.
- Provide a simple and user-friendly navigation interface.
- Demonstrate the practical application of Data Structures and Algorithms.

## Features

### Shortest Path Navigation

Users can select a starting location and a destination to calculate the shortest available route.

### Location Search

Users can search for campus locations using their names.

### Distance Calculation

The application displays the total distance of the calculated route.

### Step-by-Step Navigation

The application displays the sequence of locations that make up the calculated route.

### Location Information

Users can view information about available campus facilities.

## Data Structures and Algorithms

### Weighted Graph

The campus is represented as a weighted graph.

- Nodes represent campus locations.
- Edges represent connections between locations.
- Edge weights represent the distance between connected locations.

### Adjacency List

An adjacency-list representation is used to store the locations directly connected to each location.

### Dijkstra's Algorithm

Dijkstra's algorithm is used to find the shortest path between the selected source and destination.

A priority queue using Python's heapq module is used to efficiently process the location with the smallest current distance.

### Breadth-First Search (BFS)

BFS is implemented for graph traversal using a queue-based approach.

### Depth-First Search (DFS)

DFS is implemented for graph traversal using a stack-based approach.

## Technologies Used

- Python
- Streamlit
- Graph Data Structure
- Adjacency List
- Dijkstra's Algorithm
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Priority Queue / Heap

## Project Structure

smart-campus-navigation/
│
├── backend/
│   ├── algorithms.py
│   ├── data.py
│   └── graph.py
│
├── frontend/
│   └── app.py
│
├── test_backend.py
├── .gitignore
└── README.md

### Backend

algorithms.py contains the graph algorithms such as Dijkstra, BFS, DFS, route finding, and location search.

data.py contains the campus location information.

graph.py contains the campus graph and its connections.

### Frontend

app.py contains the Streamlit application and provides the user interface.

### Testing

test_backend.py contains tests for the backend functionality.

## How the System Works

The basic working of the system is:

User selects a starting location.

The user selects a destination.

The system represents the campus using the graph.

Dijkstra's algorithm calculates the shortest path.

The system displays the calculated route and total distance.

For example:

Main Gate → Academic Block → Computer Lab → Destination

## How to Run

### Step 1: Download the Repository

Download the project from GitHub and extract it.

Alternatively, clone the repository using:

git clone https://github.com/KhushiPanthri/smart-campus-navigation.git

### Step 2: Open the Project

Open the project folder in Visual Studio Code.

### Step 3: Install Streamlit

Open the terminal and run:

pip install streamlit

### Step 4: Open the Frontend Folder

cd frontend

### Step 5: Run the Application

streamlit run app.py

### Step 6: Open the Application

After running the application, Streamlit will provide a local address such as:

http://localhost:8501

Open this address in a web browser to use the application.

## Future Enhancements

The project can be extended with:

- Interactive campus maps
- GPS-based current location
- Mobile application
- Dynamic campus location management
- Accessibility-friendly routes
- Blocked-route detection
- Online deployment
- Real-time navigation

## Contributors

Khushi Panthri
Shristy Painuly
Aishwarya Uniyal

## Project Status

Completed Working Prototype

The current version includes graph-based campus representation, shortest-path navigation, BFS, DFS, location search, and a Streamlit user interface.

## Conclusion

Smart Campus Navigation demonstrates how Data Structures and Algorithms can be applied to a practical campus navigation problem.

By representing campus locations as a weighted graph and using Dijkstra's algorithm, the system can calculate an efficient route between two locations.

The project also demonstrates the practical implementation of graphs, adjacency lists, BFS, DFS, priority queues, and shortest-path algorithms using Python.
