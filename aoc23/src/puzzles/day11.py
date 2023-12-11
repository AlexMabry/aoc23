from itertools import combinations

from ..utils import parse_data


def solve(data, extra):
    input_data = parse_data(data)
    univ = [[char for char in line] for line in input_data]
    H, W = len(univ), len(univ[0])

    empty_cols = {i for i in range(W) if {univ[j][i] for j in range(H)} == {"."}}
    empty_rows = {i for i in range(H) if all(univ[i][j] == "." for j in range(W))}
    coords = [(i, j) for i in range(H) for j in range(W) if univ[i][j] == "#"]

    distance = 0
    for a, b in combinations(coords, 2):
        x_extra = len(set(range(min(a[0], b[0]), max(a[0], b[0]) + 1)) & empty_rows)
        y_extra = len(set(range(min(a[1], b[1]), max(a[1], b[1]) + 1)) & empty_cols)
        distance += abs(a[0] - b[0]) + abs(a[1] - b[1]) + (x_extra + y_extra) * extra

    return distance


def solve_part1(data: str):
    return solve(data, 1)


def solve_part2(data: str):
    return solve(data, 999999)
