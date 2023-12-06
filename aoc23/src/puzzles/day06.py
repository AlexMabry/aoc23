import re

from ..utils import parse_data


def solve_part1(data: str):
    input_data = parse_data(data)
    rows = [map(int, re.findall(r"(\d+)", line)) for line in input_data]
    result = 1
    for time, dist in zip(*rows):
        result *= sum(1 for tick in range(1, time) if tick * (time - tick) > dist)

    return result


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
