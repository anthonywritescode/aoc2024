from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    numbers = support.parse_numbers_split(s)

    def _transmute(n: int) -> tuple[int, ...]:
        if n == 0:
            return (1,)
        elif len(str(n)) % 2 == 0:
            nstr = str(n)
            midp = len(nstr) // 2
            return int(nstr[:midp]), int(nstr[midp:])
        else:
            return (2024 * n,)

    for _ in range(25):
        numbers = [m for n in numbers for m in _transmute(n)]

    return len(numbers)


INPUT_S = '''\
125 17
'''
EXPECTED = 55312


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
