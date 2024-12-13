from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    total = 0
    lines = s.splitlines()

    def _check(x: int, y: int, dx: int, dy: int) -> bool:
        for i, c in enumerate('XMAS'):
            cx, cy = x + i * dx, y + i * dy
            if (
                    0 <= cx < len(lines[0]) and
                    0 <= cy < len(lines) and
                    lines[cy][cx] == c
            ):
                continue
            else:
                return False
        else:
            return True

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == 'X':
                for dx, dy in support.adjacent_8(0, 0):
                    total += _check(x, y, dx, dy)
    return total


INPUT_S = '''\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''
EXPECTED = 18


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
