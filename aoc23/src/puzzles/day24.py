from itertools import combinations

from ..utils import parse_data


def get_line(x, y, dx, dy):
    return dy / dx, y - (dy / dx * x)


def intersect(hs1, hs2):
    m1, b1 = get_line(*hs1)
    m2, b2 = get_line(*hs2)
    if m1 == m2:
        return None

    ix = (b2 - b1) / (m1 - m2)
    iy = (m2 * ix) + b2
    return ix, iy


def in_future(x, y, dx, dy, ix, iy):
    return (ix - x) / dx > 0 and (iy - y) / dy > 0


def solve_part1(data: str):
    # lower, upper = 7, 27
    input_data = parse_data(data, findall=r"-?\d+")
    numbers = [[int(n) for n in row] for row in input_data]
    hailstones = {(x, y, dx, dy) for x, y, _, dx, dy, _ in numbers}
    intersections = [
        (hs1, hs2)
        for (hs1), (hs2) in combinations(hailstones, 2)
        if (intersection := intersect(hs1, hs2))
        and all(200000000000000 <= i <= 400000000000000 for i in intersection)
        and all(in_future(*hs, *intersection) for hs in (hs1, hs2))
    ]
    return len(intersections)


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
