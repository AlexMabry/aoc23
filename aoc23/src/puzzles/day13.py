from itertools import pairwise

from ..utils import parse_data


def find_fold(chars: [str]):
    return next(
        (
            p + 1
            for p, (i, j) in enumerate(pairwise(chars))
            if i == j
            and all(
                chars[p - i] == chars[p + i + 1]
                for i in range(p + 1)
                if len(chars) - i - 1 > p >= i
            )
        ),
        0,
    )


def solve_part1(data: str):
    by_row = []

    input_data = parse_data(data)
    while input_data:
        by_row.append([])
        while input_data and (row := input_data.pop(0)):
            by_row[-1].append(row)

    by_col = [["".join(row[i] for row in p) for i in range(len(p[0]))] for p in by_row]

    return sum(find_fold(r) * 100 + find_fold(c) for r, c in zip(by_row, by_col))


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
