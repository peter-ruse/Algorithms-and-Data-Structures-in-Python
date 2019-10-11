

def merge_sort(a, b):
    """Merges two sorted lists a and b into a sorted list"""
    res = []
    i = 0
    j = 0
    while True:
        if i >= len(a):
            for k in range(j, len(b)):
                res.append(b[k])
            break
        if j >= len(b):
            for k in range(i, len(a)):
                res.append(a[k])
            break
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        elif a[i] > b[j]:
            res.append(b[j])
            j += 1
        else:
            res.append(a[i])
            i += 1
    return res


if __name__ == '__main__':
    a = [3, 7, 11, 15]
    b = [4, 6, 8, 16]
    print(merge_sort(a, b))
