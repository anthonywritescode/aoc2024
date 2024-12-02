from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _is_safe(nums: list[int]) -> bool:
    if nums[1] < nums[0]:
        direction = -1
    else:
        direction = 1

    for n1, n2 in zip(nums, nums[1:]):
        diff = direction * (n2 - n1)
        if not (1 <= diff <= 3):
            return False
    else:
        return True


def compute(s: str) -> int:
    return sum(
        _is_safe(support.parse_numbers_split(line))
        for line in s.splitlines()
    )


INPUT_S = '''\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''
EXPECTED = 2


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
