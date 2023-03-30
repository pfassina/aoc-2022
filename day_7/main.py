from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


@dataclass
class File:
    name: str
    size: int

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Dir:
    name: Optional[str] 
    parent: Optional[Dir] = None
    directories: set[Dir] = field(default_factory=set)
    files: set[File] = field(default_factory=set)

    @property
    def size(self) -> int:
        return self._dir_sizes + self._file_sizes

    @property
    def _file_sizes(self) -> int:
        return sum([f.size for f in self.files])

    @property
    def _dir_sizes(self) -> int:
        return sum([d.size for d in self.directories])

    def get_all_dirs(self, dirs: list[Dir]):

        dirs.append(self)

        if len(self.directories) == 0:
            return dirs

        for d in self.directories:
            d.get_all_dirs(dirs)
            
        return dirs

    def print(self, level=0) -> None:
        new_level = level + 1
        print('\t' * new_level,f'- DIR {self.name} ({self.size})')
        for file in self.files:
            print('\t' * (new_level + 1), f'- {file.name} ({file.size})')
        for d in self.directories:
            d.print(new_level)

    def __hash__(self) -> int:
        return hash(self.name)



class LineType(Enum):
    COMMAND = auto()
    DIR = auto()
    FILE = auto()

class CommandType(Enum):
    CD = auto()
    LS = auto()


@dataclass
class CommandCD:
    name: str
    parent: str



def parse_line_type(line: str) -> LineType:
    if line[0] == '$':
        return LineType.COMMAND
    if line[0:3] == 'dir':
        return LineType.DIR
    return LineType.FILE
    
def parse_cmd_type(command: str) -> CommandType:
    if command[2] == 'c':
        return CommandType.CD
    return CommandType.LS

def parse_ls(line: str, line_type: LineType) -> str:
    if line_type == LineType.DIR:
        return line[4:]
    return line

def parse_cd(line: str, cwd: Dir, root: Dir) -> Dir:
    target = line[5:]
    if target == '..':
        assert cwd.parent
        return cwd.parent
    if target != '/':
        return [d for d in cwd.directories if d.name == target][0]
    return root

def parse_line(line: str, root: Dir, cwd: Dir) -> Dir:

    line_type = parse_line_type(line)

    if line_type == LineType.COMMAND:
        cmd = parse_cmd_type(line)
        if cmd == CommandType.LS:
            return cwd
        return parse_cd(line, cwd, root)

    if line_type == LineType.DIR:
        dir_name = parse_ls(line, line_type)
        if dir_name not in [d.name for d in cwd.directories]:
            cwd.directories.add(Dir(dir_name, parent=cwd))
        return cwd

    if line_type == LineType.FILE:
        sz, name = line.split(' ')
        if name not in [f.name for f in cwd.files]:
            cwd.files.add(File(name, int(sz)))
        return cwd

    raise NotImplemented


def parse_input(input: str) -> Dir:

    root = Dir('/')
    cwd = root

    for line in input.splitlines()[1:]:
        cwd = parse_line(line, root, cwd)

    return root


def part_one(input: str) -> int:
    root = parse_input(input)
    """ root.print() """
    dirs = root.get_all_dirs([])

    small_dirs = [d for d in dirs if d.size <= 100000]
    for sd in small_dirs:
        print(sd.name, sd.size)
    
    return sum([d.size for d in small_dirs])


def part_two(input: str) -> int:
    root = parse_input(input)
    """ root.print() """
    """ dirs = root.get_all_dirs([]) """

    total = 70000000
    required = 30000000
    current = root.size
    free = total - current
    missing = abs(free - required)

    dirs = root.get_all_dirs([])
    sizes = [d.size for d in dirs if d.size >= missing]

    return sorted(sizes)[0]


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
