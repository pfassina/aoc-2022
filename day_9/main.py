from dataclasses import dataclass
from typing import Self


@dataclass
class Movement:
    direction: str
    distance: int

    @property
    def vector(self) -> tuple[int, int]:
        if self.direction == "R":
            return (1, 0)
        if self.direction == "L":
            return (-1, 0)
        if self.direction == "U":
            return (0, -1)
        if self.direction == "D":
            return (0, 1)
        raise NotImplemented

    def take(self) -> tuple[int, int]:
        self.distance -= 1
        return self.vector


@dataclass
class Vector:
    x: int
    y: int

    def move(self, movement: tuple[int, int]) -> None:
        x, y = movement
        self.x += x
        self.y += y

    def adjacent(self, other: Self) -> bool:
        if abs(other.x - self.x) > 1:
            return False
        if abs(other.y - self.y) > 1:
            return False
        if abs(other.x - self.x) + abs(other.y - self.y) > 2:
            return False
        return True

    def move_towards(self, other: Self) -> None:
        dist = self - other

        if dist.x == 0 and dist.y != 0:
            self.y += 1 if dist.y > 0 else -1
            return
        if dist.y == 0 and dist.x != 0:
            self.x += 1 if dist.x > 0 else -1
            return
        if dist.x != 0 and dist.y != 0:
            self.x += 1 if dist.x > 0 else -1
            self.y += 1 if dist.y > 0 else -1
            return

        raise NotImplemented

    @property
    def loc(self) -> tuple[int, int]:
        return self.x, self.y

    def __sub__(self, other: Self) -> Self:
        return Vector(other.x - self.x, other.y - self.y)

    def __hash__(self) -> int:
        return hash(f"{self.x}{self.y}")


def parse_input(input: str) -> list[Movement]:
    rows = input.splitlines()
    movements = [row.split(" ") for row in rows]
    return [Movement(d, int(n)) for d, n in movements]


def part_one(input: str) -> int:
    movements = parse_input(input)

    head = Vector(0, 0)
    tail = Vector(0, 0)

    positions: set[tuple[int, int]] = {tail.loc}

    for movement in movements:
        while movement.distance > 0:
            order = movement.take()
            head.move(order)
            if head.adjacent(tail):
                continue
            tail.move_towards(head)
            positions.add(tail.loc)

    return len(positions)


def part_two(input: str) -> int:
    movements = parse_input(input)

    head = Vector(0, 0)
    t1 = Vector(0, 0)
    t2 = Vector(0, 0)
    t3 = Vector(0, 0)
    t4 = Vector(0, 0)
    t5 = Vector(0, 0)
    t6 = Vector(0, 0)
    t7 = Vector(0, 0)
    t8 = Vector(0, 0)
    t9 = Vector(0, 0)

    positions: set[tuple[int, int]] = {t9.loc}

    for movement in movements:
        while movement.distance > 0:
            order = movement.take()
            head.move(order)

            if not t1.adjacent(head):
                t1.move_towards(head)

            if not t2.adjacent(t1):
                t2.move_towards(t1)

            if not t3.adjacent(t2):
                t3.move_towards(t2)

            if not t4.adjacent(t3):
                t4.move_towards(t3)

            if not t5.adjacent(t4):
                t5.move_towards(t4)

            if not t6.adjacent(t5):
                t6.move_towards(t5)

            if not t7.adjacent(t6):
                t7.move_towards(t6)

            if not t8.adjacent(t7):
                t8.move_towards(t7)

            if not t9.adjacent(t8):
                t9.move_towards(t8)
                positions.add(t9.loc)

    return len(positions)


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
