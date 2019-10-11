
def submasks(m):
    """Gets all the submasks of a mask"""
    res = [m]
    s = m
    while s > 0:
        s = (s - 1) & m
        res.append(s)
    return res


if __name__ == '__main__':
    mask = '1111'

    print(f'mask:\n{mask}\n')
    m = int(mask, 2)

    print('submasks:')
    for s in submasks(m):
        print(bin(s)[2:].zfill(len(mask)))
