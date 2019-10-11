from functools import cmp_to_key


class SuffixArray:
    def __init__(self, s):
        n = len(s)
        self.s = s
        self.suffix_array = [0] * n
        self.inv_suffix_array = [0] * n
        self.lcp_array = [0] * n


    def build(self):
        n = len(self.s)
        order = [0] * n
        for i in range(n):
            order[i] = n - 1 - i
        order.sort(key=cmp_to_key(lambda i, j: -(self.s[i] < self.s[j])))
        classes = [0] * n
        c = [0] * n
        sa = [0] * n
        for i in range(n):
            self.suffix_array[i] = order[i]
            classes[i] = self.s[i]
        l = 1
        while l < n:
            for i in range(n):
                c[i] = classes[i]
            for i in range(n):
                if i > 0 and c[self.suffix_array[i - 1]] == c[self.suffix_array[i]] \
                    and self.suffix_array[i - 1] + l < n \
                    and c[self.suffix_array[i - 1] + l // 2] == c[self.suffix_array[i] + l // 2]:
                    classes[self.suffix_array[i]] = classes[self.suffix_array[i - 1]]
                else:
                    classes[self.suffix_array[i]] = i
            count = [0] * n
            for i in range(n):
                count[i] = i
            for i in range(n):
                sa[i] = self.suffix_array[i]
            for i in range(n):
                s1 = (sa[i] - l + n) % n
                self.suffix_array[count[classes[s1]]] = s1
                count[classes[s1]] += 1
            l *= 2
        for i in range(n):
            self.inv_suffix_array[self.suffix_array[i]] = i
        k = 0
        for i in range(n):
            if self.inv_suffix_array[i] == n - 1:
                k = 0
                continue
            j = self.suffix_array[self.inv_suffix_array[i] + 1]
            while i + k < n and j + k < n and self.s[i + k] == self.s[j + k]:
                k += 1
            self.lcp_array[self.inv_suffix_array[i]] = k
            if k > 0:
                k -= 1


if __name__ == '__main__':
    s = 'yabbadabbadoo'
    sa = SuffixArray(s)
    sa.build()
    print(sa.suffix_array)
    print(sa.lcp_array)
