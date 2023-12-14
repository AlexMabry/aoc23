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


def find_required(pattern):
    required, found, iter = set(), None, 0
    while iter < len(pattern):
        if pattern[iter] == "#":
            found = (found[0] if found else iter, iter + 1)
        elif found:
            required.add(found)
            found = None
        iter += 1

    return required


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


def in_bounds(hashes: tuple, ranges):
    return any(hashes[0] >= r[0] and hashes[1] <= r[1] for r in ranges)


def times_five(pattern, groups):
    return "?".join([pattern] * 5), [int(n) for n in ",".join([groups] * 5).split(",")]


def required_in_positions(required, positions):
    return {
        hashes: {ig for ig, ranges in positions.items() if in_bounds(hashes, ranges)}
        for hashes in required
    }


def solve_part2(data: str):
    input_data = parse_data(data, regex=r"([\.\?#]+) ([\d,]+)")
    answer = 0
    for pattern, groups in input_data:
        pattern, groups = times_five(pattern, groups)
        positions = find_positions(pattern, groups)
        required = find_required(pattern)

        before = tuple(len(p) for p in positions.values())
        after = 0
        while after != before:
            before = after

            for hashes, matches in required_in_positions(required, positions).items():
                if len(matches) == 1:
                    ig = matches.pop()
                    positions[ig] = {
                        p
                        for p in positions[ig]
                        if hashes[0] >= p[0] and hashes[1] <= p[1]
                    }

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

        value = [{p: 0 for p in positions[ig]} for ig in range(len(positions) - 1)]
        value.append({p: 1 for p in positions[len(positions) - 1]})

        for ig in range(len(positions) - 2, -1, -1):
            for p1 in positions[ig]:
                value[ig][p1] = sum(
                    value[ig + 1][p2] for p2 in positions[ig + 1] if p2[0] > p1[1]
                )

        answer += sum(value[0].values())

    print(answer)
    return None
