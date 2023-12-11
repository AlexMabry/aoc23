import re
from itertools import product

from ..utils import parse_data


def solve_part1(data: str):
    input_data = parse_data(data)

    covered = {
        (x + i, y + j)
        for y, row in enumerate(input_data)
        for x, c in enumerate(row)
        for (i, j) in product(range(-1, 2), range(-1, 2))
        if c in {"*", "#", "%", "-", "=", "$", "&", "@", "/", "+"}
    }

    total = sum(
        int(match[0])
        for y, row in enumerate(input_data)
        for match in re.finditer(r"\d+", row)
        if covered & {(x, y) for x in range(match.start(), match.end())}
    )

    return total


def solve_part2(data: str):
    input_data = parse_data(data)

    gears = {
        (x.start(), y)
        for y, row in enumerate(input_data)
        for x in re.finditer(r"\*", row)
    }

    total = 0
    for x, y in gears:
        covered = {(x + i, y + j) for (i, j) in product(range(-1, 2), range(-1, 2))}

        nums = [
            int(match[0])
            for yy in range(max(0, y - 1), min(len(input_data), y + 2))
            for match in re.finditer(r"\d+", input_data[yy])
            if covered & {(x, y) for x in range(match.start(), match.end())}
        ]

        if len(nums) == 2:
            total += nums[0] * nums[1]

    return total
