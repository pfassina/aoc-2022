#!/usr/bin/env python

import os
import shutil
import sys


def main(argv: list[str]) -> None:
    assert len(argv) > 0
    day = argv[0]
    assert os.path.exists(f"./day_{day}")
    src = [f"day_{day}/sample_1.txt", f"day_{day}/input_1.txt"]
    dst = [f"day_{day}/sample_2.txt", f"day_{day}/input_2.txt"]
    for s, d in zip(src, dst):
        shutil.copyfile(s, d)

    print("input files copied")


if __name__ == "__main__":
    main(sys.argv[1:])
