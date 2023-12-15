from ..utils import parse_data


def solve_part1(data: str):
    input_data = parse_data(data)

    answer = 0
    for step in "".join(input_data).split(","):
        current_value = 0
        for c in step:
            current_value = ((current_value + ord(c)) * 17) % 256

        answer += current_value

    return answer


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
