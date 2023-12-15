from collections import defaultdict, OrderedDict
from functools import reduce
from itertools import chain

from ..utils import parse_data


def hash_val(string):
    ords = chain([0], (ord(c) for c in string))
    return reduce(lambda a, b: (a + b) * 17 % 256, ords)


def solve_part1(data: str):
    input_data = parse_data(data)
    return sum(hash_val(step) for step in "".join(input_data).split(","))


def solve_part2(data: str):
    input_data = parse_data(data)
    steps = "".join(input_data).replace("-", "=").split(",")
    commands = ([c for c in s.split("=") if c] for s in steps)

    boxes = defaultdict(OrderedDict)
    for cmd in commands:
        label = hash_val(cmd[0])
        if len(cmd) == 2:
            boxes[label][cmd[0]] = int(cmd[1])
        elif cmd[0] in boxes[label]:
            del boxes[label][cmd[0]]

    return sum(
        (ib + 1) * (il + 1) * focal
        for ib, box in boxes.items()
        for il, focal in enumerate(box.values())
    )
