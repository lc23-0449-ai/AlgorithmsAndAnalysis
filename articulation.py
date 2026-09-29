import random
from graph import Graph
import matplotlib.pyplot as plt
#from articulation import ArticulationPointFinder


def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# Note: the * in the argument list means that any later arguments must be named, not positional
def generate_map(v, *, min_distance=0.1, random_seed=None):
    def too_close_to_an_existing_star(star):
        for s in positions:
            if distance(star, s) < min_distance:
                return True
        return False

    def no_intervening_star(here, there):
        for s in positions:
            if ((s is not here) and (s is not there)
                    and distance(here, s) < distance(here, there)
                    and distance(s, there) < distance(here, there)):
                return False
        return True

    if random_seed is not None:
        random.seed(random_seed)
    # Generate positions
    positions = []
    for i in range(v):
        p = (random.random(), random.random())
        while too_close_to_an_existing_star(p):
            p = (random.random(), random.random())
        positions.append(p)
    # Create edges
    graph = Graph(v)
    for i, p in enumerate(positions):
        for j in range(i + 1, v):
            q = positions[j]
            if no_intervening_star(p, q):
                graph.add_edge(i, j)
    return positions, graph


def display_map(positions, graph, art):
    for v in range(len(positions)):
        for w in graph.adj[v]:
            if v < w:
                plt.plot([p[0] for p in [positions[v], positions[w]]],
                         [p[1] for p in [positions[v], positions[w]]],
                         color='k', zorder=0)
    plt.scatter(*zip(*positions), marker='o', s=100, c='black', alpha=1, zorder=1)
    plt.scatter(*zip(*positions), marker='o', s=50, c=art, alpha=1, zorder=2)
    plt.show(block=True)





class ArticulationPointFinder:
    def __init__(self,g):
        self.g = g

    def _dfs(self,node, adj, visited):
            # Standard DFS to mark all reachable nodes
        visited[node] = True

        for neighbor in adj[node]:
            if not visited[neighbor]:
                self._dfs(neighbor, adj, visited)

    def _findPoints(self, adj, u, visited, disc, low, time, parent, isAP):

        # Mark vertex u as visited and assign discovery
        # time and low value
        visited[u] = 1
        time[0] += 1
        disc[u] = low[u] = time[0]
        children = 0

        # Process all adjacent vertices of u
        for v in adj[u]:

            # If v is not visited, then recursively visit it
            if not visited[v]:
                children += 1
                self._findPoints(adj, v, visited, disc, low, time, u, isAP)

                # Check if the subtree rooted at v has a
                # connection to one of the ancestors of u
                low[u] = min(low[u], low[v])

                # If u is not a root and low[v] is greater than or equal to disc[u],
                # then u is an articulation point
                if parent != -1 and low[v] >= disc[u]:
                    isAP[u] = 1

            # Update low value of u for back edge
            elif v != parent:
                low[u] = min(low[u], disc[v])

        # If u is root of DFS tree and has more than
        # one child, it is an articulation point
        if parent == -1 and children > 1:
            isAP[u] = 1

    def _articulationPoints(self,V, edges):

        adj = self.g.adj
        V = len(adj)
        disc = [0] * V
        low = [0] * V
        visited = [0] * V
        isAP = [0] * V
        time = [0]

        # Run DFS from each vertex if not
        # already visited (to handle disconnected graphs)
        for u in range(V):
            if not visited[u]:
                self._findPoints(adj, u, visited, disc, low, time, -1, isAP)

        # Collect all vertices that are articulation points
        result = [u for u in range(V) if isAP[u]]

        # If no articulation points are found, return list containing -1
        return result if result else [-1]

    @property
    def is_articulation_point(self):
        edges = []
        V = len(self.g.adj)
        for u in range(V):
            for v in self.g.adj[u]:
                if u < v:
                    edges.append((u, v))

        result = [False] * V

        vert = self._articulationPoints(V, edges)

        # Protect against the sentinel [-1]
        if vert == [-1]:
            return result

        for i in vert:
            result[i] = True

        return result


if __name__ == '__main__':
    p, g = generate_map(20)
    a = ArticulationPointFinder(g)
    display_map(p, g, a.is_articulation_point)
    exit()  # Otherwise I can't close the plot window on MacOS + TkAgg