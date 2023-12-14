from itertools import pairwise

from ..utils import parse_data


def fold_iter(puzzle, fold):
    return (
        (puzzle[fold - i], puzzle[fold + i + 1])
        for i in range(1, fold + 1)
        if fold + i + 1 < len(puzzle)
    )


def is_valid_fold(puzzle, fold):
    return all(a == b for a, b in fold_iter(puzzle, fold))


def is_valid_smudge(puzzle, fold):
    return (
        sum(
            1 if one_off(a, b) else -100 if a != b else 0
            for a, b in fold_iter(puzzle, fold)
        )
        == 1
    )


def one_off(a, b):
    return sum(1 for ca, cb in zip(a, b) if ca != cb) == 1


def find_smudge_mid(puzzle):
    return (fold for fold, (a, b) in enumerate(pairwise(puzzle)) if one_off(a, b))


def find_fold_mid(puzzle):
    return (fold for fold, (a, b) in enumerate(pairwise(puzzle)) if a == b)


def valid_smudges(puzzles):
    return sum(
        f + 1 for p in puzzles for f in find_smudge_mid(p) if is_valid_fold(p, f)
    ) + sum(f + 1 for p in puzzles for f in find_fold_mid(p) if is_valid_smudge(p, f))


def valid_folds(puzzles):
    return sum(f + 1 for p in puzzles for f in find_fold_mid(p) if is_valid_fold(p, f))


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
    transposed = [transpose(puz) for puz in puzzles]

    return valid_folds(puzzles) * 100 + valid_folds(transposed)


def solve_part2(data: str):
    input_data = parse_data(data)
    puzzles = get_puzzles(input_data)
    transposed = [transpose(puz) for puz in puzzles]

    return valid_smudges(puzzles) * 100 + valid_smudges(transposed)
