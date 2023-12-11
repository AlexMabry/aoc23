from itertools import combinations

from ..utils import parse_data


def solve(data, extra):
    input_data = parse_data(data)
    univ = [[char for char in line] for line in input_data]
    H, W = len(univ), len(univ[0])

    empty_cols = {i for i in range(W) if {univ[j][i] for j in range(H)} == {"."}}
    empty_rows = {i for i in range(H) if {univ[j][i] for j in range(W)} == {"."}}
    coords = [(i, j) for i in range(H) for j in range(W) if univ[i][j] == "#"]

    distance = 0
    for (ax, ay), (bx, by) in combinations(coords, 2):
        x_extra = len(set(range(min(ax, bx), max(ax, bx) + 1)) & empty_rows)
        y_extra = len(set(range(min(ay, by), max(ay, by) + 1)) & empty_cols)
        distance += abs(ax - bx) + abs(ay - by) + (x_extra + y_extra) * extra

    return distance


def solve_part1(data: str):
    return solve(data, 1)


def solve_part2(data: str):
    return solve(data, 999999)
