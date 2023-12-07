from dataclasses import dataclass
from itertools import groupby
from typing import List

from ..utils import parse_data


CARD_VALUES = {
    "*": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


@dataclass
class Hand:
    cards: List[str]
    bid: int
    jokers: bool = False
    values: List[int] = None

    def __post_init__(self):
        if self.jokers:
            self.cards = ["*" if c == "J" else c for c in self.cards]
        self.values = [CARD_VALUES[c] for c in self.cards]

    @property
    def strength(self):
        len_groups = len(list(groupby(sorted(self.cards))))
        max_group_len = max([len(list(g)) for _, g in groupby(sorted(self.cards))])
        joker_cnt = self.cards.count("*")
        match len_groups, max_group_len:
            case 5, 1:
                return 0 + joker_cnt
            case 4, 2:
                return 1 + joker_cnt
            case 3, 2:
                return 2 if not joker_cnt else 3 + joker_cnt
            case 3, 3:
                return 3 if not joker_cnt else 5
            case 2, 3:
                return 4 if not joker_cnt else 6
            case 2, 4:
                return 5 if not joker_cnt else 6
            case 1, 5:
                return 6

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
    input_data = parse_data(data)
    hands = sorted(
        [
            Hand([c for c in cards], int(bid), True)
            for cards, bid in [line.split(" ") for line in input_data]
        ]
    )

    return sum(hand.bid * (rank + 1) for rank, hand in enumerate(hands))
