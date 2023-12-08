import re
from itertools import cycle, tee

from ..utils import parse_data


class Node:
    name: str
    end: bool = False
    left: "Node"
    right: "Node"

    def __init__(self, name: str):
        self.name = name
        self.end = name.endswith("Z")

    def __repr__(self):
        return f"Node({self.name}) {self.left.name} <-> {self.right.name}"

    def __nonzero__(self):
        return self.end

    def set_neighbours(self, left: "Node", right: "Node"):
        self.left = left
        self.right = right


def get_nodes(input_data):
    connections = [
        match.groups()
        for line in input_data[2:]
        for match in re.finditer(r"(.+) = \((.+), (.+)\)", line)
    ]

    nodes = {name: Node(name) for (name, _, _) in connections}
    for name, left, right in connections:
        nodes[name].set_neighbours(nodes[left], nodes[right])

    return nodes


def solve_part1(data: str):
    input_data = parse_data(data)
    directions = [c for c in input_data[0]]
    nodes = get_nodes(input_data)

    current_node = nodes["AAA"]
    steps = 0
    for direction in cycle(directions):
        steps += 1
        if direction == "L":
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.name == "ZZZ":
            return steps


def solve_part2(data: str):
    input_data = parse_data(data)
    directions = [c for c in input_data[0]]
    nodes = get_nodes(input_data)
    print(len(nodes))
    ghosts = [node for name, node in nodes.items() if name.endswith("A")]
    patterns = {}

    steps = 0
    for direction in cycle(directions):
        steps += 1
        before = direction, tuple(ghost.name for ghost in ghosts)

        if before in patterns:
            ghosts = patterns[before]
            print("found pattern", ghosts)
        else:
            if direction == "L":
                ghosts = [ghost.left for ghost in ghosts]
            else:
                ghosts = [ghost.right for ghost in ghosts]

            if all(g.end for g in ghosts):
                return steps
            else:
                patterns[before] = ghosts
