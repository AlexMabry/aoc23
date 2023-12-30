from functools import reduce

import networkx as nx

from ..utils import parse_data


def solve_part1(data: str):
    input_data = parse_data(data, regex=r"(\w+): (.*)")
    edges = {n: set(e.split()) for n, e in input_data}

    G = nx.Graph(edges)
    G.remove_edges_from(nx.minimum_edge_cut(G))

    sizes = [len(component) for component in nx.connected_components(G)]
    return reduce(lambda x, y: x * y, sizes)


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
