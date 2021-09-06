#!/usr/bin/env python3
import argparse
import glob
from itertools import chain
import os
import sys
import time


parser = argparse.ArgumentParser(description="OK if ")
parser.add_argument(
    "files",
    metavar="PathPattern",
    type=str,
    nargs="+",
    help="files pattern (give them between '' if you use *",
)
parser.add_argument(
    "-w", "--warning", dest="warning", type=int, default=86400, help="TODO"
)
parser.add_argument(
    "-c", "--critical", dest="critical", type=int, default=86400 * 2, help="TODO"
)
current_time = time.time()


if __name__ == "__main__":
    try:
        args = parser.parse_args()
        globs = [glob.glob(pattern) for pattern in args.files]
        path_age = [
            current_time - os.path.getmtime(path) for path in chain.from_iterable(globs)
        ]
        if not path_age:
            print("No file found in specified path(s)")
            sys.exit(3)
        if all(map(lambda age: age > args.critical, path_age)):
            sys.exit(2)
        if all(map(lambda age: age > args.warning, path_age)):
            sys.exit(1)
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(3)
