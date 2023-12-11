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


def solve_part1(data: str):
    input_data = parse_data(data)
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
    while step not in path:
        path.append(step)
        facing = TURN[board[step]][facing]
        step = step.neighbor(facing)

    return len(path) // 2


def solve_part2(data: str):
    input_data = parse_data(data)
    # print(input_data)

    return None
