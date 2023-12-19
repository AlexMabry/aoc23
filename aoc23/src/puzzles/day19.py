import operator
import re

from ..utils import parse_data

RULES = r"(?P<cat>[xmas])(?P<l_g>.)(?P<val>\d+):(?P<tar>[a-zAR]+)|(?P<def>[a-zAR]+)"
WORKFLOW = r"([a-z]+)\{(.*)"
RATING = r"\{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)\}"


def get_system(input_data):
    blank = input_data.index("")
    return {
        g[0]: [re.match(RULES, rule).groupdict() for rule in g[1].split(",")]
        for row in input_data[:blank]
        if (g := re.match(WORKFLOW, row).groups())
    }, [
        {k: int(v) for k, v in rating.items()}
        for row in input_data[blank + 1 :]
        if (rating := re.match(RATING, row).groupdict())
    ]


def evaluate_rule(rule: dict, part: dict):
    if rule["def"]:
        return rule["def"]

    compare = operator.gt if rule["l_g"] == ">" else operator.lt
    result = compare(part[rule["cat"]], int(rule["val"]))
    return rule["tar"] if result else None


def check_part(part, workflows):
    current = "in"
    while current not in ["A", "R"]:
        rules = workflows[current].copy()
        while (current := evaluate_rule(rules.pop(0), part)) is None:
            pass

    return sum(part.values()) if current == "A" else 0


def solve_part1(data: str):
    input_data = parse_data(data)
    workflows, parts = get_system(input_data)
    return sum(check_part(part, workflows) for part in parts)


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
