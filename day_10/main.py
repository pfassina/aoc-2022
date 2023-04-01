from dataclasses import dataclass
from enum import StrEnum, auto

import numpy as np


class InstructionType(StrEnum):
    NOOP = auto()
    ADDX = auto()


@dataclass
class Instruction:
    type: InstructionType
    value: int
    cycle: int

    @property
    def output(self) -> tuple[int, int]:
        return self.value, self.cycle + self.delay

    @property
    def delay(self) -> int:
        return 2 if self.type == InstructionType.ADDX else 1

    def __repr__(self) -> str:
        return (
            f"{self.type.name} {self.value:+03d} @ cycle {self.cycle} -> {self.output}"
        )


@dataclass
class Register:
    register: np.ndarray

    def execute_instruction(self, instruction: Instruction) -> None:
        value, out_cycle = instruction.output
        if out_cycle > 240:
            return
        self.register[out_cycle - 1 :] += value

    def cycle_strength(self, cycle) -> int:
        return self.register[cycle - 1] * (cycle)

    @property
    def total_strength(self) -> int:
        cycles = [20, 60, 100, 140, 180, 220]
        return sum([self.cycle_strength(c) for c in cycles])


def parse_input(input: str) -> list[Instruction]:
    rows = input.splitlines()
    instructions = []
    cycle = 1
    for row in rows:
        if len(row) == 4:
            instruction = Instruction(InstructionType.NOOP, 0, cycle)
            instructions.append(instruction)
            cycle += instruction.delay
            continue

        inst_type, value = row.split(" ")
        instruction = Instruction(InstructionType(inst_type), int(value), cycle)
        cycle += instruction.delay
        instructions.append(instruction)

    return instructions


def part_one(input: str) -> int:
    instructions = parse_input(input)
    register = Register(np.ones(220, dtype=int))
    for i in instructions:
        register.execute_instruction(i)

    print(register.register)

    return register.total_strength


def part_two(input: str) -> int:
    instructions = parse_input(input)
    register = Register(np.ones(240, dtype=int))
    for i in instructions:
        register.execute_instruction(i)

    screen = np.zeros((6, 40), dtype=str)
    for c, (y, x) in enumerate(np.ndindex(screen.shape)):
        pos = register.register[c]
        pixels = [pos - 1, pos, pos + 1]
        if c % 40 in pixels:
            screen[(y, x)] = "#"
            continue
        screen[(y, x)] = "."

    for r in screen:
        print("".join(r))
    return 0


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
