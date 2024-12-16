from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    map_s, moves_s = s.split('\n\n')
    map_s = map_s.translate({
        ord('#'): '##',
        ord('.'): '..',
        ord('O'): '[]',
        ord('@'): '@.',
    })
    walls = support.parse_coords_hash(map_s)
    boxes = support.parse_coords_hash(map_s, wall='[')
    bot, = support.parse_coords_hash(map_s, wall='@')

    def _boxes_to_move(d: support.Direction4) -> set[tuple[int, int]]:
        boxes_to_move: set[tuple[int, int]] = set()
        if d is support.Direction4.LEFT:
            pos = d.apply(*bot)
            if pos in walls:
                return boxes_to_move
            pos = d.apply(*pos)
            while pos in boxes:
                boxes_to_move.add(pos)
                pos = d.apply(*pos)
                if pos in walls:
                    return boxes_to_move
                pos = d.apply(*pos)
            return boxes_to_move
        elif d is support.Direction4.RIGHT:
            pos = d.apply(*bot)
            while pos in boxes:
                boxes_to_move.add(pos)
                pos = d.apply(*d.apply(*pos))
            return boxes_to_move
        elif d is support.Direction4.UP or d is support.Direction4.DOWN:
            pos1 = d.apply(*bot)
            pos2 = support.Direction4.LEFT.apply(*pos1)
            layer = {pos1, pos2} & boxes
            while layer:
                boxes_to_move.update(layer)
                newlayer: set[tuple[int, int]] = set()
                for box in layer:
                    pos1 = d.apply(*box)
                    pos2 = support.Direction4.LEFT.apply(*pos1)
                    pos3 = support.Direction4.RIGHT.apply(*pos1)
                    newlayer.update((pos1, pos2, pos3))
                layer = newlayer & boxes
            return boxes_to_move
        else:
            raise AssertionError('unreachable')

    def _is_box_blocked(box: tuple[int, int], d: support.Direction4) -> bool:
        if d is support.Direction4.LEFT:
            return d.apply(*box) in walls
        elif d is support.Direction4.RIGHT:
            return d.apply(*d.apply(*box)) in walls
        elif d is support.Direction4.UP or d is support.Direction4.DOWN:
            return (
                d.apply(*box) in walls or
                support.Direction4.RIGHT.apply(*d.apply(*box)) in walls
            )
        else:
            raise AssertionError('unreachable')

    moves_s = ''.join(moves_s.split())
    for c in moves_s:
        d = support.Direction4.from_c(c)

        if d.apply(*bot) in walls:
            continue

        boxes_to_move = _boxes_to_move(d)

        if any(_is_box_blocked(box, d) for box in boxes_to_move):
            continue

        bot = d.apply(*bot)
        boxes -= boxes_to_move
        boxes |= {d.apply(*box) for box in boxes_to_move}

    return sum(100 * y + x for x, y in boxes)


INPUT_S = '''\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''
EXPECTED = 9021


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
