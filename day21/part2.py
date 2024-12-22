from __future__ import annotations

import argparse
import collections
import functools
import os.path
import sys

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


def _chunks(s: str) -> int:
    chunks = 1
    c = s[0]
    for c2 in s[1:]:
        if c2 != c:
            c = c2
            chunks += 1
    return chunks


def _paths(
        k1: tuple[int, int],
        k2: tuple[int, int],
        world: dict[tuple[int, int], str],
) -> list[str]:
    ret = []
    best: dict[tuple[int, int], int] = {}
    todo = collections.deque([(k1, '')])
    while todo:
        pos, path = todo.popleft()
        if pos == k2:
            ret.append(path)
            continue
        elif best.get(pos, sys.maxsize) < len(path):
            continue
        else:
            best[pos] = len(path)

        for d in support.Direction4:
            cand = d.apply(*pos)
            if cand in world:
                todo.append((cand, f'{path}{d.as_c()}'))

    minlen = min(len(s) for s in ret)
    ret = [s for s in ret if len(s) == minlen]
    minchunks = min(_chunks(s) for s in ret)
    ret = [s for s in ret if _chunks(s) == minchunks]
    return ret


def _all_paths(
        world: dict[tuple[int, int], str],
) -> dict[tuple[str, str], list[str]]:
    ret = {}
    all_keys = tuple(world)
    for k1 in all_keys:
        v1 = world[k1]
        for k2 in all_keys:
            v2 = world[k2]
            if k1 == k2:
                ret[(v1, v2)] = ['']
            else:
                ret[(v1, v2)] = _paths(k1, k2, world)
    return ret


KEYPAD_PATHS = _all_paths(KEYPAD_WORLD)
ARROW_PATHS = _all_paths(ARROW_WORLD)


@functools.cache
def _bot_len(s: str, bots: int) -> int:
    if bots == 0:
        return len(s)
    else:
        total = 0
        for c1, c2 in zip(f'A{s}', s):
            possible = ARROW_PATHS[(c1, c2)]
            total += min(_bot_len(f'{p}A', bots=bots - 1) for p in possible)
        return total


@functools.cache
def _keypad_len(s: str, bots: int) -> int:
    total = 0
    for c1, c2 in zip(f'A{s}', s):
        possible = KEYPAD_PATHS[(c1, c2)]
        total += min(_bot_len(f'{p}A', bots=bots) for p in possible)
    return total


def compute(s: str, *, bots: int = 25) -> int:
    total = 0
    for keypad_s in s.splitlines():
        total += _keypad_len(keypad_s, bots=bots) * int(keypad_s[:-1])
    return total


@pytest.mark.parametrize(
    ('s', 'bots', 'expected'),
    (
        ('029A', 0, 12),
        ('029A', 1, 28),
        ('029A', 2, 68),
        ('029A', 3, 164),
        ('029A', 4, 404),
        ('029A', 5, 998),
    ),
)
def test_keypad_len(s: str, bots: int, expected: int) -> None:
    assert _keypad_len(s, bots=bots) == expected


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
    assert compute(input_s, bots=2) == expected


@pytest.mark.parametrize(
    ('n', 'expected'),
    (
        (3, 310188),
        (4, 757754),
        (5, 1881090),
    ),
)
def test_larger_n(n: int, expected: int) -> None:
    assert compute(INPUT_S, bots=n) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
