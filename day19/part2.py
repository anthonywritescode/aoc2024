from __future__ import annotations

import argparse
import functools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    patterns_s, targets = s.split('\n\n')
    possible = patterns_s.split(', ')

    @functools.cache
    def _possible(s: str) -> int:
        if s == '':
            return 1

        ret = 0
        for cand in possible:
            if s.startswith(cand):
                ret += _possible(s.removeprefix(cand))
        return ret

    total = 0
    for line in targets.splitlines():
        total += _possible(line)
    return total


INPUT_S = '''\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''
EXPECTED = 16


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
