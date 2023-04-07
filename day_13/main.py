from __future__ import annotations

from ast import literal_eval
from functools import cmp_to_key
from itertools import zip_longest


def parse_input(input: str) -> list[tuple[int | list, int | list]]:
    lines = [literal_eval(line) for line in input.splitlines() if line != ""]
    return [(lines[i], lines[i + 1]) for i in range(0, len(lines), 2)]


def comp(left: int, right: int) -> int:
    if left == right:
        return 0
    return 1 if left < right else -1


def compare(p1: int | list, p2: int | list) -> int:
    if type(p1) == int and type(p2) == int:
        return comp(p1, p2)

    p1 = [p1] if type(p1) == int else p1
    p2 = [p2] if type(p2) == int else p2

    assert type(p1) == list
    assert type(p2) == list

    for l, r in zip_longest(p1, p2):
        if l is None:
            return 1
        if r is None:
            return -1
        res = compare(l, r)
        if res == 0:
            continue
        return res

    return comp(len(p1), len(p2))


def part_one(input: str) -> int:
    pairs = parse_input(input)
    correct = 0
    for i, p in enumerate(pairs, 1):
        l, r = p
        c = compare(l, r)
        correct += i if c == 1 else 0
    return correct


def part_two(input: str) -> int:
    pairs = parse_input(input)
    packets = [p for packets in pairs for p in packets] + [[[2]]] + [[[6]]]

    sorted_packets = sorted(packets, key=cmp_to_key(compare), reverse=True)
    idx = []
    for i, p in enumerate(sorted_packets, 1):
        if p == [[2]] or p == [[6]]:
            idx.append(i)

    return idx[0] * idx[1]


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
    print(result)  # 5908 too high || 5536 too low
