from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    regs_s, prog_s = s.replace(':', '').split('\n\n')
    regs = {}
    for line in regs_s.splitlines():
        _, name, val_s = line.split()
        regs[name] = int(val_s)

    def _val(i: int) -> int:
        if 0 <= i <= 3:
            return i
        elif i == 7:
            raise ValueError(f'unexpected {i=}')
        else:
            return regs[chr(ord('A') + i - 4)]

    out = []
    prog = support.parse_numbers_comma(prog_s.split()[1])
    pc = 0
    while pc < len(prog):
        op = prog[pc]
        operand = prog[pc + 1]
        if op == 0:
            regs['A'] = regs['A'] // (2 ** _val(operand))
            pc += 2
        elif op == 6:
            regs['B'] = regs['A'] // (2 ** _val(operand))
            pc += 2
        elif op == 7:
            regs['C'] = regs['A'] // (2 ** _val(operand))
            pc += 2
        elif op == 1:
            regs['B'] = regs['B'] ^ operand
            pc += 2
        elif op == 2:
            regs['B'] = _val(operand) % 8
            pc += 2
        elif op == 3:
            if regs['A'] == 0:
                pc += 2
            else:
                pc = operand
        elif op == 4:
            regs['B'] ^= regs['C']
            pc += 2
        elif op == 5:
            out.append(_val(operand) % 8)
            pc += 2

    return ','.join(str(n) for n in out)


INPUT_S = '''\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
'''
EXPECTED = '4,6,3,5,6,3,5,2,1,0'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: str) -> None:
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
