from ..utils import parse_data


def solve_part1(data: str):
    input_data = parse_data(data)
    digits = [[d for d in row if d.isdigit()] for row in input_data]
    numbers = [int(d[0] + d[-1]) for d in digits]

    return sum(numbers)


WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def replace_number_words(input_data, *, direction="left"):
    words = [
        sorted(
            (loc, word, str(num))
            for num, word in enumerate(WORDS)
            if (loc := row.find(word) if direction == "left" else row.rfind(word)) != -1
        )
        for row in input_data
    ]
    words = [(w[0][1], w[0][2]) if w else ("", "") for w in words]
    return [row.replace(word, num) for (word, num), row in zip(words, input_data)]


def solve_part2(data: str):
    input_data = parse_data(data)
    input_data = replace_number_words(input_data, direction="left")
    input_data = replace_number_words(input_data, direction="right")

    digits = [[d for d in row if d.isdigit()] for row in input_data]
    numbers = [int(d[0] + d[-1]) for d in digits]

    return sum(numbers)
