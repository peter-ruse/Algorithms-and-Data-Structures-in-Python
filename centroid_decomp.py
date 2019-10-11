
class CentroidDecomp:
    def __init__(self, adj):
        """Initialize the necessary attributes for building the centroid decomp"""
        n = len(adj)
        self.adj = adj
        self.subtree_sizes = [0] * n
        self.cd_adj = [[] for _ in range(n)]
        self.cd_root = None
        self.parent = [None]*n
        self.depth = [None]*n


    def get_subtree_sizes(self):
        """Does a depth first search to get the subtree sizes."""
        n = len(self.adj)
        s = [0]
        visited = [False] * n
        visited[0] = True
        start = [0] * n
        pointer = [0] * n
        i = 0
        while s:
            x = s[-1]
            any_more = False
            for j in range(pointer[x], len(self.adj[x])):
                y = self.adj[x][j]
                pointer[x] += 1
                if not visited[y]:
                    s.append(y)
                    i += 1
                    start[y] = i
                    any_more = True
                    visited[y] = True
                    break
            if not any_more:
                s.pop()
                self.subtree_sizes[x] = i-start[x]+1


    def get_centroids(self):
        """Iteratively re-roots the current subtree by going in the direction
        of the "heavy" subtree at each step, and re-rooting the current subtree
        at the first node where all subtrees have < 1/2 the current subtree size
        """
        n = len(self.adj)
        processed = [False] * n
        q = [0]
        i = 0
        while True:
            root = q[i]
            curr_node = q[i]
            prev_node = None
            curr_subtree_size = self.subtree_sizes[q[i]]
            while True:
                found = True
                for x in self.adj[root]:
                    if (prev_node == None or x != prev_node) and not processed[x]:
                        if self.subtree_sizes[x] > curr_subtree_size / 2:
                            self.subtree_sizes[root] -= self.subtree_sizes[x]
                            self.subtree_sizes[x] = curr_subtree_size
                            curr_node = x
                            prev_node = root
                            root = x
                            found = False
                            break
                if found:
                    break
            processed[root] = True
            if self.parent[q[i]] != None:
                self.cd_adj[self.parent[q[i]]].append(root)
                self.depth[root] = self.depth[self.parent[q[i]]] + 1
                self.parent[root] = self.parent[q[i]]
            if i == 0:
                self.cd_root = root
                self.depth[root] = 0
            if i == n - 1:
                break
            for x in self.adj[root]:
                if not processed[x]:
                    q.append(x)
                    self.parent[x] = root
            i += 1


    def build(self):
        """Builds the centroid decomposition of the tree"""
        self.get_subtree_sizes()
        self.get_centroids()


    def lca(self, x, y):
        """Finds the least common ancestor of x and y
        in the centroid decomposition tree
        """
        while self.depth[x] > self.depth[y]:
            x = self.parent[x]
        while self.depth[y] > self.depth[x]:
            y = self.parent[y]
        while x != y:
            x = self.parent[x]
            y = self.parent[y]
        return x


if __name__ == '__main__':
    # test tree
    #        0
    #        3
    #     1  2  4
    #           5
    #         6   9
    #        7 8  10
    #           11  12
    #          13   14 15
    adj = [[3], [3], [3], [0, 1, 2, 4], [3, 5], [4, 6, 9], [5, 7, 8],
        [6], [6], [5, 10], [9, 11, 12], [10, 13],
        [10, 14, 15], [11], [12], [12]]

    cd = CentroidDecomp(adj)
    cd.build()
    print(cd.cd_root)
    print(cd.cd_adj)
    print(cd.lca(9, 14))

    # this should be the centroid decomposition given by the above code:
    #            5
    #    3       6        10
    # 0 1 2 4   7 8    9  11   12
    #                     13  14 15
