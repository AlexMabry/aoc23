from itertools import batched, pairwise
from time import sleep

from ..utils import parse_data


def land(ca, cb):
    return "*" if ca == "." and cb == "O" else ca


def fall(ca, cb):
    return "." if ca == "*" else cb


def count(rocks, target="O"):
    return sum([1 for c in rocks if c == target])


def solve_part1(data: str):
    input_data = parse_data(data)
    rocks = [[c for c in row] for row in input_data]

    before = []
    while before != rocks:
        before = rocks.copy()
        for a, b in pairwise(range(len(rocks))):
            rocks[a] = [land(ca, cb) for ca, cb in zip(rocks[a], rocks[b])]
            rocks[b] = [fall(ca, cb) for ca, cb in zip(rocks[a], rocks[b])]
            rocks[a] = ["O" if ca == "*" else ca for ca in rocks[a]]

    return sum((len(rocks) - i) * count(row) for i, row in enumerate(rocks))


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
