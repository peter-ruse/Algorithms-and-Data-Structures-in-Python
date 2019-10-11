from heap import min_heap


def bellman_ford_sp(edge_adj, edges, source, sink):
    """Bellman-Ford algorithm for finding shortest path from source to sink"""
    n = len(edge_adj)
    d = [float('inf')] * n
    d[source] = 0
    visited = [False] * n
    visited[source] = 0

    # n - 1 iterations suffice (assuming no negative cycles)
    for _ in range(n - 1):
        for x in range(n):
            for y, i, dir in edge_adj[x]:
                if edges[i][dir] > 0 and d[x] + edges[i][dir + 2] < d[y]:
                    d[y] = d[x] + edges[i][dir + 2]
                    visited[y] = True

    if d[sink] == float('inf'):
        return False, _

    # update the edge costs
    potentials = [0] * n
    for x in range(n):
        if visited[x]:
            potentials[x] += d[x]
    for x in range(n):
        for y, i, dir in edge_adj[x]:
            edges[i][dir + 2] += potentials[x] - potentials[y]

    # the distances are the potentials
    return True, potentials


def dijkstra_with_potentials(edge_adj, edges, costs, potentials, source, sink):
    """Finds the shortest path from source to sink using dijkstra's algorithm.
    Augments this path and updates the node potentials and the costs.
    """
    n = len(edge_adj)
    visited = [False] * n
    parent_edge = [None] * n
    d = [float('inf')] * n
    d[source] = 0
    minheap = min_heap(n)
    for x in range(n):
        minheap.insert(x, float('inf'))
    minheap.update(source, 0)
    while minheap.heap:
        x, _ = minheap.remove()
        for y, i, dir in edge_adj[x]:
            if not visited[y]:
                if edges[i][dir] > 0 and d[x] + edges[i][dir + 2] < d[y]:
                    d[y] = d[x] + edges[i][dir + 2]
                    minheap.update(y, d[y])
                    parent_edge[y] = (x, i, dir)
        visited[x] = True
    if d[sink] == float('inf'):
        return False
    path = []
    curr_node = sink
    while curr_node != source:
        path.append(parent_edge[curr_node])
        curr_node = parent_edge[curr_node][0]
    min_resid = float('inf')
    for x, i, dir in path:
        if edges[i][dir] < min_resid:
            min_resid = edges[i][dir]

    # update the flows along the minimum path
    for _, i, dir in path:
        edges[i][dir] -= min_resid
        edges[i][1 - dir] += min_resid

    # update the potentials and the costs
    for x in range(n):
        if visited[x]:
            potentials[x] += d[x]
    for x in range(n):
        for y, i, dir in edge_adj[x]:
            edges[i][dir + 2] = (-2 * dir + 1) * costs[i] + potentials[x] - potentials[y]

    return True


def min_cost_flow_dijkstra(adj, source, sink):
    """Min cost flow algorithm using Dijkstra with potentials for successive shortest paths."""
    n = len(adj)
    edge_adj = [[] for _ in range(n)]
    edges = []
    costs = []
    i = 0
    for x in range(n):
        for y, flow, cost in adj[x]:
            edge_adj[x].append((y, i, 0))
            edge_adj[y].append((x, i, 1))
            i += 1
            edges.append([flow, 0, cost, -cost])
            costs.append(cost)
    path_exists, potentials = bellman_ford_sp(edge_adj, edges, source, sink)
    if not path_exists:
        return None
    while True:
        path_exists = dijkstra_with_potentials(edge_adj, edges, costs, potentials, source, sink)
        if not path_exists:
            break
    min_cost = 0
    for i in range(len(edges)):
        min_cost += edges[i][1] * costs[i]
    flows = [edge[1] for edge in edges]
    return min_cost, flows


if __name__ == '__main__':
    adj = [[(1, 5, 0), (2, 2, 0)],
           [(2, 3, 1), (3, 3, 4)],
           [(3, 7, 2)],
           [(4, 5, 2), (5, 7, 5), (6, 1, 8)],
           [(5, 3, 1), (7, 2, 0)],
           [(7, 4, 0)],
           [(7, 1, 0)],
           []]
    print(min_cost_flow_dijkstra(adj, 0, 7))
