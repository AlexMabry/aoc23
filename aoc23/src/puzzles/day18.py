from itertools import pairwise, groupby, batched

from ..utils import parse_data


def steps(x, y, direction, distance):
    return [
        ((x, y) for y in range(y + 1, y + distance + 1)),  # U
        ((x, y) for y in range(y - 1, y - distance - 1, -1)),  # D
        ((x, y) for x in range(x - 1, x - distance - 1, -1)),  # L
        ((x, y) for x in range(x + 1, x + distance + 1)),  # R
    ]["UDLR".index(direction)]


def ranges(i):
    for a, b in groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]


def neighbors(x, y):
    return {(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)}


def solve_part1(data: str):
    input_data = parse_data(data, regex=r"([UDLR]) (\d+) ..([0-9a-f]{6}).")
    trench = [(0, 0)]
    for direction, distance, color in input_data:
        x, y = trench[-1]
        trench.extend(steps(x, y, direction, int(distance)))

    trench = set(trench)

    xrange, yrange = [range(min(coord), max(coord) + 1) for coord in zip(*trench)]
    xbounds, ybounds = (min(xrange), max(xrange)), (min(yrange), max(yrange))

    remnant = {(x, y) for y in yrange for x in xrange} - trench
    outside = {(x, y) for (x, y) in remnant if x in xbounds or y in ybounds}

    while len(outside):
        remnant -= outside
        outside = {nbr for (x, y) in outside for nbr in neighbors(x, y)} & remnant

    return len(remnant | trench)


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
