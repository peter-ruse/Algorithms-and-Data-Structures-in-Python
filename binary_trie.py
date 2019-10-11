from sys import stdin

class TrieNode:
    def __init__(self):
        self.next = [None] * 2
        self.words = []
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.root.is_end = True
        self.root.words.append('')
        self.num_prefixes = 0


    def insert(self, word):
        """Inserts a new word into the trie"""
        curr_node = self.root
        curr_node.words.append(word)
        for c in word:
            i = ord(c) - ord('0')
            if not curr_node.next[i]:
                curr_node.next[i] = TrieNode()
                self.num_prefixes += 1
            curr_node = curr_node.next[i]
            curr_node.words.append(word)
        curr_node.is_end = True


    def is_word(self, word):
        """Returns true if the word is a word in the trie"""
        curr_node = self.root
        for c in word:
            i = ord(c) - ord('0')
            if curr_node.next[i]:
                curr_node = curr_node.next[i]
            else:
                return False
        if curr_node.is_end:
            return True
        else:
            return False


    def find_words_with_pref(self, prefix):
        """Finds all the words having prefix as a prefix"""
        curr_node = self.root
        for c in prefix:
            i = ord(c) - ord('0')
            if curr_node.next[i]:
                curr_node = curr_node.next[i]
            else:
                return []
        return curr_node.words


    def find_pref_of_word(self, word):
        """Finds all the words in the trie that are prefixes of word"""
        curr_node = self.root
        pref = []
        for i in range(len(word)):
            j = ord(word[i]) - ord('0')
            if curr_node.next[j]:
                if curr_node.next[j].is_end:
                    pref.append(word[:i + 1])
                curr_node = curr_node.next[j]
            else:
                return pref
        return pref


if __name__ == '__main__':
    t = Trie()
    t.insert('01010111')
    t.insert('010')
    t.insert('00')
    t.insert('11')
    t.insert('011')
    t.insert('0')
    t.insert('001')
    print(t.find_pref_of_word('0101'))
    print(t.find_words_with_pref('0'))
