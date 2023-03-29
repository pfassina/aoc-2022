
def find_start_packet(input: str) -> int:
    for i in range(len(input)):
        chars = input[i:i+4]
        if len(set(chars)) != 4:
            continue
        return i + 4

def find_message(input: str) -> int:
    for i in range(len(input)):
        chars = input[i:i+14]
        if len(set(chars)) != 14:
            continue
        return i + 14

def part_one(input: str) -> int:
    start = find_start_packet(input)
    return start

def part_two(input: str) -> int:
    msg = find_message(input)
    return msg


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
    result = main(p=1, s=False)
    print(result)

