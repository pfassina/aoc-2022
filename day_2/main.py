from dataclasses import dataclass
from enum import StrEnum, auto


class RPS(StrEnum):
    ROCK = auto()
    PAPER = auto()
    SCISORS = auto()


@dataclass
class Hand:
    option: str

    @property
    def rps(self) -> RPS:
        return self.translate()

    def translate(self) -> RPS:
        options: dict[str, RPS] = {
            'A': RPS.ROCK,
            'B': RPS.PAPER,
            'C': RPS.SCISORS,
            'X': RPS.ROCK,
            'Y': RPS.PAPER,
            'Z': RPS.SCISORS,
        }
        return options[self.option]


@dataclass
class Hands:
    elf: Hand
    human: Hand


@dataclass
class Strategy:
    options: list[str]

    @property
    def elf(self) -> str:
        return self.options[0]

    @property
    def human(self) -> str:
        if self.options[1] == 'X':
            return self.loose
        if self.options[1] == 'Y':
            return self.draw
        if self.options[1] == 'Z':
            return self.win
        raise NotImplemented

    @property
    def win(self) -> str:
        hand = {
            'A': 'B',
            'B': 'C',
            'C': 'A',

        }
        return hand[self.elf]

    @property
    def draw(self) -> str:
        return self.elf

    @property
    def loose(self) -> str:
        hand = {
            'A': 'C',
            'B': 'A',
            'C': 'B',

        }
        return hand[self.elf]

    @property
    def hands(self) -> Hands:
        return Hands(
            Hand(self.elf),
            Hand(self.human)
        )


@dataclass
class Game:
    hands: Hands
    
    @property
    def elf(self):
        return self.hands.elf

    @property
    def human(self):
        return self.hands.human

    @property
    def round_points(self) -> int:
        if self.elf.rps == self.human.rps:
            return 3
        if self.elf.rps == RPS.ROCK:
            return 6 if self.human.rps == RPS.PAPER else 0
        if self.elf.rps == RPS.PAPER:
            return 6 if self.human.rps == RPS.SCISORS else 0
        if self.elf.rps == RPS.SCISORS:
            return 6 if self.human.rps == RPS.ROCK else 0
        raise NotImplemented

    @property
    def hand_points(self) -> int:
        points: dict[RPS, int] = {
            RPS.ROCK: 1,
            RPS.PAPER: 2,
            RPS.SCISORS: 3,
        }
        return points[self.human.rps]

    @property
    def score(self) -> int:
        return self.round_points + self.hand_points



def part_one(input: str) -> int:
    rounds = [r.split(' ') for r in input.splitlines()]
    games = [Game(Hands(Hand(e), Hand(h))) for e, h in rounds]
    scores = [g.score for g in games]
    
    return sum(scores)

def part_two(input: str) -> int:
    rounds = [r.split(' ') for r in input.splitlines()]
    games = [Game(Strategy(r).hands) for r in rounds]
    scores = [g.score for g in games]
    return sum(scores)


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

