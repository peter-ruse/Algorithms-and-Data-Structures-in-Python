
class TrieNode:
    def __init__(self, count, ending_here):
        self.next = [None] * 26
        self.count = count
        self.ending_here = ending_here


class Trie:
    def __init__(self):
        self.root = TrieNode(0, 0)
        self.num_prefixes = 0


    def insert(self, word):
        """Inserts a word into the trie"""
        curr_node = self.root
        i = 0
        while i < len(word):
            j = ord(word[i]) - ord('a')
            if curr_node.next[j]:  # go down the edge
                (s, next_node) = curr_node.next[j]
                k = 0
                while s[k] == word[i]:
                    k += 1
                    i += 1
                    if k == len(s) or i == len(word):
                        break
                if k == len(s):  # if we land on an existing node
                    curr_node = next_node
                    next_node.count += 1
                    if i == len(word):
                        next_node.ending_here += 1
                else:  # else we split the edge
                    new_node = TrieNode(next_node.count+1, 0)
                    new_node.next[ord(s[k]) - ord('a')] = (s[k:], next_node)
                    if i != len(word):
                        new_node.next[ord(word[i]) - ord('a')] = (word[i:], TrieNode(1, 1))
                        self.num_prefixes += len(word[i:])
                    else:
                        new_node.ending_here = 1
                    curr_node.next[j] = (s[:k], new_node)
                    return
            else:
                curr_node.next[j] = (word[i:], TrieNode(1, 1))
                self.num_prefixes += len(word[i:])
                return


    def find_words_with_prefix(self, prefix):
        """Finds the number of words in the trie that have the given prefix"""
        curr_node = self.root
        i = 0
        while i < len(prefix):
            j = ord(prefix[i]) - ord('a')
            if curr_node.next[j]:
                (s, next_node) = curr_node.next[j]
                k = 0
                while s[k] == prefix[i]:
                    k += 1
                    i += 1
                    if k == len(s) or i == len(prefix):
                        break
                if i == len(prefix):
                    return next_node.count
                if k == len(s):
                    curr_node = next_node
                else:
                    return 0
            else:
                return 0


    def find_prefixes_of_word(self, word):
        """Finds the number of words in the trie that are prefixes of the given word"""
        res = 0
        curr_node = self.root
        i = 0
        while i < len(word):
            j = ord(word[i]) - ord('a')
            if curr_node.next[j]:
                (s, next_node) = curr_node.next[j]
                k = 0
                while s[k] == word[i]:
                    k += 1
                    i += 1
                    if k == len(s) or i == len(word):
                        break
                if k == len(s):
                    res += next_node.ending_here
                    curr_node = next_node
                else:
                    return res
            else:
                return res


if __name__ == '__main__':
    t = Trie()
    t.insert('boo')
    t.insert('book')
    t.insert('boom')
    t.insert('bore')
    t.insert('acquire')
    t.insert('acquiesce')
    print(t.find_words_with_prefix('boo'))
    print(t.find_prefixes_of_word('bookworm'))
