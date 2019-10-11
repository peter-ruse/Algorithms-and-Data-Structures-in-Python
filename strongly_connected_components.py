

def dfs(adj):
    """
    Inputs:
    	adj = adjacency list of the di-graph
    Output:
    	nodes = the nodes in the order they're processed
	    a node is processed when all of its children have been processed, that is,
    	when it's popped off the stack during the depth first search;
     	this order is basically a reverse topological sort in the case of a DAG
    	(directed acyclic graph)
    """
    n = len(adj)
    visited = [False] * n
    pointer = [0] * n
    nodes = []
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
                    nodes.append(y)
                    s.pop()
    return nodes


def reverse_adj(adj, n):
    rev_adj = [[] for _ in range(n)]
    for x in range(n):
        for y in adj[x]:
            rev_adj[y].append(x)
    return rev_adj


def strongly_connected_components(rev_adj, nodes, n):
    """
    Inputs:
    	rev_adj = adjacency list of the reversed di-graph
    	nodes = nodes in the order processed by dfs of the original di-graph
		      (given by the dfs function above)
    	n = number of nodes, where nodes are numbered 0, ..., n-1
    Outputs:
    	comp_num = the label of the component that each node will belong to
            in the condensed graph.
    	condensed_adj = the adjacency list of the condensed graph
		      (the graph where we collapse all nodes in every component to one node)
    	reachable = the set of nodes reachable from each node in the condensed graph
    """
    visited = [False] * n
    pointer = [0] * n
    comp_num = [-1] * n
    condensed_adj = []
    reachable = [1] * n
    i = 0
    while nodes:
        x = nodes[-1]
        if visited[x]:
            nodes.pop()
            continue
        visited[x] = True
        s = [x]
        comp_num[x] = i
        condensed_adj.append([])
        while s:
            y = s[-1]
            any_more = False
            for j in range(pointer[y], len(rev_adj[y])):
                z = rev_adj[y][j]
                pointer[y] += 1
                if not visited[z]:
                    s.append(z)
                    comp_num[z] = i
                    visited[z] = True
                    any_more = True
                    break
                elif comp_num[z] == i:
                    continue
                else:
                    condensed_adj[comp_num[z]].append(i)
                    reachable[i] = (reachable[comp_num[z]] << (i - comp_num[z])) | reachable[i]
            if not any_more:
                s.pop()
        i += 1
    return comp_num, condensed_adj, reachable


if __name__ == '__main__':
    adj = [[2, 3],
        [0],
        [1],
        [4],
        []]
    n = len(adj)
    rev_adj = reverse_adj(adj, n)
    nodes = dfs(adj, n)
    comp_num, condensed_adj, reachable = strongly_connected_components(rev_adj, nodes, n)
    print(comp_num)
    print(condensed_adj)
    print([bin(x)[2:] for x in reachable])
