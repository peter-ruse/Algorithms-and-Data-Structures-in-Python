from collections import deque
from time import sleep


def ford_fulkerson(adj, source, sink):
    """Finds the max flow from source to sink using the Ford-Fulkerson
    algorithm. Each tuple in adj[x] is of the form (y, f, c), where there is
    a directed edge from x to y, of max capacity f, and cost per unit flow c.
    """
    n = len(adj)
    flows = []
    adj_resid = [[] for _ in range(n)]
    i = 0
    for x in range(n):
        for y, flow, cost in adj[x]:
            adj_resid[x].append((y, i, 0, cost))
            adj_resid[y].append((x, i, 1, -cost))
            flows.append([flow, 0, cost])
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
            for y, i, dir, _ in adj_resid[x]:
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


def bellman_ford_cc(edge_adj, edges):
    """Bellman-Ford algorithm for identifying negative cycles"""
    n = len(adj)
    m = len(edges)
    d = [float('inf')] * n
    parent = [None] * n

    # n - 1 iterations
    component = [None] * n
    for _ in range(n - 1):
        visited = [False] * n
        comp_num = 0
        for x in range(n):
            if not visited[x]:
                d[x] = 0
                s = [x]
                component[x] = comp_num
                while s:
                    y = s.pop()
                    for z, i, dir, cost in edge_adj[y]:
                        if edges[i][dir] > 0 and (component[z] == None or component[z] == component[y]):
                            component[z] = component[y]
                            if not visited[z]:
                                s.append(z)
                            if d[y] + cost < d[z]:
                                d[z] = d[y] + cost
                                parent[z] = y, i, dir, cost
                    visited[y] = True
                comp_num += 1

    # one more iteration to see if there's a negative cycle
    found_neg_cycle = False
    visited = [False] * n
    for x in range(n):
        if not visited[x]:
            d[x] = 0
            s = [x]
            while s:
                y = s.pop()
                for z, i, dir, cost in edge_adj[y]:
                    if edges[i][dir] > 0 and (component[z] == None or component[z] == component[y]):
                        component[z] = component[y]
                        if not visited[z]:
                            s.append(z)
                        if d[y] + cost < d[z]:
                            d[z] = d[y] + cost
                            parent[z] = y, i, dir, cost
                            found_neg_cycle = True
                            break
                visited[y] = True
                if found_neg_cycle:
                    break
            if found_neg_cycle:
                break
    if not found_neg_cycle:
        return False, None

    # trace back via parents to get the cycle
    curr_node = z
    visited = [False] * n
    last_occ = [None] * n
    cycle = []
    t = 0
    while True:
        x, i, dir, cost = parent[curr_node]
        cycle.append((x, i, dir, cost))
        curr_node = x
        if visited[x]:
            break
        else:
            last_occ[x] = t
            visited[x] = True
            t += 1

    return True, cycle[last_occ[x] + 1:t + 1]


def bellman_ford_sp(edge_adj, edges, source, sink):
    """Bellman-Ford algorithm for finding shortest path from source to sink"""
    n = len(edge_adj)
    m = len(edges)
    d = [float('inf')] * n
    d[source] = 0
    parent = [None] * n

    # n - 1 iterations suffice (assuming no negative cycles)
    for _ in range(n - 1):
        for x in range(n):
            for y, i, dir, cost in edge_adj[x]:
                if edges[i][dir] > 0 and d[x] + cost < d[y]:
                    d[y] = d[x] + cost
                    parent[y] = x, i, dir, cost

    if d[sink] == float('inf'):
        return False, None, d

    # trace back via parents to get from sink back to source
    curr_node = sink
    path = []
    t = 0
    while True:
        if curr_node == source:
            break
        x, i, dir, cost = parent[curr_node]
        path.append((x, i, dir, cost))
        curr_node = x

    # the distances d are also the node potentials, which we use in Dijkstra's algo
    return True, path, d


def min_cost_flow_cc(adj, source, sink):
    """Min cost flow algorithm using Bellman-Ford for repeated cycle cancellation"""
    max_flow, flows, adj_resid = ford_fulkerson(adj, source, sink)

    # check if there is a maximum flow solution
    # (i.e., all source arcs and all sink arcs are saturated)
    for _, i, _, _ in adj_resid[source]:
        if flows[i][0] != 0:
            return None
    for _, i , _, _ in adj_resid[sink]:
        if flows[i][0] != 0:
            return None

    min_cost = 0
    for flow1, flow2, cost in flows:
        min_cost += flow2 * cost

    # if there is a maximum flow solution, there is an optimal solution,
    # which is found by gradually eliminating all negative cost cycles
    while True:
        negative_cycle_exists, cycle = bellman_ford_cc(adj_resid, flows)
        if not negative_cycle_exists:
            break
        min_resid = float('inf')
        cycle_cost = 0
        for x, i, dir, cost in cycle:
            if flows[i][dir] < min_resid:
                min_resid = flows[i][dir]
            cycle_cost += cost
        min_cost += min_resid * cycle_cost
        for x, i, dir, cost in cycle:
            flows[i][dir] -= min_resid
            flows[i][1 - dir] += min_resid

    return min_cost


def min_cost_flow_bf(adj, source, sink):
    """Min cost flow algorithm using Bellman-Ford for successive shortest paths"""
    n = len(adj)
    edges = []
    edge_adj = [[] for _ in range(n)]
    i = 0
    for x in range(n):
        for y, flow, cost in adj[x]:
            edge_adj[x].append((y, i, 0, cost))
            edge_adj[y].append((x, i, 1, -cost))
            edges.append([flow, 0, cost])
            i += 1
    min_cost = 0
    while True:
        path_exists, path, _ = bellman_ford_sp(edge_adj, edges, source, sink)
        if not path_exists:
            return min_cost, [edge[1] for edge in edges]
        min_resid = float('inf')
        path_cost = 0
        for x, i, dir, cost in path:
            if edges[i][dir] < min_resid:
                min_resid = edges[i][dir]
            path_cost += cost
        min_cost += min_resid * path_cost
        for x, i, dir, cost in path:
            edges[i][dir] -= min_resid
            edges[i][1 - dir] += min_resid


if __name__ == '__main__':
    adj = [[(1, 5, 0), (2, 2, 0)],
        [(2, 3, 1), (3, 3, 4)],
        [(3, 7, 2)],
        [(4, 5, 2), (5, 7, 5), (6, 1, 8)],
        [(5, 3, 1), (7, 2, 0)],
        [(7, 4, 0)],
        [(7, 1, 0)],
        []]
    print(min_cost_flow_bf(adj, 0, 7))
    print(min_cost_flow_cc(adj, 0, 7))
