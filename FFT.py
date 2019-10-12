
import cmath
from math import pi
from random import randrange
from time import clock


def get_pow_two(n):
    """Gets the smallest power of 2 greater than n"""
    k = 1
    logk = 0
    while k <= n:
        k *= 2
        logk += 1
    return k, logk


def FFT(p, w, n, logn, forward):
    """Gets the Fast Fourier Transform of the polynomial p."""
    y = p[:]
    for i in range(len(y), n):
        y.append(0)
    j = n//2
    for i in range(1, n - 1):
        if i >= j:
            y[i], y[j] = y[j], y[i]
        k = n//2
        while True:
            if k > j:
                break
            j -= k
            k //= 2
        j += k
    l = 2
    m = len(w) * forward
    for _ in range(logn):
        for j in range(l // 2):
            for k in range(j, n, l):
                a = y[k]
                b = w[j * m // l] * y[k + l // 2]
                y[k] = a + b
                y[k + l // 2] = a - b
        l *= 2
    if forward == -1:
        y = [y[i] / n for i in range(n)]
    return y


def multiply(p1, p2, w):
    """Multiplies two polynomials."""
    n, logn = get_pow_two(len(p1) + len(p2) - 2)
    y1 = FFT(p1, w, n, logn, 1)
    y2 = FFT(p2, w, n, logn, 1)
    y_prod = [y1[i] * y2[i] for i in range(n)]
    return FFT(y_prod, w, n, logn, -1)


def multiplication_tree(factors, w):
    """Gets the multiplication tree for a list of polynomials"""
    k, _ = get_pow_two(len(factors) - 1)
    tree = [None] * (2 * k - 1)
    for i in range(k - 1, 2 * k - 1):
        if i - k + 1 < len(factors):
            tree[i] = factors[i - k + 1]
        else:
            tree[i] = [1, 0]
    for i in range(k - 2, -1, -1):
        tree[i] = multiply(tree[2 * i + 1], tree[2 * i + 2], w)
    return tree


if __name__ == '__main__':
    deg = 50000
    p1 = [randrange(1, 100) for _ in range(deg + 1)]
    p2 = [randrange(1, 100) for _ in range(deg + 1)]
    n = 1 << 18
    w = [cmath.rect(1, 2 * pi * k / n) for k in range(n)] # precompute roots of unity

    t0 = clock()

    # FFT ...
    r_fft = multiply(p1, p2, w)
    r_fft = [round(x.real) for x in r_fft]

    t1 = clock()

    # brute force ...
    r_brute = [0] * (2 * deg + 1)
    for i in range(2 * deg + 1):
        r_brute[i] = sum(p1[k] * p2[i - k] for k in range(max(0, i - deg), min(deg + 1, i + 1)))

    t2 = clock()

    print('\n')
    print('FFT time:', t1 - t0)
    print('Brute force time:', t2 - t1)
    print('\n')
    print('first 10 fft coeff:', r_fft[:10])
    print('first 10 brute coeff:', r_brute[:10])
    print('highest degree fft coeff:', r_fft[2 * deg])
    print('highest degree brute coeff:', r_brute[-1])
    print('\n')
