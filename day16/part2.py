from __future__ import annotations

import argparse
import heapq
import os.path
import sys
from typing import NamedTuple
from typing import Self

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _best_score(
        world: set[tuple[int, int]],
        start: tuple[int, int],
        end: tuple[int, int],
) -> int:
    seen = set()
    todo = [(0, start, support.Direction4.RIGHT)]

    def _do(score: int, pos: tuple[int, int], d: support.Direction4) -> None:
        if (pos, d) not in seen:
            heapq.heappush(todo, (score, pos, d))

    while True:
        score, pos, direction = heapq.heappop(todo)

        if pos == end:
            return score
        else:
            seen.add((pos, direction))

        # can we move forward?
        cand = direction.apply(*pos)
        if cand not in world:
            _do(score + 1, cand, direction)

        # can we move turn and move forward?
        cand = direction.cw.apply(*pos)
        if cand not in world:
            _do(score + 1001, cand, direction.cw)

        # can we turn left and move forward?
        cand = direction.ccw.apply(*pos)
        if cand not in world:
            _do(score + 1001, cand, direction.ccw)


class State(NamedTuple):
    score: int
    pos: tuple[int, int]
    direction: support.Direction4
    positions_seen: frozenset[tuple[int, int]]

    @classmethod
    def initial(cls, pos: tuple[int, int]) -> Self:
        return cls(
            score=0,
            pos=pos,
            direction=support.Direction4.RIGHT,
            positions_seen=frozenset((pos,)),
        )

    def next_state(
            self,
            score: int,
            pos: tuple[int, int],
            d: support.Direction4,
    ) -> Self | None:
        if pos in self.positions_seen:
            return None

        return type(self)(
            score=score,
            pos=pos,
            direction=d,
            positions_seen=self.positions_seen | {pos},
        )


def compute(s: str) -> int:
    world = support.parse_coords_hash(s)
    start, = support.parse_coords_hash(s, wall='S')
    end, = support.parse_coords_hash(s, wall='E')

    best_score = _best_score(world, start, end)

    bests: dict[tuple[int, int], int] = {}
    sits: set[tuple[int, int]] = set()
    paths = [State.initial(start)]

    def _do(
            score: int,
            pos: tuple[int, int],
            d: support.Direction4,
            state: State,
    ) -> None:
        best_at = bests.get(pos, sys.maxsize)
        if score > best_at + 1000 or score > best_score:
            return
        else:
            bests[pos] = min(score, best_at)

        new_state = state.next_state(score, pos, d)
        if new_state is not None:
            paths.append(new_state)

    while paths:
        state = paths.pop()
        pos = state.pos
        direction = state.direction

        if pos == end and state.score == best_score:
            sits.update(state.positions_seen)
            continue

        # can we move forward?
        cand = direction.apply(*pos)
        if cand not in world:
            _do(state.score + 1, cand, direction, state)

        # can we turn right and move?
        cand = direction.cw.apply(*pos)
        if cand not in world:
            _do(state.score + 1001, cand, direction.cw, state)

        # can we turn left and move?
        cand = direction.ccw.apply(*pos)
        if cand not in world:
            _do(state.score + 1001, cand, direction.ccw, state)

    return len(sits)


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
EXPECTED = 45


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
