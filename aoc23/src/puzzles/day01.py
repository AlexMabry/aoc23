from ..utils import parse_data


def solve_part1(data: str):
    input_data = parse_data(data)
    digits = [[d for d in row if d.isdigit()] for row in input_data]
    numbers = [int(d[0] + d[-1]) for d in digits]

    return sum(numbers)


WORDS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def solve_part2(data: str):
    input_data = parse_data(data)

    left = [
        sorted(
            (loc, word, num)
            for word, num in WORDS.items()
            if (loc := row.find(word)) != -1
        )
        for row in input_data
    ]
    left = [(lwords[0][1], lwords[0][2]) if lwords else ("", "") for lwords in left]
    input_data = [row.replace(word, num) for (word, num), row in zip(left, input_data)]

    right = [
        sorted(
            (loc, word, num)
            for word, num in WORDS.items()
            if (loc := row.rfind(word)) != -1
        )
        for row in input_data
    ]
    right = [(rwords[0][1], rwords[0][2]) if rwords else ("", "") for rwords in right]
    input_data = [row.replace(word, num) for (word, num), row in zip(right, input_data)]

    digits = [[d for d in row if d.isdigit()] for row in input_data]
    numbers = [int(d[0] + d[-1]) for d in digits]

    return sum(numbers)
