from sys import stdin
from collections import deque


class TrieNode:
    def __init__(self, label):
        self.next = [None] * 26
        self.count = 0
        self.ending_here = 0
        self.suffix_link = None
        self.dict_suffix_link = None
        self.label = label


class Trie:
    def __init__(self):
        self.root = TrieNode(0)
        self.num_prefixes = 0
        self.label = 0


    def insert(self, word):
        curr_node = self.root
        for c in word:
            i = ord(c)-ord('a')
            if not curr_node.next[i]:
                self.label += 1
                curr_node.next[i] = TrieNode(self.label)
                self.num_prefixes += 1
            curr_node = curr_node.next[i]
            curr_node.count += 1
        curr_node.ending_here += 1


    def form_links(self):
        """The pre-processing part of Aho-Corasick's algorithm. It forms the
        required suffix and dictionary suffix links that are used later
        for efficient string matching
        """
        n = self.label + 1
        q = deque([self.root])
        visited = [False] * n
        visited[0] = True
        memo = [None] * n
        while q:
            x = q.popleft()
            for i in range(26):
                if x.next[i] != None:
                    y = x.next[i]
                    if not visited[y.label]:
                        q.append(y)
                        visited[y.label] = True
                        if x == self.root:
                            y.suffix_link = self.root
                        else:
                            # follow the parent's suffix links until
                            # there is a child matching this node
                            curr_node = x.suffix_link
                            while True:
                                if curr_node == None:
                                    y.suffix_link = self.root
                                    break
                                elif curr_node.next[i] != None:
                                    y.suffix_link = curr_node.next[i]
                                    break
                                else:
                                    curr_node = curr_node.suffix_link
                            # follow this node's suffix links until we
                            # reach a node that's the end of a word
                            curr_node = y.suffix_link
                            while True:
                                if curr_node == None:
                                    break
                                elif curr_node.ending_here > 0:
                                    y.dict_suffix_link = curr_node
                                    break
                                elif memo[curr_node.label] != None:
                                    y.dict_suffix_link = memo[curr_node.label]
                                    memo[y.label] = memo[curr_node.label]
                                    break
                                else:
                                    curr_node = curr_node.suffix_link


    def is_word(self, word):
        """Returns True if word is a word in the trie, False otherwise"""
        curr_node = self.root
        for c in word:
            i = ord(c) - ord('a')
            if curr_node.next[i]:
                curr_node = curr_node.next[i]
            else:
                return False
        if curr_node.ending_here > 0:
            return True
        else:
            return False


    def find_words_with_prefix(self, prefix):
        """Finds the number of words having prefix as a prefix"""
        curr_node = self.root
        for c in prefix:
            i = ord(c) - ord('a')
            if curr_node.next[i]:
                curr_node = curr_node.next[i]
            else:
                return 0
        return curr_node.count


    def find_prefixes_of_word(self, word):
        """Finds the number of words in the trie that are prefixes of word"""
        res = 0
        curr_node = self.root
        for c in word:
            i = ord(c) - ord('a')
            if curr_node.next[i]:
                res += curr_node.next[i].ending_here
                curr_node = curr_node.next[i]
            else:
                return res
        return res


    def match(self, s):
        """Finds the number of substrings of s that occur as words in the trie"""
        res = 0
        curr_node = self.root
        for c in s:
            i = ord(c) - ord('a')
            while True:
                if curr_node.next[i]:
                    curr_node = curr_node.next[i]
                    break
                else:
                    if curr_node == self.root:
                        break
                    else:
                        curr_node = curr_node.suffix_link
            curr_node_ = curr_node
            while curr_node_ != None:
                res += curr_node_.ending_here
                curr_node_ = curr_node_.dict_suffix_link
        return res


if __name__ == '__main__':
    t = Trie()
    t.insert('a')
    t.insert('ab')
    t.insert('abb')
    t.insert('bab')
    t.insert('bc')
    t.insert('bc')
    t.insert('bcd')
    t.insert('c')
    t.insert('caa')
    t.insert('ac')
    t.form_links()
    print(t.match('aca'))
    print(t.find_prefixes_of_word('abba'))
    print(t.find_words_with_prefix('bc'))
