from collections import deque


def ford_fulkerson(adj, source, sink):
    n = len(adj)
    flows = []
    adj_resid = [[] for _ in range(n)]
    i = 0
    for x in range(n):
        for y, flow in adj[x]:
            adj_resid[x].append((y, i, 0))
            adj_resid[y].append((x, i, 1))
            flows.append([flow, 0])
            i += 1
    max_flow = 0
    while True:
        found_augmenting_path = False
        visited = [False] * n
        visited[source] = True
        parent = [None] * n
        parent_edge = [None] * n
        q = deque([source])
        while q:
            x = q.popleft()
            for y, i, dir in adj_resid[x]:
                flow = flows[i][dir]
                if flow > 0 and not visited[y]:
                    q.append(y)
                    parent[y] = x
                    parent_edge[y] = (i, dir)
                    visited[y] = True
                    if y == sink:
                        found_augmenting_path = True
                        break
            if found_augmenting_path:
                break
        if found_augmenting_path:
            path = []
            x = sink
            min_resid = float('inf')
            while True:
                if x == source:
                    break
                i, dir = parent_edge[x]
                resid = flows[i][dir]
                path.append((i, dir))
                if resid < min_resid:
                    min_resid = resid
                x = parent[x]
            for i, dir in path:
                flows[i][dir] -= min_resid
                flows[i][1 - dir] += min_resid
            max_flow += min_resid
        else:
            break
    return max_flow, flows, adj_resid


if __name__ == '__main__':
    adj = [[(1, 16), (2, 13)],
           [(2, 10), (3, 12)],
           [(1, 4), (4, 14)],
           [(2, 9), (5, 20)],
           [(3, 7), (5, 4)],
           []]
    print(ford_fulkerson(adj, 0, 5))
