n = int(input())

S = {input():0 for _ in range(n)}

for w in S.keys():

    count = 0
    for sp in range(1, len(w)):

        pref = w[:sp]
        suf = w[sp:]

        if pref in S and suf in S:
            count += 1
            
    print(count)