from dataclasses import dataclass
from collections import deque


@dataclass
class Instruction:
    qty: int
    src: int
    dst: int


@dataclass
class Stack:
    _crates: list[str]

    def __post_init__(self) -> None:
        self.crates = deque(self._crates)
    
    def put(self, crates: list[str]) -> None:
        for crate in crates:
            self.crates.append(crate)
    
    def get(self, qty: int) -> list[str]:
        return [self.crates.pop() for _ in range(qty)] 

    def get_mult(self, qty: int) -> list[str]:
        crates = self.get(qty)
        return crates[::-1]

    @property
    def top(self) -> str:
        return self.crates[-1]

    def __repr__(self) -> str:
        return str([c for c in self.crates])


@dataclass
class Ship:
    stacks: dict[int, Stack] 

    def execute(self, instruction: Instruction) -> None:
        src = instruction.src
        dst = instruction.dst
        qty = instruction.qty

        crates = self.stacks[src].get(qty)
        self.stacks[dst].put(crates)

    def execute_9001(self, instruction: Instruction) -> None:
        src = instruction.src
        dst = instruction.dst
        qty = instruction.qty

        crates = self.stacks[src].get_mult(qty)
        self.stacks[dst].put(crates)

    @property
    def top_stacks(self) -> list[str]:
        return [s.top for s in self.stacks.values()]

    def __repr__(self) -> str:
        return str(self.stacks)


def parse_level(level: str) -> list[str]:
    return [''.join(level[i:i+4]).strip() for i in range(0, len(level), 4)]


def parse_input(input: str):
    rows = [l for l in input.splitlines()]

    levels  = []
    instructions = []
    stack_qty = 0
    for r in rows:
        if r.find('[') >= 0:
            levels.append(parse_level(r))
        if r.find('m') == 0:
            words = r.split(' ')
            values = [int(i) for i in words if i.isdigit()]
            instructions.append(Instruction(*values))
        if r.find(' 1') == 0:
            stack_qty = int(r[-2])

    stacks = {i: Stack([]) for i in range(1, stack_qty + 1)}
    for level in levels:
        for i, s in enumerate(level, 1):
            if s == '':
                continue
            stacks[i].crates.appendleft(s)

    return Ship(stacks), instructions


def format_result(top_stacks: list[str]) -> str:
    return ''.join([c for c in ''.join(top_stacks) if c.isalpha()])


def part_one(input: str) -> str:
    ship, instructions = parse_input(input)
    for i in instructions:
        ship.execute(i)

    return format_result(ship.top_stacks)


def part_two(input: str) -> str:
    ship, instructions = parse_input(input)
    for i in instructions:
        ship.execute_9001(i)

    return format_result(ship.top_stacks)


def main(p: int, s: bool) -> str:
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

