from __future__ import annotations

import argparse
import operator
import os.path
from collections.abc import Callable
from collections.abc import Generator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def cat(n1: int, n2: int) -> int:
    return int(f'{n1}{n2}')


def _operators(n: int) -> Generator[tuple[Callable[[int, int], int], ...]]:
    if n == 0:
        yield ()
    else:
        for rest in _operators(n - 1):
            yield (operator.add, *rest)
            yield (operator.mul, *rest)
            yield (cat, *rest)


def _possible(target: int, nums: list[int]) -> bool:
    for opcomb in _operators(len(nums) - 1):
        val = nums[0]
        for i, op in enumerate(opcomb):
            val = op(val, nums[i + 1])
            if val > target:
                break
        if val == target:
            return True
    else:
        return False


def compute(s: str) -> int:
    total = 0
    for line in s.splitlines():
        target_s, rest = line.split(': ')
        target = int(target_s)
        nums = support.parse_numbers_split(rest)

        if _possible(target, nums):
            total += target

    return total


INPUT_S = '''\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''
EXPECTED = 11387


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
