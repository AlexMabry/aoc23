from itertools import pairwise

from ..utils import parse_data


def is_valid(puzzle, fold):
    return all(
        puzzle[fold - i] == puzzle[fold + i + 1]
        for i in range(1, fold + 1)
        if len(puzzle) - i - 1 > fold >= i
    )


def find_folds(puzzle):
    return (fold for fold, (i, j) in enumerate(pairwise(puzzle)) if i == j)


def valid_folds(puzzles):
    return (f + 1 for p in puzzles for f in find_folds(p) if is_valid(p, f))


def transpose(p):
    return ["".join(row[i] for row in p) for i in range(len(p[0]))]


def get_puzzles(input_data):
    puzzles = []
    while input_data:
        puzzles.append([])
        while input_data and (row := input_data.pop(0)):
            puzzles[-1].append(row)

    return puzzles


def solve_part1(data: str):
    input_data = parse_data(data)
    puzzles = get_puzzles(input_data)
    transposed = (transpose(puz) for puz in puzzles)

    return sum(valid_folds(puzzles)) * 100 + sum(valid_folds(transposed))


def solve_part2(data: str):
    return None
