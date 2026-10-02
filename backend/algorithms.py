from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque()
    visited.add(start)
    queue.append(start)
    while queue:
        current = queue.popleft()
        print(current)
        for neighbor, distance in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

def dfs(graph, start):
    visited = set()
    stack = []
    stack.append(start)
    while stack:
        current = stack.pop()
        if current not in visited:
            visited.add(current)
            print(current)
            for neighbor, distance in graph[current]:
                if neighbor not in visited:
                    stack.append(neighbor)


import heapq
def dijkstra(graph, start):
    distances = {}
    prev_loc = {}
    for location in graph:
        distances[location] = float("inf")
        prev_loc[location] = None
    distances[start] = 0
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    while priority_queue:
        current_distance, current_location = heapq.heappop(priority_queue)
        if current_distance > distances[current_location]:
            continue
        for neighbor, distance in graph[current_location]:
            new_distance = current_distance + distance
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                prev_loc[neighbor] = current_location
                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )
    return distances, prev_loc


def find_route(prev_loc, start, destination):
    route = []
    current = destination
    while current is not None:
        route.append(current)
        if current == start:
            break
        current = prev_loc[current]
    route.reverse()
    return route


def search_locations(locations, search_term):
    results = []
    search_term = search_term.lower()
    for location in locations:
        if search_term in location.lower():
            results.append(location)
    return results


def find_shortest_route(graph, start, destination):
    if start not in graph:
        return None, "Invalid starting location"
    if destination not in graph:
        return None, "Invalid destination"
    distances, prev_loc = dijkstra(graph, start)
    if distances[destination] == float("inf"):
        return None, "No route available"
    route = find_route(prev_loc, start, destination)
    distance = distances[destination]
    return route, distance