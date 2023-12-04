import re

from ..utils import parse_data

CARD = r"Card\s+\d+: ([\d\s]+)\s+\|\s+([\d\s]+)"


def get_winning_numbers(data):
    input_data = parse_data(data)
    cards = [match.groups() for row in input_data for match in re.finditer(CARD, row)]
    numbers = [[{int(n) for n in side.split()} for side in sides] for sides in cards]
    return [len(winner & player) for [winner, player] in numbers]


def solve_part1(data: str):
    winning_numbers = get_winning_numbers(data)
    points = [2 ** (count - 1) for count in winning_numbers if count]
    return sum(points)


def solve_part2(data: str):
    winning_numbers = get_winning_numbers(data)
    counts = {n + 1: count for n, count in enumerate(winning_numbers)}
    copies = {n + 1: 1 for n in range(len(counts))}

    for card in range(1, len(counts) + 1):
        for winner in range(card + 1, card + 1 + counts[card]):
            copies[winner] += copies[card]

    return sum(copies.values())
