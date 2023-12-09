from itertools import pairwise
from re import finditer

from ..utils import parse_data


def get_ranges(data):
    return [
        [int(g) for match in finditer(r"([\d-]+)", line) for g in match.groups()]
        for line in parse_data(data)
    ]


def decompose(rng):
    answer = 0
    while set(rng) != {0}:
        answer += rng[-1]
        rng = [b - a for a, b in pairwise(rng)]
    return answer


def solve_part1(data: str):
    ranges = get_ranges(data)
    return sum(decompose(rng) for rng in ranges)


def solve_part2(data: str):
    reversed_ranges = [list(reversed(rng)) for rng in get_ranges(data)]
    return sum(decompose(rng) for rng in reversed_ranges)
