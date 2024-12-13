from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PAT = re.compile(r"(?:(do|don't)\(\)|mul\((\d+),(\d+)\))")


def compute(s: str) -> int:
    total = 0
    enabled = True
    for parts in PAT.findall(s):
        match parts:
            case 'do', '', '':
                enabled = True
            case "don't", '', '':
                enabled = False
            case '', p1, p2:
                if enabled:
                    total += int(p1) * int(p2)
            case unreachable:
                raise AssertionError(unreachable)
    return total


INPUT_S = '''\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
'''
EXPECTED = 48


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
