from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _compute(x: int, *, n: int) -> int:
    for _ in range(n):
        x ^= (x * 64)
        x %= 16777216
        x ^= (x // 32)
        x %= 16777216
        x ^= (x * 2048)
        x %= 16777216
    return x


def compute(s: str) -> int:
    total = 0
    numbers = support.parse_numbers_split(s)
    for n in numbers:
        total += _compute(n, n=2000)
    return total


INPUT_S = '''\
1
10
100
2024
'''
EXPECTED = 37327623


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
