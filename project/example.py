from data import runtests

def partition(arr, l, r):
    x = arr[r]
    i = l
    for j in range(l, r):
        if arr[j] <= x:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1

    arr[i], arr[r] = arr[r], arr[i]
    return i

def kth_smallest(arr, l, r, k):
    if 0 < k <= r - l + 1:
        index = partition(arr, l, r)
        if index - l == k - 1:
            return arr[index]
        if index - l > k - 1:
            return kth_smallest(arr, l, index - 1, k)
        return kth_smallest(arr, index + 1, r,
                           k - index + l - 1)
    print("Index out of bound")

def my_solve(n, _, k, base, wages, eq_cost):
    wages = [sorted([x[1] + eq_cost[x[0] - 1] for x in w]) for w in wages]

    result = []
    for i in range(n):
        x = min(len(base[i]), len(wages[i]))
        result.append(wages[i][0] + base[i][0])
        for j in range(1, x):
            result.append(wages[i][j] + base[i][j] - base[i][j - 1])
    val = kth_smallest(result, 0, len(result) - 1, k)
    out = 0
    count = k
    for i in result:
        if i <= val and count:
            out += i
            count -= 1
    return out

runtests(my_solve)
