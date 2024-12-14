from __future__ import annotations

import argparse
import itertools
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class File(NamedTuple):
    did: int
    size: int

    def value(self, offset: int) -> int:
        return sum(i * self.did for i in range(offset, offset + self.size))


class Free(NamedTuple):
    size: int


def compute(s: str) -> int:
    disk: list[File | Free] = []
    s = s.strip()
    it = itertools.zip_longest(s[::2], s[1::2], fillvalue=0)

    for did, (c1, c2) in enumerate(it):
        n1 = int(c1)
        n2 = int(c2)
        disk.append(File(did, n1))
        disk.append(Free(n2))

    searchfrom = len(disk) - 1

    def _pos(did: int) -> tuple[int, File]:
        nonlocal searchfrom
        segment = disk[searchfrom]
        while not isinstance(segment, File) or segment.did != did:
            searchfrom -= 1
            segment = disk[searchfrom]
        return searchfrom, segment

    def _target(*, size: int, maxpos: int) -> tuple[int, Free] | None:
        for i in range(maxpos):
            segment = disk[i]
            if isinstance(segment, Free) and segment.size >= size:
                return i, segment
        else:
            return None

    for did in range(did, -1, -1):
        pos, segment = _pos(did)

        target = _target(size=segment.size, maxpos=pos)
        if target is not None:
            target_pos, target_free = target
            if target_free.size == segment.size:
                disk[pos], disk[target_pos] = disk[target_pos], disk[pos]
            else:
                disk[pos] = Free(segment.size)
                disk[target_pos] = Free(target_free.size - segment.size)
                disk.insert(target_pos, segment)
                searchfrom += 1

    total = 0
    offset = 0
    for part in disk:
        if isinstance(part, File):
            total += part.value(offset)
        offset += part.size

    return total


INPUT_S = '''\
2333133121414131402
'''
EXPECTED = 2858


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
