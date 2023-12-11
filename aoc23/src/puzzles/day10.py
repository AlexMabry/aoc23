from ..utils import parse_data, Point

ALLOWED = {
    "N": ("|", "F", "7"),
    "S": ("|", "J", "L"),
    "E": ("-", "7", "J"),
    "W": ("-", "F", "L"),
}

TURN = {
    "|": {"N": "N", "S": "S"},
    "-": {"E": "E", "W": "W"},
    "F": {"N": "E", "W": "S"},
    "7": {"N": "W", "E": "S"},
    "J": {"S": "W", "E": "N"},
    "L": {"S": "E", "W": "N"},
}


def find_path(input_data):
    board = {
        Point(x, y): char
        for y, row in enumerate(input_data)
        for x, char in enumerate(row)
    }
    start = next(k for k, v in board.items() if v == "S")
    facing, step = next(
        (direction, point)
        for direction, point in start.cardinal_neighbors().items()
        if point in board and board[point] in ALLOWED[direction]
    )

    path = [start]
    turns = [facing]
    while step not in path:
        path.append(step)
        facing = TURN[board[step]][facing]
        turns.append(facing)
        step = step.neighbor(facing)

    return path, turns


def solve_part1(data: str):
    input_data = parse_data(data)
    path, turns = find_path(input_data)

    return len(path) // 2


def solve_part2(data: str):
    input_data = parse_data(data)
    path, turns = find_path(input_data)

    # expand the board by a factor of 2
    H, W = len(input_data) * 2, len(input_data[0]) * 2
    expanded = {Point(x, y) for y in range(H) for x in range(W)}

    # remove the path and the turns
    expanded_path = set().union(
        step
        for point, facing in zip(path, turns)
        for step in (point * 2, (point * 2).neighbor(facing))
    )
    expanded -= expanded_path

    # remove the outside until there is no more outside
    outside = {p for p in expanded if p.x in [0, W - 1] or p.y in [0, H - 1]}
    while len(outside):
        expanded -= outside
        outside = {n for p in outside for n in p.cardinal_neighbors().values()}
        outside &= expanded

    # contract the board by a factor of 2
    contracted = {Point(x, y) for y in range(0, H, 2) for x in range(0, W, 2)}
    trapped = expanded & contracted

    return len(trapped)
