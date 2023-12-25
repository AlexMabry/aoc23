import re
from types import SimpleNamespace


def parse_data(
    input_data, *, is_lines=True, is_numbers=False, regex=None, findall=None
):
    lines = input_data.splitlines()
    if regex:
        pattern = re.compile(regex)
        if pattern.groupindex.keys():
            return [
                SimpleNamespace(**pattern.search(item).groupdict())
                for item in lines
                if item
            ]
        else:
            return [pattern.search(item).groups() for item in lines if item]
    elif findall:
        pattern = re.compile(findall)
        return [re.findall(pattern, item) for item in lines if item]

    if is_numbers:
        return [int(n) for n in lines]
    elif is_lines:
        return lines
    else:
        return input_data
