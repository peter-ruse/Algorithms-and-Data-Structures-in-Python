
class SegTree:
    def __init__(self, a):
        n = len(a)
        self.a = a
        self.seg_tree = [None] * 2 * n
        for i in range(n):
            self.seg_tree[i + n] = a[i]
        for i in range(n - 1, 0, -1):
            self.seg_tree[i] = self.agg(self.seg_tree[i << 1], self.seg_tree[i << 1 | 1])


    def agg(self, x, y):
        if x[0] < y[0]:
            return x
        else:
            return y


    def query(self, l, r):
        l += len(self.a)
        r += len(self.a) + 1
        res = (float('inf'), None)
        while l < r:
            if l & 1:
                res = self.agg(res, self.seg_tree[l])
                l += 1
            if r & 1:
                r -= 1
                res = self.agg(res, self.seg_tree[r])
            l >>= 1
            r >>= 1
        return res


class LeastCommonAncestor:
    def __init__(self, adj):
        self.adj = adj
        self.tour = []
        self.first_occ = [None] * len(adj)
        self.st = None


    def euler_tour(self):
        """Does a dfs of the tree to get an euler tour in the form of an array.
        The array lists the nodes in the order they're visited, along with their
        depths, and a segment tree is initialized on this array
        """
        n = len(self.adj)
        depth = [0] * n
        visited = [False] * n
        visited[0] = True
        pointer = [0] * n
        stack = [0]
        i = 0
        while stack:
            i += 1
            x = stack[-1]
            self.tour.append((depth[x], x))
            any_more = False
            for j in range(pointer[x], len(self.adj[x])):
                y = self.adj[x][j]
                pointer[x] += 1
                if not visited[y]:
                    stack.append(y)
                    depth[y] = depth[x] + 1
                    self.first_occ[y] = i
                    visited[y] = True
                    any_more = True
                    break
            if not any_more:
                stack.pop()
        self.st = SegTree(self.tour)


    def lca(self, x, y):
        l = self.first_occ[x]
        r = self.first_occ[y]
        if l > r:
            l, r = r, l
        depth_z, z = self.st.query(l, r)
        return z


if __name__ == '__main__':
    # example tree:
    #               		0
    #    		1						2
    #		3		4				5   6   7
    #	  8   9                   10 11
    adj = [[1, 2], [0, 3, 4], [0, 6, 7, 5], [1, 8, 9],
        [1], [11, 10, 2], [2], [2], [3], [3], [5], [5]]
    lca = LeastCommonAncestor(adj)
    lca.euler_tour()
    print(lca.lca(7, 10))
    print(lca.lca(9, 4))
    print(lca.lca(4, 9))
    print(lca.lca(4, 11))
