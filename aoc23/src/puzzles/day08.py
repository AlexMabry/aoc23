import re
from itertools import cycle
from math import gcd

from ..utils import parse_data


def get_left_right(data):
    input_data = parse_data(data)
    directions = [c == "L" for c in input_data[0]]
    connections = [
        match.groups()
        for line in input_data[2:]
        for match in re.finditer(r"(.+) = \((.+), (.+)\)", line)
    ]
    left = {name: L for name, L, _ in connections}
    right = {name: R for name, _, R in connections}
    return directions, left, right


def solve_part1(data: str):
    directions, left, right = get_left_right(data)

    path, steps = "AAA", 0
    for go_left in cycle(directions):
        steps += 1
        path = left[path] if go_left else right[path]

        if path == "ZZZ":
            return steps


def solve_part2(data: str):
    directions, left, right = get_left_right(data)
    starters = [name for name in left.keys() if name.endswith("A")]
    endings = set(name for name in left.keys() if name.endswith("Z"))

    durations = {}
    for g in starters:
        path, steps = g, 0
        for go_left in cycle(directions):
            steps += 1
            path = left[path] if go_left else right[path]
            if path in endings:
                durations[g] = steps
                break

    lcm = 1
    for val in durations.values():
        lcm = lcm * val // gcd(lcm, val)

    return lcm
