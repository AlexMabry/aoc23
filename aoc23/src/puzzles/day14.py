from itertools import pairwise

from ..utils import parse_data


def tilt(rocks):
    before = []
    while before != rocks:
        before = rocks.copy()
        for a, b in pairwise(range(len(rocks))):
            rocks[a] = [
                "*" if (ca, cb) == (".", "O") else ca
                for ca, cb in zip(rocks[a], rocks[b])
            ]
            rocks[b] = ["." if ca == "*" else cb for ca, cb in zip(rocks[a], rocks[b])]
            rocks[a] = ["O" if ca == "*" else ca for ca in rocks[a]]
    return rocks


def weigh(rocks):
    return sum(
        (len(rocks) - i) * sum([1 for c in row if c == "O"])
        for i, row in enumerate(rocks)
    )


def solve_part1(data: str):
    input_data = parse_data(data)
    rocks = [[c for c in row] for row in input_data]

    return weigh(tilt(rocks))


def solve_part2(data: str):
    input_data = parse_data(data)
    rocks = [[c for c in row] for row in input_data]

    pattern = []
    remaining = 1_000_000_000
    while remaining := remaining - 1:
        for _ in range(4):
            rocks = list(zip(*reversed(tilt(rocks))))

        if 10_000 < remaining <= 999_999_900:
            if not pattern:
                pattern = [hash(tuple(str(row) for row in rocks))]
            elif (changed := hash(tuple(str(row) for row in rocks))) != pattern[0]:
                pattern.append(changed)
            else:
                remaining = remaining % len(pattern) + 1

    return weigh(rocks)
