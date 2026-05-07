from collections import deque


class Graph:
    def __init__(self):
        # Adjacency list storing each node and its connected neighbours
        self._adj: dict[str, list[str]] = {}

    def add_node(self, node: str):
        # adds a node that doesn't already exist
        if node not in self._adj:
            self._adj[node] = []

    def add_edge(self, node1: str, node2: str):
        # adds edge between two nodes
        self.add_node(node1)
        self.add_node(node2)
        # then, add to neighbor lists
        if node2 not in self._adj[node1]:
            self._adj[node1].append(node2)
        if node1 not in self._adj[node2]:
            self._adj[node2].append(node1)

    def nodes(self) -> list[str]:
        # returns a list of nodes
        return list(self._adj.keys())

    def neighbours(self, node: str) -> list[str]:
        # returns neighbors of node
        return self._adj.get(node, [])

    def bfs(self, start: str) -> list[str]:
        # returns nodes in BFS order
        visited = []
        queue = deque([start])
        seen = {start}
        while queue:
            node = queue.popleft()
            visited.append(node)
            for neighbour in sorted(self._adj[node]):
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        return visited

    def dfs(self, start: str) -> list[str]:
        # returns nodes in DFS order
        visited = []
        seen = set()

        def _recurse(node):
            seen.add(node)
            visited.append(node)
            for neighbour in sorted(self._adj[node]):
                if neighbour not in seen:
                    _recurse(neighbour)

        _recurse(start)
        return visited