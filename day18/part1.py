from __future__ import annotations

import argparse
import collections
import os.path
import sys

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, *, size: int = 71, n: int = 1024) -> int:
    world = set()
    for line in s.splitlines()[:n]:
        x, y = support.parse_numbers_comma(line)
        world.add((x, y))

    best: dict[tuple[int, int], int] = {}

    todo: collections.deque[tuple[tuple[int, int], frozenset[tuple[int, int]]]]
    todo = collections.deque([((0, 0), frozenset(((0, 0),)))])
    while todo:
        pos, seen = todo.popleft()

        best_at = best.get(pos, sys.maxsize)
        if len(seen) >= best_at:
            continue
        else:
            best[pos] = len(seen)

        if pos == (size - 1, size - 1):
            return len(seen) - 1

        for cand in support.adjacent_4(*pos):
            cx, cy = cand
            if (
                    0 <= cx < size and
                    0 <= cy < size and
                    cand not in world and
                    cand not in seen
            ):
                todo.append((cand, seen | {cand}))

    raise AssertionError('unreachable!')


INPUT_S = '''\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
'''
EXPECTED = 22


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, size=7, n=12) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
