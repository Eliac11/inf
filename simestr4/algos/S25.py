s = input() * int(200000/4)

n = len(s)

suffixes = sorted((s[i:], i) for i in range(n))
suffix_array = [suffix[1] for suffix in suffixes]

rank = [0] * n
for i, suffix_index in enumerate(suffix_array):
    rank[suffix_index] = i
lcp = [0] * n
k = 0
for i in range(n):
    if rank[i] == n - 1:
        k = 0
        continue
    j = suffix_array[rank[i] + 1]
    while i + k < n and j + k < n and s[i + k] == s[j + k]:
        k += 1
    lcp[rank[i]] = k
    if k > 0:
        k -= 1

# print(lcp)
# print(suffixes)


count = 0
for i in range(n):
    count += n - suffix_array[i] - lcp[i]
print(count)