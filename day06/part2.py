from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    world = support.parse_coords_hash(s)
    bounds = support.bounds(world)

    pos, = support.parse_coords_hash(s, wall='^')

    seen = set()
    seen1 = set()
    direction = support.Direction4.UP

    def _loops(
            pos: tuple[int, int],
            direction: support.Direction4,
            new_wall: tuple[int, int],
    ) -> bool:
        seen2 = set()
        direction = direction.cw
        while True:
            if not support.in_bounds(pos, bounds):
                return False
            elif pos in world or pos == new_wall:
                pos = direction.opposite.apply(*pos)
                direction = direction.cw
            elif (pos, direction) in seen1 or (pos, direction) in seen2:
                return True
            else:
                seen2.add((pos, direction))
                pos = direction.apply(*pos)

    found = set()
    while True:
        if not support.in_bounds(pos, bounds):
            break
        elif pos in world:
            pos = direction.opposite.apply(*pos)
            direction = direction.cw
        else:
            nextpos = direction.apply(*pos)
            if (
                    nextpos not in seen and
                    nextpos not in world and
                    _loops(pos, direction, nextpos)
            ):
                found.add(nextpos)
            seen1.add((pos, direction))
            seen.add(pos)
            pos = nextpos

    return len(found)


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
EXPECTED = 6


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
