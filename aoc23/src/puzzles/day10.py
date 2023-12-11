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

    rows = len(input_data) * 2 - 1
    cols = len(input_data[1]) * 2 - 1
    large_grid = {Point(x, y) for y in range(rows) for x in range(cols)}

    path = [start]
    grid_step = start * 2
    grid_path = {grid_step, grid_step.neighbor(facing)}
    while step not in path:
        path.append(step)
        facing = TURN[board[step]][facing]

        grid_step = step * 2
        grid_path |= {grid_step, grid_step.neighbor(facing)}

        step = step.neighbor(facing)

    new_outside = set(
        Point(x, y)
        for y in range(rows)
        for x in range(cols)
        if x == 0 or y == 0 or x == cols - 1 or y == rows - 1
    )
    new_outside -= grid_path
    outside = set()

    while len(new_outside):
        outside |= new_outside
        new_outside = set().union(
            n
            for point in new_outside
            for n in point.cardinal_neighbors().values()
            if n in large_grid
        )
        new_outside -= outside
        new_outside -= grid_path

    large_grid -= outside
    large_grid -= grid_path

    small_grid = {Point(x, y) for y in range(0, rows, 2) for x in range(0, cols, 2)}

    return len(small_grid & large_grid)
