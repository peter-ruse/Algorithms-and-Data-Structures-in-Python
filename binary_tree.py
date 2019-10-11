from collections import deque


class TreeNode:
    def __init__(self, label):
        self.left = None
        self.right = None
        self.level = 0
        self.label = label


class BinaryTree:
    def __init__(self, n):
        self.nodes = [TreeNode(i) for i in range(n)]
        self.levels = [[] for _ in range(n)]


    def insert_left(self, i, j):
        """Makes left child link from node i to node j"""
        self.nodes[i].left = self.nodes[j]
        self.nodes[j].level = self.nodes[i].level + 1


    def insert_right(self, i, j):
        """Makes left child link from node i to node j"""
        self.nodes[i].right = self.nodes[j]
        self.nodes[j].level = self.nodes[i].level + 1


    def fill_levels(self):
        """Gets the levels"""
        for node in self.nodes:
            level = node.level
            self.levels[level].append(node)


    def in_order(self):
        """Gets the in-order traversal of the binary tree"""
        visited = [False] * len(self.nodes)
        visited[0] = True
        stack = [self.nodes[0]]
        trav = []
        while stack:
            node = stack[-1]
            if node.left and not visited[node.left.label]:
                stack.append(node.left)
                visited[node.left.label] = True
                continue
            if not node.right or not visited[node.right.label]:
                trav.append(node.label + 1)
            if node.right and not visited[node.right.label]:
                stack.append(node.right)
                visited[node.right.label] = True
                continue
            stack.pop()
        return trav


    def pre_order(self):
        """Gets the pre-order traversal of the binary tree"""
        queue = deque([self.nodes[0]])
        trav = []
        while queue:
            node = queue.popleft()
            trav.append(node.label + 1)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return trav


    def post_order(self):
        """Gets the post-order traversal of the binary tree"""
        visited = [False] * len(self.nodes)
        visited[0] = True
        stack = [self.nodes[0]]
        trav = []
        while stack:
            node = stack[-1]
            if node.left and not visited[node.left.label]:
                stack.append(node.left)
                visited[node.left.label] = True
                continue
            if node.right and not visited[node.right.label]:
                stack.append(node.right)
                visited[node.right.label] = True
                continue
            trav.append(node.label + 1)
            stack.pop()
        return trav


    def swap(self, node):
        """Swaps the left and right subtrees of the node"""
        temp = node.left
        node.left = node.right
        node.right = temp
