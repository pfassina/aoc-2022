#!/usr/bin/env python

import shutil
import sys

def main(argv: list[str]) -> None:
    new_day = argv[0]
    src = 'day_0'
    dst = f'day_{new_day}'
    shutil.copytree(src, dst)


if __name__ == "__main__":
    main(sys.argv[1:])



