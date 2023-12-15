from functools import reduce
from itertools import chain

from ..utils import parse_data


def hash_val(string):
    ords = chain([0], (ord(c) for c in string))
    return reduce(lambda a, b: (a + b) * 17 % 256, ords)


def solve_part1(data: str):
    input_data = parse_data(data)
    answer = sum(hash_val(step) for step in "".join(input_data).split(","))
    return answer


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
