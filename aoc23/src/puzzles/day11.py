from itertools import combinations

import numpy as np

from ..utils import parse_data
import pandas as pd


def duplicate_rows(universe):
    for row in reversed(np.nonzero(universe.eq(".", axis=0).all(axis=1))[0]):
        if row == 0:
            universe = pd.concat([universe.iloc[0], universe], ignore_index=True)
        elif row == universe.shape[0] - 1:
            universe.append(universe.iloc[-1])
        else:
            universe = pd.concat(
                [
                    universe.iloc[:row],
                    universe.iloc[row : row + 1],
                    universe.iloc[row:],
                ],
                ignore_index=True,
            )
    universe.sort_index()
    return universe


def duplicate_columns(universe):
    for col in reversed(np.nonzero(universe.eq(".", axis=1).all(axis=0))[0]):
        if col == 0:
            universe = pd.concat(
                [universe.iloc[:, 0], universe], axis=1, ignore_index=True
            )
        elif col == universe.shape[1] - 1:
            universe.append(universe.iloc[:, -1])
        else:
            universe = pd.concat(
                [
                    universe.iloc[:, :col],
                    universe.iloc[:, col : col + 1],
                    universe.iloc[:, col:],
                ],
                axis=1,
                ignore_index=True,
            )
    universe.sort_index()
    return universe


def solve_part1(data: str):
    input_data = parse_data(data)
    universe = pd.DataFrame([[char for char in line] for line in input_data])

    universe = duplicate_rows(universe)
    universe = duplicate_columns(universe)
    stars = np.where(universe.eq("#"))
    coords = [(x, y) for x, y in zip(stars[0], stars[1])]

    distance = 0
    for a, b in combinations(coords, 2):
        distance += abs(a[0] - b[0]) + abs(a[1] - b[1])

    return distance


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
