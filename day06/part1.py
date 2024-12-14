from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    world = support.parse_coords_hash(s)
    bx, by = support.bounds(world)

    (x, y), = (
        (x, y)
        for y, line in enumerate(s.splitlines())
        for x, c in enumerate(line) if c == '^'
    )

    seen = {(x, y)}
    direction = support.Direction4.UP
    while True:
        if x not in bx.range or y not in by.range:
            break
        elif (x, y) in world:
            x, y = direction.opposite.apply(x, y)
            direction = direction.cw
            x, y = direction.apply(x, y)
        else:
            seen.add((x, y))
            x, y = direction.apply(x, y)

    return len(seen)


INPUT_S = '''\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''
EXPECTED = 41


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
