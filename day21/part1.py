from __future__ import annotations

import argparse
import collections
import os.path
from typing import NamedTuple
from typing import Self

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

KEYPAD_WORLD = {
    (0, 0): '7',
    (1, 0): '8',
    (2, 0): '9',
    (0, 1): '4',
    (1, 1): '5',
    (2, 1): '6',
    (0, 2): '1',
    (1, 2): '2',
    (2, 2): '3',
    (1, 3): '0',
    (2, 3): 'A',
}
ARROW_WORLD = {
    (1, 0): '^',
    (2, 0): 'A',
    (0, 1): '<',
    (1, 1): 'v',
    (2, 1): '>',
}


class State(NamedTuple):
    remaining: str
    keypad: tuple[int, int]
    bots: tuple[tuple[int, int], ...]

    @classmethod
    def initial(cls, s: str) -> Self:
        return cls(s, (2, 3), ((2, 0),) * 2)

    def press(self, c: str) -> State | None:
        new_bots = []
        for i, bot in enumerate(self.bots):
            if c == 'A':
                new_bots.append(bot)
                c = ARROW_WORLD[bot]
            else:
                d = support.Direction4.from_c(c)
                new_bot = d.apply(*bot)
                if new_bot not in ARROW_WORLD:
                    return None
                new_bots.append(new_bot)
                new_bots.extend(self.bots[i + 1:])
                break
        else:
            if c == 'A':
                if KEYPAD_WORLD[self.keypad] == self.remaining[0]:
                    return self._replace(remaining=self.remaining[1:])
            else:
                d = support.Direction4.from_c(c)
                new_keypad = d.apply(*self.keypad)
                if new_keypad not in KEYPAD_WORLD:
                    return None
                else:
                    return self._replace(keypad=new_keypad)

        return self._replace(bots=tuple(new_bots))


def _val(s: str) -> int:
    initial = State.initial(s)
    seen = {initial}
    todo: collections.deque[tuple[int, State]]
    todo = collections.deque([(0, initial)])

    def _next_state(newstate: State | None) -> None:
        if newstate is not None and newstate not in seen:
            todo.append((score + 1, newstate))
            seen.add(newstate)

    while todo:
        score, state = todo.popleft()

        if state.remaining == '':
            return score * int(s[:-1])

        for c in 'A<^>v':
            _next_state(state.press(c))

    raise AssertionError('unreachable')


def compute(s: str) -> int:
    return sum(_val(line) for line in s.splitlines())


INPUT_S = '''\
029A
980A
179A
456A
379A
'''
EXPECTED = 126384


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
