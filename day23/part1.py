from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    nodes: set[str] = set()
    edges: set[tuple[str, str]] = set()
    for line in s.splitlines():
        s1, s2 = line.split('-')
        assert s1 != s2, (s1, s2)
        nodes.update((s1, s2))
        edges.update(((s1, s2), (s2, s1)))

    all_nodes = sorted(nodes)
    found = set()
    for i, n1 in enumerate(all_nodes):
        for j, n2 in enumerate(all_nodes[i + 1:]):
            for n3 in all_nodes[j + 1:]:
                if (
                        (n1, n2) in edges and
                        (n1, n3) in edges and
                        (n2, n3) in edges and
                        any(n.startswith('t') for n in (n1, n2, n3))
                ):
                    found.add(frozenset((n1, n2, n3)))

    return len(found)


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
EXPECTED = 7


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
