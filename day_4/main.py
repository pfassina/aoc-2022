
from dataclasses import dataclass
from typing import Self


@dataclass
class Range:
    range: str

    @property
    def min(self) -> int:
        return int(self.range.split('-')[0])

    @property
    def max(self) -> int:
        return int(self.range.split('-')[1])


@dataclass
class Pair:
    first: Range
    second: Range

    def intersect(self) -> bool:
        if self.first.min >= self.second.min and self.first.max <= self.second.max:
            return True
        if self.second.min >= self.first.min and self.second.max <= self.first.max:
            return True
        return False

    def overlap(self) -> bool:
        if self.first.min >= self.second.min and self.first.min <= self.second.max:
            return True
        if self.first.max >= self.second.min and self.first.max <= self.second.max:
            return True
        if self.second.min >= self.first.min and self.second.min <= self.first.max:
            return True
        if self.second.max >= self.first.min and self.second.max <= self.first.max:
            return True
        return False


def get_pairs(input: str) -> list[Pair]:
    lines = input.splitlines()
    pairs = [l.split(',') for l in lines]
    return [Pair(Range(p[0]), Range(p[1])) for p in pairs]
    

def part_one(input: str) -> int:
    pairs = get_pairs(input)
    intersects = [p.intersect() for p in pairs]
    return sum(intersects)


def part_two(input: str) -> int:
    pairs = get_pairs(input)
    overlaps = [p.overlap() for p in pairs]
    return sum(overlaps)


def main(p: int, s: bool) -> int:
    file_name = 'sample' if s else 'input'
    file_version = f'_{p}.txt'
    file_path = file_name + file_version
    with open(file_path) as file:
        input = file.read()
    
    if p == 1:
        return part_one(input)
    return part_two(input)


if __name__ == "__main__":
    result = main(p=2, s=False)
    print(result)

