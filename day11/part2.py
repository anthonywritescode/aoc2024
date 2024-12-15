from __future__ import annotations

import argparse
import functools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@functools.cache
def _compute(n: int, m: int) -> int:
    if m == 0:
        return 1
    elif n == 0:
        return _compute(1, m - 1)
    elif len(str(n)) % 2 == 0:
        nstr = str(n)
        midp = len(nstr) // 2
        return (
            _compute(int(nstr[:midp]), m - 1) +
            _compute(int(nstr[midp:]), m - 1)
        )
    else:
        return _compute(2024 * n, m - 1)


def compute(s: str, *, iterations: int = 75) -> int:
    numbers = support.parse_numbers_split(s)

    return sum(_compute(n, iterations) for n in numbers)


INPUT_S = '''\
125 17
'''
EXPECTED = 55312


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, iterations=25) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
