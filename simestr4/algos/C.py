from collections import defaultdict, deque

def count_words(n, m, k, accepting_states, transitions):
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)
    accepting_states = set(accepting_states)
    
    for a, b, c in transitions:
        graph[a].append(b)
        reverse_graph[b].append(a)
    
    def bfs(start, graph):
        visited = set()
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            for neighbor in graph[node]:
                queue.append(neighbor)
        return visited
    
    reachable_from_start = bfs(1, graph)
    reachable_to_accepting = set()
    for state in accepting_states:
        reachable_to_accepting.update(bfs(state, reverse_graph))
    
    reachable = reachable_from_start & reachable_to_accepting
    
    def has_cycle():
        visited = set()
        stack = set()
        
        def dfs(node):
            if node in stack:
                return True
            if node in visited:
                return False
            visited.add(node)
            stack.add(node)
            for neighbor in graph[node]:
                if neighbor in reachable and dfs(neighbor):
                    return True
            stack.remove(node)
            return False
        
        for node in reachable:
            if node not in visited and dfs(node):
                return True
        return False
    
    if has_cycle():
        return -1
    
    dp = [0] * (n + 1)
    dp[1] = 1 
    
    order = deque()
    indegree = [0] * (n + 1)
    for u in reachable:
        for v in graph[u]:
            if v in reachable:
                indegree[v] += 1
    
    queue = deque([node for node in reachable if indegree[node] == 0])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor in reachable:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
    
    for node in order:
        for neighbor in graph[node]:
            if neighbor in reachable:
                dp[neighbor] = (dp[neighbor] + dp[node]) % (10**9 + 7)
    
    return sum(dp[state] for state in accepting_states) % (10**9 + 7)

n, m, k = map(int, input().split())
accepting_states = list(map(int, input().split()))
transitions = [tuple(input().split()) for _ in range(m)]
transitions = [(int(a), int(b), c) for a, b, c in transitions]

print(count_words(n, m, k, accepting_states, transitions))
