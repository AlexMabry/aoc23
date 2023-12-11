import re

from ..utils import parse_data


def get_games(input_data):
    games = [{"red": 0, "blue": 0, "green": 0} for _ in input_data]
    for game, row in zip(games, input_data):
        for r in re.match(r"Game \d+: (.*)", row).group(1).split("; "):
            for pull in r.split(", "):
                num, color = pull.split(" ")
                game[color] = max(int(num), game[color])

    return games


def solve_part1(data: str):
    input_data = parse_data(data)
    games = get_games(input_data)

    return sum(
        [
            i + 1
            for i, g in enumerate(games)
            if g["red"] <= 12 and g["green"] <= 13 and g["blue"] <= 14
        ]
    )


def solve_part2(data: str):
    input_data = parse_data(data)
    games = get_games(input_data)

    return sum([g["red"] * g["green"] * g["blue"] for g in games])
