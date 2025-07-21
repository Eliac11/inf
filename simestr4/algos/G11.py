def dfs(v, graph, visited):
    visited[v] = True
    for u in graph[v]:
        if not visited[u]:
            dfs(u, graph, visited)
 
def solve():
    N, M = map(int, input().split())
    
    graph = [[] for _ in range(N)]
    
    for _ in range(M):
        u, v = map(int, input().split())
        graph[u - 1].append(v - 1)
        graph[v - 1].append(u - 1)
    
    visited = [False] * N
    
    dfs(0, graph, visited)
    
    if all(visited):
        print("YES")
    else:
        print("NO")
 
solve()