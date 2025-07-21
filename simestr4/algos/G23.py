from collections import defaultdict, deque

def solve_company_problem(n, m, games):
    # Построение графа умственной отсталости
    dominance_graph = defaultdict(list)
    reverse_graph = defaultdict(list)

    for a, b, result in games:
        if result == 1:
            dominance_graph[a].append(b)
            reverse_graph[b].append(a)
        elif result == 2:
            dominance_graph[b].append(a)
            reverse_graph[a].append(b)

    # Поиск всех достижимых вершин (транзитивное замыкание)
    reachable = [set() for _ in range(n + 1)]

    def dfs(v, visited, group):
        visited.add(v)
        group.add(v)
        for neighbor in dominance_graph[v]:
            if neighbor not in visited:
                dfs(neighbor, visited, group)

    for i in range(1, n + 1):
        visited = set()
        dfs(i, visited, reachable[i])

    # Построение DAG (упрощенный граф)
    dag = defaultdict(set)
    for i in range(1, n + 1):
        for neighbor in dominance_graph[i]:
            if neighbor not in reachable[i]:
                dag[i].add(neighbor)

    # Топологическая сортировка
    in_degree = {i: 0 for i in range(1, n + 1)}
    for u in dag:
        for v in dag[u]:
            in_degree[v] += 1

    queue = deque([node for node in range(1, n + 1) if in_degree[node] == 0])
    topo_order = []

    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in dag[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Нахождение максимальной независимой антивыборки
    dp = [0] * (n + 1)
    for node in reversed(topo_order):
        dp[node] = 1
        for neighbor in dag[node]:
            dp[node] = max(dp[node], dp[neighbor] + 1)

    return max(dp)

# Ввод данных
n, m = map(int, input().split())
games = [tuple(map(int, input().split())) for _ in range(m)]

# Решение задачи
print(solve_company_problem(n, m, games))