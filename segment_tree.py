
class SegTree:
    def __init__(self, a):
        n = len(a)
        self.n = n
        self.value = [None] * 2 * n
        self.delta = [0] * 2 * n
        self.length = [1] * 2 * n
        for i in range(n):
            self.value[i + n] = a[i]
        for i in range(2 * n - 1, 1, -2):
            self.value[i >> 1] = self.agg(self.value[i], self.value[i ^ 1])
            self.length[i >> 1] = self.length[i] + self.length[i ^ 1]


    def agg(self, x, y):
        """The aggregating function. This can be min, max, multiplication, or any other
        symmetric operation.
        """
        return x + y


    def push_delta(self, i):
        """Pushes the delta at the i-th element of the *tree array* down the tree."""
        d = 0
        while i >> d > 0:
            d += 1
        d -= 2
        while d >= 0:
            x = i >> d
            self.value[x >> 1] = self.update(x >> 1)
            self.delta[x] += self.delta[x >> 1]
            self.delta[x ^ 1] += self.delta[x >> 1]
            self.delta[x >> 1] = 0
            d -= 1


    def update(self, i):
        """Applies the delta to the i-th element in the *tree array*."""
        res = self.value[i] + self.delta[i] * self.length[i]
        return res


    def range_update(self, l, r, x):
        """Increments every element in the range [l, r], inclusive of the
        current array. Does this lazily by only pushing the delta when needed.
        """
        l += self.n
        r += self.n
        self.push_delta(l)
        self.push_delta(r)
        a = l
        b = r
        while l <= r:
            if l & 1 != 0:
                self.delta[l] += x
            if r & 1 == 0:
                self.delta[r] += x
            l = (l + 1) >> 1
            r = (r - 1) >> 1
        i = a
        while i > 1:
            self.value[i >> 1] = self.agg(self.update(i), self.update(i ^ 1))
            i >>= 1
        i = b
        while i > 1:
            self.value[i >> 1] = self.agg(self.update(i), self.update(i ^ 1))
            i >>= 1


    def single_update(self, i, x):
        """Updates the value in position i of the current array to x"""
        i += self.n
        self.push_delta(i)
        self.value[i] = x
        self.delta[i] = 0
        while i > 1:
            self.value[i >> 1] = self.agg(self.update(i), self.update(i ^ 1))
            i >>= 1


    def query(self, l, r):
        """aggregates over the range [l:r], inclusive, of the current array"""
        l += self.n
        r += self.n
        self.push_delta(l)
        self.push_delta(r)
        res = 0
        found = False
        while l <= r:
            if l & 1 != 0:
                res = self.agg(res, self.update(l)) if found else self.update(l)
                found = True
            if r & 1 == 0:
                res = self.agg(res, self.update(r)) if found else self.update(r)
                found = True
            l = (l + 1) >> 1
            r = (r - 1) >> 1
        return res


if __name__ == '__main__':
    st = SegTree([0, 1, 2, 3, 4, 5]) # initialize to [0, 1, 2, 3, 4, 5]
    st.range_update(1, 3, 2) # becomes [0, 3, 4, 5, 4, 5]
    st.single_update(2, 17) # becomes [0, 3, 17, 5, 4, 5]
    print(st.query(2, 4)) # equals 26
