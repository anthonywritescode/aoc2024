from __future__ import annotations

import argparse
import collections
import math
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PAT = re.compile(r'^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$')


def compute(s: str, *, n: int = 100, w: int = 101, h: int = 103) -> int:
    quads: collections.Counter[tuple[bool, bool]] = collections.Counter()

    w_h = w // 2
    h_h = h // 2

    for line in s.splitlines():
        match = PAT.fullmatch(line)
        assert match is not None, line
        px, py = int(match[1]), int(match[2])
        vx, vy = int(match[3]), int(match[4])

        x = (px + vx * n) % w
        y = (py + vy * n) % h
        if x == w_h or y == h_h:
            continue

        quads[(x > w_h, y > h_h)] += 1

    return math.prod(quads.values())


INPUT_S = '''\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''
EXPECTED = 12


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, w=11, h=7) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
