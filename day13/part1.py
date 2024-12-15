from __future__ import annotations

import argparse
import os.path
import re
from typing import NamedTuple
from typing import Self

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

NUM = re.compile(r'X[+=](\d+), Y[+=](\d+)$')


def _nums(s: str) -> tuple[int, int]:
    match = NUM.search(s)
    assert match, s
    return int(match[1]), int(match[2])


class Game(NamedTuple):
    a: tuple[int, int]
    b: tuple[int, int]
    target: tuple[int, int]

    def solve(self) -> tuple[int, int] | None:
        x1, y1 = self.a
        x2, y2 = self.b
        x3, y3 = self.target

        """\
        A * 23 + B * 93 = 6993
          * 97     * 97 = * 97
        A * 97 + B * 12 = 2877
          * 23     * 23   * 23

        B * 93 * 97 - B * 12 * 23 = 6993 * 97 - 2877 * 23
        B * (93 * 97 - 12 * 23) = (6993 * 97 - 2877 * 23)
        B = (6993 * 97 - 2877 * 23) / (93 * 97 - 12 * 23)
        """

        # zero division???
        B = (x3 * y1 - y3 * x1) / (x2 * y1 - y2 * x1)
        if not B.is_integer() or B < 0:
            return None

        A = (x3 - B * x2) / x1
        if not A.is_integer() or A < 0:
            return None

        return int(A), int(B)

    @classmethod
    def parse(cls, s: str) -> Self:
        lines = s.splitlines()
        return cls(_nums(lines[0]), _nums(lines[1]), _nums(lines[2]))


def compute(s: str) -> int:
    total = 0
    for part in s.split('\n\n'):
        game = Game.parse(part)
        solution = game.solve()
        if solution is not None and all(p <= 100 for p in solution):
            a, b = solution
            total += 3 * a + b

    return total


INPUT_S = '''\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''
EXPECTED = 480


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
