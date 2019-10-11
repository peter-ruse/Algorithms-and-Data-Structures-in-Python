
def prime_fact(n):
    """Gets the prime factorization of n"""
    fact = {}
    d = 2
    while n > 1:
        while n % d == 0:
            fact[d] = fact.get(d, 0) + 1
            n //= d
        d += 1
        if d * d > n:
            if n > 1:
                fact[n] = fact.get(n, 0) + 1
            break
    return fact


if __name__ == '__main__':
    n = 180
    print(prime_fact(n))
