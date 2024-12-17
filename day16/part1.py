from __future__ import annotations

import argparse
import heapq
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    world = support.parse_coords_hash(s)
    start, = support.parse_coords_hash(s, wall='S')
    end, = support.parse_coords_hash(s, wall='E')

    seen = set()
    todo = [(0, start, support.Direction4.RIGHT)]

    def _do(score: int, pos: tuple[int, int], d: support.Direction4) -> None:
        if (pos, d) not in seen:
            heapq.heappush(todo, (score, pos, d))

    while todo:
        score, pos, direction = heapq.heappop(todo)

        if pos == end:
            return score
        else:
            seen.add((pos, direction))

        # can we move forward?
        cand = direction.apply(*pos)
        if cand not in world:
            _do(score + 1, cand, direction)

        cand = direction.cw.apply(*pos)
        if cand not in world:
            _do(score + 1001, cand, direction.cw)

        cand = direction.ccw.apply(*pos)
        if cand not in world:
            _do(score + 1001, cand, direction.ccw)

    raise AssertionError('unreachable')


INPUT_S = '''\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''
EXPECTED = 7036


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
