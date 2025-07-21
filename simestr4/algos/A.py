import sys

input = sys.stdin.read
data = input().splitlines()

word = data[0]

n, m, k = map(int, data[1].split())
astates = list(map(int, data[2].split()))

transitions = [{} for _ in range(n + 1)]

for i in range(3,m + 3):
    a, b, c = data[i].split()
    a, b = int(a), int(b)
    transitions[a][c] = b

current = 1

for char in word:
    if char in transitions[current]:
        current = transitions[current][char]
    else:
        print("Rejects")
        quit()

if current in astates:
    print("Accepts")
else:
    print("Rejects")
