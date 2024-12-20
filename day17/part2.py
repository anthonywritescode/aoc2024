from __future__ import annotations

import argparse
import os.path

import z3

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    _, prog_s = s.replace(':', '').split('\n\n')

    prog = support.parse_numbers_comma(prog_s.split()[1])

    o = z3.Optimize()
    orig_a = a = z3.BitVec('A', 64)

    for n in prog:
        b = a % 8
        b = b ^ 1
        c = a >> b
        b = b ^ c
        a = a >> 3
        b = b ^ 4
        o.add(b % 8 == n)
    o.add(a == 0)

    o.minimize(orig_a)

    assert o.check() == z3.sat
    return o.model()[orig_a].as_long()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
