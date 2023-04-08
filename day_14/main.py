from dataclasses import dataclass

import numpy as np
from numpy.core.multiarray import array
from numpy.lib.stride_tricks import sliding_window_view


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int


def parse_input(input: str) -> list[np.ndarray]:
    lines = input.splitlines()
    nodes = [n.split(" -> ") for n in lines]
    vectors = [np.array([[int(i) for i in v.split(",")] for v in n]) for n in nodes]

    return vectors


def get_cave_dimension(rocks: list[np.ndarray]) -> Rect:
    cave_min_x = np.inf
    cave_max_x = 0
    cave_min_y = np.inf
    cave_max_y = 0

    for rock in rocks:
        min_x = rock[:, 0].min()
        max_x = rock[:, 0].max() + 1
        min_y = 0
        max_y = rock[:, 1].max() + 1

        cave_min_x = min(min_x, cave_min_x)
        cave_max_x = max(max_x, cave_max_x)

        cave_min_y = min(min_y, cave_min_y)
        cave_max_y = max(max_y, cave_max_y)

    x = int(cave_min_x)
    y = int(cave_min_y)
    w = int(cave_max_x - cave_min_x)
    h = int(cave_max_y - cave_min_y)

    return Rect(x, y, w, h)


def adjust_w(rock: np.ndarray, x: int) -> np.ndarray:
    rock[:, 0] -= x
    return rock


def lines_to_rect(rock_lines: list[list[np.ndarray]]) -> list[Rect]:
    rects: list[Rect] = []
    for line in rock_lines:
        start, end = line
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        w = abs(start[0] - end[0]) + 1
        h = abs(start[1] - end[1]) + 1
        rects.append(Rect(x, y, w, h))

    return rects


def find_rocks(dim: Rect, rocks: list[np.ndarray]) -> list[Rect]:
    rock_lines = []
    for rock in rocks:
        adj_rock = adjust_w(rock, dim.x)
        if len(adj_rock) == 2:
            rock_lines.append(list(adj_rock))
            continue
        nodes = sliding_window_view(adj_rock, window_shape=(2, 2)).squeeze()
        rock_lines += [list(n) for n in nodes]

    return lines_to_rect(rock_lines)


def create_cave(dim: Rect, rock_lines: list[np.ndarray]) -> np.ndarray:
    cave = np.zeros((dim.h, dim.w), dtype=int)
    rocks = find_rocks(dim, rock_lines)
    for rock in rocks:
        cave[rock.y : rock.y + rock.h, rock.x : rock.x + rock.w] = 1
    return cave


def drop_sand(cave: np.ndarray, dim: Rect) -> bool:
    start = (0, 500 - dim.x)
    next = start
    current = None
    while True:
        if cave[start] == 8:
            return True
        if next[0] == dim.h:
            return True
        if cave[next] in [1, 8]:
            left = (next[0], next[1] - 1)
            right = (next[0], next[1] + 1)
            if left[1] < 0:
                return True
            if cave[left] not in [1, 8]:
                current = next
                next = left
                continue
            if right[1] == dim.w:
                return True
            if cave[right] not in [1, 8]:
                current = right
                next = right
                continue
            cave[current] = 8
            break
        current = next
        next = (next[0] + 1, next[1])
    return False


def add_floor(rocks: list[np.ndarray]) -> np.ndarray:
    dim = get_cave_dimension(rocks)
    return np.array(
        [[dim.x - dim.h, dim.y + dim.h + 1], [dim.x + dim.w - 1 + dim.h, dim.h + 1]]
    )


def part_one(input: str) -> int:
    rocks = parse_input(input)
    dim = get_cave_dimension(rocks)
    cave = create_cave(dim, rocks)

    drops = 0
    while True:
        abyss = drop_sand(cave, dim)
        if abyss:
            break
        drops += 1
    print(cave)

    return drops


def part_two(input: str) -> int:
    rocks = parse_input(input)
    rocks.append(add_floor(rocks))
    dim = get_cave_dimension(rocks)
    cave = create_cave(dim, rocks)

    drops = 0
    while True:
        abyss = drop_sand(cave, dim)
        if abyss:
            break
        drops += 1

    print(cave)

    return drops


def main(p: int, s: bool) -> int:
    file_name = "sample" if s else "input"
    file_version = f"_{p}.txt"
    file_path = file_name + file_version
    with open(file_path) as file:
        input = file.read()

    if p == 1:
        return part_one(input)
    return part_two(input)


if __name__ == "__main__":
    result = main(p=2, s=False)
    print(result)
