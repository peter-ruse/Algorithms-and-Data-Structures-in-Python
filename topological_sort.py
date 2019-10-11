

def topological_sort(adj):
    """Returns a topological sort of the nodes of a DAG (directed acyclic graph).
    In a topological sort, for every edge u -> v, u occurs before v.
    """
    n = len(adj)
    nodes = []
    visited = [False] * n
    pointer = [0] * n
    for x in range(n):
        if not visited[x]:
            s = [x]
            visited[x] = True
            while s:
                y = s[-1]
                any_more = False
                for i in range(pointer[y], len(adj[y])):
                    z = adj[y][i]
                    pointer[y] += 1
                    if not visited[z]:
                        s.append(z)
                        visited[z] = True
                        any_more = True
                        break
                if not any_more:
                    s.pop()
                    nodes.append(y)
    top_sort = []
    while nodes:
        x = nodes.pop()
        top_sort.append(x)
    return top_sort


if __name__ == '__main__':
    adj = [[], [], [3], [1], [0, 1], [0, 2]]
    print(top_sort(adj))
