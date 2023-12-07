from dataclasses import dataclass
from itertools import groupby
from typing import List

from ..utils import parse_data


HANDS = {
    (5, 1, 0): 0,
    (5, 1, 1): 1,
    (4, 2, 0): 1,
    (4, 2, 1): 3,
    (4, 2, 2): 3,
    (3, 2, 0): 2,
    (3, 2, 1): 4,
    (3, 2, 2): 5,
    (3, 3, 0): 3,
    (3, 3, 1): 5,
    (3, 3, 3): 5,
    (2, 3, 0): 4,
    (2, 3, 2): 6,
    (2, 3, 3): 6,
    (2, 4, 0): 5,
    (2, 4, 1): 6,
    (2, 4, 4): 6,
    (1, 5, 0): 6,
    (1, 5, 5): 6
}

CARD_VALUES = "*23456789TJQKA"


@dataclass
class Hand:
    cards: List[str]
    bid: int
    strength: int = None
    values: List[int] = None

    def __post_init__(self):
        groups = [[c for c in b] for a, b in groupby(sorted(self.cards))]
        self.strength = HANDS[(len(groups), max([len(g) for g in groups]), self.cards.count("*"))]
        self.values = [CARD_VALUES.index(c) for c in self.cards]

    def __lt__(self, other):
        if self.strength == other.strength:
            for v1, v2 in zip(self.values, other.values):
                if v1 != v2:
                    return v1 < v2

        return self.strength < other.strength


def solve_part1(data: str):
    input_data = parse_data(data)
    hands = sorted(
        [
            Hand([c for c in cards], int(bid))
            for cards, bid in [line.split(" ") for line in input_data]
        ]
    )

    return sum(hand.bid * (rank + 1) for rank, hand in enumerate(hands))


def solve_part2(data: str):
    return solve_part1(data.replace('J', '*'))
