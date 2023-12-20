from functools import reduce

import networkx as nx

from ..utils import parse_data


def create_graph(input_data) -> nx.DiGraph:
    g = nx.DiGraph()
    for kind, name, destinations in input_data:
        g.add_node(name, kind="FF" if kind == "%" else "CJ" if kind == "&" else "BC")
        g.add_edges_from([(name, dest) for dest in destinations.split(", ")])
    return g


def reset_graph(graph: nx.DiGraph) -> None:
    for n, kind in graph.nodes.data("kind"):
        if not kind:
            graph.nodes[n]["kind"] = None
            graph.nodes[n]["value"] = True
        elif kind == "FF":
            graph.nodes[n]["value"] = False
        elif kind == "CJ":
            for nb in graph.predecessors(n):
                graph.nodes[n][nb] = False


def graph_sections(graph: nx.DiGraph) -> list[nx.DiGraph]:
    sections = []
    for nb in graph["broadcaster"]:
        visited, queue = {"broadcaster"}, [nb]
        while queue and (node := queue.pop(0)):
            if node not in visited:
                visited.add(node)
                queue.extend(graph[node])

        sections.append(graph.subgraph(visited).copy())
    return sections


def push_button(graph: nx.DiGraph) -> tuple[int, int]:
    queue = [("button", False, "broadcaster")]
    low, high = 0, 0
    while queue:
        source, signal, dest = queue.pop(0)
        low += 0 if signal else 1
        high += 1 if signal else 0

        node = graph.nodes[dest]
        if node["kind"] == "BC":
            queue.extend((dest, signal, nb) for nb in graph[dest])
        elif node["kind"] == "FF" and not signal:
            node["value"] = not node["value"]
            queue.extend((dest, node["value"], nb) for nb in graph[dest])
        elif node["kind"] == "CJ":
            node[source] = signal
            all_high = all(node[nb] for nb in graph.predecessors(dest))
            queue.extend((dest, not all_high, nb) for nb in graph[dest])
        elif node["kind"] is None and not signal:
            node["value"] = signal

    return low, high


def solve_part1(data: str):
    input_data = parse_data(data, regex=r"([%&]?)([a-z]+) -> ([a-z, ]+)")
    graph = create_graph(input_data)
    reset_graph(graph)

    low, high = 0, 0
    for _ in range(1000):
        l, h = push_button(graph)
        low, high = low + l, high + h

    return low * high


def solve_part2(data: str):
    input_data = parse_data(data, regex=r"([%&]?)([a-z]+) -> ([a-z, ]+)")
    graph = create_graph(input_data)
    reset_graph(graph)

    answer = []
    for subgraph in graph_sections(graph):
        answer.append(0)
        while subgraph.nodes["rx"]["value"]:
            push_button(subgraph)
            answer[-1] += 1

    return reduce(lambda x, y: x * y, answer)
