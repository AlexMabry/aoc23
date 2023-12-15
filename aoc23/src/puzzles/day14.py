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


def diff(before, after):
    return tuple(
        (x, y)
        for y, (a, b) in enumerate(zip(before, after))
        for x, (ca, cb) in enumerate(zip(a, b))
        if ca != cb
    )


def solve_part1(data: str):
    input_data = parse_data(data)
    rocks = [[c for c in row] for row in input_data]
    rocks = tilt(rocks)
    return weigh(rocks)


def solve_part2(data: str):
    input_data = parse_data(data)
    rocks = [[c for c in row] for row in input_data]

    remaining = 1_000_000_001
    pattern = []
    while (remaining := remaining - 1) > 0:
        before = rocks.copy()
        for _ in range(4):
            rocks = list(zip(*reversed(tilt(rocks))))

        if 10_000 < remaining <= 999_999_900:
            if not pattern:
                pattern = [diff(before, rocks)]
            elif (changed := diff(before, rocks)) != pattern[0]:
                pattern.append(changed)
            else:
                remaining = remaining % len(pattern)

    return weigh(rocks)
