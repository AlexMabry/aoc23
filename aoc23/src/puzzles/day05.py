import re
from itertools import pairwise, batched
from typing import NamedTuple

from ..utils import parse_data


class Range(NamedTuple):
    start: int
    end: int

    def __contains__(self, value):
        return self.start <= value < self.end


class Transform(NamedTuple):
    range: Range
    offset: int

    @classmethod
    def from_row(cls, row):
        dst, src, rlen = map(int, row.split())
        return Transform(Range(src, src + rlen), dst - src)

    def __contains__(self, r):
        return r.start in self.range or r.end - 1 in self.range


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
            seed = next((seed + t.offset for t in xforms if seed in t.range), seed)
        lowest = min(lowest, seed)

    return lowest


def solve_part2(data: str):
    input_data = parse_data(data)
    seeds_match = re.match(r"seeds:\s+((\d+\s?)+)", input_data[0])
    seeds = map(int, seeds_match.group(1).split())
    map_xforms = parse_map_xforms(input_data)
    ranges = [Range(a, a + b) for a, b in batched(seeds, 2)]
    for xforms in map_xforms:
        result = []
        while ranges and (r := ranges.pop(0)):
            if match := next((t for t in xforms if r in t), None):
                result.append(
                    Range(
                        max(r.start, match.range.start) + match.offset,
                        min(r.end, match.range.end) + match.offset,
                    )
                )
                if r.start < match.range.start:
                    ranges.append(Range(r.start, match.range.start))
                if r.end > match.range.end:
                    ranges.append(Range(match.range.end, r.end))
            else:
                result.append(r)

        ranges = result

    return min(r.start for r in ranges)
