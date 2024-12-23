from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    edges: collections.defaultdict[str, set[str]]
    edges = collections.defaultdict(set)
    for line in s.splitlines():
        s1, s2 = line.split('-')
        assert s1 != s2, (s1, s2)
        edges[s1].add(s2)
        edges[s2].add(s1)

    seen = set()
    best: frozenset[str] = frozenset()
    todo = [(frozenset((n,)), frozenset(edges[n])) for n in edges]
    while todo:
        connected, possible = todo.pop()
        if len(connected) > len(best):
            best = connected
        elif connected in seen:
            continue
        else:
            seen.add(connected)

        for cand in possible:
            if connected & edges[cand] == connected:
                todo.append((connected | {cand}, possible - {cand}))

    return ','.join(sorted(best))


INPUT_S = '''\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
'''
EXPECTED = 'co,de,ka,ta'


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
