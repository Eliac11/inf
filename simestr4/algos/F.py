from collections import defaultdict, deque
 
def normalize_automaton(n, transitions, terminals):

    queue = deque([1])
    

    visited = [-1] * (n + 1)
    

    normalized = []
    

    visited[1] = 0
    state_count = 1
    

    transitions_map = defaultdict(dict)
    for a, b, c in transitions:
        transitions_map[a][c] = b
    
    while queue:
        current_state = queue.popleft()
        current_transitions = []
        

        for symbol in transitions_map[current_state].keys():
            next_state = transitions_map[current_state][symbol]
            if visited[next_state] == -1:
                visited[next_state] = state_count
                state_count += 1
                queue.append(next_state)
            current_transitions.append((symbol, visited[next_state]))
        
        normalized.append((visited[current_state], sorted(current_transitions)))
    

    terminal_states = {visited[state] for state in terminals}
    
    return normalized, terminal_states
 
def are_isomorphic(n1, transitions1, terminals1, n2, transitions2, terminals2):
    norm1, terminal_set1 = normalize_automaton(n1, transitions1, terminals1)
    norm2, terminal_set2 = normalize_automaton(n2, transitions2, terminals2)
    

    return norm1 == norm2 and terminal_set1 == terminal_set2
 
def solve():
    n1, m1, k1 = map(int, input().split())
    terminals1 = list(map(int, input().split()))
    transitions1 = [tuple(input().split()) for _ in range(m1)]
    transitions1 = [(int(a), int(b), c) for a, b, c in transitions1]
    

    n2, m2, k2 = map(int, input().split())
    terminals2 = list(map(int, input().split()))
    transitions2 = [tuple(input().split()) for _ in range(m2)]
    transitions2 = [(int(a), int(b), c) for a, b, c in transitions2]
    

    if are_isomorphic(n1, transitions1, terminals1, n2, transitions2, terminals2):
        print("YES")
    else:
        print("NO")
 
solve()