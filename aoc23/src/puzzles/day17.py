from itertools import product

import networkx as nx

from ..utils import parse_data


def move(x, y, f):
    return [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)][f]


def create_graph(nodes):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)

    for x, y, m, f in G:
        if m != 3:
            G.add_edge((x, y, m, f), (x, y, 3, (f - 1) % 4), weight=0)
            G.add_edge((x, y, m, f), (x, y, 3, (f + 1) % 4), weight=0)
        if m != 0 and (step := (*move(x, y, f), m - 1, f)) in G:
            G.add_edge((x, y, m, f), step, weight=G.nodes[step]["value"])

    return G


def solve_part1(data: str):
    input_data = parse_data(data)
    H, W = len(input_data), len(input_data[0])
    G = create_graph(
        ((x, y, m, f), {"value": int(input_data[y][x])})
        for x, y, m, f in product(range(W), range(H), range(4), range(4))
    )

    sources = {(0, 0, 3, 1), (0, 0, 3, 2)}
    targets = {(W - 1, H - 1, m, f) for m in range(4) for f in range(4)}

    return min(
        nx.dijkstra_path_length(G, s, t)
        for s, t in product(sources, targets)
        if nx.has_path(G, s, t)
    )


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
