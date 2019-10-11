
class PalNode:
    def __init__(self):
        self.start = None
        self.end = None
        self.length = None
        self.pad = [None] * 26
        self.suffix = None
        self.num_suffixes = 1
        self.count = 1

class PalTree:
    def __init__(self, s):
        self.s = s
        self.root1 = PalNode()
        self.root2 = PalNode()
        self.root1.length = -1
        self.root2.length = 0
        self.root1.suffix = self.root1
        self.root2.suffix = self.root1
        self.curr_node = self.root1
        self.nodes = []


    def build(self):
        """Builds the palindromic tree via successive insertions"""
        for i in range(len(self.s)):
            self.insert(i)


    def insert(self, i):
        """Inserts the string's i-th character into the tree."""

        # look for X such that s[i]Xs[i] is a palindrome
        temp = self.curr_node
        while True:
            curr_length = temp.length
            if i - curr_length >= 1 and self.s[i] == self.s[i - curr_length - 1]:
                break
            temp = temp.suffix

        # check if s[i]Xs[i] already exists in the tree
        if temp.pad[ord(self.s[i]) - ord('a')]:
            self.curr_node = temp.pad[ord(self.s[i]) - ord('a')]
            self.curr_node.count += 1
            return

        new_node = PalNode()
        temp.pad[ord(self.s[i]) - ord('a')] = new_node
        new_node.length = temp.length + 2
        new_node.start = i-new_node.length + 1
        new_node.end = i
        new_pal = self.s[new_node.start:new_node.end + 1]
        self.nodes.append(new_node)

        if new_node.length == 1:
            new_node.suffix = self.root2
            self.curr_node = new_node
            return

        # look for the longest proper palindromic suffix of the
        # new palindrome by traversing suffix edges
        temp = temp.suffix
        while True:
            curr_length = temp.length
            if i - curr_length >= 1 and self.s[i] == self.s[i - curr_length - 1]:
                break
            temp = temp.suffix

        # insert the suffix edge from the new palindrome to its
        # longest proper palindromic suffix
        new_node.suffix = temp.pad[ord(self.s[i]) - ord('a')]
        new_node.num_suffixes += new_node.suffix.num_suffixes
        self.curr_node = new_node


    def compute_counts(self):
        """Computes the number of occurrences of each palindrome in the tree."""

        # propagate from the last node back toward the first one,
        # updating the number of occurrences of each palindrome in the string
        for i in range(-1, -len(self.nodes) - 1, -1):
            self.nodes[i].suffix.count += self.nodes[i].count


if __name__ == '__main__':
    s = 'abacabac'
    pt = PalTree(s)
    pt.build()
    pt.compute_counts()
    for pal in pt.nodes:
        print(s[pal.start:pal.end + 1], pal.count)
