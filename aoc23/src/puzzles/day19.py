import re
from itertools import takewhile, dropwhile

from ..utils import parse_data


class Rule:
    def __init__(self, description):
        self.target = description
        self.values = [set(range(1, 4001))] * 4
        if match := re.match(r"([xmas])(.)(\d+):([a-zAR]+)", description):
            xmas, lt, val, self.target = match.groups()
            self.values["xmas".index(xmas)] = set(
                range(1, int(val)) if lt == "<" else range(int(val) + 1, 4001)
            )

    def eval(self, rating):
        return self.target if all(a in b for a, b in zip(rating, self.values)) else None


def get_workflows(input_data):
    return {
        g[0]: [Rule(r) for r in g[1].split(",")]
        for row in takewhile(lambda x: x != "", input_data)
        if (g := re.match(r"([a-z]+)\{(.*)}", row).groups())
    }


def get_parts(input_data):
    return [
        list(map(int, re.match(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)", row).groups()))
        for row in dropwhile(lambda x: not x.startswith("{"), input_data)
    ]


def check_part(rating, workflows):
    current = "in"
    while current not in ["A", "R"]:
        rules = workflows[current].copy()
        while (current := rules.pop(0).eval(rating)) is None:
            pass

    return sum(rating) if current == "A" else 0


def solve_part1(data: str):
    input_data = parse_data(data)
    workflows = get_workflows(input_data)
    parts = get_parts(input_data)
    return sum(check_part(part, workflows) for part in parts)


class Node:
    def __init__(self, name, rule):
        self.name = name
        self.L = None
        self.R = None
        if rule.target in ["A", "R"]:
            raise ValueError("Cannot create a node with a terminal rule")
        self.ranges = rule.values.copy()

    def combine(self, ranges):
        self.ranges = [self.ranges[i] & ranges[i] for i in range(4)]


def walk(node, visited):
    if node.name in visited:
        return 0
    visited.add(node.name)
    return 1 + walk(node.L, visited) + walk(node.R, visited)


def solve_part2(data: str):
    input_data = parse_data(data)
    workflows = get_workflows(input_data)

    nodes = {
        ":".join([name, str(ir)]): Node(":".join([name, str(ir)]), rule)
        for name, rules in workflows.items()
        for ir, rule in enumerate(rules)
        if rule.target not in ["A", "R"]
    }
    print("Nodes created")
    print(nodes)

    return None
