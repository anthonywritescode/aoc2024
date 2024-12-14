from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class LoopError(ValueError):
    pass


def compute(s: str) -> int:
    world = support.parse_coords_hash(s)
    bx, by = support.bounds(world)

    start, = (
        (x, y)
        for y, line in enumerate(s.splitlines())
        for x, c in enumerate(line) if c == '^'
    )

    def _try(cx: int, cy: int) -> set[tuple[int, int, support.Direction4]]:
        seen = set()
        x, y = start
        direction = support.Direction4.UP
        while True:
            if x not in bx.range or y not in by.range:
                break
            elif (x, y) in world or (x, y) == (cx, cy):
                x, y = direction.opposite.apply(x, y)
                direction = direction.cw
                x, y = direction.apply(x, y)
            elif (x, y, direction) in seen:
                raise LoopError
            else:
                seen.add((x, y, direction))
                x, y = direction.apply(x, y)

        return seen

    traced = {(x, y) for x, y, _ in _try(-999, -999)}
    traced |= {(x, y) for pt in traced for x, y in support.adjacent_8(*pt)}
    traced = {
        (x, y) for (x, y) in traced
        if x in bx.range
        if y in by.range
        if (x, y) != start
    }

    bads = set()
    for cx, cy in traced:
        try:
            _try(cx, cy)
        except LoopError:
            bads.add((cx, cy))

    return len(bads)


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
