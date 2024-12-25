from __future__ import annotations

import argparse
import operator
import os.path
from collections.abc import Callable
from typing import NamedTuple
from typing import Self

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OPS = {'AND': operator.and_, 'OR': operator.or_, 'XOR': operator.xor}


class Eq(NamedTuple):
    inputs: tuple[str, str]
    output: str
    operator: Callable[[int, int], int]

    @classmethod
    def parse(cls, s: str) -> Self:
        i1, op_s, i2, _, o = s.split()
        return cls((i1, i2), o, OPS[op_s])

    def ready(self, inputs: dict[str, int]) -> bool:
        return all(i in inputs for i in self.inputs)

    def compute(self, inputs: dict[str, int]) -> int:
        return self.operator(*(inputs[i] for i in self.inputs))


def compute(s: str) -> int:
    values_s, computes_s = s.split('\n\n')
    values = {}
    for line in values_s.splitlines():
        name, val_s = line.split(': ')
        values[name] = int(val_s)

    equations = [Eq.parse(line) for line in computes_s.splitlines()]
    while equations:
        for equation in equations:
            if equation.ready(values):
                values[equation.output] = equation.compute(values)
                equations.remove(equation)
                break
        else:
            raise AssertionError('no work done?')

    zs = sorted(((k, v) for k, v in values.items() if k.startswith('z')))
    return int(''.join(str(bit) for _, bit in reversed(zs)), 2)


INPUT_S = '''\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
'''
EXPECTED = 2024


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
