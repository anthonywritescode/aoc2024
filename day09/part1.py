from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    disk: list[int | None] = []
    s = s.strip()
    it = itertools.zip_longest(s[::2], s[1::2], fillvalue=0)
    for did, (c1, c2) in enumerate(it):
        n1 = int(c1)
        n2 = int(c2)
        disk.extend([did] * n1)
        disk.extend([None] * n2)

    def _pop(pos: int) -> int:
        last = disk.pop()
        while last is None:
            if len(disk) <= pos:
                return 0
            last = disk.pop()
        return last

    ret = 0
    for i, val in enumerate(disk):
        if val is None:
            val = _pop(i)
        ret += i * val

    return ret


INPUT_S = '''\
2333133121414131402
'''
EXPECTED = 1928


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        ('0015', 0),
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
