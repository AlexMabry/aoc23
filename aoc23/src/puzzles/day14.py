from itertools import batched, pairwise
from time import sleep

from ..utils import parse_data


def land(ca, cb):
    return "*" if ca == "." and cb == "O" else ca


def fall(ca, cb):
    return "." if ca == "*" else cb


def count(rocks, target="O"):
    return sum([1 for c in rocks if c == target])


def tilt(rocks):
    before = []
    while before != rocks:
        before = rocks.copy()
        for a, b in pairwise(range(len(rocks))):
            rocks[a] = [land(ca, cb) for ca, cb in zip(rocks[a], rocks[b])]
            rocks[b] = [fall(ca, cb) for ca, cb in zip(rocks[a], rocks[b])]
            rocks[a] = ["O" if ca == "*" else ca for ca in rocks[a]]
    return rocks


def solve_part1(data: str):
    input_data = parse_data(data)
    rocks = [[c for c in row] for row in input_data]

    rocks = tilt(rocks)

    return sum((len(rocks) - i) * count(row) for i, row in enumerate(rocks))


def rotate(rocks):
    return list(zip(*reversed(rocks)))


def condense(rocks):
    return "".join("".join(row) for row in rocks)


def hydrate(rocks):
    return [[c for c in row] for row in rocks]


def solve_part2(data: str):
    input_data = parse_data(data)
    rocks = [[c for c in row] for row in input_data]

    l1_cache = {}
    l2_cache = {}

    l2_after = rocks.copy()
    l1_key = l2_key = None
    for _ in range(1_000_000_000):
        if _ % 1_000_000 == 0:
            print(f"  {_}")

        l2_before = l2_after
        if l2_key in l2_cache:
            l2_after = hydrate((l2_key := l2_cache[l2_key]))
        else:
            l1_after = l2_before
            for __ in range(4):
                l1_before = l1_after
                if l1_key in l1_cache:
                    l1_after = hydrate((l1_key := l1_cache[l1_key]))
                else:
                    l1_after = rotate(tilt(l1_before))
                    l1_cache[l1_key] = (l1_key := condense(l1_after))

            l2_after = l1_after
            l2_cache[l2_key] = (l2_key := condense(l2_after))

    print("\n".join("".join(row) for row in rocks))

    return None
