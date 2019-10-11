
def power(n, k):
    """Finds n ^ k in log k time"""
    if k == 0:
        return 1
    x = 1
    while k > 1:
        if k % 2 == 0:
            n = n * n
        else:
            x = n * x
            n = n * n
        k //= 2
    return n * x
