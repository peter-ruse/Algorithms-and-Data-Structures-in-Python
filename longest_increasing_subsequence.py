from random import randrange

from binary_search import binary_search_ceil


def LIS(a):
    """Determines a longest increasing subsequence of the array a"""
    n = len(a)
    curr_subseq = [a[0]]
    indices = [0]
    parent = [None] * n
    for i in range(1, n):
        if a[i] > curr_subseq[-1]:
            parent[i] = indices[-1]
            curr_subseq.append(a[i])
            indices.append(i)
        else:
            j = binary_search_ceil(a[i], curr_subseq)
            curr_subseq[j] = a[i]
            indices[j] = i
            if j >= 1:
                parent[i] = indices[j - 1]
    max_len = len(curr_subseq)
    max_subseq = [None] * max_len
    i = indices[-1]
    for j in range(max_len - 1, -1, -1):
        max_subseq[j] = a[i]
        i = parent[i]
    return max_len, max_subseq


if __name__ == '__main__':
    a = [10, 22, 9, 33, 21, 50, 41, 60, 80]
    print(LIS(a))
