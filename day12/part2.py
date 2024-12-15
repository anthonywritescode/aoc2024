from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    world = {
        (x, y): c
        for y, line in enumerate(s.splitlines())
        for x, c in enumerate(line)
    }

    chunks = []

    def _chunk(pos: tuple[int, int], c: str) -> None:
        chunk = {pos}
        todo = [pos]
        while todo:
            pos = todo.pop()

            for coord in support.adjacent_4(*pos):
                if world.get(coord) == c:
                    world.pop(coord)
                    todo.append(coord)
                    chunk.add(coord)

        chunks.append(chunk)

    while world:
        k = next(iter(world))
        v = world.pop(k)
        _chunk(k, v)

    def _value(chunk: set[tuple[int, int]]) -> int:
        found: dict[tuple[int, int], set[support.Direction4]]
        found = collections.defaultdict(set)
        for pos in chunk:
            for d in support.Direction4:
                coord = d.apply(*pos)
                if coord not in chunk:
                    found[coord].add(d)

        def _process(
                pos: tuple[int, int],
                d: support.Direction4,
                d_a: support.Direction4,
        ) -> None:
            pos = d_a.apply(*pos)
            while pos in found and d in found[pos]:
                found[pos].remove(d)
                if not found[pos]:
                    found.pop(pos)
                pos = d_a.apply(*pos)

        def _del_side(pos: tuple[int, int], d: support.Direction4) -> None:
            _process(pos, d, d.cw)
            _process(pos, d, d.ccw)

        sides = 0
        while found:
            k = next(iter(found))
            v = found[k].pop()
            if not found[k]:
                found.pop(k)
            _del_side(k, v)
            sides += 1

        return len(chunk) * sides

    return sum(_value(chunk) for chunk in chunks)


INPUT_S = '''\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''
EXPECTED = 1206


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
