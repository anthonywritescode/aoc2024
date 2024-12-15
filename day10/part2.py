from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    world = support.parse_coords_int(s)

    def _score(pos: tuple[int, int]) -> int:
        completed = 0
        todo = [(pos, 0)]
        while todo:
            pos, size = todo.pop()

            if size == 9:
                completed += 1
                continue

            for coord in support.adjacent_4(*pos):
                if world.get(coord, -1) == size + 1:
                    todo.append((coord, size + 1))

        return completed

    return sum(_score(k) for k, v in world.items() if v == 0)


INPUT_S = '''\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''
EXPECTED = 81


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
