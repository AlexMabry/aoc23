import networkx as nx

from ..utils import parse_data


def create_graph(input_data):
    H, W = len(input_data), len(input_data[0])
    rocks = {(x, y) for y in range(H) for x in range(W) if input_data[y][x] == "#"}
    start = next((x, y) for y in range(H) for x in range(W) if input_data[y][x] == "S")

    G = nx.grid_2d_graph(W, H)
    G.remove_nodes_from(rocks)
    return G, start


def solve_part1(data: str):
    input_data = parse_data(data)
    G, start = create_graph(input_data)

    steps, locations = 0, [{start}]
    while (steps := steps + 1) <= 64:
        locations.append(set())
        for loc in locations[-2]:
            locations[-1].update(G.neighbors(loc))

    return len(locations[-1])


def solve_part2(data: str):
    input_data = parse_data(data)

    return None
