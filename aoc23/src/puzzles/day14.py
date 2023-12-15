from itertools import pairwise

from ..utils import parse_data


def tilt(rocks):
    before = []
    while before != rocks:
        before = rocks.copy()
        for a, b in pairwise(range(len(rocks))):
            rocks[a] = "".join(
                "*" if (ca, cb) == (".", "O") else ca
                for ca, cb in zip(rocks[a], rocks[b])
            )
            rocks[b] = "".join(
                "." if ca == "*" else cb for ca, cb in zip(rocks[a], rocks[b])
            )
            rocks[a] = "".join("O" if ca == "*" else ca for ca in rocks[a])
    return rocks


def weigh(rocks):
    return sum(
        (len(rocks) - i) * sum(1 for c in row if c == "O")
        for i, row in enumerate(rocks)
    )


def solve_part1(data: str):
    rocks = parse_data(data)

    return weigh(tilt(rocks))


def solve_part2(data: str):
    rocks = parse_data(data)

    pattern = []
    remaining = 1_000_000_000
    while remaining := remaining - 1:
        for _ in range(4):
            rocks = list(zip(*reversed(tilt(rocks))))

        if 10_000 < remaining <= 999_999_900:
            if not pattern:
                pattern = [hash(tuple(rocks))]
            elif (changed := hash(tuple(rocks))) != pattern[0]:
                pattern.append(changed)
            else:
                remaining = remaining % len(pattern) + 1

    return weigh(rocks)
