

def euler_tour1(adj):
    """Does a dfs and lists each vertex every time we descend from/to it
    and every time we ascend from/to it
    """
    n = len(adj)
    tour = []
    visited = [False]*n
    visited[0] = True
    pointer = [0]*n
    s = [0]
    while s:
        x = s[-1]
        tour.append(x)
        any_more = False
        for j in range(pointer[x], len(adj[x])):
            y = adj[x][j]
            pointer[x] += 1
            if not visited[y]:
                s.append(y)
                visited[y] = True
                any_more = True
                break
        if not any_more:
            s.pop()
    return tour


def euler_tour2(adj):
    """Does a dfs and lists each vertex exactly twice:
    once when we descend into its subtree, and once when we leave it
    """
    n = len(adj)
    tour = [0]
    visited = [False] * n
    visited[0] = True
    pointer = [0] * n
    s = [0]
    while s:
        x = s[-1]
        any_more = False
        for j in range(pointer[x], len(adj[x])):
            y = adj[x][j]
            pointer[x] += 1
            if not visited[y]:
                tour.append(y)
                s.append(y)
                visited[y] = True
                any_more = True
                break
        if not any_more:
            tour.append(x)
            s.pop()
    return tour


def euler_tour3(adj):
    """Does a dfs and lists an edge once when we descend it
    and once when we ascend it
    """
    n = len(adj)
    tour = []
    visited = [False] * n
    visited[0] = True
    pointer = [0] * n
    s = [0]
    while s:
        x = s[-1]
        any_more = False
        for i in range(pointer[x], len(adj[x])):
            y = adj[x][i]
            pointer[x] += 1
            if not visited[y]:
                s.append(y)
                tour.append((x, y))
                visited[y] = True
                any_more = True
                break
        if not any_more:
            if len(s) >= 2:
                tour.append((s[-1], s[-2]))
            s.pop()
    return tour


if __name__ == '__main__':
    # example tree:
    #               		0
    #    		1						2
    #		3		4				5   6   7
    #	  8   9                   10 11
    adj = [[1, 2], [0, 3, 4], [0, 6, 7, 5], [1, 8, 9], [1],
        [11, 10, 2], [2], [2], [3], [3], [5], [5]]
    print(euler_tour1(adj))
    print(euler_tour2(adj))
    print(euler_tour3(adj))
