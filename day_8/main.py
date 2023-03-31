import numpy as np


def parse_input(input: str) -> np.ndarray:
    rows = input.splitlines()
    trees = np.array([[int(t) for t in row] for row in rows], dtype=int)
    return trees


def create_visible_mask(trees: np.ndarray) -> np.ndarray:
    visible = np.zeros_like(trees)
    visible[0,] = True
    visible[-1,] = True
    visible[:, 0] = True
    visible[:, -1] = True
    return visible


def visible_trees(los: list[np.ndarray], height: int) -> int:
    visible_dist = []
    for direction in los:
        if not np.any(direction):
            continue
        max_dist = 0
        for i, tree in enumerate(direction, 1):
            if tree >= height:
                max_dist = max(max_dist, i)
                break
            max_dist = max(max_dist, i)
        visible_dist.append(max_dist)

    return np.multiply.reduce(np.array(visible_dist))


def part_one(input: str) -> int:
    trees = parse_input(input)
    visible = create_visible_mask(trees)
    for y, row in enumerate(trees[1:-1, 1:-1], 1):
        for x, tree in enumerate(row, 1):
            n = tree > max(trees[:y, x])
            s = tree > max(trees[y + 1 :, x])
            w = tree > max(trees[y, :x])
            e = tree > max(trees[y, x + 1 :])
            visible[y, x] = any([n, s, w, e])
    return visible.sum()


def part_two(input: str) -> int:
    trees = parse_input(input)
    scenic = np.zeros_like(trees)
    for y, x in np.ndindex(trees.shape):
        if y == 0 or y == len(trees) - 1:
            scenic[(y, x)] = 0
            continue
        if x == 0 or x == len(trees[0]) - 1:
            scenic[(y, x)] = 0
            continue

        n = np.flip(trees[:y, x])
        s = trees[y + 1 :, x] if y + 1 < len(trees) else np.array([])
        w = np.flip(trees[y, :x])
        e = trees[y, x + 1 :] if x + 1 < len(trees) else np.array([])

        height = trees[(y, x)]
        scenic[(y, x)] = visible_trees([n, s, w, e], height)

    return scenic.max()


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
