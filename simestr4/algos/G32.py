import heapq

def dijkstra(n, edges, start, end):
    graph = {i: [] for i in range(1, n + 1)}
    for b, e, w in edges:
        graph[b].append((e, w))
        graph[e].append((b, w))

    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[start] = 0
    prev = {i: None for i in range(1, n + 1)}

    pq = [(0, start)]

    while pq:
        current_dist, current_vertex = heapq.heappop(pq)

        if current_dist > dist[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex]:
            distance = current_dist + weight
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                prev[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))

    if dist[end] == float('inf'):
        return -1, []

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev[current]

    return dist[end], path[::-1]


n, m = map(int, input().split())
s, f = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]


min_weight, path = dijkstra(n, edges, s, f)


if min_weight == -1:
    print(-1)
else:
    print(min_weight)
    print(" ".join(map(str, path)))