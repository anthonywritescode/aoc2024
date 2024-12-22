from __future__ import annotations

import argparse
import collections
import os.path
from collections.abc import Generator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _compute(x: int, *, n: int) -> Generator[tuple[int, int]]:
    prev = x % 10
    for _ in range(n):
        x ^= (x * 64)
        x %= 16777216
        x ^= (x // 32)
        x %= 16777216
        x ^= (x * 2048)
        x %= 16777216

        ones = x % 10
        yield ones - prev, ones
        prev = ones


def _banans(x: int) -> dict[tuple[int, ...], int]:
    ret: dict[tuple[int, ...], int] = {}
    window4: collections.deque[int] = collections.deque(maxlen=4)
    for delta, val in _compute(x, n=2000):
        window4.append(delta)
        if len(window4) == 4:
            ret.setdefault(tuple(window4), val)
    return ret


def compute(s: str) -> int:
    total = 0
    numbers = support.parse_numbers_split(s)
    banans = [_banans(n) for n in numbers]
    best = 0
    all_keys: set[tuple[int, ...]] = set()
    for dct in banans:
        all_keys |= dct.keys()

    best = 0
    for k in all_keys:
        total = sum(banan.get(k, 0) for banan in banans)
        best = max(total, best)

    return best


INPUT_S = '''\
1
2
3
2024
'''
EXPECTED = 23


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
