from __future__ import annotations

import argparse
import functools
import operator
import os.path
from collections.abc import Callable
from typing import NamedTuple
from typing import Self

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OPS = {'AND': operator.and_, 'OR': operator.or_, 'XOR': operator.xor}


class Uncomputable(ValueError):
    pass


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


def _int_to_values(n: int, name: str) -> dict[str, int]:
    return {
        f'{name}{i:02}': int(bit)
        for i, bit in enumerate(reversed(f'{n:064b}'))
    }


def _order_equations(all_equations: tuple[Eq, ...]) -> tuple[Eq, ...]:
    values = {
        **_int_to_values(0, 'y'),
        **_int_to_values(0, 'x'),
    }
    equations = sorted(all_equations)
    new_equations = []
    while equations:
        for equation in equations:
            if equation.ready(values):
                values[equation.output] = equation.compute(values)
                equations.remove(equation)
                new_equations.append(equation)
                break
        else:
            raise Uncomputable

    return tuple(new_equations)


def _run(
        all_equations: tuple[Eq, ...],
        x: int,
        y: int,
        swap: dict[str, str] | None = None,
) -> int:
    swap = swap or {}
    values = {
        **_int_to_values(x, 'x'),
        **_int_to_values(y, 'y'),
    }
    equations = list(all_equations)
    while equations:
        for equation in equations:
            if equation.ready(values):
                output = swap.get(equation.output, equation.output)
                values[output] = equation.compute(values)
                equations.remove(equation)
                break
        else:
            raise Uncomputable

    zs = sorted(((k, v) for k, v in values.items() if k.startswith('z')))
    return int(''.join(str(bit) for _, bit in reversed(zs)), 2)


def _test(
        equations: tuple[Eq, ...],
        bit: int,
        swap: dict[str, str] | None = None,
) -> bool:
    val = 1 << bit
    try:
        got = {
            _run(equations, val, 0, swap=swap),
            _run(equations, 0, val, swap=swap),
            _run(equations, val - 1, 1, swap=swap),
            _run(equations, 1, val - 1, swap=swap),
        }
        if bit > 1:
            got.add(_run(equations, val >> 1, val >> 1, swap=swap))
    except Uncomputable:
        return False
    return got == {val}


def _bad_bits(
        equations: tuple[Eq, ...],
        highest_bit: int,
        swap: dict[str, str],
) -> set[int]:
    return {
        i
        for i in range(highest_bit)
        if not _test(equations, i, swap=swap)
    }


def compute(s: str, *, pairs: int = 4) -> str:
    _, computes_s = s.split('\n\n')
    equations = tuple(Eq.parse(line) for line in computes_s.splitlines())

    equations = _order_equations(equations)

    edges = {eq.output: eq.inputs for eq in equations}

    @functools.cache
    def _trace(node: str) -> frozenset[str]:
        seen = {node}
        todo = [node]
        while todo:
            output = todo.pop()
            for k in edges[output]:
                if not k.startswith(('x', 'y')):
                    seen.add(k)
                    todo.append(k)
        return frozenset(seen)

    def _find_pair(i: int) -> tuple[str, str]:
        prev = _trace(f'z{(i - 1):02}')
        for k1 in _trace(f'z{i:02}') - prev:
            # XXX: inputs sort of worked out that it broke the next bit
            for k2 in _trace(f'z{i + 1:02}'):
                swap = {**found, k1: k2, k2: k1}
                if (
                        _test(equations, i, swap=swap) and
                        _test(equations, i + 1, swap=swap)
                ):
                    return (k1, k2)

        raise AssertionError('unreachable!')

    found: dict[str, str] = {}
    highest_z = max(eq.output for eq in equations if eq.output.startswith('z'))
    highest_bit = int(highest_z[1:])
    for i in range(highest_bit):
        if not _test(equations, i, swap=found):
            k1, k2 = _find_pair(i)
            found[k1] = k2
            found[k2] = k1

    return ','.join(sorted(found))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
