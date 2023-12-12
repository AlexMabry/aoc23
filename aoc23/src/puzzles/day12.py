from itertools import zip_longest, combinations_with_replacement, permutations

from ..utils import parse_data


def get_bounds(num, total):
    return {
        tuple(p)
        for t in combinations_with_replacement(range(total - num + 4), num)
        for p in permutations(t)
        if sum(t) == total and all(v for v in tuple(p)[1:-1])
    }


def is_valid(dots, hashes, hash_cnt, dot_cnt):
    blanks, springs = set(), set()

    itr = 0
    for b, s in zip_longest(hash_cnt, dot_cnt, fillvalue=0):
        blanks |= set(range(itr, itr + b))
        springs |= set(range(itr + b, itr + b + s))
        itr += b + s

    return dots.issubset(blanks) and hashes.issubset(springs)


def solve_part1(data: str):
    input_data = parse_data(data, regex=r"([\.\?#]+) ([\d,]+)")

    answer = 0
    for i, (pattern, groups) in enumerate(input_data):
        dots = {i for i, c in enumerate(pattern) if c == "."}
        hashes = {i for i, c in enumerate(pattern) if c == "#"}
        springs = list(map(int, groups.split(",")))
        num, total = len(springs) + 1, len(pattern) - sum(springs)
        arrangements = get_bounds(num, total)
        answer += sum(1 for arr in arrangements if is_valid(dots, hashes, springs, arr))

    return answer


def solve_part2(data: str):
    input_data = parse_data(data)

    return None
