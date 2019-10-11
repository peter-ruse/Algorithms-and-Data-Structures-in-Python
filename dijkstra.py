from sys import stdin, stdout

from heap import min_heap


def dijkstra(adj, start, end):
    """dijkstra's algorithm for distance from start to end"""
    n = len(adj)
    minheap = min_heap(n)
    for x in range(n):
        minheap.insert(x, float('inf'))
    minheap.update(start, 0)
    visited = [False] * n
    while minheap.heap:
        x, dx = minheap.remove()
        visited[x] = True
        if x == end:
            return dx
        for y, w in adj[x]:
            if not visited[y]:
                dy = minheap.get_value(y)
                if dx + w < dy:
                    minheap.update(y, dx + w)


def dijkstra_all(adj, start):
    """dijkstra for distances from node "start" to every other node"""
    n = len(adj)
    minheap = min_heap(n)
    for x in range(n):
        minheap.insert(x, float('inf'))
    minheap.update(start, 0)
    visited = [False] * n
    d = [float('inf')] * n
    d[start] = 0
    while minheap.heap:
        x, dx = minheap.remove()
        d[x] = dx
        for y, w in adj[x]:
            if not visited[y]:
                dy = minheap.get_value(y)
                if dx + w < dy:
                    minheap.update(y, dx + w)
    return d


if __name__ == '__main__':
    adj = [[(1, 24), (2, 3), (3, 20)],
        [(0, 24)],
        [(0, 3), (3, 12)],
        [(0, 20), (2, 12)]]
    print(dijkstra_all(adj, 0))
