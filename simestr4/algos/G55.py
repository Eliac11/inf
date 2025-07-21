from collections import deque

def solve(m, n, edges, matching):

    adj = [[] for _ in range(m + 1)]
    for i in range(1, m + 1):
        for v in edges[i - 1]:
            adj[i].append(v)
    
    # паросочетания
    matched_to = [0] * (n + 1) #вершина первой доли
    for i in range(1, m + 1):
        if matching[i - 1] > 0:
            matched_to[matching[i - 1]] = i


    visited_left = [False] * (m + 1)
    visited_right = [False] * (n + 1)
    queue = deque()


    for i in range(1, m + 1):
        if matching[i - 1] == 0:
            queue.append((i, 0))
            visited_left[i] = True

    while queue:
        v, side = queue.popleft()

        if side == 0:
            for u in adj[v]:
                if not visited_right[u]:
                    visited_right[u] = True
                    if matched_to[u] != 0:
                        queue.append((matched_to[u], 0))
                        visited_left[matched_to[u]] = True
        else:
            if matched_to[v] != 0 and not visited_left[matched_to[v]]:
                queue.append((matched_to[v], 0))
                visited_left[matched_to[v]] = True


    left_set = []
    right_set = []

    for i in range(1, m + 1):
        if not visited_left[i]:
            left_set.append(i)
    for j in range(1, n + 1):
        if visited_right[j]:
            right_set.append(j)

    total_size = len(left_set) + len(right_set)

    return total_size, left_set, right_set



m, n = map(int, input().split())
edges = []
for _ in range(m):
    line = list(map(int, input().split()))
    edges.append(line[1:])
matching = list(map(int, input().split()))


total_size, left_set, right_set = solve(m, n, edges, matching)

print(total_size)
print(len(left_set), *left_set)
print(len(right_set), *right_set)
