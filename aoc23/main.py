import importlib
import sys
from datetime import datetime
from pathlib import Path

from aocd.models import Puzzle
from jinja2 import Environment, FileSystemLoader

YEAR = 2023
START_DAY = 1
END_DAY = 25

PACKAGE = __name__.split(".")[0]


def get_puzzle(day):
    # Dynamically import the day's module
    module_name = f".src.puzzles.day{day:02d}"
    day_module = importlib.import_module(module_name, package=PACKAGE)

    # Fetching data using advent-of-code-data library
    puzzle = Puzzle(year=YEAR, day=int(day))  # Replace 2023 with the actual year
    print(f"{YEAR} Day {day}:")
    return day_module, puzzle


def solve_day(day):
    day_module, puzzle = get_puzzle(day)

    if not puzzle.answered_a:
        answer_a = day_module.solve_part1(puzzle.input_data)
        print(f"  Part 1: {answer_a}")
        puzzle.answer_a = answer_a

    elif not puzzle.answered_b:
        answer_b = day_module.solve_part2(puzzle.input_data)
        print(f"  Part 1: {puzzle.answer_a}")
        print(f"  Part 2: {answer_b}")
        puzzle.answer_b = answer_b

    else:
        print("Already answered!")
        print(f"Part 1")
        print(f"  submitted: {puzzle.answer_a}")
        print(f"  rerunning: {day_module.solve_part1(puzzle.input_data)}")
        print("")
        print(f"Part 2")
        print(f"  submitted: {puzzle.answer_b}")
        print(f"  rerunning: {day_module.solve_part2(puzzle.input_data)}")


def test_day(day):
    day_module, puzzle = get_puzzle(day)

    for i, example in enumerate(puzzle.examples):
        print(f"Example {i}:")

        if not puzzle.answered_a:
            answer = day_module.solve_part1(example.input_data)
            print(f"  Part 1: {answer}")
            if not example.answer_a:
                print(f"  Answer: {example.answer_a}")
                assert str(answer) == example.answer_a, "Part 1 answer does not match"
            else:
                print(f"  Missing part 1 answer")

        elif not puzzle.answered_b:
            answer = day_module.solve_part2(example.input_data)
            print(f"  Part 2: {answer}")
            if not example.answer_b:
                print(f"  Answer: {example.answer_b}")
                assert str(answer) == example.answer_b, "Part 2 answer does not match"
            else:
                print(f"  Missing part 2 answer")

        else:
            print("   Already answered:")
            print(f"  Part 1: {puzzle.answer_a}")
            print(f"  Part 2: {puzzle.answer_b}")


def solve():
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        _day = int(sys.argv[1])
    else:
        _day = datetime.today().day

    solve_day(_day)


def test():
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        _day = int(sys.argv[1])
    else:
        _day = datetime.today().day

    test_day(_day)


def generate():
    cwd = Path.cwd()

    src_dir = cwd / PACKAGE / "src"
    src_dir.mkdir(exist_ok=True)

    puzzle_dir = src_dir / "puzzles"
    puzzle_dir.mkdir(exist_ok=True)

    puzzle_init = puzzle_dir / "__init__.py"
    puzzle_init.touch()

    loader = FileSystemLoader(cwd / PACKAGE / "templates")
    env = Environment(loader=loader)
    template = env.get_template("aocd_problem.j2")

    for day in range(START_DAY, (END_DAY + 1), 1):
        day_py = puzzle_dir / f"day{day:02}.py"
        day_py.touch()
        day_py.write_text(template.render() + "\n")
