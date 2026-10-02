from backend.graph import graph
from backend.data import locations
from backend.algorithms import bfs, dfs, dijkstra, find_route
from backend.algorithms import search_locations, find_shortest_route


# Check if all graph locations exist in our location data
print("\nValidating the Graph:")
for location in graph:
    if location not in locations:
        print("The graph location is invalid:", location)
    for neighbor, distance in graph[location]:
        if neighbor not in locations:
            print("Invalid neighbor:", neighbor)
print("Graph validation complete.")


# Test BFS
print("\nBFS traversal:")
bfs(graph, "Main Gate")


# Test DFS
print("\nDFS traversal:")
dfs(graph, "Main Gate")


# Test priority queue
import heapq
priority_queue = []
heapq.heappush(priority_queue, (100, "Admin Block"))
heapq.heappush(priority_queue, (50, "Gate 2"))
heapq.heappush(priority_queue, (150, "Ravi Canteen"))
heapq.heappush(priority_queue, (30, "Main Ground"))
print("\nPriority Queue:")
while priority_queue:
    distance, location = heapq.heappop(priority_queue)
    print(distance, location)


# Test Dijkstra
print("\nDijkstra distances from Main Gate:")
distances, prev_loc = dijkstra(graph, "Main Gate")
for location, distance in distances.items():
    print(location, ":", distance)


# Test route reconstruction
route = find_route(
    prev_loc,
    "Main Gate",
    "Santoshanand Library"
)
print("\nShortest route:")
print(route)


# Test location search
print("\nLocation search:")
results = search_locations(locations, "block")
print(results)


# Test shortest route with distance
print("\nShortest route with distance:")
route, distance = find_shortest_route(
    graph,
    "Main Gate",
    "Santoshanand Library"
)
print("Route:", route)
print("Distance:", distance)


# Test invalid location
print("\nInvalid location test:")
route, result = find_shortest_route(
    graph,
    "Wrong Place",
    "Santoshanand Library"
)
print("Route:", route)
print("Result:", result)