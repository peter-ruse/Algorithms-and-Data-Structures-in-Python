
class SuffixTreeNode:
    def __init__(self, label):
        self.children = [None] * 27
        self.parent = None
        self.suffix_link = None
        self.label = label
        self.count = 0


class SuffixTree:
    def __init__(self, s):
        self.s = s
        self.root = SuffixTreeNode(0)
        self.remaining = 0
        self.active_node = self.root
        self.active_edge = None
        self.active_length = 0
        self.label = 0


    def build(self):
        for i in range(len(self.s)):
            self.extend(i)


    def walk_down(self):
        (l, r, next_node) = self.active_node.children[ord(self.s[self.active_edge]) - ord('`')]
        if r - l + 1 > self.active_length:
            return False
        else:
            self.active_node = next_node
            self.active_edge += r - l + 1
            self.active_length -= r - l + 1
            return True


    def extend(self, i):
        self.remaining += 1
        last_internal_node = None
        while self.remaining > 0:
            if self.active_length == 0:
                self.active_edge = i
            if self.active_node.children[ord(self.s[self.active_edge]) - ord('`')] == None:
                self.label += 1
                self.active_node.children[ord(self.s[self.active_edge]) - ord('`')] = (i, float('inf'), SuffixTreeNode(self.label))
                if last_internal_node != None:
                    last_internal_node.suffix_link = self.active_node
                    last_internal_node = None
            else:
                if self.walk_down():
                    continue
                (l, r, next_node) = self.active_node.children[ord(self.s[self.active_edge]) - ord('`')]
                if self.s[l+self.active_length] == self.s[i]:
                    self.active_length += 1
                    if last_internal_node != None and self.active_node != self.root:
                        last_internal_node.suffix_link = self.active_node
                        last_internal_node = None
                    break
                self.label += 1
                new_internal_node = SuffixTreeNode(self.label)
                self.label += 1
                new_internal_node.children[ord(self.s[i]) - ord('`')] = (i, float('inf'), SuffixTreeNode(self.label))
                new_internal_node.children[ord(self.s[l+self.active_length]) - ord('`')] = (l + self.active_length, r, next_node)
                new_internal_node.suffix_link = self.root
                self.active_node.children[ord(self.s[self.active_edge]) - ord('`')] = (l, l + self.active_length - 1, new_internal_node)
                if last_internal_node != None:
                    last_internal_node.suffix_link = new_internal_node
                last_internal_node = new_internal_node
            self.remaining -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = i - self.remaining+1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link


    def suffix_array(self):
        """Does a dfs of the suffix tree to find the suffix array and the
        least common prefix array
        """
        n = len(self.s)
        m = self.label + 1
        stack = [self.root]
        pointer = [0] * m
        suffix_length = 0
        suffix_array = [0] * (n - 1)
        inv_suffix_array = [0] * (n - 1)
        lcp_array = [0] * (n - 1)
        edges = [0]
        j = 0
        while stack:
            x = stack[-1]
            any_more = False
            for i in range(pointer[x.label], 27):
                pointer[x.label] += 1
                if x.children[i] != None:
                    (l, r, y) = x.children[i]
                    y.parent = x
                    stack.append(y)
                    if r == float('inf'):
                        edge_length = n - l
                        y.count = 1
                    else:
                        edge_length = r - l + 1
                    edges.append(edge_length)
                    suffix_length += edge_length
                    any_more = True
                    if r == float('inf') and suffix_length != 1:
                        suffix_array[j] = n - suffix_length
                        j += 1
                    break
            if not any_more:
                suffix_length -= edges[-1]
                stack.pop()
                edges.pop()
                if x != self.root:
                    x.parent.count += x.count
        for i in range(n-1):
            inv_suffix_array[suffix_array[i]] = i
        k = 0
        for i in range(n - 1):
            if inv_suffix_array[i] == n - 2:
                k = 0
                continue
            j = suffix_array[inv_suffix_array[i] + 1]
            while i + k < n - 1 and j + k < n - 1 and self.s[i + k] == self.s[j + k]:
                k += 1
            lcp_array[inv_suffix_array[i]] = k
            if k > 0:
                k -= 1
        return suffix_array, lcp_array


    def find(self, t):
        i = 0
        curr_node = self.root
        while i < len(t):
            if curr_node.children[ord(t[i]) - ord('`')]:
                (l, r, next_node) = curr_node.children[ord(t[i]) - ord('`')]
                j = l
                while self.s[j] == t[i]:
                    j += 1
                    i += 1
                    if j == r + 1 or i == len(t):
                        break
                if i == len(t):
                    return next_node.count
                if j == r + 1:
                    curr_node = next_node
                else:
                    return 0
            else:
                return 0


if __name__ == '__main__':
    s = 'abbadabbadoo'
    st = SuffixTree(s + '`')
    st.build()
    print(st.suffix_array())
