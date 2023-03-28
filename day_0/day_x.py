
def part_one(input: str) -> int:
    print(input)
    return 0

def part_two(input: str) -> int:
    print(input)
    return 0


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
    result = main(p=1, s=True)
    print(result)

