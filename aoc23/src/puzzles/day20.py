import math
from itertools import groupby

import networkx as nx
from matplotlib import pyplot as plt

from ..utils import parse_data


def create_graph(input_data):
    G = nx.DiGraph()
    for kind, name, destinations in input_data:
        G.add_node(name, kind="FF" if kind == "%" else "CJ" if kind == "&" else "BC")
        G.add_edges_from([(name, dest) for dest in destinations.split(", ")])
    for n, kind in G.nodes.data("kind"):
        if not kind:
            G.nodes[n]["kind"] = "OTHER"
        elif kind == "FF":
            G.nodes[n]["value"] = False
        elif kind == "CJ":
            for nb in in_neighbors(G, n):
                G.nodes[n][nb] = False
    return G


def out_neighbors(graph, node):
    return (n for edge in graph.out_edges(node) for n in edge if n != node)


def in_neighbors(graph, node):
    return (n for edge in graph.in_edges(node) for n in edge if n != node)


def push_button(graph, part2=False):
    queue = [("button", False, "broadcaster")]
    low, high, done = 0, 0, False
    while queue:
        source, signal, dest = queue.pop(0)
        low += 0 if signal else 1
        high += 1 if signal else 0
        if dest == "rx" and not signal:
            print(low, high)
            done = part2

        node = graph.nodes[dest]
        # print(f"{source} -{'high' if signal else 'low'}-> {dest}")
        if node["kind"] == "BC":
            queue.extend((dest, signal, nb) for nb in out_neighbors(graph, dest))
        elif node["kind"] == "FF":
            if not signal:
                node["value"] = not node["value"]
                queue.extend(
                    (dest, node["value"], nb) for nb in out_neighbors(graph, dest)
                )
        elif node["kind"] == "CJ":
            node[source] = signal
            all_high = all(node[nb] for nb in in_neighbors(graph, dest))
            queue.extend((dest, not all_high, nb) for nb in out_neighbors(graph, dest))

    return low, high, done


def solve_part1(data: str):
    input_data = parse_data(data, regex=r"([%&]?)([a-z]+) -> ([a-z, ]+)")
    G = create_graph(input_data)

    low, high = 0, 0
    for _ in range(1000):
        l, h, _ = push_button(G)
        low, high = low + l, high + h

    return low * high


def ranges(i):
    for a, b in groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]


def solve_part2(data: str):
    input_data = parse_data(data, regex=r"([%&]?)([a-z]+) -> ([a-z, ]+)")
    G = create_graph(input_data)

    draw_graph(G)
    return None

    low, high, done = 0, 0, False
    while not done:
        l, h, done = push_button(G, True)
        low, high = low + l, high + h

    return low + high


def draw_graph(G):
    colors = {
        "broadcaster": "green",
        "rx": "red",
    }
    colors = [
        colors.get(n, "yellow" if kind == "FF" else "blue")
        for n, kind in G.nodes.data("kind")
    ]
    G.nodes["broadcaster"]["color"] = 0xFF00FF

    size = 8 + len(G.nodes) // 12
    plt.figure(figsize=(size, size))
    nx.draw_networkx(
        G,
        node_size=800,
        node_color=colors,
        pos=nx.kamada_kawai_layout(G),
        with_labels=True,
    )
    plt.axis("off")
    plt.show()


TEST_DATA = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
