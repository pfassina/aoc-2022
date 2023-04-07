from dataclasses import dataclass
from typing import Callable


@dataclass
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    test: Callable[[int], int]
    inspections: int = 0
    factors: bool = False

    def inspect_items(self, relief) -> list[tuple[int, int]]:
        trowed_items: list[tuple[int, int]] = []
        while len(self.items):
            self.inspections += 1
            item = self.items.pop(0)
            item = self.operation(item)
            if relief > 1:
                item = item // relief
            else:
                item = item % (2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23)
            target = self.test(item)

            trowed_items.append((item, target))

        return trowed_items

    def get_item(self, item: int) -> None:
        self.items.append(item)


def parse_items(notes: str) -> list[int]:
    return [int(i) for i in notes.split("Starting items: ")[1].split(",")]


def parse_operation(notes: str) -> Callable[[int], int]:
    expression = notes.split("Operation: new = old ")[1]
    operator = expression[0]
    factor = expression[2:]

    def func(old: int) -> int:
        new_factor = int(factor) if factor != "old" else old
        if operator == "+":
            return old + new_factor
        return old * new_factor

    return func


def parse_test(notes: list[str]) -> Callable[[int], int]:
    test = int(notes[0].split("Test: divisible by ")[1])
    true = int(notes[1].split("If true: throw to monkey ")[1])
    false = int(notes[2].split("If false: throw to monkey ")[1])

    def func(worry: int) -> int:
        return true if worry % test == 0 else false

    return func


def parse_monkey(notes: list[str]) -> Monkey:
    items = parse_items(notes[1])
    operation = parse_operation(notes[2])
    test = parse_test(notes[3:])
    return Monkey(items, operation, test)


def parse_input(input: str) -> dict[int, Monkey]:
    rows = [r.strip() for r in input.splitlines() if r != ""]
    monkey_notes = [rows[i : i + 6] for i in range(0, len(rows), 6)]
    return {i: parse_monkey(n) for i, n in enumerate(monkey_notes)}


def process_round(monkeys: dict[int, Monkey], relief=3) -> dict[int, Monkey]:
    for m in monkeys.values():
        throwed_items = m.inspect_items(relief)
        for item, target in throwed_items:
            monkeys[target].get_item(item)
    return monkeys


def part_one(input: str) -> int:
    monkeys = parse_input(input)
    for _ in range(20):
        monkeys = process_round(monkeys)

    monkey_business = sorted([b.inspections for b in monkeys.values()])
    return monkey_business[-1] * monkey_business[-2]


def part_two(input: str) -> int:
    monkeys = parse_input(input)
    for _ in range(10000):
        monkeys = process_round(monkeys, relief=1)

    monkey_business = sorted([b.inspections for b in monkeys.values()])
    return monkey_business[-1] * monkey_business[-2]


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
