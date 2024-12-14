from __future__ import annotations

import argparse
import collections
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    beacons: dict[str, list[tuple[int, int]]]
    beacons = collections.defaultdict(list)

    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c != '.':
                beacons[c].append((x, y))

    bx = range(0, len(s.splitlines()[0]))
    by = range(0, len(s.splitlines()))

    antinodes = set()
    for nodes in beacons.values():
        for (x1, y1), (x2, y2) in itertools.combinations(nodes, 2):
            dx, dy = x2 - x1, y2 - y1
            antinodes.add((x2 + dx, y2 + dy))
            antinodes.add((x1 - dx, y1 - dy))

    return len({(x, y) for x, y in antinodes if x in bx if y in by})


INPUT_S = '''\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''
EXPECTED = 14


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
