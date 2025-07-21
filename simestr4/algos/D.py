

def solve():
    n, m, k, l = map(int, input().split())

    accepting = [False] * (n + 1)
    for _ in range(k):
        state = int(input())
        accepting[state] = True
    
    transitions = [[-1] * 26 for _ in range(n + 1)]
    for _ in range(m):
        a, b, c = input().split()
        a, b = int(a), int(b)
        transitions[a][ord(c) - ord('a')] = b


    dp = [[0] * (n + 1) for _ in range(l + 1)]
    dp[0][1] = 1

    for i in range(l):
        for state in range(1, n + 1):
            if dp[i][state] > 0:
                for ch in range(26):
                    next_state = transitions[state][ch]
                    if next_state != -1:
                        dp[i + 1][next_state] = (dp[i + 1][next_state] + dp[i][state]) % (10**9 + 7)


    result = 0
    for state in range(1, n + 1):
        if accepting[state]:
            result = (result + dp[l][state]) % (10**9 + 7)

    print(result)

solve()
