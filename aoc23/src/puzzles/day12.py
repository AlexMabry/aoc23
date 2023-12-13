from itertools import zip_longest, combinations_with_replacement, permutations, islice
from functools import reduce

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


def window(seq, n=2):
    """Returns a sliding window (of width n) over data from the iterable"""
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def find_positions(pattern, groups):
    positions = {ig: set() for ig in range(len(groups))}
    for ig, g in enumerate(groups):
        min_start = sum(groups[:ig]) - len(groups[:ig])
        min_end = len(pattern) - sum(groups[ig + 1 :]) - len(groups[ig + 1 :])

        for iw, win in enumerate(window(pattern[min_start : min_end + 1], g)):
            start, end = min_start + iw, min_start + iw + g
            dots = "." in win
            hash_after = end < len(pattern) and pattern[end] == "#"
            hash_before = start > 0 and pattern[start - 1] == "#"

            if not dots and not hash_after and not hash_before:
                positions[ig].add((start, end))

    return positions


def times_five(pattern, groups):
    return "?".join([pattern] * 5), [int(n) for n in ",".join([groups] * 5).split(",")]


def solve_part2(data: str):
    input_data = parse_data(TEST_DATA, regex=r"([\.\?#]+) ([\d,]+)")
    answer = 0
    for pattern, groups in input_data[-1:]:
        pattern, groups = times_five(pattern, groups)
        positions = find_positions(pattern, groups)
        before = tuple(len(p) for p in positions.values())
        after = 0
        while after != before:
            before = after
            for ig in range(1, len(positions)):
                smallest = min(r[0] for r in positions[ig - 1])
                positions[ig] = {p for p in positions[ig] if p[0] > smallest}

            for ig in range(len(positions) - 1):
                largest = max(r[0] for r in positions[ig + 1])
                positions[ig] = {p for p in positions[ig] if largest > p[1]}

            for ig in range(1, len(positions)):
                smallest = min(r[1] for r in positions[ig - 1])
                positions[ig] = {p for p in positions[ig] if p[0] > smallest}

            for ig in range(len(positions) - 1):
                largest = max(r[1] for r in positions[ig + 1])
                positions[ig] = {p for p in positions[ig] if largest > p[1]}

            after = tuple(len(p) for p in positions.values())

        print(pattern)
        for ig, pos in positions.items():
            for p in pos:
                print(ig, p, pattern[p[0] : p[1]])
        print(reduce(lambda x, y: x * y, (len(p) for p in positions.values())))

    print(answer)
    return None


TEST_DATA = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
