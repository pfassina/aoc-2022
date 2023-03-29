

ItemType = str
Compartment = list[ItemType]
Rucksack = tuple[Compartment, Compartment]
Group = tuple[Rucksack, Rucksack, Rucksack]


def get_rucksacks(input: str) -> list[Rucksack]:
    input_lines = input.splitlines()
    items = [list(row) for row in input_lines]
    rucksacks = [(r[:len(r)//2], r[len(r)//2:]) for r in items]
    return rucksacks


def get_commons(rucksack: Rucksack) -> set[ItemType]:
    a, b = rucksack
    c = {i for i in a if i in b}
    return c

def str_to_int(item_type: ItemType) -> int:
    if item_type.isupper():
        return ord(item_type) - 38
    return ord(item_type) - 96


def get_priority(common_items: set[ItemType]) -> int:
    return sum([str_to_int(i) for i in common_items])


def get_groups(rucksacks: list[Rucksack]) -> list[Group]:
    return [tuple(rucksacks[i:i+3]) for i in range(0, len(rucksacks), 3)]

def get_badge(group: Group) -> set[ItemType]:
    a, b, c = [set(r[0] + r[1]) for r in group]
    return a.intersection(b, c)


def part_one(input: str) -> int:
    r = get_rucksacks(input)
    c = [get_commons(i) for i in r]
    p = [get_priority(i) for i in c]
    return sum(p)


def part_two(input: str) -> int:
    r = get_rucksacks(input)
    g = get_groups(r)
    b = [get_badge(i) for i in g]
    p = [get_priority(i) for i in b]
    return sum(p)


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

