from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _best_path(
        world: set[tuple[int, int]],
        start: tuple[int, int],
        end: tuple[int, int],
) -> dict[tuple[int, int], int]:
    seen = {start}
    todo: collections.deque[tuple[tuple[int, int], ...]]
    todo = collections.deque([(start,)])
    while todo:
        path = todo.popleft()
        if path[-1] == end:
            break

        for cand in support.adjacent_4(*path[-1]):
            if cand not in seen and cand not in world:
                todo.append((*path, cand))
                seen.add(cand)
    else:
        raise AssertionError('unreachable')

    return {pos: i for i, pos in enumerate(path)}


def compute(s: str, *, at_least: int = 100) -> int:
    world = support.parse_coords_hash(s)
    start, = support.parse_coords_hash(s, wall='S')
    end, = support.parse_coords_hash(s, wall='E')

    best_at = _best_path(world, start, end)

    cheats: collections.Counter[int] = collections.Counter()

    seen = {start}
    todo: collections.deque[tuple[tuple[int, int], frozenset[tuple[int, int]]]]
    todo = collections.deque([(start, frozenset((start,)))])
    while todo:
        pos, path = todo.popleft()
        if pos == end:
            continue

        # compute cheats at position!
        for dx in range(-20, 20 + 1):
            ymax = 20 - abs(dx)
            for dy in range(-ymax, ymax + 1):
                cand = (pos[0] + dx, pos[1] + dy)
                if cand not in best_at:
                    continue

                expected = len(seen) + abs(dx) + abs(dy)
                got = best_at[cand]
                if expected < got:
                    cheats[got - expected + 1] += 1

        # advance the path
        for cand in support.adjacent_4(*pos):
            if cand not in world and cand not in seen:
                todo.append((cand, path | {cand}))
                seen.add(cand)

    return sum(v for k, v in cheats.items() if k >= at_least)


INPUT_S = '''\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''
EXPECTED = 41


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, at_least=70) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
