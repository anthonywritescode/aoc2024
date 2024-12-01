from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lst1, lst2 = [], []
    for line in s.splitlines():
        n1_s, n2_s = line.split()
        lst1.append(int(n1_s))
        lst2.append(int(n2_s))

    lst1.sort()
    lst2.sort()
    return sum(abs(n2 - n1) for n1, n2 in zip(lst1, lst2))


INPUT_S = '''\
3   4
4   3
2   5
1   3
3   9
3   3
'''
EXPECTED = 11


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
