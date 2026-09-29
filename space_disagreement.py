import random
from graph import Graph
import matplotlib.pyplot as plt
from articulation import ArticulationPointFinder


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


if __name__ == '__main__':
    p, g = generate_map(20)
    a = ArticulationPointFinder(g)
    display_map(p, g, a.is_articulation_point)
    exit()  # Otherwise I can't close the plot window on MacOS + TkAgg
