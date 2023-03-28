

def part_one(input: str) -> int:
    cals: list[str] = input.split('\n')
    breaks: list[int] = [i for i, n in enumerate(cals) if n == '']
    
    intervals: list[tuple[int, int]] = [(0, breaks[0])]
    for i in range(1, len(breaks)):
        start: int = intervals[i - 1][1] + 1
        finish: int = breaks[i]
        intervals.append((start, finish))
    
    elves: list[list[int]] = [
        [int(cals[i]) for i in range(s, f)]
        for s, f in intervals
    ]

    return max([sum(c) for c in elves])

def part_two(input: str) -> int:
    cals: list[str] = input.split('\n')
    breaks: list[int] = [i for i, n in enumerate(cals) if n == '']
    
    intervals: list[tuple[int, int]] = [(0, breaks[0])]
    for i in range(1, len(breaks)):
        start: int = intervals[i - 1][1] + 1
        finish: int = breaks[i]
        intervals.append((start, finish))
    
    elves: list[list[int]] = [
        [int(cals[i]) for i in range(s, f)]
        for s, f in intervals
    ]

    top_3 = sorted([sum(c) for c in elves])
    print(top_3[-3:])
    

    return sum(top_3[-3:])



def main(p: int, s: bool) -> int:
    file_name = 'sample' if s else 'input'
    file_version = f'_1.txt'
    file_path = file_name + file_version
    with open(file_path) as file:
        input = file.read()
    
    if p == 1:
        return part_one(input)
    return part_two(input)


if __name__ == "__main__":
    result = main(p=2, s=False)
    print(result)


