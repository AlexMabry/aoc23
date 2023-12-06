import re
from itertools import pairwise
from typing import NamedTuple

from ..utils import parse_data


class Transform(NamedTuple):
    start: int
    end: int
    offset: int

    @classmethod
    def from_row(cls, row):
        dst, src, rlen = map(int, row.split())
        return Transform(src, src + rlen - 1, dst - src)

    def __contains__(self, value):
        return self.start <= value <= self.end


def parse_map_xforms(input_data):
    input_data.extend(["", "map:"])
    map_lines = [n for n, row in enumerate(input_data) if row.endswith("map:")]
    map_sections = [input_data[i + 1 : j - 1] for i, j in pairwise(map_lines)]
    return [[Transform.from_row(row) for row in section] for section in map_sections]


def solve_part1(data: str):
    input_data = parse_data(data)
    seeds_match = re.match(r"seeds:\s+((\d+\s?)+)", input_data[0])
    seeds = map(int, seeds_match.group(1).split())
    map_xforms = parse_map_xforms(input_data)

    lowest = float("inf")
    for seed in seeds:
        for xforms in map_xforms:
            seed = next((seed + t.offset for t in xforms if seed in t), seed)
        lowest = min(lowest, seed)

    return lowest


def solve_part2(data: str):
    input_data = parse_data(data)

    return None
