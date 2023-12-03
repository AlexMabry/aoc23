import re

from ..utils import parse_data


def solve_part1(data: str):
    input_data = parse_data(data)

    total = 0
    for i, game in enumerate(input_data):
        high = {"red": 0, "blue": 0, "green": 0}

        for round in re.match(r"Game \d+: (.*)", game).group(1).split("; "):
            for pull in round.split(", "):
                [num, color] = pull.split(" ")
                high[color] = max(int(num), high[color])

        if high["red"] <= 12 and high["green"] <= 13 and high["blue"] <= 14:
            total += i + 1

    return total


def solve_part2(data: str):
    input_data = parse_data(data)

    total = 0
    for i, game in enumerate(input_data):
        high = {"red": 0, "blue": 0, "green": 0}

        for round in re.match(r"Game \d+: (.*)", game).group(1).split("; "):
            for pull in round.split(", "):
                [num, color] = pull.split(" ")
                high[color] = max(int(num), high[color])

        total += high["red"] * high["green"] * high["blue"]

    return total
