from __future__ import annotations

import argparse
import itertools
import os.path
import re

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PAT = re.compile(r'^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$')


def compute(s: str, *, w: int = 101, h: int = 103) -> int:
    bots = []

    for line in s.splitlines():
        match = PAT.fullmatch(line)
        assert match is not None, line
        px, py = int(match[1]), int(match[2])
        vx, vy = int(match[3]), int(match[4])
        bots.append(((px, py), (vx, vy)))

    for n in itertools.count():
        pts = set()

        for (px, py), (vx, vy) in bots:
            x = (px + vx * n) % w
            y = (py + vy * n) % h
            pts.add((x, y))

        for midp in range(1, w - 2):
            sym_h_count = 0
            for cx, cy in pts:
                newx = midp - (cx - midp)
                sym_h_count += (newx, cy) in pts

            if sym_h_count > len(pts) / 2:
                return n

    raise AssertionError('unreachable')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
