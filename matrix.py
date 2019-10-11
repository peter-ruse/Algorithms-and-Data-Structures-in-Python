
class Matrix:
    def __init__(self, A):
        self.mat = A
        self.rows = len(A)
        self.cols = len(A[0])


    def __repr__(self):
        return '\n'.join(' '.join(map(str, row)) for row in self.mat)


    def __getitem__(self, i):
        return self.mat[i]


    def __add__(self, B):
        assert self.rows == B.rows and self.cols == B.cols
        p, q = self.rows, self.cols
        res = [[0] * q for _ in range(p)]
        for i in range(p):
            for j in range(q):
                res[i][j] = self[i][j] + B[i][j]
        return Matrix(res)


    def __mul__(self, B):
        assert self.cols == B.rows
        p, q, r = self.rows, self.cols, B.cols
        res = [[0] * r for _ in range(p)]
        for i in range(p):
            for j in range(r):
                res[i][j] = sum(self[i][k] * B[k][j] for k in range(q))
        return Matrix(res)


    def __pow__(self, k):
        assert self.rows == self.cols
        n = self.rows
        I = [[0] * n for _ in range(n)]
        for i in range(n):
            I[i][i] = 1
        if k == 0:
            return Matrix(I)
        X = Matrix(I)
        M = self
        while k > 1:
            if k % 2 == 0:
                M = M * M
            else:
                X = M * X
                M = M * M
            k //= 2
        return M * X


if __name__ == '__main__':
    A = Matrix([[1, 2, 3], [4, 5, 6]])
    B = Matrix([[7, 8], [9, 10], [11, 12]])
    print(A * B)
    C = Matrix([[1, 1], [1, 2]])
    D = Matrix([[1, 2], [2, 3]])
    print(C ** 6)
    print(C)
