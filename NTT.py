
from sys import stdin, stdout
from random import randrange
from time import process_time


def power(n, k, mod):
    """Computes n ^ k modulo mod, using binary exponentiation"""
    if k == 0:
        return 1
    x = 1
    while k > 1:
        if k % 2 == 0:
            n = n * n % mod
        else:
            x = n * x % mod
            n = n * n % mod
        k //= 2
    return n * x % mod


def get_pow_two(n):
    """First power of 2 greater than n"""
    k = 1
    logk = 0
    while k <= n:
        k *= 2
        logk += 1
    return k, logk


def NTT(p, r, n, n_inv, logn, forward, mod):
    """The Number Theoretic Transform of the polynomial p modulo mod.
    The prime should be a Fourier prime, i.e., one of the form m * 2 ^ k + 1.
    """
    y = p[:]
    for i in range(len(y), n):
        y.append(0)
    j = n // 2
    for i in range(1, n - 1):
        if i >= j:
            y[i], y[j] = y[j], y[i]
        k = n // 2
        while True:
            if k > j:
                break
            j -= k
            k //= 2
        j += k
    l = 2
    m = len(r)*forward
    for _ in range(logn):
        for j in range(l // 2):
            for k in range(j, n, l):
                a = y[k]
                b = r[j * m // l] * y[k + l // 2]
                b %= mod
                y[k] = (a + b) % mod
                y[k + l // 2] = (a - b) % mod
        l *= 2
    if forward == -1:
        y = [(y[i] * n_inv) % mod for i in range(n)]
    return y


def multiply2(p1, p2, r, mod):
    """Does fast multiplication of polynomials p1 and p2 modulo prime p"""
    n, logn = get_pow_two(len(p1) + len(p2) - 2)
    n_inv = power(n, mod - 2, mod)
    y1 = NTT(p1, r, n, n_inv, logn, 1, mod)
    y2 = NTT(p2, r, n, n_inv, logn, 1, mod)
    y3 = [(y1[i] * y2[i]) % mod for i in range(n)]
    return NTT(y3, r, n, n_inv, logn, -1, mod)


def multiply3(p1, p2, r, mod):
    """Does fast multiplication of p1 * p2 * p2"""
    n, logn = get_pow_two(len(p1) + 2 * len(p2) - 3)
    n_inv = power(n, mod - 2, mod)
    y1 = NTT(p1, r, n, n_inv, logn, 1, mod)
    y2 = NTT(p2, r, n, n_inv, logn, 1, mod)
    y3 = [1] * n
    for i in range(n):
        y3[i] *= y2[i] * y2[i]
        y3[i] %= mod
        y3[i] *= y1[i]
        y3[i] %= mod
    return NTT(y3, r, n, n_inv, logn, -1, mod)


def multiplication_tree(factors, r, mod):
    """Computes the multiplication tree for a list of factors"""
    n, _ = get_pow_two(len(factors)-1)
    tree = [None] * (2 * n - 1)
    for i in range(n - 1, 2 * n - 1):
        if i - n + 1 < len(factors):
            tree[i] = factors[i - n + 1]
        else:
            tree[i] = [1, 0]
    for i in range(n - 2, -1, -1):
        tree[i] = truncate(multiply2(tree[2 * i + 1], tree[2 * i + 2], r, mod))
    return tree


def inverse(p, m, r, mod):
    """Computes the inverse of polynomial p modulo x ^ m"""
    k, logk = get_pow_two(m)
    p_inv = [power(p[0], mod - 2, mod)]
    for i in range(logk):
        temp = multiply3(p[:1 << (i + 1)], p_inv, r, mod)
        p_inv.extend([(-x) % mod for x in temp[1 << i:1 << (i + 1)]])
    return p_inv


def divide(a, b, r, mod):
    """Returns the quotient and remainder when dividing polynomial a by polynomial b"""
    n = len(a) - 1
    m = len(b) - 1
    if n < m:
        return [0], a
    inv_b = inverse(b[::-1], n - m + 1, r, mod)
    quo = multiply2(a[::-1], inv_b, r, mod)[:n - m + 1]
    quo = quo[::-1]
    rem = multiply2(b, quo, r, mod)[:m]
    for i in range(m):
        rem[i] = (a[i] - rem[i]) % mod
    return quo, rem


def multipoint_eval(p, tree, n, r, mod):
    """Evaluates the polynomial p at the values a_1, ..., a_n
    tree is the multiplication tree for (x - a_1), ..., (x - a_n)
    """
    k = len(tree)
    res = [None] * k
    res[0] = p
    l = (k + 1) // 2 - 1
    for i in range(l):
        res[2 * i + 1], res[2 * i + 2] = divide(res[i], tree[2 * i + 1], r, mod)[1], \
            divide(res[i], tree[2 * i + 2], r, mod)[1]  # get just the remainder
    return [y[0] for y in res[l:l + n]]


def derivative(p, mod):
    res = []
    for i in range(1, len(p)):
        res.append((i * p[i]) % mod)
    return res


def truncate(p):
    while p[-1] == 0:
        p.pop()
    return p


def slow_eval(p, points, mod):
    d = len(p)
    n = len(points)
    res = [0] * n
    for i in range(n):
        x = points[i]
        t = 1
        for j in range(d):
            res[i] += (p[j] * t)
            res[i] %= mod
            t *= x
            t %= mod
    return res


if __name__ == '__main__':
    mod = 786433  # 3 * 2^18 + 1
    k = 1 << 18

    # 10 is a primitive root modulo the prime 786433,
    # so 10^((mod-1)//k) is a primitive 2^18-th root modulo 786433
    prim_root = power(10, (mod - 1) // k, mod)
    r = [1] * k
    for i in range(1, k):
        r[i] = r[i - 1] * prim_root
        r[i] %= mod

    # test the inverse function
    p = [randrange(1, mod) for _ in range(10000)]
    t0 = process_time()
    p_inv = inverse(p, len(p), r, mod)
    t1 = process_time()
    res = multiply2(p, p_inv, r, mod)  # should equal [1, 0, 0, ..., 0]
    print(res[:20])  # so this should be [1, 0, 0, ...]
    print(res[-20:])  # and this should be [0, ..., 0]
    print(f'\ntime for computing the inverse: {t1 - t0}')

    # test the multipoint eval
    points = [i for i in range(1000)]
    factors = [[-x, 1] for x in points]
    n = len(points)
    tree = multiplication_tree(factors, r, mod)
    p = [randrange(1, 10) for _ in range(20000)]

    t2 = process_time()
    fast = multipoint_eval(p, tree, n, r, mod)
    t3 = process_time()
    print(f'\nfast eval time: {t3 - t2}')

    t4 = process_time()
    slow = slow_eval(p, points, mod)
    t5 = process_time()
    print(f'\nslow eval time: {t5 - t4}')

    print(f'\nfast result: {fast[:15]}')
    print(f'\nslow result: {slow[:15]}')
