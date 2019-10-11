
def binary_search_ceil(x, a):
    """Finds the unique index i such that a[i - 1] < x <= a[i];
    the list a is assumed to be sorted in non-decreasing order
    """
    l = 0
    r = len(a) - 1
    while l <= r:
        i = (l + r) // 2
        if x <= a[i]:
            r = i - 1
        else:
            l = i + 1
    return l


def binary_search_floor(x, a):
    """Finds the unique index i such that a[i] <= x < a[i + 1];
    the list a is assumed to be sorted in non-decreasing order
    """
    l = 0
    r = len(a) - 1
    while l <= r:
        i = (l + r) // 2
        if a[i] <= x:
            l = i + 1
        else:
            r = i - 1
    return r


if __name__ == '__main__':
    a = [1, 2, 2, 3, 5, 9]
    print(binary_search_ceil(2, a))
    print(binary_search_floor(2, a))
    print(binary_search_floor(17, a))
    print(binary_search_floor(0, a))
