
class Node:
    def __init__(self):
        self.parent = self
        self.rank = 0
        self.comp_size = 1

class DisjointSet:
    def __init__(self, k):
        """initializes the disjoint sets to singleton sets {0}, ..., {k - 1}"""
        self.nodes = [Node() for i in range(k)]
        self.num_components = k


    def find(self, x):
        """returns the root node of the set that x belongs to;
        at the same time, it compresses the path from x to that root
        """
        n = self.nodes[x]
        path = []
        while n != n.parent:
            path.append(n)
            n = n.parent
        for y in path:
            y.parent = n
        return n


    def merge(self, x, y):
        """merges the sets that x and y belong to"""
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return
        if x_root.rank == y_root.rank:
            y_root.parent = x_root
            x_root.rank += 1
            x_root.comp_size = x_root.comp_size + y_root.comp_size
        elif x_root.rank > y_root.rank:
            y_root.parent = x_root
            x_root.comp_size = x_root.comp_size + y_root.comp_size
        else:
            x_root.parent = y_root
            y_root.comp_size = y_root.comp_size + x_root.comp_size
        self.num_components -= 1


if __name__ == '__main__':
    djs = DisjointSet(6) # {0}, {1}, {2}, {3}, {4}, {5}
    djs.merge(1, 3) # {0}, {1, 3}, {2}, {4}, {5}
    djs.merge(1, 4) # {0}, {1, 3, 4}, {2}, {5}
    djs.merge(2, 5) # {0}, {1, 3, 4}, {2, 5}
    print(djs.num_components) # 3
    print(djs.nodes[3].parent.comp_size) # 3
    print(djs.nodes[4].parent.comp_size) # 3
    print(djs.nodes[2].parent.comp_size) # 2
